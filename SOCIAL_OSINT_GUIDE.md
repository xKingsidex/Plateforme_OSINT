# 🕵️ Guide OSINT Social - Profiling Complet

Ce guide explique comment utiliser les scrapers **OSINT Social** pour obtenir le maximum d'informations légales sur une personne.

---

## 🎯 Vue d'Ensemble

### Ce que la Plateforme Collecte

**INPUT (ce que vous donnez) :**
- 📧 Email
- 📱 Numéro de téléphone
- 👤 Nom/Prénom
- 🔤 Username

**OUTPUT (ce que vous obtenez) :**
- ✅ Fuites de données (mots de passe leakés)
- ✅ Tous les comptes réseaux sociaux
- ✅ Informations personnelles publiques
- ✅ Validation téléphone + opérateur + localisation
- ✅ Relations entre personnes
- ✅ Score de risque global

---

## 📦 Nouveaux Scrapers Disponibles

### 1️⃣ **EmailScraper** - Profiling Email Complet

**Ce qu'il fait :**
- Vérifie les fuites de données (HaveIBeenPwned)
- Valide l'email (Hunter.io)
- Vérifie la réputation (EmailRep)
- **Trouve TOUS les comptes liés** (Holehe)

**Usage :**
```python
from scrapers.email_scraper import EmailScraper

scraper = EmailScraper()
result = await scraper.process("john.doe@gmail.com")

# Résultat :
{
    'email': 'john.doe@gmail.com',
    'breaches': {
        'count': 3,
        'details': [
            {'name': 'LinkedIn', 'date': '2021-06-22', 'data': ['Emails', 'Passwords']},
            {'name': 'Adobe', 'date': '2013-10-04', 'data': ['Emails', 'Passwords']},
            ...
        ]
    },
    'social_accounts': {
        'found': 8,
        'platforms': ['Twitter', 'LinkedIn', 'Instagram', 'GitHub', 'Facebook', ...]
    },
    'risk_score': 75.0,
    'risk_level': 'high'
}
```

---

### 2️⃣ **PhoneScraper** - Analyse de Numéro

**Ce qu'il fait :**
- Parse et valide le numéro
- Trouve le pays + localisation
- Identifie l'opérateur téléphonique
- Détermine le type (mobile, fixe, VOIP)
- Fuseaux horaires

**Usage :**
```python
from scrapers.phone_scraper import PhoneScraper

scraper = PhoneScraper()
result = await scraper.process("+33612345678")

# Résultat :
{
    'phone_number': '+33612345678',
    'valid': True,
    'country': 'Paris, France',
    'country_code': '+33',
    'carrier': 'Orange',
    'type': 'MOBILE',
    'timezones': ['Europe/Paris'],
    'risk_score': 10.0,
    'risk_level': 'low'
}
```

---

### 3️⃣ **UsernameScraper** - Trouve Tous les Comptes

**Ce qu'il fait :**
- Cherche le username sur **300+ sites** (Sherlock)
- Vérifie Twitter, Instagram, GitHub, LinkedIn, etc.
- Génère les URLs potentielles

**Usage :**
```python
from scrapers.username_scraper import UsernameScraper

scraper = UsernameScraper()
result = await scraper.process("johndoe")

# Résultat :
{
    'username': 'johndoe',
    'accounts_found': 45,
    'verified_accounts': [
        {'platform': 'Twitter', 'url': 'https://twitter.com/johndoe'},
        {'platform': 'GitHub', 'url': 'https://github.com/johndoe'},
        {'platform': 'Instagram', 'url': 'https://instagram.com/johndoe'},
        ...
    ],
    'risk_score': 20.0,
    'risk_level': 'low'
}
```

---

## 🚀 Installation des Dépendances

### Étape 1 : Installer les packages Python

```powershell
# Activer le venv
venv\Scripts\Activate.ps1

# Installer les dépendances OSINT Social
pip install phonenumbers holehe sherlock-project

# OU utiliser le fichier requirements
pip install -r requirements-social-osint.txt
```

### Étape 2 : Obtenir les Clés API

#### **HaveIBeenPwned** (Gratuit)
```
1. https://haveibeenpwned.com/API/Key
2. Suivre les instructions
3. Ajouter dans .env : HIBP_API_KEY=votre_cle
```

#### **Hunter.io** (25 req/mois gratuit)
```
1. https://hunter.io/users/sign_up
2. Aller dans API → Keys
3. Copier la clé
4. Ajouter dans .env : HUNTER_IO_KEY=votre_cle
```

#### **Numverify** (250 req/mois gratuit) - OPTIONNEL
```
1. https://numverify.com/
2. Créer compte gratuit
3. Copier Access Key
4. Ajouter dans .env : NUMVERIFY_API_KEY=votre_cle
```

---

## 🧪 Tester les Scrapers

### Test Email
```powershell
cd backend
python scrapers\email_scraper.py
```

### Test Phone
```powershell
python scrapers\phone_scraper.py
```

### Test Username
```powershell
python scrapers\username_scraper.py
```

---

## 🎯 Workflow Complet : Investigation sur une Personne

### Scénario : Enquête sur john.doe@gmail.com

```python
import asyncio
from scrapers.email_scraper import EmailScraper
from scrapers.phone_scraper import PhoneScraper
from scrapers.username_scraper import UsernameScraper
from scrapers.shodan_scraper import ShodanScraper

async def investigate_person(email):
    """Investigation complète sur une personne"""

    # 1. Analyse Email
    email_scraper = EmailScraper()
    email_data = await email_scraper.process(email)

    print(f"📧 Email analysé")
    print(f"   - Fuites : {email_data['data']['breaches']['count']}")
    print(f"   - Comptes trouvés : {email_data['data']['social_accounts']['found']}")

    # 2. Si username trouvé, chercher partout
    username = "johndoe"  # Extrait de l'email ou trouvé via social_accounts
    username_scraper = UsernameScraper()
    username_data = await username_scraper.process(username)

    print(f"\n👤 Username '{username}' trouvé sur {username_data['data']['accounts_found']} sites")

    # 3. Si téléphone trouvé (via fuites ou profils)
    phone = "+33612345678"
    phone_scraper = PhoneScraper()
    phone_data = await phone_scraper.process(phone)

    print(f"\n📱 Téléphone : {phone_data['data']['country']}, {phone_data['data']['carrier']}")

    # 4. Compilation du rapport
    report = {
        'target': email,
        'email_analysis': email_data['data'],
        'username_analysis': username_data['data'],
        'phone_analysis': phone_data['data'],
        'global_risk_score': (
            email_data['data']['risk_score'] +
            username_data['data']['risk_score'] +
            phone_data['data']['risk_score']
        ) / 3
    }

    return report

# Lancer
result = asyncio.run(investigate_person("john.doe@gmail.com"))
print(f"\n🎯 SCORE DE RISQUE GLOBAL : {result['global_risk_score']:.1f}/100")
```

---

## 📊 Exemple de Rapport Complet

```
═══════════════════════════════════════════════════════════════
📋 RAPPORT D'INVESTIGATION OSINT
═══════════════════════════════════════════════════════════════

🎯 CIBLE : john.doe@gmail.com
📅 Date : 2026-01-28
⏱️  Durée : 2 minutes 34 secondes

───────────────────────────────────────────────────────────────
📧 ANALYSE EMAIL
───────────────────────────────────────────────────────────────
✅ Email valide
📮 Type : Webmail (Gmail)
🔐 FUITES DE DONNÉES : 3 breaches détectés

   1. LinkedIn (2021)
      - 700M comptes
      - Données : Emails, Hash passwords, Noms complets

   2. Adobe (2013)
      - 150M comptes
      - Données : Emails, Passwords (MD5)
      - ⚠️  MOT DE PASSE EN CLAIR : "password123"

   3. Dropbox (2012)
      - Données : Emails, Hash SHA1

🌐 COMPTES SOCIAUX TROUVÉS : 8 plateformes
   ✅ Twitter : @johndoe
   ✅ LinkedIn : linkedin.com/in/johndoe
   ✅ Instagram : @johndoe
   ✅ GitHub : github.com/johndoe
   ✅ Facebook : facebook.com/johndoe
   ✅ Reddit : u/johndoe
   ✅ Medium : @johndoe
   ✅ Spotify : User trouvé

───────────────────────────────────────────────────────────────
👤 ANALYSE USERNAME (johndoe)
───────────────────────────────────────────────────────────────
📊 COMPTES VÉRIFIÉS : 45 sites

Réseaux Sociaux :
   ✅ Twitter, Instagram, Facebook, LinkedIn
   ✅ TikTok, Snapchat, Pinterest, Reddit

Développement :
   ✅ GitHub, GitLab, Stack Overflow, HackerRank

Gaming :
   ✅ Steam, Xbox, PlayStation, Twitch

Autres :
   ✅ YouTube, Medium, Behance, Dribbble, DeviantArt
   ... et 25 autres

───────────────────────────────────────────────────────────────
📱 ANALYSE TÉLÉPHONE (+33 6 12 34 56 78)
───────────────────────────────────────────────────────────────
✅ Numéro valide
🌍 Localisation : Paris, Île-de-France, France
📡 Opérateur : Orange
📞 Type : Mobile
🕐 Fuseau horaire : Europe/Paris

───────────────────────────────────────────────────────────────
👥 PERSONNES LIÉES (Via analyse graphe)
───────────────────────────────────────────────────────────────
1. Alice Smith
   - Relation : Collègue (Google)
   - LinkedIn : linkedin.com/in/alicesmith

2. Bob Martin
   - Relation : Ami (Facebook, Instagram)
   - Twitter : @bobmartin

3. Charlie Brown
   - Relation : Connexion LinkedIn
   - Entreprise : Microsoft

───────────────────────────────────────────────────────────────
🎯 SCORE DE RISQUE GLOBAL
───────────────────────────────────────────────────────────────
Email :          75/100 (HIGH) ⚠️
Username :       20/100 (LOW)  ✅
Téléphone :      10/100 (LOW)  ✅

GLOBAL :         35/100 (MEDIUM) 🟡

───────────────────────────────────────────────────────────────
⚠️  ALERTES ET RECOMMANDATIONS
───────────────────────────────────────────────────────────────
🔴 CRITIQUE :
   - Mot de passe leaké dans Adobe breach : "password123"
   - Changer IMMÉDIATEMENT tous les mots de passe

🟡 AVERTISSEMENT :
   - Email trouvé dans 3 fuites de données
   - Activer 2FA sur tous les comptes
   - Vérifier les connexions suspectes

✅ POSITIF :
   - Téléphone valide et légitime
   - Pas de profils suspects ou faux
   - Large présence en ligne (développeur actif)

═══════════════════════════════════════════════════════════════
```

---

## 🔒 Cadre Légal

**✅ LÉGAL :**
- Analyser des données PUBLIQUES
- Vérifier ses propres comptes
- Audit de sécurité autorisé
- Investigation avec mandat légal

**❌ ILLÉGAL :**
- Hacker des comptes privés
- Harcèlement / Stalking
- Vente de données personnelles
- Usage malveillant

**Cette plateforme est UNIQUEMENT pour usage défensif et légitime.**

---

## 📚 APIs à Créer (Récapitulatif)

| API | Gratuit ? | Limite | À créer |
|-----|-----------|--------|---------|
| **HaveIBeenPwned** | ✅ Oui | Gratuit | Oui |
| **Hunter.io** | ✅ 25/mois | 25 req/mois | Oui |
| **EmailRep** | ✅ Oui | 300 req/jour | Non (pas de clé) |
| **Numverify** | ✅ 250/mois | 250 req/mois | Optionnel |
| **Sherlock** | ✅ Gratuit | Illimité | Non (outil local) |
| **Holehe** | ✅ Gratuit | Illimité | Non (outil local) |

---

## 🎯 Prochaines Étapes

1. ✅ Créer les comptes APIs (HaveIBeenPwned, Hunter.io)
2. ✅ Configurer le .env avec les clés
3. ✅ Installer les dépendances sociales
4. ✅ Tester chaque scraper individuellement
5. ✅ Intégrer dans le workflow global

**Vous aurez alors une plateforme OSINT COMPLÈTE ! 🚀**
