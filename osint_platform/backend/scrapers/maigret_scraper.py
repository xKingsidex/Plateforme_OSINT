"""
Maigret OSINT Scraper - Meilleur que Sherlock avec 400+ sites
"""
import subprocess
import json
import os
from typing import Dict, Any
from .base_scraper import BaseScraper


class MaigretScraper(BaseScraper):
    """Scraper utilisant Maigret (meilleur que Sherlock)"""
    
    def __init__(self):
        super().__init__(rate_limit=0.5)
    
    async def scrape(self, username: str) -> Dict[str, Any]:
        """
        Recherche un username avec Maigret sur 400+ sites
        """
        print(f"🔍 [Maigret] Recherche de '{username}' sur 400+ sites...")
        
        results = {
            'username': username,
            'tool': 'Maigret',
            'profiles_found': [],
            'total_found': 0
        }
        
        try:
            # Créer un dossier temporaire
            output_dir = '/tmp/maigret_results'
            os.makedirs(output_dir, exist_ok=True)
            output_file = f'{output_dir}/{username}.json'
            
            # Exécuter Maigret
            cmd = [
                'maigret',
                username,
                '--json',
                'simple',
                '--timeout',
                '10',
                '--no-progressbar'
            ]
            
            process = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=180,
                cwd=output_dir
            )
            
            # Parser les résultats
            if process.stdout:
                try:
                    data = json.loads(process.stdout)
                    
                    profiles = []
                    for site_name, site_data in data.items():
                        if isinstance(site_data, dict) and site_data.get('status') == 'found':
                            profiles.append({
                                'platform': site_name,
                                'url': site_data.get('url'),
                                'status': 'found'
                            })
                    
                    results['profiles_found'] = profiles
                    results['total_found'] = len(profiles)
                except json.JSONDecodeError:
                    pass
            
            return results
            
        except subprocess.TimeoutExpired:
            results['error'] = 'Timeout: Maigret a mis trop de temps'
            return results
        except FileNotFoundError:
            results['error'] = 'Maigret not installed. Install with: pip install maigret'
            return results
        except Exception as e:
            results['error'] = f'Erreur Maigret: {str(e)}'
            return results
