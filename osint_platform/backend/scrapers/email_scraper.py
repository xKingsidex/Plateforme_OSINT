"""
Email OSINT Scraper - Analyse complète d'emails
Utilise: HaveIBeenPwned, Hunter.io, EmailRep, recherche Google
"""
import os
import requests
import asyncio
from typing import Dict, Any, List
from .base_scraper import BaseScraper


class EmailScraper(BaseScraper):
    """Scraper OSINT pour emails"""
    
    def __init__(self):
        super().__init__(rate_limit=1.0)
        self.hibp_api_key = os.getenv('HIBP_API_KEY', '')
        self.hunter_api_key = os.getenv('HUNTER_IO_KEY', '')
    
    async def scrape(self, email: str) -> Dict[str, Any]:
        """
        Collecte toutes les infos sur un email
        
        Args:
            email: L'adresse email à analyser
            
        Returns:
            Dict avec toutes les données OSINT
        """
        results = {
            'email': email,
            'valid': self._validate_email(email),
            'domain': email.split('@')[1] if '@' in email else None,
            'breaches': await self._check_hibp(email),
            'reputation': await self._check_emailrep(email),
            'social_profiles': await self._find_social_accounts(email)
        }
        
        return results
    
    def _validate_email(self, email: str) -> bool:
        """Validation basique d'email"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    async def _check_hibp(self, email: str) -> List[Dict]:
        """Vérifie les fuites de données sur HaveIBeenPwned"""
        try:
            await self.rate_limit_wait()
            
            url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}"
            headers = {'User-Agent': 'OSINT-Platform'}
            
            if self.hibp_api_key:
                headers['hibp-api-key'] = self.hibp_api_key
            
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 404:
                return []  # Aucune fuite trouvée
            
            if response.status_code == 200:
                breaches = response.json()
                return [{
                    'name': breach.get('Name'),
                    'date': breach.get('BreachDate'),
                    'data_classes': breach.get('DataClasses', [])
                } for breach in breaches]
            
            return []
            
        except Exception as e:
            return [{'error': str(e)}]
    
    async def _check_emailrep(self, email: str) -> Dict:
        """Vérifie la réputation de l'email via EmailRep"""
        try:
            await self.rate_limit_wait()
            
            url = f"https://emailrep.io/{email}"
            headers = {'User-Agent': 'OSINT-Platform'}
            
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'reputation': data.get('reputation', 'unknown'),
                    'suspicious': data.get('suspicious', False),
                    'references': data.get('references', 0),
                    'details': data.get('details', {})
                }
            
            return {'reputation': 'unknown'}
            
        except Exception as e:
            return {'error': str(e)}
    
    async def _find_social_accounts(self, email: str) -> List[str]:
        """Recherche les comptes sociaux associés (utilise des patterns connus)"""
        # Recherche basique - peut être étendue avec Sherlock ou autres outils
        social_platforms = []
        
        # Patterns de détection basiques
        username = email.split('@')[0]
        
        platforms = [
            {'name': 'GitHub', 'url': f'https://github.com/{username}'},
            {'name': 'Twitter', 'url': f'https://twitter.com/{username}'},
            {'name': 'LinkedIn', 'url': f'https://linkedin.com/in/{username}'},
            {'name': 'Instagram', 'url': f'https://instagram.com/{username}'},
        ]
        
        # Vérification parallèle (HEAD requests)
        tasks = [self._check_url_exists(platform) for platform in platforms]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        return [r for r in results if r and not isinstance(r, Exception)]
    
    async def _check_url_exists(self, platform: Dict) -> Dict:
        """Vérifie si une URL existe"""
        try:
            response = requests.head(platform['url'], timeout=5, allow_redirects=True)
            if response.status_code == 200:
                return platform
        except:
            pass
        return None
