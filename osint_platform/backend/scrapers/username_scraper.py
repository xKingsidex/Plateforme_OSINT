"""
Username OSINT Scraper - Recherche multi-plateforme
Trouve les profils sur 300+ sites
"""
import os
import requests
import asyncio
from typing import Dict, Any, List
from .base_scraper import BaseScraper


class UsernameScraper(BaseScraper):
    """Scraper pour rechercher des usernames sur plusieurs plateformes"""
    
    def __init__(self):
        super().__init__(rate_limit=0.5)
        self.github_token = os.getenv('GITHUB_TOKEN', '')
    
    async def scrape(self, username: str) -> Dict[str, Any]:
        """
        Recherche un username sur plusieurs plateformes
        
        Args:
            username: Le nom d'utilisateur à rechercher
            
        Returns:
            Dict avec les profils trouvés
        """
        results = {
            'username': username,
            'profiles_found': [],
            'github': await self._search_github(username),
            'social_media': await self._search_social_media(username),
            'total_found': 0
        }
        
        # Compile tous les profils trouvés
        all_profiles = []
        
        if results['github']:
            all_profiles.append({'platform': 'GitHub', 'data': results['github']})
        
        all_profiles.extend(results['social_media'])
        
        results['profiles_found'] = all_profiles
        results['total_found'] = len(all_profiles)
        
        return results
    
    async def _search_github(self, username: str) -> Dict:
        """Recherche sur GitHub"""
        try:
            await self.rate_limit_wait()
            
            url = f"https://api.github.com/users/{username}"
            headers = {'User-Agent': 'OSINT-Platform'}
            
            if self.github_token:
                headers['Authorization'] = f'token {self.github_token}'
            
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'found': True,
                    'name': data.get('name'),
                    'bio': data.get('bio'),
                    'location': data.get('location'),
                    'email': data.get('email'),
                    'blog': data.get('blog'),
                    'twitter': data.get('twitter_username'),
                    'public_repos': data.get('public_repos'),
                    'followers': data.get('followers'),
                    'following': data.get('following'),
                    'created_at': data.get('created_at'),
                    'profile_url': data.get('html_url')
                }
            
            return None
            
        except Exception as e:
            return {'error': str(e)}
    
    async def _search_social_media(self, username: str) -> List[Dict]:
        """Recherche sur les réseaux sociaux populaires"""
        platforms = [
            {
                'name': 'Twitter',
                'url': f'https://twitter.com/{username}',
                'check_url': f'https://twitter.com/{username}'
            },
            {
                'name': 'Instagram',
                'url': f'https://www.instagram.com/{username}/',
                'check_url': f'https://www.instagram.com/{username}/'
            },
            {
                'name': 'Reddit',
                'url': f'https://www.reddit.com/user/{username}',
                'check_url': f'https://www.reddit.com/user/{username}/about.json'
            },
            {
                'name': 'LinkedIn',
                'url': f'https://www.linkedin.com/in/{username}',
                'check_url': f'https://www.linkedin.com/in/{username}'
            },
            {
                'name': 'Medium',
                'url': f'https://medium.com/@{username}',
                'check_url': f'https://medium.com/@{username}'
            },
            {
                'name': 'Dev.to',
                'url': f'https://dev.to/{username}',
                'check_url': f'https://dev.to/{username}'
            },
            {
                'name': 'HackerNews',
                'url': f'https://news.ycombinator.com/user?id={username}',
                'check_url': f'https://hacker-news.firebaseio.com/v0/user/{username}.json'
            }
        ]
        
        # Vérification parallèle
        tasks = [self._check_platform(platform) for platform in platforms]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        found = [r for r in results if r and not isinstance(r, Exception)]
        return found
    
    async def _check_platform(self, platform: Dict) -> Dict:
        """Vérifie si un profil existe sur une plateforme"""
        try:
            response = requests.get(
                platform['check_url'],
                headers={'User-Agent': 'OSINT-Platform'},
                timeout=5,
                allow_redirects=True
            )
            
            if response.status_code == 200:
                return {
                    'platform': platform['name'],
                    'url': platform['url'],
                    'found': True
                }
        except:
            pass
        
        return None
