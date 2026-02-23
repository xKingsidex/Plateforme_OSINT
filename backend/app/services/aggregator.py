#!/usr/bin/env python3
"""
🔥 OSINT Aggregator - Orchestre toutes les recherches OSINT
Lance les recherches en parallèle et agrège les résultats
"""

import os
import sys
import asyncio
from typing import Dict, List, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

# Import des modules OSINT existants
from osint_person_search import OSINTSearchEngine
from osint_social_search import SocialMediaSearcher, run_sherlock


class OSINTAggregator:
    """Agrège toutes les recherches OSINT en une seule plateforme"""

    def __init__(self):
        self.person_engine = OSINTSearchEngine()
        self.social_searcher = SocialMediaSearcher()

    async def search(
        self,
        query: str,
        detected_types: List[str],
        search_types: Optional[List[str]] = None,
        deep_search: bool = False
    ) -> Dict:
        """
        Lance toutes les recherches OSINT pertinentes

        Args:
            query: La requête à chercher
            detected_types: Types détectés (email, phone, name, etc.)
            search_types: Types de recherche à effectuer (optionnel)
            deep_search: Active les recherches approfondies (Sherlock, etc.)

        Returns:
            Dict avec tous les résultats agrégés
        """
        results = {
            "query": query,
            "detected_types": detected_types,
            "timestamp": datetime.now().isoformat(),
            "sources": {}
        }

        tasks = []

        # ═══════════════════════════════════════════════════════════
        # 1. RECHERCHE EMAIL
        # ═══════════════════════════════════════════════════════════
        if "email" in detected_types:
            # Hunter.io - Vérification email
            task = self._run_in_thread(
                self.person_engine.hunter.verify_email,
                query
            )
            tasks.append(("hunter_verify", task))

            # HIBP - Fuites de données
            task = self._run_in_thread(
                self.person_engine.hibp.check_email,
                query
            )
            tasks.append(("hibp", task))

            # VirusTotal - Scanner le domaine de l'email
            domain = query.split('@')[1] if '@' in query else None
            if domain:
                task = self._run_in_thread(
                    self.person_engine.virustotal.scan_domain,
                    domain
                )
                tasks.append(("virustotal", task))

            # GitHub - Chercher avec username extrait de l'email
            username = query.split('@')[0]
            task = self._run_in_thread(
                self.person_engine.github.search_user,
                username
            )
            tasks.append(("github", task))

        # ═══════════════════════════════════════════════════════════
        # 2. RECHERCHE USERNAME
        # ═══════════════════════════════════════════════════════════
        if "username" in detected_types:
            # GitHub
            task = self._run_in_thread(
                self.person_engine.github.search_user,
                query
            )
            tasks.append(("github", task))

            # Réseaux sociaux (30+ plateformes)
            task = self._run_in_thread(
                self.social_searcher.search_username,
                query
            )
            tasks.append(("social_media", task))

            # Sherlock (si deep_search activé)
            if deep_search:
                task = self._run_in_thread(
                    run_sherlock,
                    query
                )
                tasks.append(("sherlock", task))

        # ═══════════════════════════════════════════════════════════
        # 3. RECHERCHE NOM COMPLET
        # ═══════════════════════════════════════════════════════════
        if "name" in detected_types:
            # Extraire prénom/nom
            parts = query.split()
            first_name = parts[0] if len(parts) > 0 else None
            last_name = parts[-1] if len(parts) > 1 else None

            # Recherche sociale
            username_guess = query.lower().replace(' ', '')
            task = self._run_in_thread(
                self.social_searcher.search_username,
                username_guess
            )
            tasks.append(("social_media", task))

        # ═══════════════════════════════════════════════════════════
        # 4. RECHERCHE IP
        # ═══════════════════════════════════════════════════════════
        if "ip" in detected_types:
            # Shodan
            task = self._run_in_thread(
                self.person_engine.shodan.search_ip,
                query
            )
            tasks.append(("shodan", task))

        # ═══════════════════════════════════════════════════════════
        # 5. RECHERCHE DOMAINE
        # ═══════════════════════════════════════════════════════════
        if "domain" in detected_types:
            # VirusTotal
            task = self._run_in_thread(
                self.person_engine.virustotal.scan_domain,
                query
            )
            tasks.append(("virustotal", task))

        # ═══════════════════════════════════════════════════════════
        # COLLECTER LES RÉSULTATS
        # ═══════════════════════════════════════════════════════════
        with ThreadPoolExecutor(max_workers=10) as executor:
            for source, future in tasks:
                try:
                    result = await asyncio.get_event_loop().run_in_executor(
                        executor,
                        lambda: future
                    )

                    if result and not (isinstance(result, dict) and result.get("error")):
                        results["sources"][source] = result
                    else:
                        results["sources"][source] = {
                            "status": "failed",
                            "reason": result.get("error", "Unknown") if isinstance(result, dict) else "Unknown"
                        }
                except Exception as e:
                    results["sources"][source] = {
                        "status": "failed",
                        "reason": str(e)
                    }

        return results

    def _run_in_thread(self, func, *args, **kwargs):
        """Exécute une fonction de manière synchrone et retourne le résultat"""
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return {"error": str(e)}

    def generate_summary(self, results: Dict) -> Dict:
        """
        Génère un résumé des résultats

        Args:
            results: Résultats complets de la recherche

        Returns:
            Dict avec le résumé
        """
        sources = results.get("sources", {})

        summary = {
            "total_sources": len(sources),
            "successful": 0,
            "failed": 0,
            "key_findings": []
        }

        for source, data in sources.items():
            if isinstance(data, dict) and data.get("status") == "failed":
                summary["failed"] += 1
            else:
                summary["successful"] += 1

                # Ajouter les découvertes importantes
                if source == "hibp" and data.get("breached"):
                    summary["key_findings"].append({
                        "source": "HIBP",
                        "type": "alert",
                        "message": f"⚠️ Email compromis dans {data.get('count', 0)} fuite(s)"
                    })

                elif source == "github" and not data.get("error"):
                    summary["key_findings"].append({
                        "source": "GitHub",
                        "type": "info",
                        "message": f"✅ Profil trouvé: {data.get('username')} ({data.get('public_repos', 0)} repos)"
                    })

                elif source == "social_media" and data.get("found"):
                    count = len(data.get("found", []))
                    summary["key_findings"].append({
                        "source": "Social Media",
                        "type": "info",
                        "message": f"✅ {count} profil(s) social(aux) trouvé(s)"
                    })

                elif source == "shodan" and not data.get("error"):
                    summary["key_findings"].append({
                        "source": "Shodan",
                        "type": "info",
                        "message": f"✅ IP: {data.get('ip')} ({data.get('country', 'Unknown')})"
                    })

        return summary


# ═══════════════════════════════════════════════════════════════
# TESTS
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import asyncio

    async def test():
        aggregator = OSINTAggregator()

        print("🔍 Test de l'agrégateur OSINT\n")

        # Test avec un email
        results = await aggregator.search(
            query="test@example.com",
            detected_types=["email"],
            deep_search=False
        )

        summary = aggregator.generate_summary(results)

        print(f"Résultats: {len(results['sources'])} source(s)")
        print(f"Résumé: {summary}")

    asyncio.run(test())
