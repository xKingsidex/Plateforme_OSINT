#!/usr/bin/env python3
"""
Script de vérification des API Keys configurées
"""

import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

print("╔════════════════════════════════════════════════════════╗")
print("║     🔍 Vérification des API Keys                      ║")
print("╚════════════════════════════════════════════════════════╝\n")

# Définir les APIs et leur priorité
apis = {
    "⭐ PRIORITAIRE (Gratuites)": [
        ("SHODAN_API_KEY", "Shodan", "https://account.shodan.io/"),
        ("VIRUSTOTAL_API_KEY", "VirusTotal", "https://www.virustotal.com/"),
        ("GITHUB_TOKEN", "GitHub", "https://github.com/settings/tokens"),
    ],
    "📦 OPTIONNELLES (Gratuites limitées)": [
        ("NUMVERIFY_API_KEY", "NumVerify", "https://numverify.com/"),
        ("HUNTER_IO_KEY", "Hunter.io", "https://hunter.io/"),
    ],
    "💰 PAYANTES (À obtenir plus tard)": [
        ("HIBP_API_KEY", "Have I Been Pwned", "https://haveibeenpwned.com/API/Key"),
        ("CENSYS_API_ID", "Censys", "https://censys.io/"),
    ],
    "🗄️ BASES DE DONNÉES": [
        ("DATABASE_URL", "PostgreSQL", "Configuration locale"),
        ("NEO4J_URI", "Neo4j", "Configuration locale"),
        ("REDIS_URL", "Redis", "Configuration locale"),
    ],
}

# Vérifier chaque catégorie
for category, api_list in apis.items():
    print(f"\n{category}")
    print("─" * 60)

    for key, name, url in api_list:
        value = os.getenv(key)

        if value and value != f"your_{key.lower()}_here" and "change_this" not in value:
            # Afficher les 10 premiers caractères de la clé
            masked = value[:10] + "..." if len(value) > 10 else value
            print(f"  ✅ {name:<20} Configurée ({masked})")
        else:
            print(f"  ❌ {name:<20} MANQUANTE")
            print(f"     └─ Obtenir ici: {url}")

# Résumé
print("\n" + "═" * 60)
configured = sum(
    1 for _, api_list in apis.items()
    for key, _, _ in api_list
    if os.getenv(key) and os.getenv(key) != f"your_{key.lower()}_here"
)
total = sum(len(api_list) for _, api_list in apis.items())

print(f"📊 Résumé: {configured}/{total} APIs configurées")

if configured < 3:
    print("\n⚠️  RECOMMANDATION:")
    print("   Configure au moins Shodan, VirusTotal et GitHub Token")
    print("   pour commencer à utiliser la plateforme OSINT.")
elif configured >= 3:
    print("\n✅ Configuration minimale OK!")
    print("   Tu peux commencer à utiliser la plateforme.")

print("\n💡 Astuce:")
print("   Les APIs manquantes seront simplement ignorées.")
print("   Le système fonctionnera avec ce qui est disponible.\n")
