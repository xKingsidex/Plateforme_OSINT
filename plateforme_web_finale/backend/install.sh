#!/bin/bash
# ═══════════════════════════════════════════════════════════════
# SCRIPT D'INSTALLATION AUTOMATIQUE - PLATEFORME OSINT WEB
# ═══════════════════════════════════════════════════════════════

set -e  # Arrêter en cas d'erreur

echo "═══════════════════════════════════════════════════════════════"
echo "🚀 INSTALLATION PLATEFORME OSINT WEB"
echo "═══════════════════════════════════════════════════════════════"
echo ""

# Vérifier qu'on est dans un venv
if [ -z "$VIRTUAL_ENV" ]; then
    echo "⚠️  ATTENTION: Pas de venv activé !"
    echo ""
    echo "Active ton venv d'abord :"
    echo "  source /home/enzo/osint-venv/bin/activate"
    echo ""
    read -p "Continuer quand même ? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    echo "✅ Virtual environment activé: $VIRTUAL_ENV"
fi

echo ""
echo "📦 Installation des dépendances minimales..."
echo ""

pip install --upgrade pip
pip install -r requirements-minimal.txt

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "✅ INSTALLATION TERMINÉE !"
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "🚀 Pour lancer la plateforme :"
echo "   python run_app.py"
echo ""
echo "📚 Documentation API :"
echo "   http://localhost:8000/api/docs"
echo ""
echo "═══════════════════════════════════════════════════════════════"
