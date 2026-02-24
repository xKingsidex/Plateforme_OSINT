"""
OSINT Scrapers Package - ULTIMATE Edition
Includes ALL real OSINT tools:
- Sherlock, Maigret (400+ sites)
- Holehe, h8mail
- Socialscan
- theHarvester
- Sublist3r
"""
from .email_scraper import EmailScraper
from .username_scraper import UsernameScraper
from .phone_scraper import PhoneScraper
from .domain_scraper import DomainScraper
from .sherlock_scraper import SherlockScraper
from .holehe_scraper import HoleheScraper
from .socialscan_scraper import SocialscanScraper
from .maigret_scraper import MaigretScraper
from .theharvester_scraper import TheHarvesterScraper
from .h8mail_scraper import H8mailScraper
from .sublist3r_scraper import Sublist3rScraper

__all__ = [
    'EmailScraper',
    'UsernameScraper',
    'PhoneScraper',
    'DomainScraper',
    'SherlockScraper',
    'HoleheScraper',
    'SocialscanScraper',
    'MaigretScraper',
    'TheHarvesterScraper',
    'H8mailScraper',
    'Sublist3rScraper'
]
