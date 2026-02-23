#!/usr/bin/env python3
"""
🧪 Test de la plateforme OSINT
Vérifie que tous les modules sont correctement importables
"""

import sys
import os

print("╔══════════════════════════════════════════════════════════════╗")
print("║        🧪 TEST DE LA PLATEFORME OSINT                       ║")
print("╚══════════════════════════════════════════════════════════════╝\n")

errors = []
success = []

# Test 1: Import du détecteur
print("1️⃣  Test du détecteur d'input...")
try:
    sys.path.insert(0, '/home/user/Plateforme_OSINT/backend')
    from app.services.detector import InputDetector

    detector = InputDetector()

    # Test avec un email
    result = detector.detect("test@example.com")
    assert "email" in result["types"], "Email non détecté"

    # Test avec un username
    result = detector.detect("johndoe")
    assert "username" in result["types"], "Username non détecté"

    # Test avec une IP
    result = detector.detect("8.8.8.8")
    assert "ip" in result["types"], "IP non détectée"

    success.append("✅ Détecteur d'input")
    print("   ✅ OK\n")
except Exception as e:
    errors.append(f"❌ Détecteur: {e}")
    print(f"   ❌ ERREUR: {e}\n")

# Test 2: Import des modules OSINT existants
print("2️⃣  Test des modules OSINT existants...")
try:
    from osint_person_search import OSINTSearchEngine
    from osint_social_search import SocialMediaSearcher

    engine = OSINTSearchEngine()
    searcher = SocialMediaSearcher()

    success.append("✅ Modules OSINT")
    print("   ✅ OK\n")
except Exception as e:
    errors.append(f"❌ Modules OSINT: {e}")
    print(f"   ❌ ERREUR: {e}\n")

# Test 3: Vérifier la structure des fichiers
print("3️⃣  Test de la structure des fichiers...")
try:
    required_files = [
        "backend/app/main.py",
        "backend/app/services/detector.py",
        "backend/app/services/aggregator.py",
        "backend/Dockerfile",
        "backend/requirements.txt",
        "frontend/index.html",
        "frontend/js/app.js",
        "frontend/js/api.js",
        "frontend/css/style.css",
        "frontend/Dockerfile",
        "frontend/nginx.conf",
        "docker-compose.yml",
        "start.sh",
        "QUICKSTART.md"
    ]

    base_path = "/home/user/Plateforme_OSINT"
    missing = []

    for file in required_files:
        full_path = os.path.join(base_path, file)
        if not os.path.exists(full_path):
            missing.append(file)

    if missing:
        raise Exception(f"Fichiers manquants: {', '.join(missing)}")

    success.append("✅ Structure des fichiers")
    print("   ✅ OK\n")
except Exception as e:
    errors.append(f"❌ Structure: {e}")
    print(f"   ❌ ERREUR: {e}\n")

# Test 4: Vérifier le .env
print("4️⃣  Test du fichier .env...")
try:
    env_path = "/home/user/Plateforme_OSINT/.env"
    if os.path.exists(env_path):
        success.append("✅ Fichier .env présent")
        print("   ✅ Fichier .env trouvé\n")
    else:
        print("   ⚠️  Fichier .env non trouvé (sera créé depuis .env.example)\n")
except Exception as e:
    errors.append(f"❌ .env: {e}")
    print(f"   ❌ ERREUR: {e}\n")

# Résumé
print("\n" + "="*70)
print("📊 RÉSUMÉ DES TESTS")
print("="*70)

print(f"\n✅ Tests réussis: {len(success)}")
for s in success:
    print(f"   {s}")

if errors:
    print(f"\n❌ Tests échoués: {len(errors)}")
    for e in errors:
        print(f"   {e}")
    print("\n⚠️  Il y a des erreurs à corriger avant de démarrer la plateforme")
    sys.exit(1)
else:
    print("\n🎉 Tous les tests sont passés !")
    print("\n📋 Prochaines étapes:")
    print("   1. Vérifier que Docker est installé sur votre machine")
    print("   2. Configurer vos API keys dans le fichier .env")
    print("   3. Lancer: ./start.sh  ou  docker-compose up -d")
    print("   4. Ouvrir: http://localhost:3000")
    print("\n✨ La plateforme est prête à être déployée !")
