"""
h8mail OSINT Scraper - Email breach hunting
"""
import subprocess
import json
from typing import Dict, Any
from .base_scraper import BaseScraper


class H8mailScraper(BaseScraper):
    """Scraper utilisant h8mail pour trouver les breaches d'emails"""
    
    def __init__(self):
        super().__init__(rate_limit=1.0)
    
    async def scrape(self, email: str) -> Dict[str, Any]:
        """
        Recherche les breaches pour un email
        """
        print(f"🔍 [h8mail] Hunting breaches for '{email}'...")
        
        results = {
            'email': email,
            'tool': 'h8mail',
            'breaches': [],
            'passwords_found': 0,
            'total_breaches': 0
        }
        
        try:
            # Exécuter h8mail
            cmd = [
                'h8mail',
                '-t', email,
                '--no-color'
            ]
            
            process = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            # Parser la sortie
            output = process.stdout
            
            breaches = []
            for line in output.split('\n'):
                if 'Found' in line or 'Password' in line:
                    breaches.append(line.strip())
            
            results['breaches'] = breaches
            results['total_breaches'] = len(breaches)
            
            return results
            
        except subprocess.TimeoutExpired:
            results['error'] = 'Timeout'
            return results
        except FileNotFoundError:
            results['error'] = 'h8mail not installed. Install with: pip install h8mail'
            return results
        except Exception as e:
            results['error'] = f'Erreur h8mail: {str(e)}'
            return results
