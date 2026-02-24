"""
Holehe OSINT Scraper - Vérification email sur 120+ sites
Utilise l'outil Holehe officiel
"""
import subprocess
import json
from typing import Dict, Any, List
from .base_scraper import BaseScraper


class HoleheScraper(BaseScraper):
    """Scraper utilisant Holehe pour vérifier des emails"""
    
    def __init__(self):
        super().__init__(rate_limit=0.5)
    
    async def scrape(self, email: str) -> Dict[str, Any]:
        """
        Vérifie si un email existe sur 120+ sites
        
        Args:
            email: L'adresse email à vérifier
            
        Returns:
            Dict avec les sites où l'email est trouvé
        """
        print(f"🔍 [Holehe] Vérification de '{email}' sur 120+ sites...")
        
        results = {
            'email': email,
            'tool': 'Holehe',
            'accounts_found': [],
            'total_found': 0
        }
        
        try:
            # Exécuter Holehe
            cmd = [
                'holehe',
                email,
                '--only-used'  # Seulement les comptes trouvés
            ]
            
            process = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=180
            )
            
            # Parser la sortie
            output_lines = process.stdout.split('\n')
            accounts = []
            
            for line in output_lines:
                # Holehe affiche "[+]" pour les comptes trouvés
                if '[+]' in line or 'Exists on' in line:
                    # Extraire le nom du site
                    parts = line.split()
                    if len(parts) >= 2:
                        site_name = parts[-1] if parts[-1] not in ['on', 'Exists'] else parts[-2]
                        accounts.append({
                            'platform': site_name,
                            'status': 'found',
                            'email_exists': True
                        })
            
            results['accounts_found'] = accounts
            results['total_found'] = len(accounts)
            
            return results
            
        except subprocess.TimeoutExpired:
            results['error'] = 'Timeout: Holehe a mis trop de temps'
            return results
        except Exception as e:
            results['error'] = f'Erreur Holehe: {str(e)}'
            return results
