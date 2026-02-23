#!/bin/bash

# ═══════════════════════════════════════════════════════════════
# OSINT Platform - Script de démarrage
# ═══════════════════════════════════════════════════════════════

set -e

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║        🔍 OSINT PLATFORM - DÉMARRAGE                        ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Vérifier que Docker est installé
if ! command -v docker &> /dev/null; then
    echo "❌ Docker n'est pas installé"
    echo "📥 Installer Docker: https://docs.docker.com/get-docker/"
    exit 1
fi

# Vérifier que docker-compose est installé
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose n'est pas installé"
    echo "📥 Installer Docker Compose: https://docs.docker.com/compose/install/"
    exit 1
fi

echo "✅ Docker est installé"
echo ""

# Vérifier que le fichier .env existe
if [ ! -f .env ]; then
    echo "⚠️  Fichier .env non trouvé"
    if [ -f .env.example ]; then
        echo "📋 Copie de .env.example vers .env"
        cp .env.example .env
        echo "⚠️  IMPORTANT: Éditez le fichier .env avec vos clés API avant de continuer!"
        echo ""
        read -p "Appuyez sur Entrée pour continuer ou Ctrl+C pour annuler..."
    else
        echo "❌ Fichier .env.example non trouvé"
        exit 1
    fi
fi

echo "✅ Fichier .env trouvé"
echo ""

# Construire les images Docker
echo "🏗️  Construction des images Docker..."
docker-compose build

echo ""
echo "🚀 Démarrage des services..."
docker-compose up -d

echo ""
echo "⏳ Attente que les services soient prêts..."
sleep 10

# Vérifier le statut des services
echo ""
echo "📊 Statut des services:"
docker-compose ps

echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║              ✅ PLATEFORME DÉMARRÉE !                       ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
echo "🌐 Interface Web    : http://localhost:3000"
echo "📚 API Documentation: http://localhost:8000/api/docs"
echo "🔍 API Health Check : http://localhost:8000/api/health"
echo ""
echo "📋 Commandes utiles:"
echo "   docker-compose logs -f              # Voir les logs"
echo "   docker-compose logs -f backend      # Logs du backend"
echo "   docker-compose logs -f frontend     # Logs du frontend"
echo "   docker-compose down                 # Arrêter la plateforme"
echo "   docker-compose restart              # Redémarrer la plateforme"
echo ""
echo "🎯 Prochaines étapes:"
echo "   1. Ouvrir http://localhost:3000"
echo "   2. Entrer un email, téléphone, nom, username, IP ou domaine"
echo "   3. Lancer la recherche OSINT"
echo ""
echo "Bonne recherche ! 🔍"
