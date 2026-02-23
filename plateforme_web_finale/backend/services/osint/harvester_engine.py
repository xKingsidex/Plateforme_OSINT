"""
═══════════════════════════════════════════════════════════════
HARVESTER ENGINE
Collecte d'emails, domaines, sous-domaines, personnes
Inspiré de theHarvester
═══════════════════════════════════════════════════════════════
"""

import asyncio
import re
from typing import List, Dict, Any, Set
import aiohttp
from urllib.parse import quote_plus


class HarvesterEngine:
    """Moteur de collecte d'informations OSINT"""

    def __init__(self):
        self.email_pattern = re.compile(
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        )

        self.subdomain_pattern = re.compile(
            r'(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}'
        )

        # Sources pour la collecte (gratuites)
        self.search_engines = [
            'google',
            'bing',
            'duckduckgo',
            'yahoo'
        ]

    async def harvest_person(self, name: str, domain: str = None) -> Dict[str, Any]:
        """
        Collecte toutes les informations sur une personne

        Args:
            name: Nom de la personne
            domain: Domaine d'entreprise (optionnel)

        Returns:
            Dictionnaire avec emails, domaines, sous-domaines, etc.
        """
        results = {
            'name': name,
            'domain': domain,
            'emails': set(),
            'domains': set(),
            'subdomains': set(),
            'people': set(),
            'social_links': set(),
            'companies': set(),
            'job_titles': set()
        }

        tasks = []

        # 1. Recherche d'emails
        tasks.append(self._search_emails(name, domain))

        # 2. Recherche de domaines
        if domain:
            tasks.append(self._search_subdomains(domain))

        # 3. Recherche de personnes liées
        tasks.append(self._search_related_people(name))

        # 4. Recherche d'entreprises
        tasks.append(self._search_companies(name))

        # 5. Recherche de liens sociaux
        tasks.append(self._search_social_links(name))

        # Exécuter toutes les recherches
        search_results = await asyncio.gather(*tasks, return_exceptions=True)

        # Agréger les résultats
        for result in search_results:
            if isinstance(result, dict) and not isinstance(result, Exception):
                for key in results.keys():
                    if key in result:
                        if isinstance(results[key], set):
                            results[key].update(result[key])
                        else:
                            results[key] = result[key]

        # Convertir les sets en listes
        for key in results.keys():
            if isinstance(results[key], set):
                results[key] = sorted(list(results[key]))

        return results

    async def _search_emails(self, name: str, domain: str = None) -> Dict[str, Set[str]]:
        """Recherche d'emails associés à un nom"""
        emails = set()

        # Générer des patterns d'emails possibles
        if domain:
            email_patterns = self._generate_email_patterns(name, domain)
            emails.update(email_patterns)

        # Recherche sur moteurs de recherche (simulée)
        search_queries = [
            f'"{name}" email',
            f'"{name}" @gmail.com',
            f'"{name}" @outlook.com',
            f'"{name}" contact'
        ]

        if domain:
            search_queries.append(f'"{name}" @{domain}')

        # En production, faire de vraies recherches sur les moteurs
        # Pour l'instant, retourner les patterns générés
        return {'emails': emails}

    async def _search_subdomains(self, domain: str) -> Dict[str, Set[str]]:
        """Recherche de sous-domaines"""
        subdomains = set()

        # Sous-domaines courants à tester
        common_subdomains = [
            'www', 'mail', 'ftp', 'webmail', 'smtp', 'pop', 'ns1', 'ns2',
            'admin', 'portal', 'dev', 'staging', 'test', 'api', 'blog',
            'shop', 'store', 'support', 'help', 'cdn', 'static', 'assets'
        ]

        for sub in common_subdomains:
            subdomain = f"{sub}.{domain}"
            # En production, vérifier si le sous-domaine existe (DNS lookup)
            # Pour l'instant, juste ajouter à la liste
            subdomains.add(subdomain)

        return {'subdomains': subdomains}

    async def _search_related_people(self, name: str) -> Dict[str, Set[str]]:
        """Recherche de personnes liées"""
        people = set()

        # En production:
        # - Scraper LinkedIn pour les collègues
        # - Chercher sur Facebook/Twitter les amis/followers
        # - Analyser les mentions communes

        # Simulation pour l'instant
        return {'people': people}

    async def _search_companies(self, name: str) -> Dict[str, Set[str]]:
        """Recherche d'entreprises liées"""
        companies = set()

        # Recherche LinkedIn, Crunchbase, etc.
        # Patterns de recherche
        search_queries = [
            f'"{name}" CEO',
            f'"{name}" founder',
            f'"{name}" company',
            f'site:linkedin.com "{name}" company'
        ]

        # En production, scraper ces sources
        return {'companies': companies}

    async def _search_social_links(self, name: str) -> Dict[str, Set[str]]:
        """Recherche de liens vers profils sociaux"""
        social_links = set()

        # Patterns de liens sociaux
        social_patterns = [
            r'https?://(?:www\.)?linkedin\.com/in/[\w\-]+',
            r'https?://(?:www\.)?twitter\.com/[\w\-]+',
            r'https?://(?:www\.)?github\.com/[\w\-]+',
            r'https?://(?:www\.)?facebook\.com/[\w\-\.]+',
            r'https?://(?:www\.)?instagram\.com/[\w\-\.]+',
        ]

        # En production, rechercher ces patterns dans les pages web
        return {'social_links': social_links}

    def _generate_email_patterns(self, name: str, domain: str) -> Set[str]:
        """Génère des patterns d'emails possibles"""
        emails = set()

        # Nettoyer le nom
        parts = name.lower().split()
        if len(parts) < 2:
            return emails

        first = parts[0]
        last = parts[-1]

        # Patterns courants
        patterns = [
            f"{first}.{last}@{domain}",
            f"{first}_{last}@{domain}",
            f"{first}{last}@{domain}",
            f"{first[0]}.{last}@{domain}",
            f"{first[0]}{last}@{domain}",
            f"{last}.{first}@{domain}",
            f"{last}{first}@{domain}",
            f"{first}@{domain}",
            f"{last}@{domain}",
            f"{first}.{last[0]}@{domain}",
            f"{first[0]}.{last[0]}@{domain}",
        ]

        emails.update(patterns)
        return emails

    async def harvest_domain(self, domain: str) -> Dict[str, Any]:
        """
        Collecte toutes les informations sur un domaine

        Args:
            domain: Nom de domaine

        Returns:
            Informations sur le domaine
        """
        results = {
            'domain': domain,
            'emails': set(),
            'subdomains': set(),
            'employees': set(),
            'technologies': set(),
            'ip_addresses': set()
        }

        tasks = [
            self._search_subdomains(domain),
            self._search_domain_emails(domain),
            self._search_domain_employees(domain)
        ]

        search_results = await asyncio.gather(*tasks, return_exceptions=True)

        # Agréger
        for result in search_results:
            if isinstance(result, dict):
                for key in results.keys():
                    if key in result and isinstance(results[key], set):
                        results[key].update(result[key])

        # Convertir sets en listes
        for key in results.keys():
            if isinstance(results[key], set):
                results[key] = sorted(list(results[key]))

        return results

    async def _search_domain_emails(self, domain: str) -> Dict[str, Set[str]]:
        """Recherche tous les emails d'un domaine"""
        emails = set()

        # Recherche sur moteurs avec patterns
        search_queries = [
            f'@{domain}',
            f'site:{domain} contact',
            f'site:{domain} email',
        ]

        # En production, utiliser theHarvester, Hunter.io API, etc.
        return {'emails': emails}

    async def _search_domain_employees(self, domain: str) -> Dict[str, Set[str]]:
        """Recherche les employés d'un domaine"""
        employees = set()

        # LinkedIn scraping
        # site:linkedin.com "{domain}"

        return {'employees': employees}


class EmailValidator:
    """Validateur d'emails"""

    def __init__(self):
        self.email_regex = re.compile(
            r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        )

    def is_valid_format(self, email: str) -> bool:
        """Vérifie le format d'un email"""
        return bool(self.email_regex.match(email))

    async def verify_email_exists(self, email: str) -> Dict[str, Any]:
        """
        Vérifie si un email existe vraiment

        En production, utiliser:
        - SMTP verification
        - Hunter.io API
        - EmailRep.io
        """
        return {
            'email': email,
            'valid_format': self.is_valid_format(email),
            'exists': None,  # Nécessite API
            'disposable': False,
            'free_provider': self._is_free_provider(email)
        }

    def _is_free_provider(self, email: str) -> bool:
        """Vérifie si c'est un fournisseur gratuit"""
        free_providers = [
            'gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com',
            'protonmail.com', 'icloud.com', 'aol.com', 'mail.com'
        ]

        domain = email.split('@')[-1].lower()
        return domain in free_providers


async def test_harvester():
    """Test du Harvester Engine"""
    engine = HarvesterEngine()

    test_name = "John Doe"
    test_domain = "example.com"

    print(f"\n{'='*60}")
    print(f"TEST: Harvester Engine")
    print(f"{'='*60}\n")

    # Test recherche personne
    print(f"🔍 Recherche pour: {test_name}")
    person_results = await engine.harvest_person(test_name, test_domain)

    print(f"\n📧 Emails générés ({len(person_results['emails'])}):")
    for email in person_results['emails'][:10]:
        print(f"   - {email}")

    # Test recherche domaine
    print(f"\n🌐 Recherche de domaine: {test_domain}")
    domain_results = await engine.harvest_domain(test_domain)

    print(f"\n📊 Sous-domaines trouvés ({len(domain_results['subdomains'])}):")
    for subdomain in domain_results['subdomains'][:10]:
        print(f"   - {subdomain}")

    # Test validation email
    validator = EmailValidator()
    test_email = f"john.doe@{test_domain}"
    validation = await validator.verify_email_exists(test_email)

    print(f"\n✉️ Validation de {test_email}:")
    print(f"   - Format valide: {validation['valid_format']}")
    print(f"   - Provider gratuit: {validation['free_provider']}")


if __name__ == "__main__":
    asyncio.run(test_harvester())
