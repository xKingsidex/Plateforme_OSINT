"""
═══════════════════════════════════════════════════════════════
NAME VARIATIONS GENERATOR
Génère toutes les variations possibles d'un nom pour OSINT
═══════════════════════════════════════════════════════════════
"""

import re
from typing import List, Set
from itertools import permutations


class NameVariationsGenerator:
    """Génère toutes les variations possibles d'un nom"""

    def __init__(self):
        self.common_separators = ['', '.', '_', '-']

    def generate_all_variations(self, full_name: str) -> List[str]:
        """
        Génère toutes les variations possibles d'un nom

        Exemples:
        John Doe →
          - John Doe, Doe John
          - J. Doe, John D., J.D., JD
          - john.doe, john_doe, johndoe
          - j.doe, jdoe, doe.j
        """
        variations = set()

        # Nettoyer le nom
        cleaned_name = self._clean_name(full_name)
        parts = cleaned_name.split()

        if len(parts) == 0:
            return []

        # 1. Variations de format complet
        variations.update(self._full_name_variations(parts))

        # 2. Variations avec initiales
        variations.update(self._initial_variations(parts))

        # 3. Variations username (lowercase, separators)
        variations.update(self._username_variations(parts))

        # 4. Variations email locales
        variations.update(self._email_local_variations(parts))

        # 5. Variations inversées
        variations.update(self._reversed_variations(parts))

        # Retourner une liste triée sans doublons
        return sorted(list(variations))

    def _clean_name(self, name: str) -> str:
        """Nettoie un nom (supprime ponctuation, espaces multiples)"""
        # Supprimer les caractères spéciaux sauf espaces
        name = re.sub(r'[^\w\s]', '', name)
        # Supprimer les espaces multiples
        name = re.sub(r'\s+', ' ', name)
        return name.strip()

    def _full_name_variations(self, parts: List[str]) -> Set[str]:
        """Variations de format complet"""
        variations = set()

        if len(parts) >= 2:
            # John Doe
            variations.add(' '.join(parts))

            # Doe John (inversé)
            variations.add(' '.join(reversed(parts)))

            # JOHN DOE (uppercase)
            variations.add(' '.join(parts).upper())

            # john doe (lowercase)
            variations.add(' '.join(parts).lower())

        return variations

    def _initial_variations(self, parts: List[str]) -> Set[str]:
        """Variations avec initiales"""
        variations = set()

        if len(parts) >= 2:
            first = parts[0]
            last = parts[-1]

            # J. Doe
            variations.add(f"{first[0]}. {last}")
            variations.add(f"{first[0].upper()}. {last.capitalize()}")

            # John D.
            variations.add(f"{first} {last[0]}.")
            variations.add(f"{first.capitalize()} {last[0].upper()}.")

            # J.D.
            variations.add(f"{first[0]}.{last[0]}.")
            variations.add(f"{first[0].upper()}.{last[0].upper()}.")

            # JD (sans points)
            variations.add(f"{first[0]}{last[0]}")
            variations.add(f"{first[0].upper()}{last[0].upper()}")

            # J Doe (sans point)
            variations.add(f"{first[0]} {last}")
            variations.add(f"{first[0].upper()} {last.capitalize()}")

        return variations

    def _username_variations(self, parts: List[str]) -> Set[str]:
        """Variations de type username"""
        variations = set()

        if len(parts) >= 2:
            first = parts[0].lower()
            last = parts[-1].lower()

            for sep in self.common_separators:
                # johndoe, john.doe, john_doe, john-doe
                variations.add(f"{first}{sep}{last}")

                # doejohn (inversé)
                variations.add(f"{last}{sep}{first}")

                # jdoe, j.doe, j_doe
                variations.add(f"{first[0]}{sep}{last}")

                # doej (inversé)
                variations.add(f"{last}{sep}{first[0]}")

        elif len(parts) == 1:
            # Nom unique en minuscules
            variations.add(parts[0].lower())

        return variations

    def _email_local_variations(self, parts: List[str]) -> Set[str]:
        """Variations pour la partie locale d'un email"""
        variations = set()

        if len(parts) >= 2:
            first = parts[0].lower()
            last = parts[-1].lower()

            # Formats courants d'emails
            variations.add(f"{first}.{last}")  # john.doe
            variations.add(f"{first}_{last}")  # john_doe
            variations.add(f"{first}{last}")   # johndoe
            variations.add(f"{first[0]}.{last}")  # j.doe
            variations.add(f"{first[0]}{last}")   # jdoe
            variations.add(f"{first}.{last[0]}")  # john.d
            variations.add(f"{last}.{first}")  # doe.john
            variations.add(f"{last}{first}")   # doejohn

            # Avec chiffres courants (naissance, etc.)
            for num in ['', '1', '2', '01', '02', '123']:
                if num:
                    variations.add(f"{first}.{last}{num}")
                    variations.add(f"{first}{last}{num}")
                    variations.add(f"{first[0]}.{last}{num}")

        return variations

    def _reversed_variations(self, parts: List[str]) -> Set[str]:
        """Variations avec ordre inversé"""
        variations = set()

        if len(parts) >= 2:
            # Toutes les permutations
            for perm in permutations(parts):
                variations.add(' '.join(perm))
                variations.add(''.join(perm).lower())
                variations.add('.'.join(p.lower() for p in perm))
                variations.add('_'.join(p.lower() for p in perm))

        return variations

    def generate_email_variations(self, name: str, domains: List[str] = None) -> List[str]:
        """
        Génère des variations d'emails possibles

        Args:
            name: Nom complet
            domains: Liste de domaines (gmail.com, outlook.com, etc.)

        Returns:
            Liste d'emails possibles
        """
        if domains is None:
            # Domaines les plus courants
            domains = [
                'gmail.com',
                'outlook.com',
                'hotmail.com',
                'yahoo.com',
                'protonmail.com',
                'icloud.com'
            ]

        emails = set()
        local_parts = self._email_local_variations(name.split())

        for local in local_parts:
            for domain in domains:
                emails.add(f"{local}@{domain}")

        return sorted(list(emails))

    def generate_username_variations(self, name: str) -> List[str]:
        """
        Génère des variations de usernames pour réseaux sociaux

        Returns:
            Liste de usernames possibles
        """
        parts = name.split()
        usernames = set()

        # Récupérer toutes les variations username
        usernames.update(self._username_variations(parts))

        # Ajouter des variations avec chiffres
        base_usernames = list(usernames)
        for base in base_usernames:
            # Ajouter des chiffres courants
            for num in ['1', '2', '12', '123', '01', '02', '21', '69', '420']:
                usernames.add(f"{base}{num}")
                usernames.add(f"{base}_{num}")
                usernames.add(f"{num}{base}")

            # Ajouter des suffixes courants
            for suffix in ['official', 'real', 'the', 'og', 'tv', 'yt', 'ttv']:
                usernames.add(f"{base}_{suffix}")
                usernames.add(f"{base}{suffix}")
                usernames.add(f"the_{base}")

        return sorted(list(usernames))


def test_name_variations():
    """Test du générateur de variations"""
    generator = NameVariationsGenerator()

    test_name = "John Doe"

    print(f"\n{'='*60}")
    print(f"TEST: Variations pour '{test_name}'")
    print(f"{'='*60}\n")

    # Toutes les variations
    all_variations = generator.generate_all_variations(test_name)
    print(f"📝 Variations de nom ({len(all_variations)}):")
    for var in all_variations[:20]:  # Afficher les 20 premières
        print(f"   - {var}")
    if len(all_variations) > 20:
        print(f"   ... et {len(all_variations) - 20} autres\n")

    # Variations d'emails
    email_variations = generator.generate_email_variations(test_name)
    print(f"\n📧 Variations d'emails ({len(email_variations)}):")
    for email in email_variations[:15]:  # Afficher les 15 premières
        print(f"   - {email}")
    if len(email_variations) > 15:
        print(f"   ... et {len(email_variations) - 15} autres\n")

    # Variations de usernames
    username_variations = generator.generate_username_variations(test_name)
    print(f"\n👤 Variations de usernames ({len(username_variations)}):")
    for username in username_variations[:20]:  # Afficher les 20 premières
        print(f"   - {username}")
    if len(username_variations) > 20:
        print(f"   ... et {len(username_variations) - 20} autres\n")


if __name__ == "__main__":
    test_name_variations()
