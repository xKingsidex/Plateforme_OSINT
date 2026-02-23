"""
Email OSINT Scraper - Complete email profiling
Uses: HaveIBeenPwned, Hunter.io, EmailRep, Holehe
"""
import os
import requests
from typing import Dict, Any, List
from dotenv import load_dotenv
from scrapers.base_scraper import BaseScraper
import subprocess
import json

load_dotenv()


class EmailScraper(BaseScraper):
    """Scraper OSINT complet pour emails"""

    def __init__(self):
        super().__init__({'rate_limit': 1})
        self.hibp_api_key = os.getenv('HIBP_API_KEY')
        self.hunter_api_key = os.getenv('HUNTER_IO_KEY')

    async def scrape(self, email: str) -> Dict[str, Any]:
        """
        Collecte toutes les infos sur un email

        Args:
            email: L'adresse email à analyser

        Returns:
            Dict avec toutes les données collectées
        """
        results = {
            'email': email,
            'breaches': await self._check_hibp(email),
            'email_validation': await self._validate_email(email),
            'email_reputation': await self._check_emailrep(email),
            'social_accounts': await self._find_accounts(email)
        }

        return results

    async def _check_hibp(self, email: str) -> List[Dict]:
        """Vérifie les fuites sur HaveIBeenPwned"""
        try:
            await self.rate_limit_wait()

            url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}"
            headers = {}

            if self.hibp_api_key:
                headers['hibp-api-key'] = self.hibp_api_key

            response = requests.get(url, headers=headers, timeout=10)

            if response.status_code == 404:
                return []  # Pas de fuites

            if response.status_code == 200:
                breaches = response.json()
                return [
                    {
                        'name': breach.get('Name'),
                        'title': breach.get('Title'),
                        'domain': breach.get('Domain'),
                        'breach_date': breach.get('BreachDate'),
                        'added_date': breach.get('AddedDate'),
                        'pwn_count': breach.get('PwnCount'),
                        'description': breach.get('Description'),
                        'data_classes': breach.get('DataClasses', [])
                    }
                    for breach in breaches
                ]

            return []
        except Exception as e:
            return [{'error': str(e)}]

    async def _validate_email(self, email: str) -> Dict:
        """Valide l'email avec Hunter.io"""
        try:
            if not self.hunter_api_key:
                return {'error': 'Hunter.io API key not configured'}

            await self.rate_limit_wait()

            url = f"https://api.hunter.io/v2/email-verifier"
            params = {
                'email': email,
                'api_key': self.hunter_api_key
            }

            response = requests.get(url, params=params, timeout=10)

            if response.status_code == 200:
                data = response.json().get('data', {})
                return {
                    'valid': data.get('status') == 'valid',
                    'score': data.get('score'),
                    'regexp': data.get('regexp'),
                    'gibberish': data.get('gibberish'),
                    'disposable': data.get('disposable'),
                    'webmail': data.get('webmail'),
                    'mx_records': data.get('mx_records'),
                    'smtp_server': data.get('smtp_server'),
                    'smtp_check': data.get('smtp_check')
                }

            return {'error': f'Status code: {response.status_code}'}
        except Exception as e:
            return {'error': str(e)}

    async def _check_emailrep(self, email: str) -> Dict:
        """Vérifie la réputation de l'email"""
        try:
            await self.rate_limit_wait()

            url = f"https://emailrep.io/{email}"
            response = requests.get(url, timeout=10)

            if response.status_code == 200:
                data = response.json()
                return {
                    'reputation': data.get('reputation'),
                    'suspicious': data.get('suspicious'),
                    'references': data.get('references'),
                    'details': data.get('details', {})
                }

            return {'error': f'Status code: {response.status_code}'}
        except Exception as e:
            return {'error': str(e)}

    async def _find_accounts(self, email: str) -> Dict:
        """
        Trouve tous les comptes liés à l'email avec Holehe

        Note: Nécessite holehe installé: pip install holehe
        """
        try:
            # Vérifier si holehe est installé
            result = subprocess.run(
                ['holehe', email, '--only-used', '--no-color'],
                capture_output=True,
                text=True,
                timeout=60
            )

            if result.returncode == 0:
                # Parser la sortie de holehe
                accounts_found = []
                for line in result.stdout.split('\n'):
                    if '[+]' in line:
                        # Format: [+] Twitter: https://twitter.com/...
                        parts = line.split('[+]')[1].strip().split(':')
                        if len(parts) >= 2:
                            platform = parts[0].strip()
                            accounts_found.append(platform)

                return {
                    'found': len(accounts_found),
                    'platforms': accounts_found,
                    'raw_output': result.stdout
                }

            return {'error': 'Holehe not installed or failed', 'stderr': result.stderr}
        except FileNotFoundError:
            return {'error': 'Holehe not installed. Install with: pip install holehe'}
        except Exception as e:
            return {'error': str(e)}

    def parse(self, raw_data: Dict) -> Dict[str, Any]:
        """Parse les données email"""
        email = raw_data.get('email')
        breaches = raw_data.get('breaches', [])
        validation = raw_data.get('email_validation', {})
        reputation = raw_data.get('email_reputation', {})
        social_accounts = raw_data.get('social_accounts', {})

        # Calcul du score de risque
        risk_score = 0.0

        # Fuites de données (max 50 points)
        if breaches and not breaches[0].get('error'):
            breach_count = len(breaches)
            risk_score += min(breach_count * 10, 50)

        # Email invalide/suspect (20 points)
        if validation.get('disposable') or validation.get('gibberish'):
            risk_score += 20

        # Réputation (30 points)
        if reputation.get('suspicious'):
            risk_score += 30

        parsed = {
            'email': email,
            'breaches': {
                'count': len(breaches) if not breaches or not breaches[0].get('error') else 0,
                'details': breaches if not breaches or not breaches[0].get('error') else []
            },
            'validation': validation,
            'reputation': reputation,
            'social_accounts': social_accounts,
            'risk_score': min(risk_score, 100),
            'risk_level': self._get_risk_level(risk_score)
        }

        return parsed

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


# Test
if __name__ == "__main__":
    import asyncio

    async def test():
        print("=" * 70)
        print("🧪 TEST DU EMAIL SCRAPER")
        print("=" * 70)

        scraper = EmailScraper()

        # Test avec un email de test
        test_email = "test@example.com"
        print(f"\n📧 Analysing: {test_email}\n")

        result = await scraper.process(test_email)

        print("=" * 70)
        print("📊 RÉSULTATS")
        print("=" * 70)

        if result['status'] == 'success':
            data = result['data']

            print(f"\n📧 Email : {data['email']}")
            print(f"\n🔐 FUITES DE DONNÉES : {data['breaches']['count']}")

            if data['breaches']['count'] > 0:
                print("\n⚠️  Breaches détectées :")
                for breach in data['breaches']['details'][:5]:
                    print(f"   - {breach['name']} ({breach['breach_date']})")
                    print(f"     Données : {', '.join(breach['data_classes'][:5])}")

            print(f"\n✅ VALIDATION :")
            val = data['validation']
            if 'error' not in val:
                print(f"   Valid : {val.get('valid')}")
                print(f"   Score : {val.get('score')}/100")
                print(f"   Disposable : {val.get('disposable')}")
                print(f"   Webmail : {val.get('webmail')}")

            print(f"\n🌐 COMPTES SOCIAUX :")
            accounts = data['social_accounts']
            if 'error' not in accounts:
                print(f"   Trouvés : {accounts.get('found', 0)}")
                if accounts.get('platforms'):
                    for platform in accounts['platforms']:
                        print(f"   ✅ {platform}")

            print(f"\n🎯 Score de risque : {data['risk_score']:.1f}/100")
            print(f"📊 Niveau de risque : {data['risk_level'].upper()}")

        else:
            print(f"❌ Erreur : {result['error']}")

        print("\n" + "=" * 70)

    asyncio.run(test())
