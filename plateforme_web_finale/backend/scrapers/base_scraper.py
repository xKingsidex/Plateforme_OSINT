"""
Base scraper class for all OSINT scrapers
"""
from abc import ABC, abstractmethod
from typing import Dict, Any
import asyncio
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BaseScraper(ABC):
    """Classe de base pour tous les scrapers OSINT"""

    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.rate_limit = self.config.get('rate_limit', 1)  # requests per second
        logger.info(f"✅ Initializing {self.__class__.__name__}")

    @abstractmethod
    async def scrape(self, target: str) -> Dict[str, Any]:
        """
        Collecte les données brutes depuis la source

        Args:
            target: La cible à analyser (IP, email, domain, etc.)

        Returns:
            Dict contenant les données brutes
        """
        pass

    @abstractmethod
    def parse(self, raw_data: Dict) -> Dict[str, Any]:
        """
        Parse et nettoie les données brutes

        Args:
            raw_data: Données brutes de scrape()

        Returns:
            Dict contenant les données nettoyées
        """
        pass

    async def process(self, target: str) -> Dict[str, Any]:
        """
        Pipeline complet : scrape + parse + enrich

        Args:
            target: La cible à analyser

        Returns:
            Dict avec status et données
        """
        try:
            logger.info(f"🔍 Processing target: {target}")

            # 1. Scraping
            raw_data = await self.scrape(target)

            # 2. Parsing
            parsed_data = self.parse(raw_data)

            logger.info(f"✅ Successfully processed {target}")

            return {
                'status': 'success',
                'target': target,
                'source': self.__class__.__name__,
                'data': parsed_data
            }

        except Exception as e:
            logger.error(f"❌ Error processing {target}: {str(e)}")
            return {
                'status': 'error',
                'target': target,
                'source': self.__class__.__name__,
                'error': str(e)
            }

    async def rate_limit_wait(self):
        """Respecte le rate limit configuré"""
        await asyncio.sleep(1 / self.rate_limit)
