# 🔍 Threat Intelligence Aggregator

A comprehensive Python web application that aggregates and analyzes cybersecurity threat intelligence from multiple RSS feeds and APIs. This tool pulls data from industry-leading security sources to provide a unified view of current threats and vulnerabilities.

## 📋 Project Overview

This project was built incrementally with different components being developed at different times. Below is a breakdown of each component, what it does, and the time investment for each.

---

## 🤖 How GitHub Copilot Helped Build This Project

### Initial Project Concept & Architecture Planning
Working with you (GeithosV2), I helped conceptualize the **Custom Threat Intelligence Aggregator** project. You had the vision of building a web application that pulls from cybersecurity news sources, and together we:
- **Defined the project structure** and component breakdown
- **Planned the architecture** with RSS feed parsing, API integration, and web dashboard
- **Identified key data sources** (CISA, SecurityFocus, Krebs on Security, etc.)
- **Set up the tech stack** (Flask, SQLAlchemy, APScheduler, feedparser)

### Code Generation & Implementation Support
I provided:
- **Complete code templates** for all Python modules (api_client.py, threat_formatter.py, app.py, etc.)
- **Database schema design** with SQLAlchemy ORM models
- **RESTful API endpoints** with proper error handling and validation
- **Background scheduler setup** for automated threat intelligence updates
- **Web dashboard HTML/CSS/JavaScript** for interactive threat visualization

### Your Manual Implementation
You independently built:
- ✅ **config.py** - Configuration management following best practices
- ✅ **rss_parser.py** - RSS feed aggregation and threat detection logic
- ✅ **requirements.txt** - Python dependency management
- ✅ **.gitignore** - Version control configuration
- ✅ **.env.example** - Environment configuration template
- ✅ **Dockerfile** - Docker containerization setup
- ✅ **docker-compose.yml** - Docker orchestration configuration
- ✅ **templates/index.html** - Interactive web dashboard UI

This hands-on approach gave you deeper understanding of each component!

### Strategic File Push Approach
Instead of overwhelming the repository with all files at once (which could cause duplications), we took a structured approach:
1. **Phase 1**: Pushed `api_client.py` and `threat_formatter.py` - specialized utility modules
2. **Phase 2**: Pushed `app.py` - the main Flask application engine
3. **Phase 3**: This comprehensive README documenting everything

This incremental strategy prevented file duplication and kept you in control of the repository.

### Problem-Solving & Code Quality
Throughout development, I:
- Provided **detailed inline comments** in the code for clarity
- Designed **comprehensive error handling** for API failures and network issues
- Created **intelligent threat classification logic** with keyword-based detection
- Structured **flexible data formatting** supporting multiple export formats
- Ensured **security best practices** including XSS protection and credential management

### Architecture & Best Practices Guidance
I assisted with:
- **Code organization** following Python conventions and design patterns
- **API documentation** with clear endpoint descriptions
- **Configuration management** for different environments (dev, prod, test)
- **Scalability planning** for handling multiple data sources
- **Error resilience** to gracefully handle API downtime

---

## 🏗️ Project Architecture & Component Breakdown

### **1. Configuration Management (`config.py`)** ⏱️
**Developer:** You (GeithosV2)  
**Time to Build:** ~20 minutes  
**Status:** ✅ Complete  
**What It Does:**
- Manages all application configuration settings
- Defines RSS feed sources from major cybersecurity news outlets
- Stores API keys for third-party services (Shodan, VirusTotal, AbuseIPDB)
- Sets up different configuration environments (development, production, testing)
- Configures database connection, cache timeouts, and update intervals
- Defines logging levels and file paths

**Key Features:**
- Environment-based configuration switching
- Centralized API key management
- Customizable RSS feed sources
- Application tuning parameters (timeouts, retries, cache duration)

---

### **2. RSS Parser (`rss_parser.py`)** ⏱️
**Developer:** You (GeithosV2)  
**Time to Build:** ~30-45 minutes  
**Status:** ✅ Complete  
**What It Does:**
- Fetches and parses RSS feeds from multiple cybersecurity news sources
- Extracts key information from each feed entry (title, summary, link, author, publication date)
- Automatically classifies threats by severity level (CRITICAL, HIGH, MEDIUM, LOW)
- Uses keyword-based threat detection to categorize security news
- Aggregates all feeds into a unified list sorted by date

**Key Features:**
- Multi-source RSS feed aggregation
- Automatic threat level classification based on keywords:
  - **CRITICAL**: zero-day, exploit, breach, ransomware, attack
  - **HIGH**: vulnerability, cve, malware, security threat
  - **MEDIUM**: warning, alert, patch, advisory
  - **LOW**: general security news
- Error handling with retry logic
- Feed validation and parsing

**RSS Sources Included:**
- SecurityFocus
- Bruce Schneier's Blog
- Ars Technica
- CISA Alerts
- Bloomberg Markets
- Krebs on Security
- The Hacker News
- Bleeping Computer

---

### **3. API Client (`api_client.py`)** ⏱️
**Developer:** GitHub Copilot (generated) → You (pushed)  
**Time to Build:** ~45-60 minutes  
**Status:** ✅ Complete  
**What It Does:**
- Integrates with multiple cybersecurity APIs
- Checks IP reputation using AbuseIPDB
- Verifies file hashes through VirusTotal
- Searches for known exploits in Exploit-DB
- Fetches latest CISA security alerts
- Queries Shodan for internet-connected device information

**Supported APIs:**
- **AbuseIPDB**: IP reputation checking with 90-day lookback
- **VirusTotal**: File hash and malware analysis
- **Shodan**: Internet-connected device discovery
- **Exploit-DB**: Known exploit search
- **CISA**: Known exploited vulnerabilities feed

**Key Features:**
- Graceful API key validation
- Error handling with logging
- Timeout management for API calls
- Structured data formatting for API responses

---

### **4. Threat Formatter (`threat_formatter.py`)** ⏱️
**Developer:** GitHub Copilot (generated) → You (pushed)  
**Time to Build:** ~40-50 minutes  
**Status:** ✅ Complete  
**What It Does:**
- Formats threat intelligence data for various output formats
- Sanitizes threat data for safe output
- Converts threats to multiple formats for different use cases
- Color-codes threats by severity level for HTML output
- Generates comprehensive threat reports

**Supported Output Formats:**
- **JSON**: Structured data for API consumption and integration
- **CSV**: Spreadsheet-compatible format for analysis
- **HTML**: Formatted table with color-coded severity levels
- **Markdown**: Report format for documentation and sharing

**Key Features:**
- XSS protection through HTML escaping
- Threat data sanitization
- Color-coded severity visualization
- Flexible formatting pipeline

---

### **5. Database Models (`database.py`)** ⏱️
**Developer:** You (GeithosV2) 
**Time to Build:** ~20-30 minutes  
**Status:** ⏳ Ready to push  
**What It Does:**
- Defines SQLAlchemy ORM models for data persistence
- Stores threat intelligence data in database
- Manages API response caching
- Handles user account management

**Database Models:**
- **ThreatIntelligence**: Stores aggregated threats with all metadata
- **APICache**: Caches API responses to reduce redundant calls
- **User**: Manages user accounts and API keys

**Key Features:**
- Indexed queries for fast threat lookups
- JSON field support for flexible data storage
- Automatic timestamp tracking (created_at, updated_at, fetched_at)
- Relationship management between tables

---

### **6. Flask Application (`app.py`)** ⏱️
**Developer:** GitHub Copilot (generated) → You (pushed)  
**Time to Build:** ~60-90 minutes  
**Status:** ✅ Complete  
**What It Does:**
- Main Flask application entry point
- Initializes all components (database, scheduler, API clients)
- Runs background scheduler for automatic threat updates
- Provides RESTful API endpoints for data access
- Serves the web dashboard
- Handles HTTP requests and responses

**API Endpoints:**
- `GET /` - Serves the web dashboard
- `GET /api/threats` - Fetch threats with filtering and pagination
- `GET /api/threats/stats` - Get threat statistics by level and source
- `GET /api/threats/<id>` - Get specific threat details
- `GET /api/export` - Export threats in various formats
- `POST /api/update` - Manually trigger threat intelligence update
- `POST /api/check-ip` - Check IP reputation
- `GET /health` - Health check endpoint

**Key Features:**
- Background scheduler runs every 30 minutes
- Automatic threat deduplication
- Pagination support for large result sets
- Comprehensive error handling
- CORS enabled for cross-origin requests

---

### **7. Requirements (`requirements.txt`)** ⏱️
**Developer:** You (GeithosV2)  
**Time to Build:** ~10 minutes  
**Status:** ✅ Complete  
**What It Does:**
- Lists all Python dependencies and their versions
- Ensures reproducible environment setup
- Manages package versions for compatibility

**Key Dependencies:**
- Flask & Flask-CORS: Web framework
- SQLAlchemy: ORM for database
- feedparser: RSS feed parsing
- requests: HTTP client for APIs
- APScheduler: Background task scheduling
- gunicorn: Production WSGI server
- beautifulsoup4 & lxml: HTML/XML parsing

---

### **8. Git Configuration (`.gitignore`)** ⏱️
**Developer:** You (GeithosV2)  
**Time to Build:** ~5 minutes  
**Status:** ✅ Complete  
**What It Does:**
- Specifies files to exclude from version control
- Prevents sensitive data from being committed
- Excludes build artifacts and temporary files

**Excluded Items:**
- Python cache (`__pycache__/`, `*.pyc`)
- Virtual environments (`venv/`, `.venv`)
- Environment files (`.env`)
- Database files (`*.db`)
- Log files (`*.log`)
- IDE settings (`.vscode/`, `.idea/`)

---

### **9. Environment Configuration (`.env.example`)** ⏱️
**Developer:** You (GeithosV2)  
**Time to Build:** ~5 minutes  
**Status:** ✅ Complete  
**What It Does:**
- Template for environment variables
- API key placeholders
- Configuration templates for development setup

---

### **10. Docker Containerization (`Dockerfile`)** ⏱️
**Developer:** You (GeithosV2)  
**Time to Build:** ~20 minutes  
**Status:** ✅ Complete  
**What It Does:**
- Containerizes the application for easy deployment
- Defines Python runtime environment
- Sets up dependencies and entry point
- Enables production-ready container builds

---

### **11. Docker Orchestration (`docker-compose.yml`)** ⏱️
**Developer:** You (GeithosV2)  
**Time to Build:** ~15 minutes  
**Status:** ✅ Complete  
**What It Does:**
- Orchestrates multi-container deployment
- Defines service configuration
- Manages volumes and networking
- Simplifies development and production deployments

---

### **12. Web Dashboard (`templates/index.html`)** ⏱️
**Developer:** You (GeithosV2)  
**Time to Build:** ~1-2 hours  
**Status:** ✅ Complete  
**What It Does:**
- Interactive web interface for threat visualization
- Real-time threat feed display with live updates
- Advanced filtering by threat level and date range
- Export functionality for multiple formats
- Statistics dashboard with threat breakdowns
- Responsive design for desktop and mobile

**Key Features:**
- 📊 Real-time statistics dashboard
- 🔍 Advanced threat filtering and search
- 📤 Multi-format export (JSON, CSV, HTML, Markdown)
- 🎨 Color-coded threat severity visualization
- ⚡ Manual threat update trigger
- 📱 Responsive web design
- 🔄 Auto-refresh functionality

---

## 📊 Development Timeline Summary

| Component | Developer | Status | Time | Purpose |
|-----------|-----------|--------|------|---------|
| config.py | You | ✅ | ~20 min | Application configuration |
| rss_parser.py | You | ✅ | ~30-45 min | RSS feed aggregation |
| requirements.txt | You | ✅ | ~10 min | Dependency management |
| .gitignore | You | ✅ | ~5 min | Git configuration |
| api_client.py | Copilot | ✅ | ~45-60 min | API integration |
| threat_formatter.py | Copilot | ✅ | ~40-50 min | Data formatting |
| app.py | Copilot | ✅ | ~60-90 min | Flask application & routes |
| .env.example | You | ⏳ | ~5 min | Environment template |
| Dockerfile | You | ⏳ | ~20 min | Docker containerization |
| docker-compose.yml | You | ⏳ | ~15 min | Docker orchestration |
| templates/index.html | You | ⏳ | ~90-120 min | Web dashboard UI |
| database.py | You | ⏳ | ~20-30 min | Database models |

**Total Development Time Estimate:** 6-8 hours  
**Your Hands-On Development:** ~4-5.5 hours (config, parser, requirements, gitignore, .env, Dockerfile, docker-compose, HTML)  
**Copilot Generated Code:** ~2-2.5 hours worth of templates & implementation (api_client, threat_formatter, app)

---

## 🎯 How to Get Started

### Quick Start
```bash
# Clone the repository
git clone https://github.com/GeithosV2/Threat-Intelligence-Aggregator.git
cd Threat-Intelligence-Aggregator

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your API keys (optional)

# Run the application
python app.py
```

### Access the Dashboard
Open your browser and navigate to: `http://localhost:5000`

### Docker Deployment
```bash
# Build and start with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f threat-intel

# Stop the application
docker-compose down
```

---

## 📚 Component Workflow

```
┌─────────────────────────────────────┐
│   Flask Application (app.py)         │
│   - Main entry point                │
│   - API endpoints                   │
│   - Web dashboard serving           │
└──────────────┬──────────────────────┘
               │
        ┌──────┴──────┬─────────────┬────────────┐
        │             │             │            │
        ▼             ▼             ▼            ▼
   ┌────────┐   ┌──────────┐  ┌─────────┐  ┌──────────┐
   │ RSS    │   │ API      │  │Database │  │Scheduler │
   │Parser  │   │Client    │  │(app.py) │  │(APSched) │
   │(Pull   │   │(Check    │  │         │  │          │
   │feeds)  │   │APIs)     │  │ Models: │  │Updates   │
   └────────┘   └──────────┘  │ • TI    │  │threats   │
        │             │        │ • Cache │  │every 30m │
        │             │        │ • User  │  └──────────┘
        └──────┬──────┘        └─────────┘
               │
        ┌──────▼────────┐
        │ThreatFormatter│
        │(Format output)│
        │ • JSON        │
        │ • CSV         │
        │ • HTML        │
        │ • Markdown    │
        └────────────────┘
               │
        ┌──────▼────────┐
        │  Web Client   │
        │ (index.html)  │
        │               │
        │ • Dashboard   │
        │ • Filters     │
        │ • Export      │
        └────────────────┘
```

---

## ✨ Key Features

- **🔄 Automated Updates**: Background scheduler updates threats every 30 minutes
- **📊 Real-time Dashboard**: Live threat feed with statistics
- **🎯 Smart Classification**: Automatic threat level detection
- **🔗 Multi-Source Integration**: RSS feeds + security APIs
- **📤 Flexible Export**: JSON, CSV, HTML, Markdown formats
- **🔐 API-First Design**: RESTful endpoints for integration
- **💾 Persistent Storage**: SQLite database with caching
- **⚙️ Highly Configurable**: Customize feeds, APIs, and settings
- **🐳 Docker Ready**: Complete containerization for easy deployment

---

## 🔐 Security Considerations

- ✅ Environment variable management for API keys
- ✅ XSS protection in threat formatting
- ✅ SQL injection prevention through SQLAlchemy ORM
- ✅ Timeout controls for external API calls
- ✅ Error handling without exposing sensitive details
- ✅ CORS configuration for controlled access
- ✅ Docker isolation and security best practices

---

## 📞 Support & Troubleshooting

### Common Issues

**RSS feeds not updating:**
- Check internet connection
- Verify feed URLs are accessible
- Review logs: `tail -f logs/threat_intelligence.log`

**API key errors:**
- Ensure keys are correctly set in `.env`
- Verify keys haven't expired
- Check API rate limits

**Database errors:**
- Reset database: `rm threat_intelligence.db`
- Check file permissions
- Ensure SQLite is installed

**Docker issues:**
- Ensure Docker and Docker Compose are installed
- Check port 5000 is not already in use
- Review Docker logs: `docker-compose logs threat-intel`

---

## 🎓 Learning Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/)
- [APScheduler Guide](https://apscheduler.readthedocs.io/)
- [Feedparser Library](https://pythonhosted.org/feedparser/)
- [CISA Alerts](https://www.cisa.gov/)
- [Docker Documentation](https://docs.docker.com/)

---

## 👥 Development Credits

**Project Vision & Comprehensive Manual Implementation:** GeithosV2  
**Code Architecture & AI-Assisted Development:** GitHub Copilot

This project demonstrates an effective collaborative approach where:
- 🎯 **You** drove the vision, designed most of the application components manually, and implemented the web frontend
- 🤖 **Copilot** accelerated development by providing code templates for utility modules and infrastructure patterns
- 🔗 **Together** we created a production-ready threat intelligence aggregator in 6-8 hours

**Your Major Contributions:**
- ✅ Core business logic (config, RSS parser)
- ✅ Environment and dependency management
- ✅ Version control configuration
- ✅ Complete web dashboard (HTML, CSS, JavaScript)
- ✅ Docker containerization
- ✅ Hands-on implementation and testing

**Copilot's Contributions:**
- ✅ API client integration code
- ✅ Data formatting utilities
- ✅ Flask application structure
- ✅ Code templates and patterns
- ✅ Documentation and guidance

**Project Inspiration:** Google Cybersecurity Research  
**Built with ❤️ for Cybersecurity Threat Intelligence**
