"""
Username OSINT Scraper
Uses: Sherlock, Maigret (find social media accounts by username)
"""
import subprocess
import json
from typing import Dict, Any, List
from scrapers.base_scraper import BaseScraper


class UsernameScraper(BaseScraper):
    """Scraper pour trouver tous les comptes d'un username"""

    def __init__(self):
        super().__init__({'rate_limit': 0.5})  # Lent, beaucoup de requêtes

    async def scrape(self, username: str) -> Dict[str, Any]:
        """
        Trouve tous les comptes sociaux d'un username

        Args:
            username: Le pseudo à rechercher

        Returns:
            Dict avec tous les comptes trouvés
        """
        results = {
            'username': username,
            'sherlock_results': await self._run_sherlock(username),
            'manual_checks': self._check_popular_platforms(username)
        }

        return results

    async def _run_sherlock(self, username: str) -> Dict:
        """
        Lance Sherlock pour trouver le username sur 300+ sites

        Installation: pip install sherlock-project
        """
        try:
            # Lancer Sherlock
            result = subprocess.run(
                ['sherlock', username, '--json', '--timeout', '10', '--print-found'],
                capture_output=True,
                text=True,
                timeout=300  # 5 minutes max
            )

            if result.returncode == 0:
                # Parser la sortie JSON
                try:
                    # Sherlock output peut avoir du texte avant le JSON
                    output_lines = result.stdout.strip().split('\n')
                    json_line = None

                    for line in output_lines:
                        if line.startswith('{'):
                            json_line = line
                            break

                    if json_line:
                        data = json.loads(json_line)
                        return {
                            'found_count': len(data),
                            'accounts': data,
                            'success': True
                        }

                except json.JSONDecodeError:
                    # Si le JSON parse échoue, parser manuellement
                    accounts_found = []
                    for line in result.stdout.split('\n'):
                        if '[+]' in line or '✓' in line:
                            accounts_found.append(line.strip())

                    return {
                        'found_count': len(accounts_found),
                        'accounts': accounts_found,
                        'success': True,
                        'raw_output': result.stdout
                    }

            return {
                'error': 'Sherlock failed',
                'stderr': result.stderr,
                'success': False
            }

        except FileNotFoundError:
            return {
                'error': 'Sherlock not installed. Install with: pip install sherlock-project',
                'success': False
            }
        except subprocess.TimeoutExpired:
            return {
                'error': 'Sherlock timeout (5 min exceeded)',
                'success': False
            }
        except Exception as e:
            return {
                'error': str(e),
                'success': False
            }

    def _check_popular_platforms(self, username: str) -> Dict:
        """
        Génère les URLs potentielles pour les plateformes populaires

        Note: Ces URLs ne sont pas vérifiées, juste générées
        """
        platforms = {
            'Twitter': f'https://twitter.com/{username}',
            'Instagram': f'https://instagram.com/{username}',
            'GitHub': f'https://github.com/{username}',
            'LinkedIn': f'https://linkedin.com/in/{username}',
            'Facebook': f'https://facebook.com/{username}',
            'Reddit': f'https://reddit.com/user/{username}',
            'YouTube': f'https://youtube.com/@{username}',
            'TikTok': f'https://tiktok.com/@{username}',
            'Twitch': f'https://twitch.tv/{username}',
            'Medium': f'https://medium.com/@{username}',
            'Pinterest': f'https://pinterest.com/{username}',
            'Snapchat': f'https://snapchat.com/add/{username}',
            'Telegram': f'https://t.me/{username}',
            'Discord': f'{username}#????',  # Discord needs discriminator
            'Spotify': f'https://open.spotify.com/user/{username}',
            'SoundCloud': f'https://soundcloud.com/{username}',
            'Vimeo': f'https://vimeo.com/{username}',
            'Behance': f'https://behance.net/{username}',
            'Dribbble': f'https://dribbble.com/{username}',
            'DeviantArt': f'https://deviantart.com/{username}',
            'Flickr': f'https://flickr.com/people/{username}',
            'Steam': f'https://steamcommunity.com/id/{username}',
            'Xbox': f'https://account.xbox.com/profile?gamertag={username}',
            'PlayStation': f'https://psnprofiles.com/{username}',
        }

        return {
            'count': len(platforms),
            'urls': platforms,
            'note': 'URLs générées (non vérifiées). Utilisez Sherlock pour vérification.'
        }

    def parse(self, raw_data: Dict) -> Dict[str, Any]:
        """Parse les résultats username"""
        username = raw_data.get('username')
        sherlock = raw_data.get('sherlock_results', {})
        manual = raw_data.get('manual_checks', {})

        # Compilation des résultats
        accounts_found = []

        if sherlock.get('success'):
            if isinstance(sherlock.get('accounts'), dict):
                # Format JSON de Sherlock
                for platform, data in sherlock['accounts'].items():
                    accounts_found.append({
                        'platform': platform,
                        'url': data if isinstance(data, str) else data.get('url_user'),
                        'verified': True
                    })
            elif isinstance(sherlock.get('accounts'), list):
                # Format texte parsé
                for line in sherlock['accounts']:
                    accounts_found.append({
                        'platform': line.split(':')[0].replace('[+]', '').strip(),
                        'info': line,
                        'verified': True
                    })

        # Score basé sur le nombre de comptes trouvés
        risk_score = 0.0
        account_count = len(accounts_found)

        # Beaucoup de comptes = personne active en ligne (pas forcément risque)
        # Mais peut indiquer une large surface d'attaque
        if account_count > 50:
            risk_score = 30
        elif account_count > 20:
            risk_score = 20
        elif account_count > 10:
            risk_score = 10

        parsed = {
            'username': username,
            'accounts_found': account_count,
            'verified_accounts': accounts_found,
            'potential_urls': manual.get('urls', {}),
            'sherlock_success': sherlock.get('success', False),
            'risk_score': risk_score,
            'risk_level': self._get_risk_level(risk_score),
            'summary': f"{account_count} comptes trouvés pour '{username}'"
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
        print("🧪 TEST DU USERNAME SCRAPER")
        print("=" * 70)

        scraper = UsernameScraper()

        # Test avec un username populaire
        test_username = "google"  # Username connu sur plusieurs plateformes
        print(f"\n🔍 Searching for: {test_username}\n")
        print("⏳ Cela peut prendre 1-3 minutes...\n")

        result = await scraper.process(test_username)

        print("=" * 70)
        print("📊 RÉSULTATS")
        print("=" * 70)

        if result['status'] == 'success':
            data = result['data']

            print(f"\n👤 Username : {data['username']}")
            print(f"📊 Comptes trouvés : {data['accounts_found']}")

            if data['sherlock_success']:
                print(f"\n✅ COMPTES VÉRIFIÉS :")
                for i, account in enumerate(data['verified_accounts'][:15], 1):
                    platform = account.get('platform', 'Unknown')
                    url = account.get('url', account.get('info', ''))
                    print(f"   {i}. {platform}: {url}")

                if data['accounts_found'] > 15:
                    print(f"\n   ... et {data['accounts_found'] - 15} autres")

            print(f"\n📋 URLs potentielles générées : {len(data['potential_urls'])}")
            print(f"\n🎯 Score : {data['risk_score']:.1f}/100")
            print(f"📊 Niveau : {data['risk_level'].upper()}")
            print(f"\n📝 {data['summary']}")

        else:
            print(f"❌ Erreur : {result['error']}")

        print("\n" + "=" * 70)
        print("\n💡 Note : Sherlock vérifie 300+ sites, ça peut prendre du temps")
        print("💡 Si Sherlock n'est pas installé : pip install sherlock-project")

    asyncio.run(test())
