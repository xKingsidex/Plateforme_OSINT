#!/usr/bin/env python3
"""
🚀 OSINT Platform - Launcher Script
Lance la plateforme web avec tous les chemins correctement configurés
"""

import sys
import os
from pathlib import Path

# Ajouter les chemins nécessaires au PYTHONPATH
backend_dir = Path(__file__).parent.absolute()
root_dir = backend_dir.parent.parent
plateforme_dir = backend_dir.parent

# Ajouter tous les chemins nécessaires
sys.path.insert(0, str(backend_dir))
sys.path.insert(0, str(backend_dir / 'app'))
sys.path.insert(0, str(root_dir))

print("🔧 Configuration des chemins...")
print(f"   Backend: {backend_dir}")
print(f"   Root: {root_dir}")
print(f"   Plateforme: {plateforme_dir}")
print()

# Vérifier les dépendances critiques
print("🔍 Vérification des dépendances...")
try:
    import fastapi
    import uvicorn
    print("   ✅ FastAPI & Uvicorn")
except ImportError as e:
    print(f"   ❌ FastAPI manquant: {e}")
    print("   📦 Installer avec: pip install fastapi uvicorn")
    sys.exit(1)

try:
    import pydantic
    print("   ✅ Pydantic")
except ImportError:
    print("   ❌ Pydantic manquant")
    print("   📦 Installer avec: pip install pydantic")
    sys.exit(1)

print()
print("=" * 80)
print("🚀 Démarrage de l'OSINT Platform API...")
print("=" * 80)
print()
print("📡 API disponible sur: http://localhost:8000")
print("📚 Documentation: http://localhost:8000/api/docs")
print("🔍 Health check: http://localhost:8000/api/health")
print()
print("=" * 80)
print()

# Importer et lancer l'application
try:
    from app.main import app

    if __name__ == "__main__":
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
except Exception as e:
    print(f"❌ Erreur au démarrage: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
