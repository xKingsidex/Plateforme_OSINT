"""
Base Scraper - Classe de base pour tous les scrapers OSINT
"""
import time
import asyncio
from typing import Dict, Any
from abc import ABC, abstractmethod


class BaseScraper(ABC):
    """Classe abstraite pour tous les scrapers"""
    
    def __init__(self, rate_limit: float = 1.0):
        self.rate_limit = rate_limit  # Secondes entre requêtes
        self.last_request_time = 0
        
    async def rate_limit_wait(self):
        """Attend le temps nécessaire pour respecter le rate limit"""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.rate_limit:
            await asyncio.sleep(self.rate_limit - elapsed)
        self.last_request_time = time.time()
    
    @abstractmethod
    async def scrape(self, target: str) -> Dict[str, Any]:
        """Méthode abstraite à implémenter par chaque scraper"""
        pass
