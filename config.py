import os 
from dotenv import load_dotenv

load_dotenv()

class Config:
  """Base Configuration"""
  SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-productions')
  SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///Threat_Intelligence.db')
  SQLALCHEMY_TRACK_MODIFICATIONS = False 

# RSS Feed Configuration
RSS_FEEDS = [
  'https://feeds.securityfocus.com/secuityfocus/home',
  'https://www.schneier.com/feed/atom/',
  'https://www.cisa.gov/feed/all.xml',
  'https://feeds2.bloomberg.com/markets/news.rss',
  'https://krebsonsecurity.com/feed/',
  'https://thehackernews.com/feeds/posts/default',
  'https://www.bleepingcomputer.com/feed/',
]

# API Configuration 
SHODAN_API_KEY = os.getenv('SHODAN_API_KEY','')
VIRUSTOTAL_API_KEY = os.getenv('VIRUSTOTAL_API_KEY','')
ABUSEIPDB_API_KEY = os.getenv('ABUSEIPDB_API_KEY','')

#Application Settings 
ITEMS_PER_PAGE = 20
CACHE_TIMEOUT = 3600 #1 HOUR
UPDATE_INTERVAL = 1800 #30 MINUTES
MAX_RETRIES = 3
TIMEOUT = 10 

#Logging 
LOG_LEVEL = os.getenv('LOG_LEVEL','INFO')
LOG_FILE = 'log/Threat_Intelligence.log'

class DevlopmentConfig(Config):
  """Devlopment Configuration"""
  DEBUG = True
  TESTING = False 

class ProductionConfig(Config):
  """Production Configuration"""
  DEBUG = False
  TESTING = False 

class TestingConfig(Config):
  """Testing Configuration"""
  TESTING = True 
  SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

config = {
  'development': DevlopmentConfig,
  'production' : ProductionConfig,
  'testing' = : TestingConfig,
  'default' = : DevelopmentConfig
}
  
