"""
═══════════════════════════════════════════════════════════════
DATA CORRELATION ENGINE
Corrèle les données OSINT de différentes sources
Trouve les liens entre emails, usernames, domaines, personnes
═══════════════════════════════════════════════════════════════
"""

from typing import Dict, List, Any, Set
from dataclasses import dataclass, field
from collections import defaultdict
import re


@dataclass
class OSINTEntity:
    """Entité OSINT (personne, email, username, etc.)"""
    entity_type: str  # person, email, username, domain, phone, company
    value: str
    confidence: float  # 0.0 - 1.0
    sources: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    related_entities: Set[str] = field(default_factory=set)


class DataCorrelationEngine:
    """Moteur de corrélation de données OSINT"""

    def __init__(self):
        self.entities = {}  # entity_id -> OSINTEntity
        self.relationships = defaultdict(set)  # entity_id -> set of related entity_ids
        self.confidence_scores = {}

    def add_entity(self, entity: OSINTEntity) -> str:
        """Ajoute une entité"""
        entity_id = f"{entity.entity_type}:{entity.value}"
        self.entities[entity_id] = entity
        return entity_id

    def correlate_data(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Corrèle toutes les données collectées

        Args:
            raw_data: Données brutes de toutes les sources

        Returns:
            Données corrélées avec relations
        """
        correlated = {
            'primary_identity': {},
            'verified_emails': [],
            'potential_emails': [],
            'verified_usernames': [],
            'potential_usernames': [],
            'social_profiles': [],
            'professional_profiles': [],
            'companies': [],
            'domains': [],
            'phone_numbers': [],
            'addresses': [],
            'related_people': [],
            'confidence_score': 0.0,
            'data_sources': set(),
            'relationships': defaultdict(list)
        }

        # 1. Identifier l'identité principale
        correlated['primary_identity'] = self._identify_primary_identity(raw_data)

        # 2. Corréler les emails
        email_correlation = self._correlate_emails(raw_data)
        correlated['verified_emails'] = email_correlation['verified']
        correlated['potential_emails'] = email_correlation['potential']

        # 3. Corréler les usernames
        username_correlation = self._correlate_usernames(raw_data)
        correlated['verified_usernames'] = username_correlation['verified']
        correlated['potential_usernames'] = username_correlation['potential']

        # 4. Corréler les profils sociaux
        correlated['social_profiles'] = self._correlate_social_profiles(raw_data)

        # 5. Corréler les profils professionnels
        correlated['professional_profiles'] = self._correlate_professional_profiles(raw_data)

        # 6. Corréler les entreprises
        correlated['companies'] = self._correlate_companies(raw_data)

        # 7. Corréler les domaines
        correlated['domains'] = self._correlate_domains(raw_data)

        # 8. Corréler les téléphones
        correlated['phone_numbers'] = self._correlate_phones(raw_data)

        # 9. Trouver les personnes liées
        correlated['related_people'] = self._find_related_people(raw_data)

        # 10. Calculer le score de confiance global
        correlated['confidence_score'] = self._calculate_confidence_score(correlated)

        # 11. Tracker les sources de données
        correlated['data_sources'] = self._extract_data_sources(raw_data)

        # 12. Établir les relations
        correlated['relationships'] = self._build_relationships(correlated)

        return correlated

    def _identify_primary_identity(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Identifie l'identité principale"""
        identity = {
            'full_name': data.get('query', ''),
            'first_name': '',
            'last_name': '',
            'variations': data.get('name_variations', []),
            'confidence': 1.0  # On a au moins le nom de la recherche
        }

        # Extraire prénom/nom
        query = data.get('query', '')
        parts = query.split()
        if len(parts) >= 2:
            identity['first_name'] = parts[0]
            identity['last_name'] = parts[-1]

        return identity

    def _correlate_emails(self, data: Dict[str, Any]) -> Dict[str, List[Dict]]:
        """Corrèle les emails trouvés"""
        verified = []
        potential = []

        # Emails de différentes sources
        all_emails = set()

        # Hunter.io
        if 'hunter_verify' in data.get('sources', {}):
            hunter_data = data['sources']['hunter_verify']
            if hunter_data.get('status') == 'success':
                email = hunter_data.get('data', {}).get('email')
                if email:
                    verified.append({
                        'email': email,
                        'confidence': 0.9,
                        'source': 'hunter.io',
                        'verified': True
                    })

        # Harvester
        if 'harvester' in data.get('sources', {}):
            harvester_emails = data['sources']['harvester'].get('emails', [])
            all_emails.update(harvester_emails)

        # Google dorking
        if 'google_dork' in data.get('sources', {}):
            dork_emails = data['sources']['google_dork'].get('emails', [])
            all_emails.update(dork_emails)

        # Classifier les emails
        for email in all_emails:
            # Vérifier si déjà vérifié
            if any(e['email'] == email for e in verified):
                continue

            # Calculer la confiance basée sur le pattern
            confidence = self._calculate_email_confidence(email, data)

            if confidence >= 0.7:
                verified.append({
                    'email': email,
                    'confidence': confidence,
                    'source': 'correlation',
                    'verified': False
                })
            else:
                potential.append({
                    'email': email,
                    'confidence': confidence,
                    'source': 'correlation',
                    'verified': False
                })

        return {
            'verified': verified,
            'potential': potential
        }

    def _correlate_usernames(self, data: Dict[str, Any]) -> Dict[str, List[Dict]]:
        """Corrèle les usernames trouvés"""
        verified = []
        potential = []

        # Sherlock results
        if 'sherlock' in data.get('sources', {}):
            sherlock_data = data['sources']['sherlock']
            if isinstance(sherlock_data, dict):
                for site, profile_data in sherlock_data.items():
                    if isinstance(profile_data, dict) and profile_data.get('found'):
                        verified.append({
                            'username': profile_data.get('username'),
                            'platform': site,
                            'url': profile_data.get('url'),
                            'confidence': 0.95,
                            'source': 'sherlock',
                            'verified': True
                        })

        # Google dork social profiles
        if 'google_dork' in data.get('sources', {}):
            social_profiles = data['sources']['google_dork'].get('social_profiles', [])
            for profile in social_profiles:
                username = profile.get('username')
                if username and not any(u['username'] == username for u in verified):
                    verified.append({
                        'username': username,
                        'platform': profile.get('site'),
                        'url': profile.get('url'),
                        'confidence': 0.8,
                        'source': 'google_dork',
                        'verified': False
                    })

        return {
            'verified': verified,
            'potential': potential
        }

    def _correlate_social_profiles(self, data: Dict[str, Any]) -> List[Dict]:
        """Corrèle les profils sociaux"""
        profiles = []

        # Google dork
        if 'google_dork' in data.get('sources', {}):
            dork_profiles = data['sources']['google_dork'].get('social_profiles', [])
            profiles.extend(dork_profiles)

        # Sherlock
        if 'sherlock' in data.get('sources', {}):
            sherlock_data = data['sources']['sherlock']
            if isinstance(sherlock_data, dict):
                for site, profile_data in sherlock_data.items():
                    if isinstance(profile_data, dict) and profile_data.get('found'):
                        profiles.append({
                            'platform': site,
                            'url': profile_data.get('url'),
                            'username': profile_data.get('username'),
                            'confidence': 0.95
                        })

        # Dédupliquer par URL
        seen_urls = set()
        unique_profiles = []
        for profile in profiles:
            url = profile.get('url')
            if url and url not in seen_urls:
                seen_urls.add(url)
                unique_profiles.append(profile)

        return unique_profiles

    def _correlate_professional_profiles(self, data: Dict[str, Any]) -> List[Dict]:
        """Corrèle les profils professionnels"""
        profiles = []

        # Google dork
        if 'google_dork' in data.get('sources', {}):
            prof_profiles = data['sources']['google_dork'].get('professional_profiles', [])
            profiles.extend(prof_profiles)

        # LinkedIn from Sherlock
        if 'sherlock' in data.get('sources', {}):
            sherlock_data = data['sources']['sherlock']
            if isinstance(sherlock_data, dict):
                linkedin = sherlock_data.get('LinkedIn', {})
                if linkedin.get('found'):
                    profiles.append({
                        'platform': 'LinkedIn',
                        'url': linkedin.get('url'),
                        'confidence': 0.95
                    })

        return profiles

    def _correlate_companies(self, data: Dict[str, Any]) -> List[Dict]:
        """Corrèle les entreprises"""
        companies = set()

        # Hunter.io domain
        if 'hunter_verify' in data.get('sources', {}):
            hunter_data = data['sources']['hunter_verify']
            if hunter_data.get('status') == 'success':
                domain = hunter_data.get('data', {}).get('domain')
                if domain:
                    companies.add(domain)

        # Harvester
        if 'harvester' in data.get('sources', {}):
            harvester_companies = data['sources']['harvester'].get('companies', [])
            companies.update(harvester_companies)

        # Google dork
        if 'google_dork' in data.get('sources', {}):
            dork_companies = data['sources']['google_dork'].get('companies', [])
            companies.update(dork_companies)

        return [{'name': company, 'confidence': 0.7} for company in companies]

    def _correlate_domains(self, data: Dict[str, Any]) -> List[Dict]:
        """Corrèle les domaines"""
        domains = set()

        # Extraire domaines des emails
        all_emails = []
        if 'harvester' in data.get('sources', {}):
            all_emails.extend(data['sources']['harvester'].get('emails', []))

        for email in all_emails:
            domain = email.split('@')[-1]
            domains.add(domain)

        # Harvester subdomains
        if 'harvester' in data.get('sources', {}):
            subdomains = data['sources']['harvester'].get('subdomains', [])
            for subdomain in subdomains:
                # Extraire le domaine principal
                parts = subdomain.split('.')
                if len(parts) >= 2:
                    domain = '.'.join(parts[-2:])
                    domains.add(domain)

        return [{'domain': domain, 'confidence': 0.8} for domain in domains]

    def _correlate_phones(self, data: Dict[str, Any]) -> List[Dict]:
        """Corrèle les numéros de téléphone"""
        phones = set()

        # Google dork
        if 'google_dork' in data.get('sources', {}):
            dork_phones = data['sources']['google_dork'].get('phones', [])
            phones.update(dork_phones)

        return [{'phone': phone, 'confidence': 0.6} for phone in phones]

    def _find_related_people(self, data: Dict[str, Any]) -> List[Dict]:
        """Trouve les personnes liées"""
        people = set()

        # Harvester
        if 'harvester' in data.get('sources', {}):
            harvester_people = data['sources']['harvester'].get('people', [])
            people.update(harvester_people)

        return [{'name': person, 'confidence': 0.5} for person in people]

    def _calculate_email_confidence(self, email: str, data: Dict[str, Any]) -> float:
        """Calcule la confiance pour un email"""
        confidence = 0.5  # Base

        # Si le nom de la personne est dans l'email
        query = data.get('query', '').lower()
        email_local = email.split('@')[0].lower()

        # Vérifier si les parties du nom sont dans l'email
        name_parts = query.split()
        matches = sum(1 for part in name_parts if part.lower() in email_local)

        if matches >= 2:
            confidence = 0.9
        elif matches == 1:
            confidence = 0.7

        # Si c'est un provider gratuit, moins de confiance
        free_providers = ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com']
        domain = email.split('@')[-1]
        if domain in free_providers:
            confidence *= 0.9

        return min(confidence, 1.0)

    def _calculate_confidence_score(self, correlated: Dict[str, Any]) -> float:
        """Calcule un score de confiance global"""
        score = 0.0
        weights = {
            'verified_emails': 0.3,
            'verified_usernames': 0.25,
            'social_profiles': 0.2,
            'professional_profiles': 0.15,
            'companies': 0.1
        }

        for key, weight in weights.items():
            items = correlated.get(key, [])
            if items:
                score += weight

        return min(score, 1.0)

    def _extract_data_sources(self, data: Dict[str, Any]) -> Set[str]:
        """Extrait les sources de données utilisées"""
        sources = set()

        if 'sources' in data:
            for source_name, source_data in data['sources'].items():
                if isinstance(source_data, dict) and source_data.get('status') == 'success':
                    sources.add(source_name)

        return sources

    def _build_relationships(self, correlated: Dict[str, Any]) -> Dict[str, List]:
        """Construit un graphe de relations"""
        relationships = defaultdict(list)

        # Email -> Username (même personne)
        for email_data in correlated.get('verified_emails', []):
            email = email_data['email']
            for username_data in correlated.get('verified_usernames', []):
                username = username_data['username']
                relationships[f"email:{email}"].append({
                    'type': 'same_person',
                    'target': f"username:{username}",
                    'confidence': 0.8
                })

        # Username -> Social Profile
        for username_data in correlated.get('verified_usernames', []):
            username = username_data['username']
            platform = username_data.get('platform')
            if platform:
                relationships[f"username:{username}"].append({
                    'type': 'has_profile',
                    'target': f"social:{platform}",
                    'confidence': 0.9
                })

        # Email -> Company (via domain)
        for email_data in correlated.get('verified_emails', []):
            email = email_data['email']
            domain = email.split('@')[-1]
            for company in correlated.get('companies', []):
                if domain in company['name']:
                    relationships[f"email:{email}"].append({
                        'type': 'works_at',
                        'target': f"company:{company['name']}",
                        'confidence': company['confidence']
                    })

        return dict(relationships)


def test_correlation():
    """Test du moteur de corrélation"""
    print(f"\n{'='*60}")
    print(f"TEST: Data Correlation Engine")
    print(f"{'='*60}\n")

    # Données simulées
    raw_data = {
        'query': 'John Doe',
        'name_variations': ['John Doe', 'Doe John', 'J. Doe'],
        'sources': {
            'hunter_verify': {
                'status': 'success',
                'data': {
                    'email': 'john.doe@company.com',
                    'domain': 'company.com'
                }
            },
            'sherlock': {
                'GitHub': {
                    'found': True,
                    'url': 'https://github.com/johndoe',
                    'username': 'johndoe'
                },
                'Twitter': {
                    'found': True,
                    'url': 'https://twitter.com/johndoe',
                    'username': 'johndoe'
                }
            },
            'harvester': {
                'emails': ['john.doe@company.com', 'j.doe@company.com'],
                'companies': ['company.com']
            }
        }
    }

    engine = DataCorrelationEngine()
    correlated = engine.correlate_data(raw_data)

    print(f"📊 Résultats de corrélation:")
    print(f"\n👤 Identité principale:")
    print(f"   {correlated['primary_identity']}")

    print(f"\n📧 Emails vérifiés ({len(correlated['verified_emails'])}):")
    for email in correlated['verified_emails']:
        print(f"   - {email['email']} (confiance: {email['confidence']:.2f})")

    print(f"\n👥 Usernames vérifiés ({len(correlated['verified_usernames'])}):")
    for username in correlated['verified_usernames']:
        print(f"   - {username['username']} @ {username['platform']}")

    print(f"\n📱 Profils sociaux ({len(correlated['social_profiles'])}):")
    for profile in correlated['social_profiles']:
        print(f"   - {profile['platform']}: {profile.get('url')}")

    print(f"\n🏢 Entreprises ({len(correlated['companies'])}):")
    for company in correlated['companies']:
        print(f"   - {company['name']}")

    print(f"\n🎯 Score de confiance global: {correlated['confidence_score']:.2f}")

    print(f"\n🔗 Relations ({len(correlated['relationships'])}):")
    for entity, relations in list(correlated['relationships'].items())[:5]:
        print(f"   {entity}:")
        for rel in relations[:3]:
            print(f"      → {rel['type']}: {rel['target']}")


if __name__ == "__main__":
    test_correlation()
