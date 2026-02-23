#!/bin/bash

##############################################################################
# SCRIPT D'INSTALLATION DES OUTILS OSINT
# Installe tous les outils OSINT nécessaires pour la plateforme
##############################################################################

set -e  # Exit on error

echo "═══════════════════════════════════════════════════════════════"
echo "  🔧 INSTALLATION DES OUTILS OSINT"
echo "═══════════════════════════════════════════════════════════════"
echo ""

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Fonction pour afficher les messages
print_status() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

# Vérifier si on est root
if [ "$EUID" -ne 0 ]; then
    print_warning "Ce script doit être exécuté avec sudo"
    echo "Usage: sudo bash install_osint_tools.sh"
    exit 1
fi

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "  📦 INSTALLATION DES DÉPENDANCES SYSTÈME"
echo "═══════════════════════════════════════════════════════════════"
echo ""

# Mettre à jour les packages
print_status "Mise à jour des packages..."
apt-get update -qq

# Installer les dépendances
print_status "Installation des dépendances système..."
apt-get install -y -qq \
    python3 \
    python3-pip \
    python3-dev \
    git \
    curl \
    wget \
    build-essential \
    libssl-dev \
    libffi-dev \
    tor \
    > /dev/null 2>&1

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "  🕵️  INSTALLATION DE SHERLOCK (300+ sites)"
echo "═══════════════════════════════════════════════════════════════"
echo ""

if command -v sherlock &> /dev/null; then
    print_warning "Sherlock est déjà installé"
else
    print_status "Installation de Sherlock..."
    pip3 install sherlock-project --quiet
    print_status "Sherlock installé avec succès !"
fi

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "  📧 INSTALLATION DE HOLEHE (vérification email)"
echo "═══════════════════════════════════════════════════════════════"
echo ""

if command -v holehe &> /dev/null; then
    print_warning "Holehe est déjà installé"
else
    print_status "Installation de Holehe..."
    pip3 install holehe --quiet
    print_status "Holehe installé avec succès !"
fi

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "  🔍 INSTALLATION DE MAIGRET (recherche username avancée)"
echo "═══════════════════════════════════════════════════════════════"
echo ""

if command -v maigret &> /dev/null; then
    print_warning "Maigret est déjà installé"
else
    print_status "Installation de Maigret..."
    pip3 install maigret --quiet
    print_status "Maigret installé avec succès !"
fi

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "  🌐 INSTALLATION DE THEHARVESTER"
echo "═══════════════════════════════════════════════════════════════"
echo ""

if command -v theHarvester &> /dev/null; then
    print_warning "theHarvester est déjà installé"
else
    print_status "Installation de theHarvester..."
    pip3 install theHarvester --quiet || {
        print_warning "Installation pip échouée, installation depuis GitHub..."
        cd /tmp
        git clone https://github.com/laramies/theHarvester.git
        cd theHarvester
        pip3 install -r requirements.txt --quiet
        python3 setup.py install
        cd ..
        rm -rf theHarvester
    }
    print_status "theHarvester installé avec succès !"
fi

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "  📱 INSTALLATION DE PHONEINFOGA (optionnel)"
echo "═══════════════════════════════════════════════════════════════"
echo ""

if command -v phoneinfoga &> /dev/null; then
    print_warning "PhoneInfoga est déjà installé"
else
    print_status "Installation de PhoneInfoga..."
    # PhoneInfoga nécessite Go, on le skip si Go n'est pas installé
    if command -v go &> /dev/null; then
        go install github.com/sundowndev/phoneinfoga/v2@latest
        print_status "PhoneInfoga installé avec succès !"
    else
        print_warning "Go n'est pas installé, PhoneInfoga sera skippé"
        print_warning "Pour l'installer: apt install golang-go && go install github.com/sundowndev/phoneinfoga/v2@latest"
    fi
fi

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "  🐍 INSTALLATION DES DÉPENDANCES PYTHON"
echo "═══════════════════════════════════════════════════════════════"
echo ""

print_status "Installation des packages Python..."
pip3 install --quiet \
    aiohttp \
    beautifulsoup4 \
    requests \
    dnspython \
    python-whois \
    phonenumbers

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "  ✅ INSTALLATION TERMINÉE"
echo "═══════════════════════════════════════════════════════════════"
echo ""

echo "Outils installés avec succès :"
echo ""
echo "  ✓ Sherlock       - Recherche username sur 300+ sites"
echo "  ✓ Holehe         - Vérification email sur sites"
echo "  ✓ Maigret        - Recherche username avancée"
echo "  ✓ theHarvester   - Collecte emails, domaines, IPs"
echo ""

# Vérifier les installations
echo "═══════════════════════════════════════════════════════════════"
echo "  🔍 VÉRIFICATION DES INSTALLATIONS"
echo "═══════════════════════════════════════════════════════════════"
echo ""

check_tool() {
    if command -v $1 &> /dev/null; then
        print_status "$1 : OK"
    else
        print_error "$1 : NON INSTALLÉ"
    fi
}

check_tool "sherlock"
check_tool "holehe"
check_tool "maigret"
check_tool "theHarvester"

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "  📝 PROCHAINES ÉTAPES"
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "1. Tester Sherlock :"
echo "   sherlock johndoe"
echo ""
echo "2. Tester Holehe :"
echo "   holehe test@example.com"
echo ""
echo "3. Lancer la plateforme OSINT :"
echo "   docker-compose up --build"
echo ""
echo "═══════════════════════════════════════════════════════════════"

exit 0
