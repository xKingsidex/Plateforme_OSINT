#!/usr/bin/env python3
"""
🔍 OSINT Social Search - Recherche de profils sur les réseaux sociaux
Usage: python3 osint_social_search.py <username ou "Nom Complet">
"""

import os
import sys
import json
import subprocess
import requests
from datetime import datetime
from typing import Dict, List
from urllib.parse import quote_plus


# ═══════════════════════════════════════════════════════════════
# RECHERCHE SUR RÉSEAUX SOCIAUX
# ═══════════════════════════════════════════════════════════════

class SocialMediaSearcher:
    """Cherche un username sur les principaux réseaux sociaux"""

    # Liste des plateformes populaires avec leurs patterns d'URL
    PLATFORMS = {
        "Twitter/X": "https://twitter.com/{}",
        "Instagram": "https://www.instagram.com/{}",
        "Facebook": "https://www.facebook.com/{}",
        "LinkedIn": "https://www.linkedin.com/in/{}",
        "GitHub": "https://github.com/{}",
        "Reddit": "https://www.reddit.com/user/{}",
        "TikTok": "https://www.tiktok.com/@{}",
        "YouTube": "https://www.youtube.com/@{}",
        "Medium": "https://medium.com/@{}",
        "Pinterest": "https://www.pinterest.com/{}",
        "Snapchat": "https://www.snapchat.com/add/{}",
        "Twitch": "https://www.twitch.tv/{}",
        "Discord": "https://discord.com/users/{}",
        "Telegram": "https://t.me/{}",
        "WhatsApp": "https://wa.me/{}",
        "Spotify": "https://open.spotify.com/user/{}",
        "SoundCloud": "https://soundcloud.com/{}",
        "Behance": "https://www.behance.net/{}",
        "Dribbble": "https://dribbble.com/{}",
        "DeviantArt": "https://{}.deviantart.com",
        "Vimeo": "https://vimeo.com/{}",
        "Flickr": "https://www.flickr.com/photos/{}",
        "Tumblr": "https://{}.tumblr.com",
        "Stack Overflow": "https://stackoverflow.com/users/{}",
        "GitLab": "https://gitlab.com/{}",
        "Patreon": "https://www.patreon.com/{}",
        "OnlyFans": "https://onlyfans.com/{}",
        "Linktree": "https://linktr.ee/{}",
        "Cash App": "https://cash.app/${}",
        "Venmo": "https://venmo.com/{}",
    }

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    def check_url_exists(self, url: str) -> bool:
        """Vérifie si une URL existe (code 200)"""
        try:
            response = self.session.head(url, timeout=5, allow_redirects=True)
            # Codes valides : 200 (OK), 301/302 (redirect mais existe)
            return response.status_code in [200, 301, 302]
        except:
            return False

    def search_username(self, username: str) -> Dict:
        """
        Cherche un username sur tous les réseaux sociaux

        Args:
            username: Username à chercher

        Returns:
            Dict avec les profils trouvés
        """
        print(f"🔍 Recherche du username: {username}")
        print(f"⏳ Test de {len(self.PLATFORMS)} plateformes...\n")

        results = {
            "username": username,
            "timestamp": datetime.now().isoformat(),
            "found": [],
            "not_found": []
        }

        for i, (platform, url_pattern) in enumerate(self.PLATFORMS.items(), 1):
            url = url_pattern.format(username)

            print(f"[{i}/{len(self.PLATFORMS)}] {platform:20s} → ", end='', flush=True)

            if self.check_url_exists(url):
                print(f"✅ TROUVÉ")
                results["found"].append({
                    "platform": platform,
                    "url": url,
                    "username": username
                })
            else:
                print(f"❌")
                results["not_found"].append(platform)

        return results


# ═══════════════════════════════════════════════════════════════
# RECHERCHE AVEC SHERLOCK (si installé)
# ═══════════════════════════════════════════════════════════════

def run_sherlock(username: str) -> Dict:
    """
    Lance Sherlock pour chercher sur 300+ sites

    Args:
        username: Username à chercher

    Returns:
        Dict avec résultats Sherlock ou None si non installé
    """
    print("\n🔎 SHERLOCK - Recherche avancée sur 300+ sites")
    print("="*70)

    # Vérifier si Sherlock est installé
    try:
        result = subprocess.run(
            ['sherlock', '--version'],
            capture_output=True,
            timeout=5
        )
        sherlock_installed = result.returncode == 0
    except:
        sherlock_installed = False

    if not sherlock_installed:
        print("⚠️  Sherlock n'est pas installé")
        print("\n📦 Pour l'installer:")
        print("   pip install sherlock-project")
        print("   OU")
        print("   git clone https://github.com/sherlock-project/sherlock.git")
        print("   cd sherlock && pip install -r requirements.txt")
        return None

    print(f"✅ Sherlock détecté! Lancement de la recherche...\n")

    # Créer le dossier de résultats s'il n'existe pas
    os.makedirs("sherlock_results", exist_ok=True)
    output_file = f"sherlock_results/{username}.txt"

    try:
        # Lancer Sherlock
        result = subprocess.run(
            ['sherlock', username, '--output', output_file, '--timeout', '10'],
            capture_output=True,
            text=True,
            timeout=120  # 2 minutes max
        )

        if result.returncode == 0:
            print(f"✅ Recherche Sherlock terminée!")
            print(f"📄 Résultats sauvegardés: {output_file}")

            # Lire les résultats
            if os.path.exists(output_file):
                with open(output_file, 'r') as f:
                    lines = f.readlines()
                    found_count = len([l for l in lines if l.strip() and not l.startswith('#')])
                    print(f"🎯 {found_count} profil(s) trouvé(s) par Sherlock\n")

            return {
                "status": "success",
                "output_file": output_file,
                "profiles_found": found_count
            }
        else:
            print(f"❌ Erreur Sherlock: {result.stderr}")
            return None

    except subprocess.TimeoutExpired:
        print("⏱️  Timeout - Sherlock a pris trop de temps")
        return None
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return None


# ═══════════════════════════════════════════════════════════════
# GOOGLE DORKS POUR RECHERCHE SOCIALE
# ═══════════════════════════════════════════════════════════════

def generate_google_dorks(name: str = None, username: str = None) -> List[str]:
    """
    Génère des Google Dorks pour chercher des profils sociaux

    Args:
        name: Nom complet
        username: Username

    Returns:
        Liste de Google Dorks à utiliser
    """
    dorks = []

    if name:
        name_quoted = quote_plus(f'"{name}"')
        dorks.extend([
            f"https://www.google.com/search?q={name_quoted}+site:linkedin.com",
            f"https://www.google.com/search?q={name_quoted}+site:twitter.com",
            f"https://www.google.com/search?q={name_quoted}+site:facebook.com",
            f"https://www.google.com/search?q={name_quoted}+site:instagram.com",
            f"https://www.google.com/search?q={name_quoted}+site:github.com",
            f"https://www.google.com/search?q={name_quoted}+inurl:profile",
            f"https://www.google.com/search?q={name_quoted}+inurl:about",
        ])

    if username:
        username_quoted = quote_plus(username)
        dorks.extend([
            f"https://www.google.com/search?q={username_quoted}+site:twitter.com",
            f"https://www.google.com/search?q={username_quoted}+site:instagram.com",
            f"https://www.google.com/search?q={username_quoted}+site:github.com",
            f"https://www.google.com/search?q={username_quoted}+site:reddit.com",
        ])

    return dorks


# ═══════════════════════════════════════════════════════════════
# AFFICHAGE DES RÉSULTATS
# ═══════════════════════════════════════════════════════════════

def display_results(results: Dict, sherlock_results: Dict = None, dorks: List[str] = None):
    """Affiche les résultats de manière lisible"""

    print("\n" + "="*70)
    print("🎯 RAPPORT - RECHERCHE DE PROFILS SOCIAUX")
    print("="*70)

    print(f"\n🔍 Recherche pour: {results['username']}")
    print(f"⏰ Timestamp: {results['timestamp']}")

    # Profils trouvés
    found = results.get("found", [])
    if found:
        print(f"\n✅ PROFILS TROUVÉS ({len(found)}):")
        print("-"*70)
        for profile in found:
            print(f"   📱 {profile['platform']:20s} → {profile['url']}")
    else:
        print(f"\n❌ Aucun profil trouvé avec ce username")

    # Résultats Sherlock
    if sherlock_results and sherlock_results.get("status") == "success":
        print(f"\n🔎 SHERLOCK:")
        print(f"   ✅ {sherlock_results.get('profiles_found', 0)} profils trouvés")
        print(f"   📄 Rapport: {sherlock_results.get('output_file')}")

    # Google Dorks
    if dorks:
        print(f"\n🔍 GOOGLE DORKS - Recherche manuelle recommandée:")
        print("-"*70)
        for i, dork in enumerate(dorks[:5], 1):  # Afficher les 5 premiers
            print(f"   {i}. {dork}")
        if len(dorks) > 5:
            print(f"   ... et {len(dorks) - 5} autre(s) dork(s)")

    print("\n" + "="*70)
    print(f"✅ Recherche terminée")
    print("="*70 + "\n")


def save_report(results: Dict, sherlock_results: Dict = None, filename: str = None):
    """Sauvegarde le rapport en JSON"""
    if not filename:
        username = results["username"].replace(" ", "_").lower()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"social_report_{username}_{timestamp}.json"

    full_results = {
        "manual_search": results,
        "sherlock": sherlock_results
    }

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(full_results, f, indent=2, ensure_ascii=False)

    print(f"💾 Rapport sauvegardé: {filename}")


# ═══════════════════════════════════════════════════════════════
# POINT D'ENTRÉE
# ═══════════════════════════════════════════════════════════════

def main():
    """Point d'entrée principal"""

    print("╔══════════════════════════════════════════════════════════════╗")
    print("║  🔍 OSINT Social Search - Recherche de profils sociaux       ║")
    print("╚══════════════════════════════════════════════════════════════╝\n")

    # Vérifier les arguments
    if len(sys.argv) < 2:
        print("❌ Usage:")
        print("   python3 osint_social_search.py <username>")
        print("   python3 osint_social_search.py \"Nom Complet\"")
        print("\n📌 Exemples:")
        print("   python3 osint_social_search.py johndoe")
        print("   python3 osint_social_search.py elonmusk")
        print('   python3 osint_social_search.py "Elon Musk"')
        sys.exit(1)

    query = sys.argv[1]

    # Déterminer si c'est un nom ou un username
    is_full_name = ' ' in query
    username = query if not is_full_name else query.lower().replace(' ', '')
    name = query if is_full_name else None

    print(f"🎯 Cible:")
    if name:
        print(f"   Nom complet: {name}")
        print(f"   Username généré: {username}")
    else:
        print(f"   Username: {username}")
    print()

    # 1. Recherche manuelle sur les plateformes populaires
    searcher = SocialMediaSearcher()
    results = searcher.search_username(username)

    # 2. Lancer Sherlock si disponible
    sherlock_results = run_sherlock(username)

    # 3. Générer des Google Dorks
    dorks = generate_google_dorks(name=name, username=username)

    # 4. Afficher les résultats
    display_results(results, sherlock_results, dorks)

    # 5. Sauvegarder le rapport
    save_report(results, sherlock_results)


if __name__ == "__main__":
    main()
