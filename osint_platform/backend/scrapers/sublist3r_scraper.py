"""
Sublist3r OSINT Scraper - Subdomain enumeration
"""
import subprocess
from typing import Dict, Any
from .base_scraper import BaseScraper


class Sublist3rScraper(BaseScraper):
    """Scraper utilisant Sublist3r pour énumérer les subdomains"""
    
    def __init__(self):
        super().__init__(rate_limit=1.0)
    
    async def scrape(self, domain: str) -> Dict[str, Any]:
        """
        Énumère les subdomains d'un domaine
        """
        print(f"🔍 [Sublist3r] Enumerating subdomains for '{domain}'...")
        
        results = {
            'domain': domain,
            'tool': 'Sublist3r',
            'subdomains': [],
            'total_found': 0
        }
        
        try:
            # Exécuter Sublist3r
            cmd = [
                'sublist3r',
                '-d', domain,
                '-t', '10',  # 10 threads
                '-o', f'/tmp/sublist3r_{domain}.txt'
            ]
            
            process = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=120
            )
            
            # Lire les résultats du fichier
            try:
                with open(f'/tmp/sublist3r_{domain}.txt', 'r') as f:
                    subdomains = [line.strip() for line in f if line.strip()]
                    results['subdomains'] = subdomains
                    results['total_found'] = len(subdomains)
            except FileNotFoundError:
                # Parser depuis stdout si fichier non trouvé
                subdomains = []
                for line in process.stdout.split('\n'):
                    if domain in line and line.strip():
                        subdomains.append(line.strip())
                results['subdomains'] = subdomains
                results['total_found'] = len(subdomains)
            
            return results
            
        except subprocess.TimeoutExpired:
            results['error'] = 'Timeout'
            return results
        except FileNotFoundError:
            results['error'] = 'Sublist3r not installed. Install with: pip install sublist3r'
            return results
        except Exception as e:
            results['error'] = f'Erreur Sublist3r: {str(e)}'
            return results
