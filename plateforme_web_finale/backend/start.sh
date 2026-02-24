#!/bin/bash
# ═══════════════════════════════════════════════════════════════
# SCRIPT DE DÉMARRAGE RAPIDE - PLATEFORME OSINT WEB
# ═══════════════════════════════════════════════════════════════

set -e

# Vérifier qu'on est dans le bon répertoire
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo "═══════════════════════════════════════════════════════════════"
echo "🚀 DÉMARRAGE PLATEFORME OSINT WEB"
echo "═══════════════════════════════════════════════════════════════"
echo ""

# Vérifier le venv
if [ -z "$VIRTUAL_ENV" ]; then
    echo "⚠️  Venv non activé, tentative d'activation automatique..."

    # Essayer de trouver le venv
    if [ -f "/home/enzo/osint-venv/bin/activate" ]; then
        source /home/enzo/osint-venv/bin/activate
        echo "✅ Venv activé: $VIRTUAL_ENV"
    elif [ -f "../osint-venv/bin/activate" ]; then
        source ../osint-venv/bin/activate
        echo "✅ Venv activé: $VIRTUAL_ENV"
    else
        echo "❌ Venv introuvable !"
        echo ""
        echo "Active-le manuellement :"
        echo "  source /home/enzo/osint-venv/bin/activate"
        exit 1
    fi
fi

echo ""
echo "🔍 Vérification des dépendances..."

# Vérifier FastAPI
if ! python -c "import fastapi" 2>/dev/null; then
    echo "❌ FastAPI manquant !"
    echo ""
    echo "Installer les dépendances avec :"
    echo "  ./install.sh"
    echo ""
    echo "Ou manuellement :"
    echo "  pip install -r requirements-minimal.txt"
    exit 1
fi

echo "✅ Dépendances OK"
echo ""

# Lancer l'application
echo "═══════════════════════════════════════════════════════════════"
echo "🌐 Lancement du serveur..."
echo "═══════════════════════════════════════════════════════════════"
echo ""

python run_app.py
