import json
import logging
from typing import Dict, List, Optional
from datetime import datetime
from html import escape

logger = logging.getLogger(__name__)

class ThreatFormatter:
    """Format threat intelligence data for various outputs"""
    
    @staticmethod
    def format_as_json(threats: List[Dict]) -> str:
        """Format threats as JSON"""
        try:
            formatted_threats = []
            for threat in threats:
                formatted_threat = ThreatFormatter._sanitize_threat(threat)
                formatted_threats.append(formatted_threat)
            
            return json.dumps(formatted_threats, indent=2, default=str)
        
        except Exception as e:
            logger.error(f"Error formatting threats as JSON: {str(e)}")
            return json.dumps({"error": "Failed to format threats"})
    
    @staticmethod
    def format_as_html(threats: List[Dict]) -> str:
        """Format threats as HTML table"""
        try:
            html = '<table border="1" cellpadding="10" cellspacing="0">'
            html += '<thead><tr><th>Source</th><th>Title</th><th>Threat Level</th><th>Date</th><th>Link</th></tr></thead>'
            html += '<tbody>'
            
            for threat in threats:
                threat_level = threat.get('threat_level', 'UNKNOWN')
                level_color = ThreatFormatter._get_threat_color(threat_level)
                
                html += f'<tr>'
                html += f'<td>{escape(str(threat.get("source", "Unknown")))}</td>'
                html += f'<td>{escape(str(threat.get("title", "N/A"))[:100])}</td>'
                html += f'<td style="background-color: {level_color}">{threat_level}</td>'
                html += f'<td>{threat.get("pub_date", "N/A")}</td>'
                link = threat.get('link', '#')
                html += f'<td><a href="{escape(link)}" target="_blank">View</a></td>'
                html += f'</tr>'
            
            html += '</tbody></table>'
            return html
        
        except Exception as e:
            logger.error(f"Error formatting threats as HTML: {str(e)}")
            return "<p>Error formatting threats</p>"
    
    @staticmethod
    def format_as_csv(threats: List[Dict]) -> str:
        """Format threats as CSV"""
        try:
            import csv
            from io import StringIO
            
            output = StringIO()
            fieldnames = ['source', 'title', 'threat_level', 'pub_date', 'author', 'link']
            writer = csv.DictWriter(output, fieldnames=fieldnames)
            
            writer.writeheader()
            for threat in threats:
                row = {
                    'source': threat.get('source', ''),
                    'title': threat.get('title', '')[:100],
                    'threat_level': threat.get('threat_level', ''),
                    'pub_date': threat.get('pub_date', ''),
                    'author': threat.get('author', ''),
                    'link': threat.get('link', '')
                }
                writer.writerow(row)
            
            return output.getvalue()
        
        except Exception as e:
            logger.error(f"Error formatting threats as CSV: {str(e)}")
            return "Error formatting threats"
    
    @staticmethod
    def format_as_markdown(threats: List[Dict]) -> str:
        """Format threats as Markdown"""
        try:
            md = "# Threat Intelligence Report\n\n"
            md += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            md += f"Total Threats: {len(threats)}\n\n"
            
            # Group by threat level
            critical = [t for t in threats if t.get('threat_level') == 'CRITICAL']
            high = [t for t in threats if t.get('threat_level') == 'HIGH']
            medium = [t for t in threats if t.get('threat_level') == 'MEDIUM']
            low = [t for t in threats if t.get('threat_level') == 'LOW']
            
            md += f"## Summary\n\n"
            md += f"- **CRITICAL**: {len(critical)}\n"
            md += f"- **HIGH**: {len(high)}\n"
            md += f"- **MEDIUM**: {len(medium)}\n"
            md += f"- **LOW**: {len(low)}\n\n"
            
            # CRITICAL threats
            if critical:
                md += "## CRITICAL Threats\n\n"
                for threat in critical:
                    md += ThreatFormatter._format_threat_markdown(threat)
            
            # HIGH threats
            if high:
                md += "## HIGH Priority Threats\n\n"
                for threat in high:
                    md += ThreatFormatter._format_threat_markdown(threat)
            
            return md
        
        except Exception as e:
            logger.error(f"Error formatting threats as Markdown: {str(e)}")
            return "# Error formatting threats"
    
    @staticmethod
    def _format_threat_markdown(threat: Dict) -> str:
        """Format a single threat as Markdown"""
        md = f"### {threat.get('title', 'Untitled')}\n\n"
        md += f"- **Source**: {threat.get('source', 'Unknown')}\n"
        md += f"- **Date**: {threat.get('pub_date', 'N/A')}\n"
        md += f"- **Author**: {threat.get('author', 'Unknown')}\n"
        md += f"- **Threat Level**: {threat.get('threat_level', 'UNKNOWN')}\n\n"
        
        summary = threat.get('summary', '')[:200]
        if summary:
            md += f"**Summary**: {summary}...\n\n"
        
        link = threat.get('link', '')
        if link:
            md += f"[Read More]({link})\n\n"
        
        return md
    
    @staticmethod
    def _sanitize_threat(threat: Dict) -> Dict:
        """Sanitize threat data for output"""
        return {
            'source': str(threat.get('source', 'Unknown')),
            'title': str(threat.get('title', 'Untitled')),
            'summary': str(threat.get('summary', ''))[:500],
            'link': str(threat.get('link', '')),
            'pub_date': str(threat.get('pub_date', '')),
            'author': str(threat.get('author', 'Unknown')),
            'threat_level': str(threat.get('threat_level', 'UNKNOWN')),
            'tags': threat.get('tags', [])
        }
    
    @staticmethod
    def _get_threat_color(threat_level: str) -> str:
        """Get color for threat level"""
        colors = {
            'CRITICAL': '#FF0000',
            'HIGH': '#FF6600',
            'MEDIUM': '#FFCC00',
            'LOW': '#00CC00'
        }
        return colors.get(threat_level, '#808080')
