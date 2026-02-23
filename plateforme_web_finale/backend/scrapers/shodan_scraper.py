"""
Shodan scraper - Scan IPs for open ports and vulnerabilities
"""
import os
from typing import Dict, Any
import shodan
from dotenv import load_dotenv
from scrapers.base_scraper import BaseScraper

load_dotenv()


class ShodanScraper(BaseScraper):
    """Scraper pour Shodan API"""

    def __init__(self, api_key: str = None):
        super().__init__({'rate_limit': 1})  # 1 request/second pour free tier
        self.api_key = api_key or os.getenv('SHODAN_API_KEY')

        if not self.api_key:
            raise ValueError("❌ SHODAN_API_KEY not found in environment")

        self.api = shodan.Shodan(self.api_key)

    async def scrape(self, ip_address: str) -> Dict[str, Any]:
        """
        Récupère les informations Shodan pour une IP

        Args:
            ip_address: L'adresse IP à scanner

        Returns:
            Dict contenant les données brutes de Shodan
        """
        try:
            await self.rate_limit_wait()
            result = self.api.host(ip_address)
            return result
        except shodan.APIError as e:
            return {'error': str(e), 'ip': ip_address}

    def parse(self, raw_data: Dict) -> Dict[str, Any]:
        """
        Parse les données Shodan

        Args:
            raw_data: Données brutes de l'API Shodan

        Returns:
            Dict avec données structurées
        """
        if 'error' in raw_data:
            return {
                'error': raw_data['error'],
                'ip': raw_data.get('ip', 'unknown')
            }

        # Extraction des informations principales
        parsed = {
            'ip': raw_data.get('ip_str'),
            'organization': raw_data.get('org', 'Unknown'),
            'isp': raw_data.get('isp', 'Unknown'),
            'country': raw_data.get('country_name', 'Unknown'),
            'city': raw_data.get('city', 'Unknown'),
            'os': raw_data.get('os'),
            'ports_open': raw_data.get('ports', []),
            'vulnerabilities': list(raw_data.get('vulns', [])),
            'tags': raw_data.get('tags', []),
            'hostnames': raw_data.get('hostnames', []),
            'domains': raw_data.get('domains', []),
            'services': []
        }

        # Extraction des services sur chaque port
        for item in raw_data.get('data', []):
            service = {
                'port': item.get('port'),
                'protocol': item.get('transport', 'tcp'),
                'product': item.get('product'),
                'version': item.get('version'),
                'banner': item.get('data', '')[:200]  # Limiter la taille
            }
            parsed['services'].append(service)

        # Calcul du score de risque
        parsed['risk_score'] = self._calculate_risk_score(raw_data)
        parsed['risk_level'] = self._get_risk_level(parsed['risk_score'])

        return parsed

    def _calculate_risk_score(self, data: Dict) -> float:
        """
        Calcule un score de risque basé sur les données Shodan

        Args:
            data: Données brutes Shodan

        Returns:
            Score de 0 à 100
        """
        score = 0.0

        # Nombre de ports ouverts (max 30 points)
        ports_count = len(data.get('ports', []))
        score += min(ports_count * 3, 30)

        # Vulnérabilités connues (max 50 points)
        vulns_count = len(data.get('vulns', []))
        score += min(vulns_count * 15, 50)

        # Ports critiques ouverts (10 points par port)
        critical_ports = {
            21: 'FTP',
            22: 'SSH',
            23: 'Telnet',
            445: 'SMB',
            1433: 'MS-SQL',
            3306: 'MySQL',
            3389: 'RDP',
            5432: 'PostgreSQL',
            6379: 'Redis',
            27017: 'MongoDB'
        }
        open_critical = set(data.get('ports', [])) & set(critical_ports.keys())
        score += len(open_critical) * 10

        return min(score, 100)

    def _get_risk_level(self, score: float) -> str:
        """Convertit le score en niveau de risque"""
        if score >= 75:
            return 'critical'
        elif score >= 50:
            return 'high'
        elif score >= 25:
            return 'medium'
        else:
            return 'low'


# Test du scraper
if __name__ == "__main__":
    import asyncio

    async def test():
        """Test le scraper Shodan"""
        print("=" * 60)
        print("🧪 TEST DU SCRAPER SHODAN")
        print("=" * 60)

        scraper = ShodanScraper()

        # Test avec Google DNS (8.8.8.8)
        print("\n📍 Scanning 8.8.8.8 (Google DNS)...\n")
        result = await scraper.process('8.8.8.8')

        print("=" * 60)
        print("📊 RÉSULTATS")
        print("=" * 60)

        if result['status'] == 'success':
            data = result['data']

            if 'error' in data:
                print(f"❌ Erreur : {data['error']}")
            else:
                print(f"✅ Status : SUCCESS")
                print(f"\n📍 IP : {data['ip']}")
                print(f"🏢 Organisation : {data['organization']}")
                print(f"🌍 Pays : {data['country']}")
                print(f"🏙️  Ville : {data['city']}")
                print(f"🖥️  OS : {data['os'] or 'Unknown'}")
                print(f"\n🔌 Ports ouverts : {data['ports_open']}")
                print(f"\n⚠️  Vulnérabilités : {len(data['vulnerabilities'])}")
                if data['vulnerabilities']:
                    for vuln in data['vulnerabilities'][:5]:
                        print(f"   - {vuln}")

                print(f"\n🎯 Score de risque : {data['risk_score']:.1f}/100")
                print(f"📊 Niveau de risque : {data['risk_level'].upper()}")

                if data['services']:
                    print(f"\n🔧 Services détectés :")
                    for service in data['services'][:5]:
                        print(f"   - Port {service['port']}: {service['product'] or 'Unknown'} "
                              f"({service['protocol']})")

        else:
            print(f"❌ Erreur : {result['error']}")

        print("\n" + "=" * 60)

    # Lancer le test
    asyncio.run(test())
