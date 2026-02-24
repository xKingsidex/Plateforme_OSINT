"""
theHarvester OSINT Scraper - Email harvesting & reconnaissance
"""
import subprocess
import json
from typing import Dict, Any
from .base_scraper import BaseScraper


class TheHarvesterScraper(BaseScraper):
    """Scraper utilisant theHarvester pour email harvesting"""
    
    def __init__(self):
        super().__init__(rate_limit=1.0)
    
    async def scrape(self, domain: str) -> Dict[str, Any]:
        """
        Harvest des emails et infos sur un domaine
        """
        print(f"🔍 [theHarvester] Harvesting '{domain}'...")
        
        results = {
            'domain': domain,
            'tool': 'theHarvester',
            'emails': [],
            'hosts': [],
            'ips': [],
            'total_found': 0
        }
        
        try:
            # Exécuter theHarvester
            cmd = [
                'theHarvester',
                '-d', domain,
                '-b', 'all',  # Toutes les sources
                '-l', '500',  # Limite de résultats
                '-f', f'/tmp/harvester_{domain}'  # Output file
            ]
            
            process = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=120
            )
            
            # Parser la sortie
            output = process.stdout
            
            # Extraire les emails
            emails = []
            for line in output.split('\n'):
                if '@' in line and domain in line:
                    email = line.strip().split()[-1]
                    if '@' in email:
                        emails.append(email)
            
            results['emails'] = list(set(emails))
            results['total_found'] = len(emails)
            
            return results
            
        except subprocess.TimeoutExpired:
            results['error'] = 'Timeout: theHarvester a mis trop de temps'
            return results
        except FileNotFoundError:
            results['error'] = 'theHarvester not installed. Install with: pip install theHarvester'
            return results
        except Exception as e:
            results['error'] = f'Erreur theHarvester: {str(e)}'
            return results
