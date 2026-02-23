"""
═══════════════════════════════════════════════════════════════
GOOGLE DORKING MODULE
Recherche intelligente sur Google avec dorks OSINT
═══════════════════════════════════════════════════════════════
"""

import asyncio
import re
from typing import List, Dict, Any
from urllib.parse import quote_plus
import aiohttp
from bs4 import BeautifulSoup


class GoogleDorkingEngine:
    """Moteur de recherche Google avec dorks OSINT"""

    def __init__(self):
        self.social_media_sites = [
            'linkedin.com',
            'twitter.com',
            'facebook.com',
            'instagram.com',
            'github.com',
            'reddit.com',
            'medium.com',
            'dev.to',
            'stackoverflow.com',
            'youtube.com',
            'tiktok.com',
            'pinterest.com',
            'tumblr.com',
            'flickr.com',
            'vimeo.com',
            'behance.net',
            'dribbble.com',
            'soundcloud.com',
            'spotify.com',
            'twitch.tv'
        ]

        self.professional_sites = [
            'linkedin.com',
            'about.me',
            'crunchbase.com',
            'angel.co',
            'wellfound.com',
            'f6s.com',
            'producthunt.com'
        ]

        self.email_patterns = [
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        ]

        self.phone_patterns = [
            r'\+?\d{1,4}[-.\s]?\(?\d{1,3}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9}',
            r'\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b'
        ]

    async def search_person(self, name: str, name_variations: List[str] = None) -> Dict[str, Any]:
        """
        Recherche une personne sur Internet avec Google Dorking

        Args:
            name: Nom de la personne
            name_variations: Variations du nom

        Returns:
            Dictionnaire avec les résultats trouvés
        """
        results = {
            'name': name,
            'social_profiles': [],
            'professional_profiles': [],
            'emails': [],
            'phones': [],
            'websites': [],
            'mentions': [],
            'related_people': [],
            'companies': []
        }

        # Utiliser les variations ou juste le nom
        search_terms = name_variations if name_variations else [name]

        # Limiter à 5 variations pour ne pas spammer Google
        search_terms = search_terms[:5]

        tasks = []

        # 1. Recherche sur réseaux sociaux
        for term in search_terms[:3]:  # Top 3 variations
            for site in self.social_media_sites[:10]:  # Top 10 sites
                tasks.append(self._search_site(term, site))

        # 2. Recherche sur sites professionnels
        for term in search_terms[:2]:
            for site in self.professional_sites:
                tasks.append(self._search_site(term, site))

        # 3. Recherche d'emails
        for term in search_terms[:3]:
            tasks.append(self._search_emails(term))

        # 4. Recherche de téléphones
        for term in search_terms[:2]:
            tasks.append(self._search_phones(term))

        # Exécuter toutes les recherches en parallèle
        search_results = await asyncio.gather(*tasks, return_exceptions=True)

        # Agréger les résultats
        for result in search_results:
            if isinstance(result, dict) and not isinstance(result, Exception):
                # Social profiles
                if 'social_profiles' in result:
                    results['social_profiles'].extend(result['social_profiles'])

                # Professional profiles
                if 'professional_profiles' in result:
                    results['professional_profiles'].extend(result['professional_profiles'])

                # Emails
                if 'emails' in result:
                    results['emails'].extend(result['emails'])

                # Phones
                if 'phones' in result:
                    results['phones'].extend(result['phones'])

                # Websites
                if 'websites' in result:
                    results['websites'].extend(result['websites'])

                # Companies
                if 'companies' in result:
                    results['companies'].extend(result['companies'])

        # Dédupliquer
        results['social_profiles'] = self._deduplicate_list(results['social_profiles'])
        results['professional_profiles'] = self._deduplicate_list(results['professional_profiles'])
        results['emails'] = list(set(results['emails']))
        results['phones'] = list(set(results['phones']))
        results['websites'] = list(set(results['websites']))
        results['companies'] = list(set(results['companies']))

        return results

    async def _search_site(self, name: str, site: str) -> Dict[str, Any]:
        """Recherche sur un site spécifique"""
        query = f'site:{site} "{name}"'
        results = await self._google_search(query, num_results=5)

        response = {
            'social_profiles': [],
            'professional_profiles': [],
            'websites': []
        }

        # Classifier les résultats
        for url in results:
            if site in self.social_media_sites:
                response['social_profiles'].append({
                    'site': site,
                    'url': url,
                    'username': self._extract_username(url, site)
                })
            elif site in self.professional_sites:
                response['professional_profiles'].append({
                    'site': site,
                    'url': url,
                    'profile': self._extract_profile_name(url)
                })
            else:
                response['websites'].append(url)

        return response

    async def _search_emails(self, name: str) -> Dict[str, List[str]]:
        """Recherche d'emails associés à un nom"""
        queries = [
            f'"{name}" email',
            f'"{name}" @gmail.com',
            f'"{name}" @outlook.com',
            f'"{name}" contact'
        ]

        emails = []

        for query in queries:
            results = await self._google_search(query, num_results=10)

            # Extraire les emails des résultats (simulé ici)
            # En production, il faudrait scraper les pages
            for url in results:
                # Pattern d'extraction d'email depuis URL ou snippet
                potential_emails = self._extract_emails_from_text(url)
                emails.extend(potential_emails)

        return {'emails': list(set(emails))}

    async def _search_phones(self, name: str) -> Dict[str, List[str]]:
        """Recherche de numéros de téléphone"""
        queries = [
            f'"{name}" phone',
            f'"{name}" tel',
            f'"{name}" mobile',
            f'"{name}" contact'
        ]

        phones = []

        for query in queries:
            results = await self._google_search(query, num_results=5)

            # Extraire les numéros (simulé ici)
            for url in results:
                potential_phones = self._extract_phones_from_text(url)
                phones.extend(potential_phones)

        return {'phones': list(set(phones))}

    async def _google_search(self, query: str, num_results: int = 10) -> List[str]:
        """
        Effectue une recherche Google (simulée)

        IMPORTANT: En production, utilisez Google Custom Search API
        ou un service de scraping légal
        """
        # SIMULATION - En production, utiliser Google Custom Search API
        # https://developers.google.com/custom-search/v1/overview

        # Pour l'instant, retourner des résultats simulés
        # pour éviter de spammer Google
        print(f"🔍 Google Dork: {query}")

        # En production, faire:
        # api_key = "YOUR_GOOGLE_API_KEY"
        # search_engine_id = "YOUR_SEARCH_ENGINE_ID"
        # url = f"https://www.googleapis.com/customsearch/v1?key={api_key}&cx={search_engine_id}&q={quote_plus(query)}"
        #
        # async with aiohttp.ClientSession() as session:
        #     async with session.get(url) as response:
        #         data = await response.json()
        #         return [item['link'] for item in data.get('items', [])]

        # Simulation pour le moment
        return []

    def _extract_username(self, url: str, site: str) -> str:
        """Extrait le username depuis une URL"""
        # Patterns courants pour extraire username
        patterns = {
            'twitter.com': r'twitter\.com/([^/\?]+)',
            'github.com': r'github\.com/([^/\?]+)',
            'instagram.com': r'instagram\.com/([^/\?]+)',
            'linkedin.com': r'linkedin\.com/in/([^/\?]+)',
            'facebook.com': r'facebook\.com/([^/\?]+)',
        }

        pattern = patterns.get(site, r'{}/([\w\-\.]+)'.format(re.escape(site)))

        match = re.search(pattern, url)
        return match.group(1) if match else ''

    def _extract_profile_name(self, url: str) -> str:
        """Extrait le nom du profil depuis une URL"""
        # Extraire le dernier segment de l'URL
        segments = url.rstrip('/').split('/')
        return segments[-1] if segments else ''

    def _extract_emails_from_text(self, text: str) -> List[str]:
        """Extrait les emails depuis un texte"""
        emails = []
        for pattern in self.email_patterns:
            matches = re.findall(pattern, text)
            emails.extend(matches)
        return emails

    def _extract_phones_from_text(self, text: str) -> List[str]:
        """Extrait les numéros de téléphone depuis un texte"""
        phones = []
        for pattern in self.phone_patterns:
            matches = re.findall(pattern, text)
            phones.extend(matches)
        return phones

    def _deduplicate_list(self, items: List[Dict]) -> List[Dict]:
        """Déduplique une liste de dictionnaires"""
        seen = set()
        unique_items = []

        for item in items:
            # Utiliser l'URL comme clé unique
            key = item.get('url', str(item))
            if key not in seen:
                seen.add(key)
                unique_items.append(item)

        return unique_items

    def generate_dorks_for_person(self, name: str) -> List[str]:
        """
        Génère une liste de Google Dorks pour rechercher une personne

        Returns:
            Liste de dorks à utiliser
        """
        dorks = []

        # 1. Recherche de base
        dorks.append(f'"{name}"')

        # 2. Réseaux sociaux
        for site in self.social_media_sites[:15]:
            dorks.append(f'site:{site} "{name}"')

        # 3. Emails
        dorks.append(f'"{name}" email')
        dorks.append(f'"{name}" @gmail.com')
        dorks.append(f'"{name}" @outlook.com')
        dorks.append(f'"{name}" contact')

        # 4. Téléphones
        dorks.append(f'"{name}" phone')
        dorks.append(f'"{name}" mobile')

        # 5. Professionnel
        dorks.append(f'"{name}" CEO')
        dorks.append(f'"{name}" founder')
        dorks.append(f'"{name}" developer')
        dorks.append(f'"{name}" engineer')

        # 6. Documents
        dorks.append(f'"{name}" filetype:pdf')
        dorks.append(f'"{name}" CV filetype:pdf')
        dorks.append(f'"{name}" resume filetype:pdf')

        # 7. Sites professionnels
        dorks.append(f'site:linkedin.com/in "{name}"')
        dorks.append(f'site:github.com "{name}"')

        return dorks


async def test_google_dorking():
    """Test du moteur Google Dorking"""
    engine = GoogleDorkingEngine()

    test_name = "John Doe"

    print(f"\n{'='*60}")
    print(f"TEST: Google Dorking pour '{test_name}'")
    print(f"{'='*60}\n")

    # Générer les dorks
    dorks = engine.generate_dorks_for_person(test_name)
    print(f"📝 Google Dorks générés ({len(dorks)}):")
    for dork in dorks[:15]:
        print(f"   - {dork}")
    if len(dorks) > 15:
        print(f"   ... et {len(dorks) - 15} autres\n")

    # Recherche (simulée pour l'instant)
    print(f"\n🔍 Recherche en cours...\n")
    results = await engine.search_person(test_name)

    print(f"\n📊 Résultats:")
    print(f"   - Profils sociaux trouvés: {len(results['social_profiles'])}")
    print(f"   - Profils professionnels: {len(results['professional_profiles'])}")
    print(f"   - Emails trouvés: {len(results['emails'])}")
    print(f"   - Téléphones trouvés: {len(results['phones'])}")
    print(f"   - Sites web: {len(results['websites'])}")


if __name__ == "__main__":
    asyncio.run(test_google_dorking())
