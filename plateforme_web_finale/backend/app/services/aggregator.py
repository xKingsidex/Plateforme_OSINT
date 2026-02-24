#!/usr/bin/env python3
"""
🔥 ADVANCED OSINT AGGREGATOR - PROFESSIONAL GRADE
Orchestre toutes les recherches OSINT avec le nouveau moteur avancé
Créé par un ingénieur cybersécurité
"""

import asyncio
from typing import Dict, List, Optional
from datetime import datetime

# Import du nouveau moteur OSINT avancé
from services.osint.advanced_osint_engine import AdvancedOSINTEngine

# Imports des modules existants (fallback)
try:
    from osint_person_search import OSINTSearchEngine
    from osint_social_search import SocialMediaSearcher, run_sherlock
    LEGACY_MODULES_AVAILABLE = True
except ImportError:
    LEGACY_MODULES_AVAILABLE = False


class AdvancedOSINTAggregator:
    """
    Agrégateur OSINT ultra-fonctionnel avec nouveau moteur avancé

    Fonctionnalités:
    - Recherche multi-sources (300+ sites)
    - Génération automatique de variations de noms/usernames/emails
    - Corrélation de données intelligente
    - Google Dorking automatique
    - Intégration Sherlock, Holehe, theHarvester
    - Scoring de confiance
    - Rapports HTML professionnels
    """

    def __init__(self, config: Dict = None):
        # Nouveau moteur OSINT avancé
        self.advanced_engine = AdvancedOSINTEngine(config)

        # Modules legacy (fallback)
        if LEGACY_MODULES_AVAILABLE:
            try:
                self.person_engine = OSINTSearchEngine()
                self.social_searcher = SocialMediaSearcher()
            except:
                self.person_engine = None
                self.social_searcher = None
        else:
            self.person_engine = None
            self.social_searcher = None

    async def search(
        self,
        query: str,
        detected_types: List[str],
        search_types: Optional[List[str]] = None,
        deep_search: bool = False,
        options: Dict = None
    ) -> Dict:
        """
        Lance toutes les recherches OSINT avec le moteur avancé

        Args:
            query: La requête à chercher
            detected_types: Types détectés (email, phone, name, username, etc.)
            search_types: Types de recherche à effectuer (optionnel)
            deep_search: Active les recherches approfondies (Sherlock 300+ sites)
            options: Options supplémentaires

        Returns:
            Dict avec tous les résultats agrégés et corrélés
        """
        print(f"\n{'='*80}")
        print(f"🎯 ADVANCED OSINT AGGREGATOR - RECHERCHE AVANCÉE")
        print(f"{'='*80}")
        print(f"Query: {query}")
        print(f"Types détectés: {detected_types}")
        print(f"Deep Search: {deep_search}")
        print(f"{'='*80}\n")

        options = options or {}

        # ═══════════════════════════════════════════════════════════
        # DÉTERMINER LE TYPE DE RECHERCHE
        # ═══════════════════════════════════════════════════════════

        search_mode = self._determine_search_mode(query, detected_types)

        print(f"🔍 Mode de recherche: {search_mode}\n")

        # ═══════════════════════════════════════════════════════════
        # RECHERCHE AVEC LE MOTEUR AVANCÉ
        # ═══════════════════════════════════════════════════════════

        if search_mode in ['person', 'name', 'username']:
            # Utiliser le moteur avancé pour les personnes
            results = await self.advanced_engine.search_person_advanced(
                query=query,
                deep_search=deep_search,
                options=options
            )

            # Ajouter les métadonnées
            results['search_mode'] = search_mode
            results['aggregator_version'] = 'advanced_v2.0'

        elif search_mode == 'email':
            # Recherche email avancée
            results = await self._search_email_advanced(query, deep_search, options)

        elif search_mode == 'ip':
            # Recherche IP (legacy pour l'instant)
            results = await self._search_ip_legacy(query, options)

        elif search_mode == 'domain':
            # Recherche domaine avancée
            results = await self._search_domain_advanced(query, options)

        elif search_mode == 'phone':
            # Recherche téléphone
            results = await self._search_phone_advanced(query, options)

        else:
            # Recherche générique
            results = await self.advanced_engine.search_person_advanced(
                query=query,
                deep_search=deep_search,
                options=options
            )
            results['search_mode'] = 'generic'

        # ═══════════════════════════════════════════════════════════
        # GÉNÉRER LE RÉSUMÉ
        # ═══════════════════════════════════════════════════════════

        results['summary'] = self.generate_summary(results)

        print(f"\n{'='*80}")
        print(f"✅ RECHERCHE TERMINÉE")
        print(f"{'='*80}")
        print(f"Sources interrogées: {results['summary'].get('total_sources_queried', 0)}")
        print(f"Emails vérifiés: {results['summary'].get('verified_emails', 0)}")
        print(f"Profils sociaux: {results['summary'].get('social_profiles_found', 0)}")
        print(f"Score de confiance: {results['summary'].get('confidence_score', 0):.0%}")
        print(f"Temps d'exécution: {results.get('execution_time', 0):.2f}s")
        print(f"{'='*80}\n")

        return results

    def _determine_search_mode(self, query: str, detected_types: List[str]) -> str:
        """Détermine le mode de recherche optimal"""
        if 'email' in detected_types:
            return 'email'
        elif 'ip' in detected_types:
            return 'ip'
        elif 'domain' in detected_types:
            return 'domain'
        elif 'phone' in detected_types:
            return 'phone'
        elif 'username' in detected_types:
            return 'username'
        elif 'name' in detected_types or 'person' in detected_types:
            return 'person'
        else:
            # Par défaut, traiter comme un nom de personne
            return 'person'

    async def _search_email_advanced(
        self,
        email: str,
        deep_search: bool,
        options: Dict
    ) -> Dict:
        """Recherche email avec le moteur avancé"""
        print(f"📧 Recherche email avancée pour: {email}")

        # Extraire le nom depuis l'email
        local_part = email.split('@')[0]
        domain = email.split('@')[1] if '@' in email else None

        # Créer un nom approximatif depuis l'email local part
        # john.doe -> John Doe
        name_guess = local_part.replace('.', ' ').replace('_', ' ').replace('-', ' ').title()

        # Rechercher la personne
        results = await self.advanced_engine.search_person_advanced(
            query=name_guess,
            deep_search=deep_search,
            options=options
        )

        # Ajouter les infos email spécifiques
        results['email_analysis'] = {
            'email': email,
            'domain': domain,
            'local_part': local_part,
            'guessed_name': name_guess
        }

        # Recherches email legacy si disponible
        if self.person_engine:
            try:
                # Hunter.io
                hunter_result = self.person_engine.hunter.verify_email(email)
                results['sources']['hunter_verify'] = hunter_result

                # HIBP
                hibp_result = self.person_engine.hibp.check_email(email)
                results['sources']['hibp'] = hibp_result

                # VirusTotal sur le domaine
                if domain:
                    vt_result = self.person_engine.virustotal.scan_domain(domain)
                    results['sources']['virustotal'] = vt_result

            except Exception as e:
                print(f"⚠️  Erreur modules legacy: {e}")

        return results

    async def _search_ip_legacy(self, ip: str, options: Dict) -> Dict:
        """Recherche IP (legacy)"""
        print(f"🌐 Recherche IP: {ip}")

        results = {
            'query': ip,
            'search_type': 'ip',
            'timestamp': datetime.now().isoformat(),
            'sources': {}
        }

        if self.person_engine:
            try:
                # Shodan
                shodan_result = self.person_engine.shodan.search_ip(ip)
                results['sources']['shodan'] = shodan_result
            except Exception as e:
                print(f"⚠️  Erreur Shodan: {e}")

        return results

    async def _search_domain_advanced(self, domain: str, options: Dict) -> Dict:
        """Recherche domaine avancée"""
        print(f"🌍 Recherche domaine: {domain}")

        # Utiliser le harvester pour le domaine
        harvester_results = await self.advanced_engine.harvester.harvest_domain(domain)

        results = {
            'query': domain,
            'search_type': 'domain',
            'timestamp': datetime.now().isoformat(),
            'sources': {
                'harvester': harvester_results
            }
        }

        # VirusTotal legacy si disponible
        if self.person_engine:
            try:
                vt_result = self.person_engine.virustotal.scan_domain(domain)
                results['sources']['virustotal'] = vt_result
            except Exception as e:
                print(f"⚠️  Erreur VirusTotal: {e}")

        return results

    async def _search_phone_advanced(self, phone: str, options: Dict) -> Dict:
        """Recherche téléphone"""
        print(f"📱 Recherche téléphone: {phone}")

        # Pour l'instant, utiliser Google dorking
        google_results = await self.advanced_engine.google_engine._search_phones(phone)

        results = {
            'query': phone,
            'search_type': 'phone',
            'timestamp': datetime.now().isoformat(),
            'sources': {
                'google_dork': google_results
            }
        }

        return results

    def generate_summary(self, results: Dict) -> Dict:
        """
        Génère un résumé amélioré des résultats

        Args:
            results: Résultats complets de la recherche

        Returns:
            Dict avec le résumé détaillé
        """
        # Si le moteur avancé a déjà généré un résumé, l'utiliser
        if 'summary' in results and results['summary']:
            return results['summary']

        # Sinon, générer un résumé legacy
        sources = results.get("sources", {})
        correlated = results.get("correlated_data", {})

        summary = {
            "total_sources": len(sources),
            "successful": 0,
            "failed": 0,
            "verified_emails": len(correlated.get('verified_emails', [])),
            "potential_emails": len(correlated.get('potential_emails', [])),
            "verified_usernames": len(correlated.get('verified_usernames', [])),
            "social_profiles_found": len(correlated.get('social_profiles', [])),
            "professional_profiles_found": len(correlated.get('professional_profiles', [])),
            "companies_found": len(correlated.get('companies', [])),
            "confidence_score": correlated.get('confidence_score', 0.0),
            "key_findings": []
        }

        # Compter succès/échecs
        for source, data in sources.items():
            if isinstance(data, dict):
                if data.get("status") == "failed" or data.get("error"):
                    summary["failed"] += 1
                else:
                    summary["successful"] += 1

                # Key findings
                if source == "hibp" and data.get("breached"):
                    summary["key_findings"].append({
                        "source": "HIBP",
                        "type": "alert",
                        "message": f"⚠️ Email compromis dans {data.get('count', 0)} fuite(s)"
                    })

                elif source == "sherlock" and data.get("found"):
                    count = len(data.get("found", {}))
                    summary["key_findings"].append({
                        "source": "Sherlock",
                        "type": "info",
                        "message": f"✅ {count} profil(s) social(aux) trouvé(s)"
                    })

        return summary

    def generate_html_report(self, results: Dict) -> str:
        """Génère un rapport HTML professionnel"""
        return self.advanced_engine.generate_html_report(results)


# ═══════════════════════════════════════════════════════════════
# BACKWARD COMPATIBILITY
# Alias pour l'ancien nom
# ═══════════════════════════════════════════════════════════════

OSINTAggregator = AdvancedOSINTAggregator


# ═══════════════════════════════════════════════════════════════
# TESTS
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import asyncio

    async def test():
        aggregator = AdvancedOSINTAggregator()

        print("🔥 Test de l'agrégateur OSINT AVANCÉ\n")

        # Test avec un nom
        results = await aggregator.search(
            query="John Doe",
            detected_types=["name"],
            deep_search=False  # Mettre True pour activer Sherlock
        )

        print("\n" + "="*80)
        print("RÉSUMÉ FINAL")
        print("="*80)
        print(f"Query: {results['query']}")
        print(f"Emails vérifiés: {results['summary']['verified_emails']}")
        print(f"Profils sociaux: {results['summary']['social_profiles_found']}")
        print(f"Score de confiance: {results['summary']['confidence_score']:.0%}")
        print(f"Temps d'exécution: {results.get('execution_time', 0):.2f}s")
        print("="*80)

    asyncio.run(test())
