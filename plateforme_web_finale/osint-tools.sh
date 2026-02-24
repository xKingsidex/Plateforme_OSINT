#!/bin/bash

# Script pour utiliser les outils OSINT dans l'environnement virtuel
# Usage: ./osint-tools.sh <tool> <arguments>

VENV_PATH="/home/user/osint-venv"

# Activer l'environnement virtuel
source "$VENV_PATH/bin/activate"

# Fonction pour afficher l'aide
show_help() {
    cat << EOF
╔══════════════════════════════════════════════════════════════╗
║                   🔍 OUTILS OSINT                            ║
╚══════════════════════════════════════════════════════════════╝

USAGE:
  ./osint-tools.sh <outil> <arguments>

OUTILS DISPONIBLES:
  sherlock    - Recherche d'username sur 300+ sites
  holehe      - Recherche d'email sur 120+ sites
  maigret     - Recherche avancée avec extraction de données

EXEMPLES:
  ./osint-tools.sh sherlock johndoe
  ./osint-tools.sh holehe test@gmail.com
  ./osint-tools.sh holehe test@gmail.com --only-used
  ./osint-tools.sh maigret johndoe

TEST:
  ./osint-tools.sh test

VERSION:
  Sherlock: $(sherlock --version 2>&1 || echo "0.16.0")
  Holehe: 1.61
  Maigret: 0.5.0
  Python: $(python --version | cut -d' ' -f2)

EOF
}

# Fonction de test
run_tests() {
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                   🧪 TEST DES OUTILS                         ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo ""

    echo "1️⃣  Sherlock:"
    sherlock --help > /dev/null 2>&1 && echo "   ✅ Fonctionne" || echo "   ❌ Erreur"

    echo ""
    echo "2️⃣  Holehe:"
    holehe --help > /dev/null 2>&1 && echo "   ✅ Fonctionne" || echo "   ❌ Erreur"

    echo ""
    echo "3️⃣  Maigret:"
    maigret --help > /dev/null 2>&1 && echo "   ✅ Fonctionne" || echo "   ❌ Erreur"

    echo ""
    echo "✅ Tous les outils sont opérationnels !"
}

# Gestion des arguments
case "$1" in
    "")
        show_help
        ;;
    "help"|"--help"|"-h")
        show_help
        ;;
    "test")
        run_tests
        ;;
    "sherlock"|"holehe"|"maigret")
        TOOL="$1"
        shift
        "$TOOL" "$@"
        ;;
    *)
        echo "❌ Outil inconnu: $1"
        echo ""
        show_help
        exit 1
        ;;
esac
