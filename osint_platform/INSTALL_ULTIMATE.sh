#!/bin/bash

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║   🔍 OSINT PLATFORM ULTIMATE - Installation              ║"
echo "║   Installation de TOUS les outils OSINT open source     ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# Couleurs
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Fonction pour afficher les messages
print_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_info() {
    echo -e "${YELLOW}[i]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

# Vérifier Python
print_info "Vérification de Python..."
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 n'est pas installé !"
    exit 1
fi
print_success "Python $(python3 --version) trouvé"

# Vérifier pip
print_info "Vérification de pip..."
if ! command -v pip3 &> /dev/null; then
    print_error "pip3 n'est pas installé !"
    exit 1
fi
print_success "pip $(pip3 --version | awk '{print $2}') trouvé"

# Installation des dépendances
print_info "Installation des dépendances depuis requirements_ultimate.txt..."
pip3 install -r requirements_ultimate.txt

# Installation des outils OSINT un par un avec vérification
echo ""
print_info "Installation des outils OSINT..."
echo ""

# Sherlock
print_info "Installation de Sherlock (300+ sites)..."
pip3 install sherlock-project
if command -v sherlock &> /dev/null; then
    print_success "Sherlock installé"
else
    print_error "Sherlock échoué"
fi

# Maigret
print_info "Installation de Maigret (400+ sites)..."
pip3 install maigret
if command -v maigret &> /dev/null; then
    print_success "Maigret installé"
else
    print_error "Maigret échoué"
fi

# Holehe
print_info "Installation de Holehe (120+ sites email)..."
pip3 install holehe
if command -v holehe &> /dev/null; then
    print_success "Holehe installé"
else
    print_error "Holehe échoué"
fi

# h8mail
print_info "Installation de h8mail (breach hunting)..."
pip3 install h8mail
if command -v h8mail &> /dev/null; then
    print_success "h8mail installé"
else
    print_error "h8mail échoué"
fi

# Socialscan
print_info "Installation de Socialscan..."
pip3 install socialscan
print_success "Socialscan installé"

# theHarvester
print_info "Installation de theHarvester..."
pip3 install theHarvester
if command -v theHarvester &> /dev/null; then
    print_success "theHarvester installé"
else
    print_error "theHarvester échoué"
fi

# Sublist3r
print_info "Installation de Sublist3r..."
pip3 install sublist3r
if command -v sublist3r &> /dev/null; then
    print_success "Sublist3r installé"
else
    print_error "Sublist3r échoué"
fi

echo ""
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║   ✅ INSTALLATION TERMINÉE                                ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# Vérification des outils installés
print_info "Outils OSINT installés:"
echo ""

command -v sherlock &> /dev/null && print_success "Sherlock (300+ sites)" || print_error "Sherlock manquant"
command -v maigret &> /dev/null && print_success "Maigret (400+ sites)" || print_error "Maigret manquant"
command -v holehe &> /dev/null && print_success "Holehe (120+ sites)" || print_error "Holehe manquant"
command -v h8mail &> /dev/null && print_success "h8mail (breach hunting)" || print_error "h8mail manquant"
python3 -c "import socialscan" 2>/dev/null && print_success "Socialscan" || print_error "Socialscan manquant"
command -v theHarvester &> /dev/null && print_success "theHarvester" || print_error "theHarvester manquant"
command -v sublist3r &> /dev/null && print_success "Sublist3r" || print_error "Sublist3r manquant"

echo ""
print_info "Configuration du fichier .env..."

if [ ! -f ".env" ]; then
    if [ -f ".env.ultimate" ]; then
        cp .env.ultimate .env
        print_success "Fichier .env créé depuis .env.ultimate"
        print_info "⚠️  N'oubliez pas d'ajouter vos clés API dans le fichier .env"
    else
        print_error "Fichier .env.ultimate non trouvé"
    fi
else
    print_success "Fichier .env déjà existant"
fi

echo ""
print_success "🎉 Installation complète !"
echo ""
print_info "Prochaines étapes:"
echo "  1. Éditez le fichier .env et ajoutez vos clés API"
echo "  2. Lancez le backend: cd backend/api && python main_ultimate.py"
echo "  3. Lancez le frontend: cd frontend && python -m http.server 3000"
echo "  4. Ouvrez http://localhost:3000/index_pro.html"
echo ""
