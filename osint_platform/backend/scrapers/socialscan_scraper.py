"""
Socialscan OSINT Scraper - Vérification rapide username/email
Utilise l'outil Socialscan
"""
import asyncio
from typing import Dict, Any, List
from .base_scraper import BaseScraper

try:
    from socialscan.util import Platforms, sync_execute_queries
except ImportError:
    print("⚠️ Socialscan not installed. Install with: pip install socialscan")
    sync_execute_queries = None


class SocialscanScraper(BaseScraper):
    """Scraper utilisant Socialscan pour vérifier rapidement"""
    
    def __init__(self):
        super().__init__(rate_limit=0.1)
    
    async def scrape(self, query: str) -> Dict[str, Any]:
        """
        Vérifie rapidement un username ou email
        
        Args:
            query: Username ou email à vérifier
            
        Returns:
            Dict avec les plateformes où le compte existe
        """
        if not sync_execute_queries:
            return {'error': 'Socialscan not installed'}
        
        print(f"🔍 [Socialscan] Vérification rapide de '{query}'...")
        
        results = {
            'query': query,
            'tool': 'Socialscan',
            'platforms_found': [],
            'total_found': 0
        }
        
        try:
            # Plateformes à checker
            platforms = [
                Platforms.GITHUB,
                Platforms.TWITTER,
                Platforms.INSTAGRAM,
                Platforms.REDDIT,
                Platforms.PINTEREST,
                Platforms.TUMBLR
            ]
            
            # Exécuter les requêtes
            response = await asyncio.to_thread(
                sync_execute_queries,
                [query],
                platforms
            )
            
            # Parser les résultats
            found_platforms = []
            for platform_response in response:
                if platform_response.available == False:  # Account exists
                    found_platforms.append({
                        'platform': platform_response.platform.value,
                        'query': platform_response.query,
                        'available': False,
                        'status': 'found'
                    })
            
            results['platforms_found'] = found_platforms
            results['total_found'] = len(found_platforms)
            
            return results
            
        except Exception as e:
            results['error'] = f'Erreur Socialscan: {str(e)}'
            return results
