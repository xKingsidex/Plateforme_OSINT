"""
Phone Number OSINT Scraper
Uses: phonenumbers library, Numverify API (optionnel)
"""
import os
import phonenumbers
from phonenumbers import geocoder, carrier, timezone
import requests
from typing import Dict, Any
from dotenv import load_dotenv
from scrapers.base_scraper import BaseScraper

load_dotenv()


class PhoneScraper(BaseScraper):
    """Scraper pour analyse de numéros de téléphone"""

    def __init__(self):
        super().__init__({'rate_limit': 1})
        self.numverify_key = os.getenv('NUMVERIFY_API_KEY')

    async def scrape(self, phone_number: str) -> Dict[str, Any]:
        """
        Analyse un numéro de téléphone

        Args:
            phone_number: Numéro au format international (+33612345678)

        Returns:
            Dict avec infos du numéro
        """
        results = {
            'phone_number': phone_number,
            'basic_info': self._parse_with_phonenumbers(phone_number),
            'numverify_info': await self._check_numverify(phone_number) if self.numverify_key else None
        }

        return results

    def _parse_with_phonenumbers(self, phone_number: str) -> Dict:
        """Parse le numéro avec la lib phonenumbers (gratuit, offline)"""
        try:
            # Parser le numéro
            parsed = phonenumbers.parse(phone_number, None)

            # Validation
            is_valid = phonenumbers.is_valid_number(parsed)
            is_possible = phonenumbers.is_possible_number(parsed)

            # Localisation
            country = geocoder.description_for_number(parsed, "fr")
            country_code = parsed.country_code
            national_number = parsed.national_number

            # Opérateur (peut ne pas toujours fonctionner)
            carrier_name = carrier.name_for_number(parsed, "fr")

            # Type de numéro
            number_type = phonenumbers.number_type(parsed)
            type_map = {
                0: 'FIXED_LINE',
                1: 'MOBILE',
                2: 'FIXED_LINE_OR_MOBILE',
                3: 'TOLL_FREE',
                4: 'PREMIUM_RATE',
                5: 'SHARED_COST',
                6: 'VOIP',
                7: 'PERSONAL_NUMBER',
                8: 'PAGER',
                9: 'UAN',
                10: 'VOICEMAIL',
                -1: 'UNKNOWN'
            }

            # Fuseau horaire
            timezones = timezone.time_zones_for_number(parsed)

            return {
                'valid': is_valid,
                'possible': is_possible,
                'international_format': phonenumbers.format_number(
                    parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL
                ),
                'national_format': phonenumbers.format_number(
                    parsed, phonenumbers.PhoneNumberFormat.NATIONAL
                ),
                'e164_format': phonenumbers.format_number(
                    parsed, phonenumbers.PhoneNumberFormat.E164
                ),
                'country_code': f"+{country_code}",
                'country': country,
                'carrier': carrier_name or 'Unknown',
                'type': type_map.get(number_type, 'UNKNOWN'),
                'timezones': list(timezones)
            }

        except phonenumbers.phonenumberutil.NumberParseException as e:
            return {'error': f'Invalid phone number: {str(e)}'}
        except Exception as e:
            return {'error': str(e)}

    async def _check_numverify(self, phone_number: str) -> Dict:
        """
        Vérifie avec Numverify API (optionnel, plus d'infos)

        Free plan: 250 requests/month
        https://numverify.com/
        """
        try:
            await self.rate_limit_wait()

            url = "http://apilayer.net/api/validate"
            params = {
                'access_key': self.numverify_key,
                'number': phone_number,
                'format': 1
            }

            response = requests.get(url, params=params, timeout=10)

            if response.status_code == 200:
                data = response.json()

                if data.get('valid'):
                    return {
                        'valid': data.get('valid'),
                        'number': data.get('number'),
                        'local_format': data.get('local_format'),
                        'international_format': data.get('international_format'),
                        'country_prefix': data.get('country_prefix'),
                        'country_code': data.get('country_code'),
                        'country_name': data.get('country_name'),
                        'location': data.get('location'),
                        'carrier': data.get('carrier'),
                        'line_type': data.get('line_type')
                    }
                else:
                    return {'error': 'Number not valid', 'details': data}

            return {'error': f'API error: {response.status_code}'}

        except Exception as e:
            return {'error': str(e)}

    def parse(self, raw_data: Dict) -> Dict[str, Any]:
        """Parse les données du téléphone"""
        phone = raw_data.get('phone_number')
        basic = raw_data.get('basic_info', {})
        numverify = raw_data.get('numverify_info')

        # Calcul du risque
        risk_score = 0.0

        # Numéro invalide = risque
        if not basic.get('valid'):
            risk_score += 50

        # VOIP = potentiellement suspect (anonymat)
        if basic.get('type') == 'VOIP':
            risk_score += 30

        # Pas d'opérateur identifié
        if basic.get('carrier') == 'Unknown':
            risk_score += 20

        parsed = {
            'phone_number': phone,
            'valid': basic.get('valid', False),
            'international_format': basic.get('international_format'),
            'country': basic.get('country'),
            'country_code': basic.get('country_code'),
            'carrier': basic.get('carrier'),
            'type': basic.get('type'),
            'timezones': basic.get('timezones', []),
            'numverify_data': numverify,
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
        print("🧪 TEST DU PHONE SCRAPER")
        print("=" * 70)

        scraper = PhoneScraper()

        # Tests avec différents numéros
        test_numbers = [
            "+33612345678",  # France mobile
            "+14155552671",  # USA
            "+442071838750",  # UK
        ]

        for phone in test_numbers:
            print(f"\n📱 Analysing: {phone}\n")

            result = await scraper.process(phone)

            print("-" * 70)

            if result['status'] == 'success':
                data = result['data']

                print(f"📱 Numéro : {data['phone_number']}")
                print(f"✅ Valide : {data['valid']}")
                print(f"🌍 Pays : {data['country']} ({data['country_code']})")
                print(f"📞 Opérateur : {data['carrier']}")
                print(f"📡 Type : {data['type']}")

                if data['timezones']:
                    print(f"🕐 Fuseaux : {', '.join(data['timezones'])}")

                if data['numverify_data'] and 'error' not in data['numverify_data']:
                    print(f"\n🔍 Info Numverify :")
                    nv = data['numverify_data']
                    print(f"   Location : {nv.get('location')}")
                    print(f"   Line Type : {nv.get('line_type')}")

                print(f"\n🎯 Score de risque : {data['risk_score']:.1f}/100")
                print(f"📊 Niveau : {data['risk_level'].upper()}")

            else:
                print(f"❌ Erreur : {result['error']}")

            print()

        print("=" * 70)

    asyncio.run(test())
