"""
Phone Number OSINT Scraper
Utilise: Numverify, recherches publiques
"""
import os
import requests
from typing import Dict, Any
from .base_scraper import BaseScraper


class PhoneScraper(BaseScraper):
    """Scraper OSINT pour numéros de téléphone"""
    
    def __init__(self):
        super().__init__(rate_limit=1.0)
        self.numverify_api_key = os.getenv('NUMVERIFY_API_KEY', '')
    
    async def scrape(self, phone: str) -> Dict[str, Any]:
        """
        Analyse un numéro de téléphone
        
        Args:
            phone: Numéro de téléphone à analyser
            
        Returns:
            Dict avec informations sur le numéro
        """
        # Nettoyage du numéro
        clean_phone = phone.replace('+', '').replace(' ', '').replace('-', '')
        
        results = {
            'phone': phone,
            'clean_phone': clean_phone,
            'validation': await self._validate_number(clean_phone),
            'carrier': await self._get_carrier_info(clean_phone)
        }
        
        return results
    
    async def _validate_number(self, phone: str) -> Dict:
        """Valide et obtient des infos via Numverify"""
        if not self.numverify_api_key:
            return {'error': 'NUMVERIFY_API_KEY manquante'}
        
        try:
            await self.rate_limit_wait()
            
            url = "http://apilayer.net/api/validate"
            params = {
                'access_key': self.numverify_api_key,
                'number': phone,
                'format': 1
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'valid': data.get('valid', False),
                    'country': data.get('country_name'),
                    'country_code': data.get('country_code'),
                    'location': data.get('location'),
                    'carrier': data.get('carrier'),
                    'line_type': data.get('line_type')
                }
            
            return {'valid': False}
            
        except Exception as e:
            return {'error': str(e)}
    
    async def _get_carrier_info(self, phone: str) -> Dict:
        """Obtient des informations sur l'opérateur"""
        # Patterns basiques pour identifier les opérateurs (France)
        operators = {
            '06': 'Mobile',
            '07': 'Mobile',
            '01': 'Fixe - Île-de-France',
            '02': 'Fixe - Nord-Ouest',
            '03': 'Fixe - Nord-Est',
            '04': 'Fixe - Sud-Est',
            '05': 'Fixe - Sud-Ouest',
            '09': 'VoIP'
        }
        
        if len(phone) >= 2:
            prefix = phone[:2]
            return {
                'type': operators.get(prefix, 'Inconnu'),
                'prefix': prefix
            }
        
        return {'type': 'Inconnu'}
