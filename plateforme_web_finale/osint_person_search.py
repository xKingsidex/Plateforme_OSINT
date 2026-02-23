#!/usr/bin/env python3
"""
🔍 OSINT Person Search - Recherche complète sur une personne
Usage: python3 osint_person_search.py "John Doe" john.doe@example.com
"""

import os
import sys
import json
import requests
from datetime import datetime
from typing import Dict, List, Optional
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor, as_completed

# Charger les variables d'environnement
load_dotenv()


# ═══════════════════════════════════════════════════════════════
# CLASSES API (réutilisées depuis api_examples.py)
# ═══════════════════════════════════════════════════════════════

class ShodanAPI:
    """API Shodan pour scanner des IPs"""
    def __init__(self):
        self.api_key = os.getenv("SHODAN_API_KEY")
        self.base_url = "https://api.shodan.io"

    def search_ip(self, ip_address: str) -> Optional[Dict]:
        if not self.api_key:
            return {"error": "SHODAN_API_KEY manquante"}

        url = f"{self.base_url}/shodan/host/{ip_address}"
        params = {"key": self.api_key}

        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            return {
                "ip": data.get("ip_str"),
                "organization": data.get("org"),
                "os": data.get("os"),
                "ports": data.get("ports", []),
                "hostnames": data.get("hostnames", []),
                "country": data.get("country_name"),
                "city": data.get("city"),
                "vulnerabilities": data.get("vulns", [])
            }
        except Exception as e:
            return {"error": str(e)}


class HunterAPI:
    """API Hunter.io pour trouver des emails"""
    def __init__(self):
        self.api_key = os.getenv("HUNTER_API_KEY")
        self.base_url = "https://api.hunter.io/v2"

    def find_email(self, domain: str, first_name: str = None, last_name: str = None) -> Optional[Dict]:
        if not self.api_key:
            return {"error": "HUNTER_API_KEY manquante"}

        url = f"{self.base_url}/email-finder"
        params = {
            "domain": domain,
            "api_key": self.api_key
        }

        if first_name:
            params["first_name"] = first_name
        if last_name:
            params["last_name"] = last_name

        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            if data.get("data"):
                return {
                    "email": data["data"].get("email"),
                    "score": data["data"].get("score"),
                    "sources": data["data"].get("sources", [])
                }
            return {"error": "Email non trouvé"}
        except Exception as e:
            return {"error": str(e)}

    def verify_email(self, email: str) -> Optional[Dict]:
        if not self.api_key:
            return {"error": "HUNTER_API_KEY manquante"}

        url = f"{self.base_url}/email-verifier"
        params = {
            "email": email,
            "api_key": self.api_key
        }

        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            if data.get("data"):
                return {
                    "email": email,
                    "status": data["data"].get("status"),
                    "score": data["data"].get("score"),
                    "disposable": data["data"].get("disposable"),
                    "webmail": data["data"].get("webmail")
                }
            return {"error": "Vérification impossible"}
        except Exception as e:
            return {"error": str(e)}


class HaveIBeenPwnedAPI:
    """API HIBP pour vérifier les fuites de données"""
    def __init__(self):
        self.api_key = os.getenv("HIBP_API_KEY")
        self.base_url = "https://haveibeenpwned.com/api/v3"

    def check_email(self, email: str) -> Optional[Dict]:
        if not self.api_key:
            return {"error": "HIBP_API_KEY manquante"}

        url = f"{self.base_url}/breachedaccount/{email}"
        headers = {
            "hibp-api-key": self.api_key,
            "user-agent": "OSINT-Platform"
        }

        try:
            response = requests.get(url, headers=headers, timeout=10)

            if response.status_code == 404:
                return {"breached": False, "message": "Email non trouvé dans les fuites"}

            response.raise_for_status()
            breaches = response.json()

            return {
                "breached": True,
                "count": len(breaches),
                "breaches": [
                    {
                        "name": b.get("Name"),
                        "date": b.get("BreachDate"),
                        "description": b.get("Description"),
                        "data_classes": b.get("DataClasses")
                    }
                    for b in breaches
                ]
            }
        except Exception as e:
            return {"error": str(e)}


class GitHubAPI:
    """API GitHub pour chercher des utilisateurs"""
    def __init__(self):
        self.api_key = os.getenv("GITHUB_TOKEN")
        self.base_url = "https://api.github.com"

    def search_user(self, username: str) -> Optional[Dict]:
        url = f"{self.base_url}/users/{username}"
        headers = {}

        if self.api_key:
            headers["Authorization"] = f"token {self.api_key}"

        try:
            response = requests.get(url, headers=headers, timeout=10)

            if response.status_code == 404:
                return {"error": "Utilisateur non trouvé"}

            response.raise_for_status()
            data = response.json()

            return {
                "username": data.get("login"),
                "name": data.get("name"),
                "bio": data.get("bio"),
                "company": data.get("company"),
                "location": data.get("location"),
                "email": data.get("email"),
                "blog": data.get("blog"),
                "public_repos": data.get("public_repos"),
                "followers": data.get("followers"),
                "following": data.get("following"),
                "created_at": data.get("created_at"),
                "profile_url": data.get("html_url")
            }
        except Exception as e:
            return {"error": str(e)}


class VirusTotalAPI:
    """API VirusTotal pour scanner des domaines"""
    def __init__(self):
        self.api_key = os.getenv("VIRUSTOTAL_API_KEY")
        self.base_url = "https://www.virustotal.com/api/v3"

    def scan_domain(self, domain: str) -> Optional[Dict]:
        if not self.api_key:
            return {"error": "VIRUSTOTAL_API_KEY manquante"}

        url = f"{self.base_url}/domains/{domain}"
        headers = {"x-apikey": self.api_key}

        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()

            stats = data.get("data", {}).get("attributes", {}).get("last_analysis_stats", {})

            return {
                "domain": domain,
                "malicious": stats.get("malicious", 0),
                "suspicious": stats.get("suspicious", 0),
                "harmless": stats.get("harmless", 0),
                "undetected": stats.get("undetected", 0),
                "is_safe": stats.get("malicious", 0) == 0
            }
        except Exception as e:
            return {"error": str(e)}


# ═══════════════════════════════════════════════════════════════
# MOTEUR DE RECHERCHE OSINT
# ═══════════════════════════════════════════════════════════════

class OSINTSearchEngine:
    """Moteur de recherche OSINT pour agréger toutes les sources"""

    def __init__(self):
        self.shodan = ShodanAPI()
        self.hunter = HunterAPI()
        self.hibp = HaveIBeenPwnedAPI()
        self.github = GitHubAPI()
        self.virustotal = VirusTotalAPI()

    def search_person(self, name: str = None, email: str = None, username: str = None, domain: str = None) -> Dict:
        """
        Recherche OSINT complète sur une personne

        Args:
            name: Nom complet (ex: "John Doe")
            email: Adresse email
            username: Username GitHub/social
            domain: Domaine d'entreprise
        """
        results = {
            "target": {
                "name": name,
                "email": email,
                "username": username,
                "domain": domain
            },
            "timestamp": datetime.now().isoformat(),
            "sources": {}
        }

        tasks = []

        # Préparer les tâches de recherche
        with ThreadPoolExecutor(max_workers=5) as executor:

            # 1. Hunter.io - Vérifier l'email si fourni
            if email:
                tasks.append(("hunter_verify", executor.submit(self.hunter.verify_email, email)))

            # 2. Hunter.io - Chercher l'email depuis le nom + domaine
            if name and domain:
                name_parts = name.split()
                first_name = name_parts[0] if len(name_parts) > 0 else None
                last_name = name_parts[-1] if len(name_parts) > 1 else None
                tasks.append(("hunter_find", executor.submit(self.hunter.find_email, domain, first_name, last_name)))

            # 3. HIBP - Vérifier les fuites de données
            if email:
                tasks.append(("hibp", executor.submit(self.hibp.check_email, email)))

            # 4. GitHub - Chercher l'utilisateur
            if username:
                tasks.append(("github", executor.submit(self.github.search_user, username)))
            elif email:
                # Essayer avec la partie avant @ comme username
                possible_username = email.split('@')[0]
                tasks.append(("github", executor.submit(self.github.search_user, possible_username)))

            # 5. VirusTotal - Scanner le domaine
            if domain:
                tasks.append(("virustotal", executor.submit(self.virustotal.scan_domain, domain)))
            elif email:
                domain_from_email = email.split('@')[1]
                tasks.append(("virustotal", executor.submit(self.virustotal.scan_domain, domain_from_email)))

            # Collecter les résultats
            for source, future in tasks:
                try:
                    result = future.result(timeout=15)
                    if result and not result.get("error"):
                        results["sources"][source] = result
                    else:
                        results["sources"][source] = {"status": "failed", "reason": result.get("error", "Unknown")}
                except Exception as e:
                    results["sources"][source] = {"status": "failed", "reason": str(e)}

        return results


# ═══════════════════════════════════════════════════════════════
# AFFICHAGE DES RÉSULTATS
# ═══════════════════════════════════════════════════════════════

def display_results(results: Dict):
    """Affiche les résultats de manière lisible"""

    print("\n" + "="*70)
    print("🔍 RAPPORT OSINT - RECHERCHE SUR UNE PERSONNE")
    print("="*70)

    # Cible
    target = results["target"]
    print(f"\n📋 CIBLE:")
    if target.get("name"):
        print(f"   Nom: {target['name']}")
    if target.get("email"):
        print(f"   Email: {target['email']}")
    if target.get("username"):
        print(f"   Username: {target['username']}")
    if target.get("domain"):
        print(f"   Domaine: {target['domain']}")

    print(f"\n⏰ Timestamp: {results['timestamp']}")

    # Résultats par source
    sources = results.get("sources", {})

    # Hunter.io
    if "hunter_verify" in sources:
        data = sources["hunter_verify"]
        print(f"\n📧 HUNTER.IO - Vérification Email")
        print(f"   Statut: {data.get('status', 'N/A')}")
        print(f"   Score: {data.get('score', 'N/A')}/100")
        print(f"   Jetable: {'Oui' if data.get('disposable') else 'Non'}")
        print(f"   Webmail: {'Oui' if data.get('webmail') else 'Non'}")

    if "hunter_find" in sources:
        data = sources["hunter_find"]
        print(f"\n📧 HUNTER.IO - Recherche Email")
        print(f"   Email trouvé: {data.get('email', 'N/A')}")
        print(f"   Confiance: {data.get('score', 'N/A')}/100")

    # HIBP
    if "hibp" in sources:
        data = sources["hibp"]
        print(f"\n🔓 HAVE I BEEN PWNED - Fuites de données")
        if data.get("breached"):
            print(f"   ⚠️  COMPROMIS dans {data.get('count', 0)} fuites!")
            for breach in data.get("breaches", [])[:3]:
                print(f"\n   🚨 {breach['name']} ({breach['date']})")
                print(f"      Données: {', '.join(breach.get('data_classes', []))}")
        else:
            print(f"   ✅ Email non trouvé dans les fuites")

    # GitHub
    if "github" in sources:
        data = sources["github"]
        if not data.get("error"):
            print(f"\n💻 GITHUB - Profil utilisateur")
            print(f"   Username: {data.get('username', 'N/A')}")
            print(f"   Nom: {data.get('name', 'N/A')}")
            print(f"   Bio: {data.get('bio', 'N/A')}")
            print(f"   Entreprise: {data.get('company', 'N/A')}")
            print(f"   Localisation: {data.get('location', 'N/A')}")
            print(f"   Repos publics: {data.get('public_repos', 'N/A')}")
            print(f"   Followers: {data.get('followers', 'N/A')}")
            print(f"   URL: {data.get('profile_url', 'N/A')}")

    # VirusTotal
    if "virustotal" in sources:
        data = sources["virustotal"]
        print(f"\n🛡️  VIRUSTOTAL - Réputation du domaine")
        print(f"   Domaine: {data.get('domain', 'N/A')}")
        print(f"   Sûr: {'✅ Oui' if data.get('is_safe') else '❌ Non'}")
        print(f"   Malveillant: {data.get('malicious', 0)}")
        print(f"   Suspect: {data.get('suspicious', 0)}")

    print("\n" + "="*70)
    print(f"✅ Recherche terminée - {len(sources)} source(s) interrogée(s)")
    print("="*70 + "\n")


def save_report(results: Dict, filename: str = None):
    """Sauvegarde le rapport en JSON"""
    if not filename:
        target_name = results["target"].get("name", "unknown").replace(" ", "_").lower()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"osint_report_{target_name}_{timestamp}.json"

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"💾 Rapport sauvegardé: {filename}")


# ═══════════════════════════════════════════════════════════════
# POINT D'ENTRÉE
# ═══════════════════════════════════════════════════════════════

def main():
    """Point d'entrée principal"""

    print("╔══════════════════════════════════════════════════════════════╗")
    print("║  🔍 OSINT Person Search - Recherche complète sur une personne ║")
    print("╚══════════════════════════════════════════════════════════════╝\n")

    # Vérifier les arguments
    if len(sys.argv) < 2:
        print("❌ Usage:")
        print("   python3 osint_person_search.py <email>")
        print("   python3 osint_person_search.py <email> <username>")
        print("   python3 osint_person_search.py \"John Doe\" john.doe@company.com johndoe")
        print("\n📌 Exemples:")
        print("   python3 osint_person_search.py test@example.com")
        print("   python3 osint_person_search.py \"Elon Musk\" elon@spacex.com elonmusk spacex.com")
        sys.exit(1)

    # Parser les arguments
    args = sys.argv[1:]

    name = None
    email = None
    username = None
    domain = None

    # Détecter automatiquement le type d'argument
    for arg in args:
        if '@' in arg:
            email = arg
            # Extraire le domaine depuis l'email
            if not domain:
                domain = arg.split('@')[1]
        elif ' ' in arg:
            name = arg
        else:
            username = arg

    # Si aucun email mais un domaine fourni explicitement
    if not email and len(args) > 3:
        domain = args[3]

    print(f"🎯 Recherche OSINT sur:")
    if name:
        print(f"   Nom: {name}")
    if email:
        print(f"   Email: {email}")
    if username:
        print(f"   Username: {username}")
    if domain:
        print(f"   Domaine: {domain}")
    print()

    # Lancer la recherche
    engine = OSINTSearchEngine()

    print("⏳ Interrogation des sources OSINT...")
    results = engine.search_person(
        name=name,
        email=email,
        username=username,
        domain=domain
    )

    # Afficher les résultats
    display_results(results)

    # Sauvegarder le rapport
    save_report(results)


if __name__ == "__main__":
    main()
