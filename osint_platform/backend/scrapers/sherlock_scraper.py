"""
Sherlock OSINT Scraper - Recherche username sur 300+ sites
Utilise l'outil Sherlock officiel
"""
import subprocess
import json
import os
from typing import Dict, Any, List
from .base_scraper import BaseScraper


class SherlockScraper(BaseScraper):
    """Scraper utilisant Sherlock pour rechercher des usernames"""
    
    def __init__(self):
        super().__init__(rate_limit=0.5)
    
    async def scrape(self, username: str) -> Dict[str, Any]:
        """
        Recherche un username avec Sherlock sur 300+ sites
        
        Args:
            username: Le nom d'utilisateur à rechercher
            
        Returns:
            Dict avec les profils trouvés
        """
        print(f"🔍 [Sherlock] Recherche de '{username}' sur 300+ sites...")
        
        results = {
            'username': username,
            'tool': 'Sherlock',
            'profiles_found': [],
            'total_found': 0
        }
        
        try:
            # Créer un dossier temporaire pour les résultats
            output_dir = '/tmp/sherlock_results'
            os.makedirs(output_dir, exist_ok=True)
            output_file = f'{output_dir}/{username}.json'
            
            # Exécuter Sherlock en mode JSON
            cmd = [
                'sherlock',
                username,
                '--json',
                output_file,
                '--timeout',
                '10'
            ]
            
            process = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=120
            )
            
            # Lire les résultats JSON
            if os.path.exists(output_file):
                with open(output_file, 'r') as f:
                    sherlock_data = json.load(f)
                
                # Parser les résultats
                profiles = []
                for platform, data in sherlock_data.items():
                    if isinstance(data, dict) and data.get('status') == 'Claimed':
                        profiles.append({
                            'platform': platform,
                            'url': data.get('url'),
                            'status': 'found',
                            'response_time': data.get('response_time')
                        })
                
                results['profiles_found'] = profiles
                results['total_found'] = len(profiles)
                
                # Nettoyage
                os.remove(output_file)
            
            return results
            
        except subprocess.TimeoutExpired:
            results['error'] = 'Timeout: Sherlock a mis trop de temps'
            return results
        except Exception as e:
            results['error'] = f'Erreur Sherlock: {str(e)}'
            return results
