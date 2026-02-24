#!/bin/bash

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║   🔍 INSTALLATION DES OUTILS OSINT PROFESSIONNELS        ║"
echo "╚═══════════════════════════════════════════════════════════╝"

# Sherlock - Username search sur 300+ sites
echo "📥 Installation de Sherlock..."
pip install sherlock-project

# Holehe - Email checker sur 120+ sites
echo "📥 Installation de Holehe..."
pip install holehe

# theHarvester - Email harvesting
echo "📥 Installation de theHarvester..."
pip install theHarvester

# Socialscan - Username/Email checker rapide
echo "📥 Installation de Socialscan..."
pip install socialscan

# Phoneinfoga - Phone OSINT
echo "📥 Installation de Phoneinfoga..."
pip install phonenumbers

# Requests et autres
echo "📥 Installation des dépendances..."
pip install aiohttp bs4 lxml

echo ""
echo "✅ TOUS LES OUTILS OSINT SONT INSTALLÉS !"
echo ""
