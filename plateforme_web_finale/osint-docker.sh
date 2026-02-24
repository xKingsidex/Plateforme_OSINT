#!/bin/bash

##############################################################################
# OSINT TOOLS VIA DOCKER - WRAPPER SCRIPT
# Permet d'utiliser Sherlock, Holehe, Maigret sans casser le système
##############################################################################

# Couleurs
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

IMAGE_NAME="osint-tools"
DOCKERFILE="Dockerfile.osint"

# Fonction pour afficher l'aide
show_help() {
    echo "Usage: $0 <command> [arguments]"
    echo ""
    echo "Commands:"
    echo "  build              - Builder l'image Docker avec les outils OSINT"
    echo "  sherlock <user>    - Rechercher un username avec Sherlock"
    echo "  holehe <email>     - Vérifier un email avec Holehe"
    echo "  maigret <user>     - Rechercher un username avec Maigret"
    echo "  shell              - Ouvrir un shell dans le container"
    echo "  test               - Tester tous les outils"
    echo ""
    echo "Examples:"
    echo "  $0 build"
    echo "  $0 sherlock johndoe"
    echo "  $0 holehe test@example.com"
    echo "  $0 maigret johndoe"
}

# Vérifier si Docker est installé
check_docker() {
    if ! command -v docker &> /dev/null; then
        echo -e "${RED}❌ Docker n'est pas installé !${NC}"
        echo "Installez Docker : https://docs.docker.com/get-docker/"
        exit 1
    fi
}

# Builder l'image Docker
build_image() {
    echo -e "${GREEN}🔨 Building OSINT tools Docker image...${NC}"

    if [ ! -f "$DOCKERFILE" ]; then
        echo -e "${RED}❌ Dockerfile not found: $DOCKERFILE${NC}"
        exit 1
    fi

    docker build -f "$DOCKERFILE" -t "$IMAGE_NAME" .

    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Image built successfully!${NC}"
    else
        echo -e "${RED}❌ Build failed!${NC}"
        exit 1
    fi
}

# Vérifier si l'image existe
check_image() {
    if ! docker image inspect "$IMAGE_NAME" &> /dev/null; then
        echo -e "${YELLOW}⚠️  Image '$IMAGE_NAME' not found. Building...${NC}"
        build_image
    fi
}

# Exécuter Sherlock
run_sherlock() {
    local username="$1"

    if [ -z "$username" ]; then
        echo -e "${RED}❌ Username required!${NC}"
        echo "Usage: $0 sherlock <username>"
        exit 1
    fi

    echo -e "${GREEN}🕵️  Sherlock: Searching for '$username' on 300+ sites...${NC}"
    docker run --rm "$IMAGE_NAME" sherlock "$username" --print-found
}

# Exécuter Holehe
run_holehe() {
    local email="$1"

    if [ -z "$email" ]; then
        echo -e "${RED}❌ Email required!${NC}"
        echo "Usage: $0 holehe <email>"
        exit 1
    fi

    echo -e "${GREEN}📧 Holehe: Verifying '$email' on 100+ sites...${NC}"
    docker run --rm "$IMAGE_NAME" holehe "$email"
}

# Exécuter Maigret
run_maigret() {
    local username="$1"

    if [ -z "$username" ]; then
        echo -e "${RED}❌ Username required!${NC}"
        echo "Usage: $0 maigret <username>"
        exit 1
    fi

    echo -e "${GREEN}🔍 Maigret: Searching for '$username'...${NC}"
    docker run --rm "$IMAGE_NAME" maigret "$username"
}

# Ouvrir un shell
run_shell() {
    echo -e "${GREEN}🐚 Opening shell in OSINT container...${NC}"
    docker run --rm -it "$IMAGE_NAME" /bin/bash
}

# Tester tous les outils
run_test() {
    echo -e "${GREEN}🧪 Testing all OSINT tools...${NC}"
    echo ""

    echo "1. Sherlock version:"
    docker run --rm "$IMAGE_NAME" sherlock --version
    echo ""

    echo "2. Holehe version:"
    docker run --rm "$IMAGE_NAME" holehe --version
    echo ""

    echo "3. Maigret version:"
    docker run --rm "$IMAGE_NAME" maigret --version
    echo ""

    echo -e "${GREEN}✅ All tools are working!${NC}"
}

# Main
check_docker

COMMAND="${1:-help}"

case "$COMMAND" in
    build)
        build_image
        ;;
    sherlock)
        check_image
        run_sherlock "$2"
        ;;
    holehe)
        check_image
        run_holehe "$2"
        ;;
    maigret)
        check_image
        run_maigret "$2"
        ;;
    shell)
        check_image
        run_shell
        ;;
    test)
        check_image
        run_test
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo -e "${RED}❌ Unknown command: $COMMAND${NC}"
        echo ""
        show_help
        exit 1
        ;;
esac
