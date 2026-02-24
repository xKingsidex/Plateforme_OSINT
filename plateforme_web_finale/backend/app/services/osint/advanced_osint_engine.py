"""
═══════════════════════════════════════════════════════════════
ADVANCED OSINT ENGINE - PROFESSIONAL GRADE
Moteur OSINT ultra-fonctionnel pour vraie collecte d'intelligence
Créé par un ingénieur cybersécurité
═══════════════════════════════════════════════════════════════
"""

import asyncio
import json
import subprocess
import os
from typing import Dict, List, Any, Optional
from datetime import datetime
import aiohttp
from pathlib import Path

# Imports des modules OSINT custom
from .name_variations import NameVariationsGenerator
from .google_dorking import GoogleDorkingEngine
from .harvester_engine import HarvesterEngine, EmailValidator
from .data_correlation import DataCorrelationEngine


class AdvancedOSINTEngine:
    """
    Moteur OSINT professionnel ultra-fonctionnel

    Capacités:
    - Recherche multi-sources (300+ sites)
    - Corrélation de données automatique
    - Recherche approfondie avec variations
    - Intégration outils OSINT externes
    - Scoring de confiance intelligent
    """

    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}

        # Initialiser les moteurs
        self.name_generator = NameVariationsGenerator()
        self.google_engine = GoogleDorkingEngine()
        self.harvester = HarvesterEngine()
        self.correlator = DataCorrelationEngine()
        self.email_validator = EmailValidator()

        # Configuration des outils externes
        self.sherlock_installed = self._check_tool_installed('sherlock')
        self.holehe_installed = self._check_tool_installed('holehe')
        self.maigret_installed = self._check_tool_installed('maigret')

        # Résultats temporaires
        self.temp_dir = Path('/tmp/osint_results')
        self.temp_dir.mkdir(exist_ok=True)

    def _check_tool_installed(self, tool_name: str) -> bool:
        """Vérifie si un outil est installé"""
        try:
            result = subprocess.run(
                ['which', tool_name],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except:
            return False

    async def search_person_advanced(
        self,
        query: str,
        deep_search: bool = False,
        options: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Recherche OSINT avancée sur une personne

        Args:
            query: Nom de la personne ou identifiant
            deep_search: Activer la recherche approfondie (Sherlock 300+ sites)
            options: Options supplémentaires

        Returns:
            Résultats OSINT complets et corrélés
        """
        print(f"\n{'='*80}")
        print(f"🎯 ADVANCED OSINT SEARCH: {query}")
        print(f"{'='*80}\n")

        start_time = datetime.now()
        options = options or {}

        # Structure des résultats
        results = {
            'query': query,
            'search_type': 'person',
            'timestamp': start_time.isoformat(),
            'deep_search': deep_search,
            'sources': {},
            'correlated_data': {},
            'summary': {},
            'execution_time': 0
        }

        # Étape 1: Générer les variations de nom
        print("📝 [1/8] Génération des variations de nom...")
        name_variations = self.name_generator.generate_all_variations(query)
        username_variations = self.name_generator.generate_username_variations(query)
        email_variations = self.name_generator.generate_email_variations(query)

        print(f"   ✅ {len(name_variations)} variations de nom")
        print(f"   ✅ {len(username_variations)} variations de username")
        print(f"   ✅ {len(email_variations)} variations d'email")

        results['name_variations'] = name_variations
        results['username_variations'] = username_variations
        results['email_variations'] = email_variations

        # Étape 2: Recherche avec Sherlock (usernames sur 300+ sites)
        if deep_search and self.sherlock_installed:
            print("\n🕵️  [2/8] Sherlock - Recherche sur 300+ sites sociaux...")
            sherlock_results = await self._run_sherlock(username_variations[:10])
            results['sources']['sherlock'] = sherlock_results
            print(f"   ✅ {len(sherlock_results.get('found', {}))} profils trouvés")
        else:
            print("\n⏭️  [2/8] Sherlock - Skippé (deep_search=False ou non installé)")
            results['sources']['sherlock'] = {'status': 'skipped'}

        # Étape 3: Holehe (vérification email sur sites)
        if self.holehe_installed and email_variations:
            print("\n📧 [3/8] Holehe - Vérification emails sur sites...")
            holehe_results = await self._run_holehe(email_variations[:5])
            results['sources']['holehe'] = holehe_results
            print(f"   ✅ {len(holehe_results.get('accounts', {}))} comptes trouvés")
        else:
            print("\n⏭️  [3/8] Holehe - Skippé (non installé)")
            results['sources']['holehe'] = {'status': 'skipped'}

        # Étape 4: Google Dorking
        print("\n🔍 [4/8] Google Dorking - Recherche intelligente...")
        google_results = await self.google_engine.search_person(query, name_variations[:5])
        results['sources']['google_dork'] = google_results
        print(f"   ✅ {len(google_results.get('social_profiles', []))} profils sociaux")
        print(f"   ✅ {len(google_results.get('emails', []))} emails potentiels")

        # Étape 5: theHarvester (emails, domaines, sous-domaines)
        print("\n🌐 [5/8] Harvester - Collecte emails/domaines...")
        harvester_results = await self.harvester.harvest_person(query)
        results['sources']['harvester'] = harvester_results
        print(f"   ✅ {len(harvester_results.get('emails', []))} emails générés")
        print(f"   ✅ {len(harvester_results.get('domains', []))} domaines")

        # Étape 6: Validation des emails
        print("\n✉️  [6/8] Validation des emails...")
        validated_emails = await self._validate_emails(
            list(set(
                email_variations[:10] +
                google_results.get('emails', []) +
                harvester_results.get('emails', [])
            ))
        )
        results['sources']['email_validation'] = validated_emails
        valid_count = sum(1 for e in validated_emails if e.get('valid_format'))
        print(f"   ✅ {valid_count}/{len(validated_emails)} emails valides")

        # Étape 7: Recherche de téléphones/adresses (si activé)
        if options.get('search_phone', False):
            print("\n📱 [7/8] Recherche de numéros de téléphone...")
            phone_results = await self._search_phones(query)
            results['sources']['phones'] = phone_results
            print(f"   ✅ {len(phone_results.get('numbers', []))} numéros trouvés")
        else:
            print("\n⏭️  [7/8] Recherche téléphone - Skippé")
            results['sources']['phones'] = {'status': 'skipped'}

        # Étape 8: CORRÉLATION DE DONNÉES
        print("\n🔗 [8/8] Corrélation et analyse des données...")
        correlated = self.correlator.correlate_data(results)
        results['correlated_data'] = correlated

        print(f"\n📊 Résultats de corrélation:")
        print(f"   ✅ {len(correlated.get('verified_emails', []))} emails vérifiés")
        print(f"   ✅ {len(correlated.get('verified_usernames', []))} usernames vérifiés")
        print(f"   ✅ {len(correlated.get('social_profiles', []))} profils sociaux")
        print(f"   ✅ {len(correlated.get('professional_profiles', []))} profils pro")
        print(f"   ✅ {len(correlated.get('companies', []))} entreprises")
        print(f"   🎯 Score de confiance: {correlated.get('confidence_score', 0):.2%}")

        # Résumé final
        end_time = datetime.now()
        execution_time = (end_time - start_time).total_seconds()

        results['summary'] = {
            'total_variations_generated': len(name_variations) + len(username_variations) + len(email_variations),
            'total_sources_queried': len([s for s in results['sources'].values() if s.get('status') != 'skipped']),
            'verified_emails': len(correlated.get('verified_emails', [])),
            'potential_emails': len(correlated.get('potential_emails', [])),
            'verified_usernames': len(correlated.get('verified_usernames', [])),
            'social_profiles_found': len(correlated.get('social_profiles', [])),
            'professional_profiles_found': len(correlated.get('professional_profiles', [])),
            'companies_found': len(correlated.get('companies', [])),
            'confidence_score': correlated.get('confidence_score', 0),
            'execution_time_seconds': execution_time
        }

        results['execution_time'] = execution_time

        print(f"\n{'='*80}")
        print(f"✅ RECHERCHE TERMINÉE EN {execution_time:.2f}s")
        print(f"{'='*80}\n")

        return results

    async def _run_sherlock(self, usernames: List[str]) -> Dict[str, Any]:
        """Exécute Sherlock pour rechercher usernames sur 300+ sites"""
        if not self.sherlock_installed:
            return {'status': 'not_installed', 'found': {}}

        results = {'status': 'success', 'found': {}, 'not_found': []}

        for username in usernames[:5]:  # Limiter à 5 pour ne pas être trop long
            try:
                output_file = self.temp_dir / f"sherlock_{username}.json"

                # Commande Sherlock
                cmd = [
                    'sherlock',
                    username,
                    '--json',
                    str(output_file),
                    '--timeout', '10',
                    '--print-found'
                ]

                print(f"      🔍 Sherlock: {username}...")

                process = await asyncio.create_subprocess_exec(
                    *cmd,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )

                try:
                    stdout, stderr = await asyncio.wait_for(
                        process.communicate(),
                        timeout=120  # 2 minutes max
                    )

                    # Lire les résultats JSON
                    if output_file.exists():
                        with open(output_file, 'r') as f:
                            sherlock_data = json.load(f)
                            results['found'][username] = sherlock_data

                        # Compter les sites trouvés
                        found_sites = sum(1 for site_data in sherlock_data.values()
                                        if isinstance(site_data, dict) and
                                        site_data.get('status', {}).get('status') == 'Claimed')

                        print(f"         ✅ {found_sites} profils trouvés pour {username}")

                except asyncio.TimeoutError:
                    print(f"         ⏱️  Timeout pour {username}")
                    process.kill()

            except Exception as e:
                print(f"         ❌ Erreur Sherlock pour {username}: {e}")
                results['not_found'].append(username)

        return results

    async def _run_holehe(self, emails: List[str]) -> Dict[str, Any]:
        """Exécute Holehe pour vérifier emails sur sites"""
        if not self.holehe_installed:
            return {'status': 'not_installed', 'accounts': {}}

        results = {'status': 'success', 'accounts': {}}

        for email in emails[:3]:  # Limiter à 3 emails
            try:
                cmd = ['holehe', email, '--only-used']

                print(f"      📧 Holehe: {email}...")

                process = await asyncio.create_subprocess_exec(
                    *cmd,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )

                try:
                    stdout, stderr = await asyncio.wait_for(
                        process.communicate(),
                        timeout=60
                    )

                    # Parser la sortie
                    output = stdout.decode('utf-8')
                    sites_found = []

                    for line in output.split('\n'):
                        if '[+]' in line:  # Site trouvé
                            site_name = line.split('[+]')[-1].strip()
                            sites_found.append(site_name)

                    results['accounts'][email] = sites_found
                    print(f"         ✅ {len(sites_found)} comptes trouvés")

                except asyncio.TimeoutError:
                    print(f"         ⏱️  Timeout pour {email}")
                    process.kill()

            except Exception as e:
                print(f"         ❌ Erreur Holehe pour {email}: {e}")

        return results

    async def _validate_emails(self, emails: List[str]) -> List[Dict[str, Any]]:
        """Valide les emails"""
        validated = []

        for email in emails:
            validation = await self.email_validator.verify_email_exists(email)
            validated.append(validation)

        return validated

    async def _search_phones(self, query: str) -> Dict[str, Any]:
        """Recherche de numéros de téléphone"""
        # En production: utiliser phoneinfoga, etc.
        return {
            'status': 'not_implemented',
            'numbers': []
        }

    def generate_html_report(self, results: Dict[str, Any]) -> str:
        """Génère un rapport HTML professionnel"""
        correlated = results.get('correlated_data', {})
        summary = results.get('summary', {})

        html = f"""
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OSINT Report - {results['query']}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 2rem;
            color: #333;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 16px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 2rem;
            text-align: center;
        }}
        .header h1 {{ font-size: 2.5rem; margin-bottom: 0.5rem; }}
        .header p {{ opacity: 0.9; }}
        .content {{ padding: 2rem; }}
        .section {{
            margin-bottom: 2rem;
            padding: 1.5rem;
            background: #f8f9fa;
            border-radius: 12px;
            border-left: 4px solid #667eea;
        }}
        .section h2 {{
            color: #667eea;
            margin-bottom: 1rem;
            font-size: 1.5rem;
        }}
        .item {{
            background: white;
            padding: 1rem;
            margin: 0.5rem 0;
            border-radius: 8px;
            border: 1px solid #e0e0e0;
        }}
        .badge {{
            display: inline-block;
            padding: 0.25rem 0.75rem;
            background: #667eea;
            color: white;
            border-radius: 12px;
            font-size: 0.875rem;
            margin-right: 0.5rem;
        }}
        .badge.success {{ background: #10b981; }}
        .badge.warning {{ background: #f59e0b; }}
        .confidence {{
            float: right;
            color: #666;
            font-size: 0.875rem;
        }}
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin-bottom: 2rem;
        }}
        .stat-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 1.5rem;
            border-radius: 12px;
            text-align: center;
        }}
        .stat-value {{
            font-size: 2.5rem;
            font-weight: bold;
            margin-bottom: 0.5rem;
        }}
        .stat-label {{
            opacity: 0.9;
            font-size: 0.875rem;
            text-transform: uppercase;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎯 OSINT Intelligence Report</h1>
            <p>Advanced reconnaissance for: <strong>{results['query']}</strong></p>
            <p>Generated: {results['timestamp']}</p>
        </div>

        <div class="content">
            <!-- Statistics -->
            <div class="stats">
                <div class="stat-card">
                    <div class="stat-value">{summary.get('verified_emails', 0)}</div>
                    <div class="stat-label">Verified Emails</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{summary.get('verified_usernames', 0)}</div>
                    <div class="stat-label">Verified Usernames</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{summary.get('social_profiles_found', 0)}</div>
                    <div class="stat-label">Social Profiles</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{summary.get('confidence_score', 0):.0%}</div>
                    <div class="stat-label">Confidence Score</div>
                </div>
            </div>

            <!-- Verified Emails -->
            <div class="section">
                <h2>📧 Verified Emails</h2>
                {self._render_list(correlated.get('verified_emails', []), 'email')}
            </div>

            <!-- Social Profiles -->
            <div class="section">
                <h2>📱 Social Profiles</h2>
                {self._render_social_profiles(correlated.get('social_profiles', []))}
            </div>

            <!-- Professional Profiles -->
            <div class="section">
                <h2>💼 Professional Profiles</h2>
                {self._render_list(correlated.get('professional_profiles', []), 'profile')}
            </div>

            <!-- Companies -->
            <div class="section">
                <h2>🏢 Companies</h2>
                {self._render_list(correlated.get('companies', []), 'company')}
            </div>

            <!-- Execution Info -->
            <div class="section">
                <h2>⚙️ Execution Information</h2>
                <div class="item">
                    <strong>Total sources queried:</strong> {summary.get('total_sources_queried', 0)}<br>
                    <strong>Execution time:</strong> {summary.get('execution_time_seconds', 0):.2f} seconds<br>
                    <strong>Deep search:</strong> {'Yes' if results.get('deep_search') else 'No'}
                </div>
            </div>
        </div>
    </div>
</body>
</html>
"""
        return html

    def _render_list(self, items: List[Dict], item_type: str) -> str:
        """Rend une liste d'items en HTML"""
        if not items:
            return "<p>No data found</p>"

        html = ""
        for item in items:
            if item_type == 'email':
                html += f"""
                <div class="item">
                    <strong>{item.get('email')}</strong>
                    <span class="confidence">Confidence: {item.get('confidence', 0):.0%}</span><br>
                    <span class="badge">{'Verified' if item.get('verified') else 'Potential'}</span>
                    <span class="badge success">{item.get('source', 'unknown')}</span>
                </div>
                """
            elif item_type == 'company':
                html += f"""
                <div class="item">
                    <strong>{item.get('name')}</strong>
                    <span class="confidence">Confidence: {item.get('confidence', 0):.0%}</span>
                </div>
                """
            elif item_type == 'profile':
                html += f"""
                <div class="item">
                    <strong>{item.get('platform')}</strong>
                    <span class="confidence">Confidence: {item.get('confidence', 0):.0%}</span><br>
                    <a href="{item.get('url')}" target="_blank">{item.get('url')}</a>
                </div>
                """

        return html

    def _render_social_profiles(self, profiles: List[Dict]) -> str:
        """Rend les profils sociaux en HTML"""
        if not profiles:
            return "<p>No social profiles found</p>"

        html = ""
        for profile in profiles:
            html += f"""
            <div class="item">
                <strong>{profile.get('platform')}</strong>
                <span class="confidence">Confidence: {profile.get('confidence', 0):.0%}</span><br>
                <strong>Username:</strong> {profile.get('username', 'N/A')}<br>
                <a href="{profile.get('url')}" target="_blank">{profile.get('url')}</a>
            </div>
            """

        return html


# Fonction de test
async def test_advanced_osint():
    """Test du moteur OSINT avancé"""
    engine = AdvancedOSINTEngine()

    # Test avec un nom
    results = await engine.search_person_advanced(
        query="John Doe",
        deep_search=False,  # Mettre True pour activer Sherlock
        options={'search_phone': False}
    )

    # Afficher le résumé
    print("\n" + "="*80)
    print("RÉSUMÉ FINAL")
    print("="*80)
    print(json.dumps(results['summary'], indent=2))


if __name__ == "__main__":
    asyncio.run(test_advanced_osint())
