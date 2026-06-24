import os
import logging
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from config import config
from database import db, ThreatIntelligence
from rss_parser import RSSParser
from api_client import APIClient
from threat_formatter import ThreatFormatter
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
config_name = os.getenv('FLASK_ENV', 'development')
app.config.from_object(config[config_name])

# Initialize extensions
db.init_app(app)
CORS(app)

# Initialize scheduler
scheduler = BackgroundScheduler()

def update_threat_intelligence():
    """Background task to update threat intelligence"""
    logger.info("Starting threat intelligence update...")
    
    with app.app_context():
        try:
            # Fetch RSS feeds
            rss_parser = RSSParser()
            rss_entries = rss_parser.aggregate_feeds()
            
            # Store in database
            for entry in rss_entries:
                existing = ThreatIntelligence.query.filter_by(
                    title=entry['title'],
                    source=entry['source']
                ).first()
                
                if not existing:
                    threat = ThreatIntelligence(
                        source=entry['source'],
                        title=entry['title'],
                        summary=entry['summary'],
                        link=entry['link'],
                        pub_date=entry['pub_date'],
                        author=entry['author'],
                        threat_level=entry['threat_level'],
                        tags=entry['tags']
                    )
                    db.session.add(threat)
            
            # Fetch CISA alerts
            api_client = APIClient()
            cisa_alerts = api_client.get_cisa_alerts()
            
            if cisa_alerts:
                for alert in cisa_alerts:
                    existing = ThreatIntelligence.query.filter_by(
                        title=alert.get('cve_id'),
                        source='CISA'
                    ).first()
                    
                    if not existing:
                        threat = ThreatIntelligence(
                            source=alert['source'],
                            title=alert.get('cve_id', 'Unknown CVE'),
                            summary=alert.get('short_description', ''),
                            link=alert.get('date_added', ''),
                            pub_date=datetime.now(),
                            author='CISA',
                            threat_level=alert['threat_level'],
                            tags=['cisa', 'cve', alert.get('vendor', '')]
                        )
                        db.session.add(threat)
            
            db.session.commit()
            logger.info("Threat intelligence update completed successfully")
        
        except Exception as e:
            logger.error(f"Error updating threat intelligence: {str(e)}")
            db.session.rollback()

@app.before_request
def initialize_database():
    """Initialize database tables"""
    db.create_all()

@app.route('/', methods=['GET'])
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/api/threats', methods=['GET'])
def get_threats():
    """Get threat intelligence data with filtering options"""
    try:
        # Get query parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        threat_level = request.args.get('threat_level', None)
        source = request.args.get('source', None)
        days = request.args.get('days', 7, type=int)
        
        # Build query
        query = ThreatIntelligence.query
        
        # Filter by date
        cutoff_date = datetime.now() - timedelta(days=days)
        query = query.filter(ThreatIntelligence.pub_date >= cutoff_date)
        
        # Filter by threat level
        if threat_level:
            query = query.filter_by(threat_level=threat_level)
        
        # Filter by source
        if source:
            query = query.filter_by(source=source)
        
        # Sort by date
        query = query.order_by(ThreatIntelligence.pub_date.desc())
        
        # Paginate
        paginated = query.paginate(page=page, per_page=per_page)
        
        threats = [threat.to_dict() for threat in paginated.items]
        
        return jsonify({
            'success': True,
            'data': threats,
            'total': paginated.total,
            'pages': paginated.pages,
            'current_page': page
        })
    
    except Exception as e:
        logger.error(f"Error retrieving threats: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to retrieve threats'
        }), 500

@app.route('/api/threats/stats', methods=['GET'])
def get_threat_stats():
    """Get threat statistics"""
    try:
        total_threats = ThreatIntelligence.query.count()
        critical = ThreatIntelligence.query.filter_by(threat_level='CRITICAL').count()
        high = ThreatIntelligence.query.filter_by(threat_level='HIGH').count()
        medium = ThreatIntelligence.query.filter_by(threat_level='MEDIUM').count()
        low = ThreatIntelligence.query.filter_by(threat_level='LOW').count()
        
        sources = db.session.query(ThreatIntelligence.source, db.func.count()).group_by(ThreatIntelligence.source).all()
        
        return jsonify({
            'success': True,
            'data': {
                'total_threats': total_threats,
                'by_level': {
                    'critical': critical,
                    'high': high,
                    'medium': medium,
                    'low': low
                },
                'by_source': {source: count for source, count in sources}
            }
        })
    
    except Exception as e:
        logger.error(f"Error retrieving threat statistics: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to retrieve statistics'
        }), 500

@app.route('/api/threats/<int:threat_id>', methods=['GET'])
def get_threat(threat_id):
    """Get specific threat details"""
    try:
        threat = ThreatIntelligence.query.get_or_404(threat_id)
        return jsonify({
            'success': True,
            'data': threat.to_dict()
        })
    
    except Exception as e:
        logger.error(f"Error retrieving threat {threat_id}: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Threat not found'
        }), 404

@app.route('/api/export', methods=['GET'])
def export_threats():
    """Export threats in various formats"""
    try:
        format_type = request.args.get('format', 'json').lower()
        threat_level = request.args.get('threat_level', None)
        
        # Get threats
        query = ThreatIntelligence.query
        if threat_level:
            query = query.filter_by(threat_level=threat_level)
        
        threats = [threat.to_dict() for threat in query.all()]
        
        # Format based on type
        if format_type == 'json':
            return jsonify(threats)
        elif format_type == 'csv':
            csv_data = ThreatFormatter.format_as_csv(threats)
            return csv_data, 200, {'Content-Type': 'text/csv'}
        elif format_type == 'markdown':
            md_data = ThreatFormatter.format_as_markdown(threats)
            return md_data, 200, {'Content-Type': 'text/markdown'}
        elif format_type == 'html':
            html_data = ThreatFormatter.format_as_html(threats)
            return html_data, 200, {'Content-Type': 'text/html'}
        else:
            return jsonify({'error': 'Invalid format'}), 400
    
    except Exception as e:
        logger.error(f"Error exporting threats: {str(e)}")
        return jsonify({'error': 'Export failed'}), 500

@app.route('/api/update', methods=['POST'])
def manual_update():
    """Manually trigger threat intelligence update"""
    try:
        update_threat_intelligence()
        return jsonify({
            'success': True,
            'message': 'Threat intelligence updated successfully'
        })
    
    except Exception as e:
        logger.error(f"Error in manual update: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Update failed'
        }), 500

@app.route('/api/check-ip', methods=['POST'])
def check_ip():
    """Check IP reputation"""
    try:
        data = request.get_json()
        ip = data.get('ip')
        
        if not ip:
            return jsonify({'error': 'IP address required'}), 400
        
        api_client = APIClient()
        result = api_client.check_ip_reputation(ip)
        
        if result:
            return jsonify({'success': True, 'data': result})
        else:
            return jsonify({'success': False, 'error': 'Failed to check IP'}), 500
    
    except Exception as e:
        logger.error(f"Error checking IP: {str(e)}")
        return jsonify({'error': 'Failed to check IP'}), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal server error: {str(error)}")
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    # Start scheduler
    scheduler.add_job(update_threat_intelligence, 'interval', seconds=1800)
    scheduler.start()
    
    logger.info("Starting Threat Intelligence Aggregator...")
    app.run(debug=True, host='0.0.0.0', port=5000)
