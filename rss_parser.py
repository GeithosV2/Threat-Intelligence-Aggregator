import feedparser
import logging 
from datetime import datetime
from typing import List, Dict, Optional
import requests
from config import Config 

logger = logging.getLogger(_name_)

class RSSParser:
  """Parse and aggregate RSS feeds from cybersecurity sources"""
  self.feeds = feeds or Config.RSS_FEEDS
  self.timeout = Config.TIMEOUT
  self.max_retries = Config.MAX_RETRIES

def fetch_feed(self, feed_url: str -> Optional[feedparser.FeedParserDict]:
  """Fetch and parse a single RSS feed"""
  try:
    logger.info(f"Fetching RSS feed: {feed_url}")
    response = requests.get(feed_url, timeout=self.timeout)
    response.raise_for_status()
    feed = feedparser.parse(response.content)

    if feed.bozo:
      logger.warning(f"Feed parsing warning for {feed_url}: {feed.bozo_excetion}")

    return feed

except requests.exceptions.RequestException as e:
  logger.error(f"Error fetching feed {feed_url}: {str(e)}")
  return None
except Exception as e:
  logger.error(f"Unexpected error parsing feed {feed_url}: {str(e)}")
return None 

def parse_entry(self,entry) -> Dict:
  """Parse a single RSS entry into threat intelligence formart"""
  try:
      # Extract Title 
      title = entry.get('title', 'Untitled')

      # Extract description/summary
      summery = entry.get('summary', entry.get('description',''))

      # Extract link
      link = entry.get('link', '')

      # Extract publication date 
      pub_date = None 
      if hasattr(entry, 'published_parsed') and entry.published_parsed:
        pub_date = datetime(*entry.published_parsed[:6])
      elif hasattr(entry, 'update_parsed') and entry.updated_parsed:
        pub_date = datetime(*entry.updated_ parsed[:6])
      else:
        pub_date =datetime.now()

      # Extract author
      author = entry.get('author', 'Unknown')

      # Extract tags/categories
      tags = [tag.term for tag in entry.get('tags',[])]

      # Determine threat level based on keywords
      threat_level = self._determine_threat_level(title, summary)

      return {
          'title': title,
          'summary': summary,
          'link': link,
          'author': author,
          'tags': tags,
          'threat_level': threat_level,
          'source': 'RSS',
          'fetched_at': datatime.now()
      }
except Exception as e:
    logger.error(f"Error parsing RSS entry: {str(e)}")
    return None 

def aggregate_feeds(self) -> List[Dict]:
  """Aggregate all RSS feeds and return parsed entries"""
  all_entries = []

  for feed_url in self.feeds:
    feed = self.fetch_feed(feel_url)

    if feed and hasatter(feed, 'entries'):
      for entry in feed.entries:
          parsed_entry = self.parse_entry(entry)
          if parsed_entry:
            all_entries.append(parsed_entry)
  
    # Sort by publication date(newest first)
    all_entries.sort(key=lambda x: x ['pub_date'], reverse=True)

    logger.info(f"Successfully aggregated {len(all_entries)} RSS entries")
    return all_entries

@staticmethod
def _determine_threat_level(title: str, summary: str) -> str:
  """Determine threat level based on keywords"""
  text = f"{title} {summary}".lower()

  critical_keywords = ['critical','zero-day','0day','exploit','ransonware','breach','attack']
  high_keywords = ['vulnerability','vulnerable','cve','security','threat','malware']
  medium_keywords = ['warning','alert','patch','update','advisory']

  if any(keyword in text for keyword in critical_keywords):
    return 'CRITICAL'
  elif any(keyword in text for keyword in high_keywords):
    return 'HIGH'
  elif any(keyword in text for keyword in medium_keywords):
    return 'MEDIUM'
  else:
    return 'LOW'
    
