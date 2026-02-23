#!/usr/bin/env python3
"""
🎯 Input Detector - Détecte automatiquement le type d'input
Supporte: email, phone, name, username, IP, domain, URL
"""

import re
from typing import Dict, List
from urllib.parse import urlparse


class InputDetector:
    """Détecte automatiquement le type d'input pour la recherche OSINT"""

    # Regex patterns
    EMAIL_PATTERN = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    PHONE_PATTERN = re.compile(r'^[\+]?[(]?[0-9]{1,4}[)]?[-\s\.]?[(]?[0-9]{1,4}[)]?[-\s\.]?[0-9]{1,9}$')
    IP_PATTERN = re.compile(r'^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$')
    DOMAIN_PATTERN = re.compile(r'^(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$')
    USERNAME_PATTERN = re.compile(r'^[a-zA-Z0-9_-]{3,30}$')

    def __init__(self):
        pass

    def detect(self, query: str) -> Dict:
        """
        Détecte le type d'input

        Args:
            query: La requête à analyser

        Returns:
            Dict avec les types détectés et la confiance
        """
        query = query.strip()
        detected_types = []
        confidence = {}

        # 1. Email
        if self.EMAIL_PATTERN.match(query):
            detected_types.append("email")
            confidence["email"] = 0.95

        # 2. Téléphone
        elif self.PHONE_PATTERN.match(query.replace(" ", "")):
            detected_types.append("phone")
            confidence["phone"] = 0.90

        # 3. IP Address
        elif self.IP_PATTERN.match(query):
            detected_types.append("ip")
            confidence["ip"] = 1.0

        # 4. Domain
        elif self.DOMAIN_PATTERN.match(query) and '.' in query:
            detected_types.append("domain")
            confidence["domain"] = 0.85

        # 5. URL
        elif query.startswith(('http://', 'https://', 'www.')):
            detected_types.append("url")
            confidence["url"] = 1.0
            # Extraire le domaine de l'URL
            parsed = urlparse(query if query.startswith('http') else f'http://{query}')
            if parsed.netloc:
                detected_types.append("domain")
                confidence["domain"] = 0.90

        # 6. Username (3-30 caractères alphanumériques + _-)
        elif self.USERNAME_PATTERN.match(query):
            detected_types.append("username")
            confidence["username"] = 0.75

        # 7. Nom complet (contient un espace)
        elif ' ' in query and len(query.split()) >= 2:
            detected_types.append("name")
            confidence["name"] = 0.80

        # 8. Fallback - considérer comme username/name
        else:
            if len(query) >= 3:
                detected_types.append("username")
                confidence["username"] = 0.50

        # Suggestions de recherche
        suggestions = self._generate_suggestions(query, detected_types)

        return {
            "query": query,
            "types": detected_types,
            "confidence": confidence,
            "suggestions": suggestions
        }

    def _generate_suggestions(self, query: str, detected_types: List[str]) -> List[str]:
        """Génère des suggestions de recherche"""
        suggestions = []

        if "email" in detected_types:
            suggestions.extend([
                "Vérifier les fuites de données (HIBP)",
                "Rechercher des profils sociaux",
                "Valider l'email (Hunter.io)",
                "Chercher sur GitHub"
            ])

        if "phone" in detected_types:
            suggestions.extend([
                "Identifier l'opérateur téléphonique",
                "Vérifier le pays/région",
                "Rechercher sur réseaux sociaux"
            ])

        if "username" in detected_types:
            suggestions.extend([
                "Rechercher sur 30+ réseaux sociaux",
                "Lancer Sherlock (300+ sites)",
                "Chercher sur GitHub",
                "Google Dorks"
            ])

        if "name" in detected_types:
            suggestions.extend([
                "Rechercher sur LinkedIn",
                "Rechercher sur Facebook/Twitter",
                "Google Dorks avancés",
                "Rechercher des emails associés"
            ])

        if "ip" in detected_types:
            suggestions.extend([
                "Scanner avec Shodan",
                "Géolocaliser l'IP",
                "Vérifier les ports ouverts",
                "Identifier l'organisation"
            ])

        if "domain" in detected_types:
            suggestions.extend([
                "WHOIS lookup",
                "Scanner avec VirusTotal",
                "Rechercher les emails du domaine",
                "Vérifier les DNS records"
            ])

        return suggestions[:5]  # Limiter à 5 suggestions


# ═══════════════════════════════════════════════════════════════
# TESTS
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    detector = InputDetector()

    test_inputs = [
        "john.doe@example.com",
        "+33612345678",
        "8.8.8.8",
        "example.com",
        "johndoe123",
        "John Doe",
        "https://example.com/page"
    ]

    print("🎯 Test du détecteur d'input\n")
    for test in test_inputs:
        result = detector.detect(test)
        print(f"Input: {test}")
        print(f"Types: {', '.join(result['types'])}")
        print(f"Confiance: {result['confidence']}")
        print(f"Suggestions: {result['suggestions'][:2]}")
        print("-" * 60)
