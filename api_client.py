import requests
import logging
from typing import Dict, List, Optional
from datetime import datetime
from config import Config

logger = logging.getLogger(__name__)

class APIClient:
    """Client for integrating with cybersecurity APIs"""
    
    def __init__(self):
        """Initialize API client with configuration"""
        self.shodan_key = Config.SHODAN_API_KEY
        self.virustotal_key = Config.VIRUSTOTAL_API_KEY
        self.abuseipdb_key = Config.ABUSEIPDB_API_KEY
        self.timeout = Config.TIMEOUT
    
    def check_ip_reputation(self, ip: str) -> Optional[Dict]:
        """Check IP reputation using AbuseIPDB API"""
        if not self.abuseipdb_key:
            logger.warning("AbuseIPDB API key not configured")
            return None
        
        try:
            url = 'https://api.abuseipdb.com/api/v2/check'
            headers = {
                'Key': self.abuseipdb_key,
                'Accept': 'application/json'
            }
            params = {
                'ipAddress': ip,
                'maxAgeInDays': 90,
                'verbose': True
            }
            
            response = requests.get(url, headers=headers, params=params, timeout=self.timeout)
            response.raise_for_status()
            
            data = response.json()
            return {
                'source': 'AbuseIPDB',
                'ip': ip,
                'data': data.get('data', {}),
                'fetched_at': datetime.now()
            }
        
        except Exception as e:
            logger.error(f"Error checking IP reputation for {ip}: {str(e)}")
            return None
    
    def check_file_hash(self, file_hash: str) -> Optional[Dict]:
        """Check file hash using VirusTotal API"""
        if not self.virustotal_key:
            logger.warning("VirusTotal API key not configured")
            return None
        
        try:
            url = f'https://www.virustotal.com/api/v3/files/{file_hash}'
            headers = {
                'x-apikey': self.virustotal_key
            }
            
            response = requests.get(url, headers=headers, timeout=self.timeout)
            response.raise_for_status()
            
            data = response.json()
            return {
                'source': 'VirusTotal',
                'hash': file_hash,
                'data': data.get('data', {}),
                'fetched_at': datetime.now()
            }
        
        except Exception as e:
            logger.error(f"Error checking file hash {file_hash}: {str(e)}")
            return None
    
    def search_exploits(self, query: str) -> Optional[Dict]:
        """Search for exploits related to a query using public APIs"""
        try:
            # Using Exploit-DB API
            url = 'https://services.exploitdb.com/v1/search'
            params = {
                'q': query,
                'type': 'remote'
            }
            
            response = requests.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            
            data = response.json()
            return {
                'source': 'Exploit-DB',
                'query': query,
                'results': data,
                'fetched_at': datetime.now()
            }
        
        except Exception as e:
            logger.error(f"Error searching exploits for {query}: {str(e)}")
            return None
    
    def get_cisa_alerts(self) -> Optional[List[Dict]]:
        """Fetch latest CISA security alerts"""
        try:
            url = 'https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json'
            
            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()
            
            data = response.json()
            vulnerabilities = data.get('vulnerabilities', [])
            
            formatted_alerts = []
            for vuln in vulnerabilities[:10]:  # Get top 10
                formatted_alerts.append({
                    'source': 'CISA',
                    'cve_id': vuln.get('cveID'),
                    'vendor': vuln.get('vendor'),
                    'product': vuln.get('product'),
                    'vulnerability_name': vuln.get('vulnerabilityName'),
                    'date_added': vuln.get('dateAdded'),
                    'short_description': vuln.get('shortDescription', ''),
                    'threat_level': 'CRITICAL',
                    'fetched_at': datetime.now()
                })
            
            logger.info(f"Successfully fetched {len(formatted_alerts)} CISA alerts")
            return formatted_alerts
        
        except Exception as e:
            logger.error(f"Error fetching CISA alerts: {str(e)}")
            return None
    
    def get_shodan_data(self, query: str) -> Optional[Dict]:
        """Search Shodan for internet-connected device information"""
        if not self.shodan_key:
            logger.warning("Shodan API key not configured")
            return None
        
        try:
            url = 'https://api.shodan.io/shodan/host/search'
            params = {
                'q': query,
                'key': self.shodan_key,
                'limit': 10
            }
            
            response = requests.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            
            data = response.json()
            return {
                'source': 'Shodan',
                'query': query,
                'results': data.get('matches', []),
                'total_results': data.get('total'),
                'fetched_at': datetime.now()
            }
        
        except Exception as e:
            logger.error(f"Error searching Shodan for {query}: {str(e)}")
            return None
