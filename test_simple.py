#!/usr/bin/env python3
"""
Script de test simple pour vérifier le .env
"""

import os
from dotenv import load_dotenv

# Charger le fichier .env
load_dotenv()

print("=" * 60)
print("🔍 TEST DE CONFIGURATION")
print("=" * 60)

# Liste des APIs à vérifier
apis = {
    "SHODAN_API_KEY": "Shodan",
    "VIRUSTOTAL_API_KEY": "VirusTotal",
    "GITHUB_TOKEN": "GitHub",
    "NUMVERIFY_API_KEY": "NumVerify",
    "HUNTER_IO_KEY": "Hunter.io",
    "HIBP_API_KEY": "Have I Been Pwned",
}

configured = 0
missing = 0

for key, name in apis.items():
    value = os.getenv(key)

    # Vérifier si la clé existe et n'est pas la valeur par défaut
    if value and not value.startswith("your_") and "your_github_token_here" not in value:
        print(f"✅ {name:<20} CONFIGURÉE")
        configured += 1
    else:
        print(f"❌ {name:<20} manquante")
        missing += 1

print("=" * 60)
print(f"📊 Résultat: {configured} APIs configurées, {missing} manquantes")
print("=" * 60)

if configured > 0:
    print("\n✅ TON .ENV FONCTIONNE !")
    print(f"   Tu as {configured} API(s) prête(s) à utiliser.")
else:
    print("\n⚠️  Aucune API configurée")
    print("   Tu peux quand même tester les scrapers de base.")

print("\n🎯 Prochaine étape: Tester un scraper OSINT")
