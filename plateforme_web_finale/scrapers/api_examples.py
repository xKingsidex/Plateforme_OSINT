#!/usr/bin/env python3
"""
Exemples d'utilisation des APIs OSINT
Nécessite: pip install requests python-dotenv
"""

import os
import requests
from dotenv import load_dotenv
from typing import Dict, Optional

# Charger les variables d'environnement depuis .env
load_dotenv()


class NumVerifyAPI:
    """API pour vérifier les numéros de téléphone"""

    def __init__(self):
        self.api_key = os.getenv("NUMVERIFY_API_KEY")
        self.base_url = "http://apilayer.net/api"

    def validate_phone(self, phone_number: str) -> Optional[Dict]:
        """
        Vérifie un numéro de téléphone

        Args:
            phone_number: Numéro au format international (ex: 14158586273)

        Returns:
            Dict avec infos du numéro ou None si erreur
        """
        if not self.api_key:
            print("❌ NUMVERIFY_API_KEY manquante dans .env")
            return None

        url = f"{self.base_url}/validate"
        params = {
            "access_key": self.api_key,
            "number": phone_number,
            "format": 1
        }

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            if data.get("valid"):
                return {
                    "valid": True,
                    "number": data.get("number"),
                    "country": data.get("country_name"),
                    "location": data.get("location"),
                    "carrier": data.get("carrier"),
                    "line_type": data.get("line_type")
                }
            else:
                return {"valid": False, "error": "Numéro invalide"}

        except Exception as e:
            print(f"❌ Erreur NumVerify: {e}")
            return None


class HaveIBeenPwnedAPI:
    """API pour vérifier les fuites de données (breaches)"""

    def __init__(self):
        self.api_key = os.getenv("HIBP_API_KEY")
        self.base_url = "https://haveibeenpwned.com/api/v3"

    def check_email(self, email: str) -> Optional[Dict]:
        """
        Vérifie si un email a été compromis dans des fuites de données

        Args:
            email: Adresse email à vérifier

        Returns:
            Dict avec les breaches trouvées ou None
        """
        if not self.api_key:
            print("❌ HIBP_API_KEY manquante dans .env")
            return None

        url = f"{self.base_url}/breachedaccount/{email}"
        headers = {
            "hibp-api-key": self.api_key,
            "user-agent": "OSINT-Platform"
        }

        try:
            response = requests.get(url, headers=headers)

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
            print(f"❌ Erreur HIBP: {e}")
            return None


class ShodanAPI:
    """API pour rechercher des appareils IoT et vulnérabilités"""

    def __init__(self):
        self.api_key = os.getenv("SHODAN_API_KEY")
        self.base_url = "https://api.shodan.io"

    def search_ip(self, ip_address: str) -> Optional[Dict]:
        """
        Recherche des informations sur une adresse IP

        Args:
            ip_address: Adresse IP à analyser

        Returns:
            Dict avec infos de l'IP ou None
        """
        if not self.api_key:
            print("❌ SHODAN_API_KEY manquante dans .env")
            return None

        url = f"{self.base_url}/shodan/host/{ip_address}"
        params = {"key": self.api_key}

        try:
            response = requests.get(url, params=params)
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
            print(f"❌ Erreur Shodan: {e}")
            return None


class VirusTotalAPI:
    """API pour analyser des URLs/fichiers pour du malware"""

    def __init__(self):
        self.api_key = os.getenv("VIRUSTOTAL_API_KEY")
        self.base_url = "https://www.virustotal.com/api/v3"

    def scan_url(self, url: str) -> Optional[Dict]:
        """
        Scan une URL pour détecter du malware

        Args:
            url: URL à scanner

        Returns:
            Dict avec résultats du scan ou None
        """
        if not self.api_key:
            print("❌ VIRUSTOTAL_API_KEY manquante dans .env")
            return None

        headers = {"x-apikey": self.api_key}

        # Soumettre l'URL
        submit_url = f"{self.base_url}/urls"
        data = {"url": url}

        try:
            response = requests.post(submit_url, headers=headers, data=data)
            response.raise_for_status()

            # Récupérer les résultats
            analysis_id = response.json()["data"]["id"]
            analysis_url = f"{self.base_url}/analyses/{analysis_id}"

            analysis_response = requests.get(analysis_url, headers=headers)
            analysis_response.raise_for_status()

            stats = analysis_response.json()["data"]["attributes"]["stats"]

            return {
                "url": url,
                "malicious": stats.get("malicious", 0),
                "suspicious": stats.get("suspicious", 0),
                "harmless": stats.get("harmless", 0),
                "undetected": stats.get("undetected", 0),
                "is_safe": stats.get("malicious", 0) == 0
            }

        except Exception as e:
            print(f"❌ Erreur VirusTotal: {e}")
            return None


# ═══════════════════════════════════════════════════════════════
# EXEMPLES D'UTILISATION
# ═══════════════════════════════════════════════════════════════

def example_numverify():
    """Exemple: Vérifier un numéro de téléphone"""
    print("\n" + "="*60)
    print("📞 Test NumVerify - Vérification de numéro")
    print("="*60)

    numverify = NumVerifyAPI()
    result = numverify.validate_phone("14158586273")

    if result and result.get("valid"):
        print(f"✅ Numéro valide: {result['number']}")
        print(f"   Pays: {result['country']}")
        print(f"   Opérateur: {result['carrier']}")
        print(f"   Type: {result['line_type']}")
    else:
        print("❌ Numéro invalide ou erreur")


def example_haveibeenpwned():
    """Exemple: Vérifier un email compromis"""
    print("\n" + "="*60)
    print("🔓 Test Have I Been Pwned - Fuites de données")
    print("="*60)

    hibp = HaveIBeenPwnedAPI()
    result = hibp.check_email("test@example.com")

    if result:
        if result.get("breached"):
            print(f"⚠️  Email compromis dans {result['count']} fuites!")
            for breach in result["breaches"][:3]:  # Afficher les 3 premières
                print(f"\n   🚨 {breach['name']} ({breach['date']})")
                print(f"      Données: {', '.join(breach['data_classes'])}")
        else:
            print("✅ Email non trouvé dans les fuites de données")


def example_shodan():
    """Exemple: Analyser une IP"""
    print("\n" + "="*60)
    print("🌐 Test Shodan - Analyse IP")
    print("="*60)

    shodan = ShodanAPI()
    result = shodan.search_ip("8.8.8.8")  # Google DNS

    if result:
        print(f"✅ IP: {result['ip']}")
        print(f"   Organisation: {result['organization']}")
        print(f"   Pays: {result['country']} - {result['city']}")
        print(f"   OS: {result['os']}")
        print(f"   Ports ouverts: {', '.join(map(str, result['ports'][:10]))}")
        if result['vulnerabilities']:
            print(f"   ⚠️  Vulnérabilités: {len(result['vulnerabilities'])}")


def example_virustotal():
    """Exemple: Scanner une URL"""
    print("\n" + "="*60)
    print("🛡️  Test VirusTotal - Scan URL")
    print("="*60)

    vt = VirusTotalAPI()
    result = vt.scan_url("https://www.google.com")

    if result:
        print(f"URL: {result['url']}")
        print(f"✅ Sûre: {'Oui' if result['is_safe'] else 'Non'}")
        print(f"   Malveillant: {result['malicious']}")
        print(f"   Suspect: {result['suspicious']}")
        print(f"   Inoffensif: {result['harmless']}")


if __name__ == "__main__":
    """Point d'entrée principal"""

    print("╔════════════════════════════════════════════════════════╗")
    print("║     🔍 OSINT Platform - Exemples d'API                ║")
    print("╚════════════════════════════════════════════════════════╝")

    # Vérifier que le fichier .env existe
    if not os.path.exists(".env"):
        print("\n⚠️  ATTENTION: Fichier .env introuvable!")
        print("   Créez-le depuis .env.example:")
        print("   $ cp .env.example .env")
        print("   $ nano .env  # Ajoutez vos API keys")
        exit(1)

    # Lancer les exemples
    try:
        example_numverify()
        example_haveibeenpwned()
        example_shodan()
        example_virustotal()

        print("\n" + "="*60)
        print("✅ Tests terminés!")
        print("="*60)

    except KeyboardInterrupt:
        print("\n\n⏸️  Tests interrompus par l'utilisateur")
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
