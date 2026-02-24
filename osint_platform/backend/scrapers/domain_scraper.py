"""
Domain OSINT Scraper
Analyse les domaines, whois, DNS, etc.
"""
import os
import requests
from typing import Dict, Any
from .base_scraper import BaseScraper


class DomainScraper(BaseScraper):
    """Scraper OSINT pour domaines"""
    
    def __init__(self):
        super().__init__(rate_limit=1.0)
        self.virustotal_api_key = os.getenv('VIRUSTOTAL_API_KEY', '')
    
    async def scrape(self, domain: str) -> Dict[str, Any]:
        """
        Analyse un domaine
        
        Args:
            domain: Nom de domaine à analyser
            
        Returns:
            Dict avec informations sur le domaine
        """
        results = {
            'domain': domain,
            'dns': await self._get_dns_info(domain),
            'virustotal': await self._check_virustotal(domain),
            'ssl': await self._check_ssl(domain)
        }
        
        return results
    
    async def _get_dns_info(self, domain: str) -> Dict:
        """Obtient les enregistrements DNS"""
        try:
            # Utilisation de l'API DNS Google
            url = f"https://dns.google/resolve?name={domain}"
            
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'records': data.get('Answer', []),
                    'status': data.get('Status')
                }
            
            return {}
            
        except Exception as e:
            return {'error': str(e)}
    
    async def _check_virustotal(self, domain: str) -> Dict:
        """Vérifie la réputation sur VirusTotal"""
        if not self.virustotal_api_key:
            return {'error': 'VIRUSTOTAL_API_KEY manquante'}
        
        try:
            await self.rate_limit_wait()
            
            url = f"https://www.virustotal.com/api/v3/domains/{domain}"
            headers = {'x-apikey': self.virustotal_api_key}
            
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                stats = data.get('data', {}).get('attributes', {}).get('last_analysis_stats', {})
                return {
                    'malicious': stats.get('malicious', 0),
                    'suspicious': stats.get('suspicious', 0),
                    'clean': stats.get('harmless', 0),
                    'undetected': stats.get('undetected', 0)
                }
            
            return {}
            
        except Exception as e:
            return {'error': str(e)}
    
    async def _check_ssl(self, domain: str) -> Dict:
        """Vérifie le certificat SSL"""
        try:
            import ssl
            import socket
            
            context = ssl.create_default_context()
            with socket.create_connection((domain, 443), timeout=5) as sock:
                with context.wrap_socket(sock, server_hostname=domain) as ssock:
                    cert = ssock.getpeercert()
                    
                    return {
                        'issuer': dict(x[0] for x in cert['issuer']),
                        'subject': dict(x[0] for x in cert['subject']),
                        'valid_from': cert.get('notBefore'),
                        'valid_until': cert.get('notAfter'),
                        'version': cert.get('version')
                    }
        except Exception as e:
            return {'error': str(e)}
