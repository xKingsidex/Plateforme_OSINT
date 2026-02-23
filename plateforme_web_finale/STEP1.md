# 📚 STEP 1 - Installation et Configuration Complète

**Guide complet pour installer la Plateforme OSINT sur Windows**

Ce document contient UNIQUEMENT les étapes qui fonctionnent (pas d'erreurs).

---

## 📋 Prérequis

Avant de commencer, vous devez avoir :
- ✅ Windows 10 ou 11
- ✅ Connexion internet
- ✅ Droits administrateur sur votre PC
- ✅ ~2-3 heures devant vous

---

## 🎯 Vue d'ensemble : Ce que vous allez installer

À la fin de ce guide, vous aurez :
- ✅ Python 3.11.9 installé
- ✅ Environnement virtuel (venv) créé
- ✅ Tous les packages Python installés
- ✅ Structure du projet complète
- ✅ Plateforme prête pour la Phase 2 (APIs)

---

## ⚠️ IMPORTANT : Version de Python

**NE PAS installer Python 3.14 ou 3.13 !**

Ces versions sont trop récentes et causent des erreurs de compilation.

**✅ Version RECOMMANDÉE : Python 3.11.9**

---

## 📥 ÉTAPE 1 : Télécharger Python 3.11.9 (5 min)

### 1.1 Téléchargement

1. **Ouvrir** ce lien dans votre navigateur :
   ```
   https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe
   ```

2. **Télécharger** le fichier (environ 25 MB)

### 1.2 Installation

1. **Lancer** le fichier `python-3.11.9-amd64.exe`

2. **⚠️ CRUCIAL : Cocher "Add python.exe to PATH"** (en bas de la fenêtre)

3. **Cliquer** sur "Install Now"

4. **Attendre** la fin de l'installation (2-3 minutes)

5. **Cliquer** sur "Close"

### 1.3 Vérification

1. **Ouvrir** PowerShell :
   - Appuyez sur `Windows + X`
   - Cliquez sur "Windows PowerShell" ou "Terminal"

2. **Taper** cette commande :
   ```powershell
   python --version
   ```

3. **Résultat attendu :**
   ```
   Python 3.11.9
   ```

**✅ Si vous voyez `Python 3.11.9`, c'est bon !**

---

## 📁 ÉTAPE 2 : Cloner le Projet (2 min)

### 2.1 Naviguer vers le dossier de travail

```powershell
# Exemple : Aller dans Documents
cd C:\Users\VOTRE_NOM\Documents

# OU créer un dossier dédié
mkdir Projets
cd Projets
```

### 2.2 Cloner le repository

```powershell
git clone https://github.com/xKingsidex/Plateforme_OSINT.git
cd Plateforme_OSINT
```

### 2.3 Vérifier les fichiers

```powershell
dir
```

**Résultat attendu :** Vous devez voir :
```
README.md
GETTING_STARTED.md
ARCHITECTURE.md
backend/
frontend/
requirements.txt
requirements-windows.txt
docker-compose.yml
...
```

**✅ Si vous voyez ces fichiers, c'est bon !**

---

## 🐍 ÉTAPE 3 : Créer l'Environnement Virtuel (5 min)

### 3.1 Créer le venv

```powershell
python -m venv venv
```

**Attendez 30-60 secondes** (création de l'environnement)

### 3.2 Activer le venv

```powershell
venv\Scripts\Activate.ps1
```

**⚠️ Si erreur "Execution Policy" :**

```powershell
# Exécuter cette commande UNE FOIS
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Puis réessayer
venv\Scripts\Activate.ps1
```

### 3.3 Vérifier l'activation

**Votre prompt doit maintenant montrer `(venv)` au début :**

```
(venv) PS C:\Users\...\Plateforme_OSINT>
```

**✅ Si vous voyez `(venv)`, c'est activé !**

---

## 📦 ÉTAPE 4 : Installer les Packages Python (15-20 min)

### 4.1 Mettre à jour pip

```powershell
pip install --upgrade pip
```

### 4.2 Installer les dépendances essentielles

**Copiez et collez cette LONGUE commande** (tout d'un coup) :

```powershell
pip install fastapi==0.104.1 uvicorn[standard]==0.24.0 pydantic==2.5.0 pydantic-settings==2.1.0 sqlalchemy==2.0.23 psycopg2-binary neo4j==5.14.0 redis==5.0.1 alembic==1.12.1 selenium==4.15.2 beautifulsoup4==4.12.2 requests==2.31.0 aiohttp==3.9.0 shodan==1.31.0 python-whois==0.8.0 dnspython==2.4.2 transformers==4.35.0 spacy==3.7.2 networkx==3.2.1 celery==5.3.4 python-dotenv==1.0.0 loguru==0.7.2 pytest==7.4.3 python-multipart==0.0.6 reportlab==4.0.7 jinja2==3.1.2 matplotlib==3.8.2 seaborn==0.13.0
```

**⏳ Cela va prendre 10-15 minutes.**

Vous allez voir défiler plein de packages qui s'installent.

**Résultat attendu (à la fin) :**
```
Successfully installed fastapi-0.104.1 uvicorn-0.24.0 ...
```

### 4.3 Installer les dépendances OSINT Social

```powershell
pip install phonenumbers holehe sherlock-project
```

**⏳ Cela prend 2-3 minutes.**

### 4.4 Télécharger le modèle spaCy

```powershell
python -m spacy download en_core_web_sm
```

**⏳ Cela télécharge ~40 MB.**

**Résultat attendu :**
```
✔ Download and installation successful
```

### 4.5 Vérification complète

```powershell
python -c "import fastapi, spacy, sqlalchemy, shodan, requests; print('✅ Tous les packages sont installés !')"
```

**Résultat attendu :**
```
✅ Tous les packages sont installés !
```

**✅ Si vous voyez ce message, tout est bon !**

---

## 🐳 ÉTAPE 5 : Installer Docker Desktop (10 min)

### 5.1 Téléchargement

1. **Aller sur** : https://www.docker.com/products/docker-desktop/

2. **Télécharger** "Docker Desktop for Windows"

3. **Lancer** l'installateur

### 5.2 Installation

1. **Suivre** l'assistant d'installation

2. **Cocher** "Use WSL 2 instead of Hyper-V" (recommandé)

3. **Cliquer** sur "Install"

4. **Attendre** (5-10 minutes)

5. **Redémarrer** Windows si demandé

### 5.3 Vérification

1. **Lancer** Docker Desktop manuellement (icône Windows)

2. **Attendre** que "Docker Desktop is running" s'affiche (1-2 minutes)

3. **Ouvrir** PowerShell et taper :

```powershell
docker --version
docker-compose --version
```

**Résultat attendu :**
```
Docker version 24.x.x
docker-compose version 1.29.x
```

**✅ Si vous voyez les versions, Docker est installé !**

---

## ⚙️ ÉTAPE 6 : Lancer les Services Docker (5 min)

### 6.1 Démarrer les conteneurs

**Dans le dossier `Plateforme_OSINT` :**

```powershell
docker-compose up -d
```

**⏳ Première fois : téléchargement des images (5-10 minutes)**

**Résultat attendu :**
```
Creating osint_postgres ... done
Creating osint_neo4j    ... done
Creating osint_redis    ... done
```

### 6.2 Vérifier que tout tourne

```powershell
docker-compose ps
```

**Résultat attendu :**
```
NAME              STATUS
osint_postgres    Up
osint_neo4j       Up
osint_redis       Up
```

**✅ Si les 3 services sont "Up", tout est bon !**

---

## 🗄️ ÉTAPE 7 : Initialiser la Base de Données (2 min)

### 7.1 Activer le venv (si pas déjà fait)

```powershell
venv\Scripts\Activate.ps1
```

### 7.2 Créer les tables

```powershell
cd backend
python init_db.py
```

**Résultat attendu :**
```
🗄️  Initializing database...
✅ Database tables created successfully!

Tables created:
  - investigations
  - collected_data
  - alerts
```

**✅ Si vous voyez ce message, la BDD est prête !**

---

## 🧪 ÉTAPE 8 : Tester le Scraper Shodan (2 min)

**⚠️ Note :** Pour cette étape, vous aurez besoin d'une clé API Shodan.

**Si vous n'avez PAS encore de clé, passez à l'ÉTAPE 9 pour en obtenir une.**

### 8.1 Configurer la clé (temporaire pour test)

Créez un fichier `.env` :

```powershell
# Retourner à la racine du projet
cd ..

# Copier le template
copy .env.example .env

# Éditer le fichier
notepad .env
```

Dans Notepad, ajoutez au minimum :

```env
SHODAN_API_KEY=votre_cle_shodan_ici
```

Sauvegardez (Ctrl+S) et fermez.

### 8.2 Lancer le test

```powershell
cd backend
python scrapers\shodan_scraper.py
```

**Résultat attendu (si vous avez la clé Shodan) :**

```
============================================================
🧪 TEST DU SCRAPER SHODAN
============================================================

📍 Scanning 8.8.8.8 (Google DNS)...

✅ Initializing ShodanScraper
🔍 Processing target: 8.8.8.8
✅ Successfully processed 8.8.8.8

============================================================
📊 RÉSULTATS
============================================================
✅ Status : SUCCESS

📍 IP : 8.8.8.8
🏢 Organisation : Google LLC
🌍 Pays : United States
🏙️  Ville : Mountain View
...
🎯 Score de risque : 6.0/100
📊 Niveau de risque : LOW
```

**✅ Si vous voyez les infos sur 8.8.8.8, le scraper marche !**

---

## 🔑 ÉTAPE 9 : Obtenir les Clés API (30-60 min)

**Guide détaillé pour créer tous les comptes API gratuits.**

### 9.1 Shodan (OBLIGATOIRE) - 5 min

**Gratuit : 100 requêtes/mois**

1. **Aller sur** : https://account.shodan.io/register

2. **Remplir** :
   - Email
   - Username
   - Mot de passe

3. **Confirmer** l'email (vérifier votre boîte mail)

4. **Se connecter** : https://account.shodan.io/login

5. **Copier** la clé API sur https://account.shodan.io/

6. **Coller** dans un fichier texte (Notepad)

**Format de la clé :** `abcdefgh1234567890xyz`

---

### 9.2 GitHub Token (RECOMMANDÉ) - 5 min

**Gratuit : 5000 requêtes/heure**

1. **Se connecter** à GitHub

2. **Aller sur** : https://github.com/settings/tokens

3. **Cliquer** : "Generate new token" → "Generate new token (classic)"

4. **Remplir** :
   - Note : `OSINT Platform`
   - Expiration : `No expiration` (ou 90 days)

5. **Cocher** :
   - ✅ `repo` (tout)
   - ✅ `read:user`
   - ✅ `read:org`

6. **Scroller** en bas → "Generate token"

7. **⚠️ COPIER IMMÉDIATEMENT** (vous ne le reverrez plus !)

8. **Coller** dans votre fichier texte

**Format du token :** `ghp_abc123xyz789...`

---

### 9.3 Hunter.io (RECOMMANDÉ) - 5 min

**Gratuit : 25 requêtes/mois**

1. **Aller sur** : https://hunter.io/users/sign_up

2. **Créer compte** (email + mot de passe)

3. **Confirmer** l'email

4. **Se connecter**

5. **Dashboard** → "API" dans le menu

6. **Copier** la clé API

7. **Coller** dans votre fichier texte

---

### 9.4 VirusTotal (OPTIONNEL) - 3 min

**Gratuit : 4 requêtes/minute**

1. **Aller sur** : https://www.virustotal.com/gui/join-us

2. **Se connecter** avec Google (ou créer compte)

3. **Cliquer** sur votre profil (en haut à droite)

4. **Cliquer** sur "API Key"

5. **Copier** la clé

6. **Coller** dans votre fichier texte

---

### 9.5 Numverify (OPTIONNEL) - 3 min

**Gratuit : 250 requêtes/mois**

1. **Aller sur** : https://numverify.com/

2. **Cliquer** : "Get Free API Key"

3. **Créer compte** gratuit

4. **Confirmer** l'email

5. **Dashboard** → Copier "Access Key"

6. **Coller** dans votre fichier texte

---

### 9.6 Configurer le .env avec TOUTES les clés

**Ouvrir le fichier .env :**

```powershell
notepad .env
```

**Remplacer les valeurs :**

```env
# Database (NE PAS CHANGER)
DATABASE_URL=postgresql://osint:osint123@localhost:5432/osint_db
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=osint_neo4j_pass
REDIS_URL=redis://localhost:6379

# APIs - REMPLACER PAR VOS CLÉS
SHODAN_API_KEY=VOTRE_CLE_SHODAN_ICI
GITHUB_TOKEN=ghp_VOTRE_TOKEN_GITHUB
HUNTER_IO_KEY=VOTRE_CLE_HUNTER
VIRUSTOTAL_API_KEY=VOTRE_CLE_VIRUSTOTAL
NUMVERIFY_API_KEY=VOTRE_CLE_NUMVERIFY

# Celery (NE PAS CHANGER)
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# Security (NE PAS CHANGER pour l'instant)
SECRET_KEY=dev_secret_key_change_in_production
```

**Sauvegarder** (Ctrl+S) et **fermer** Notepad.

---

## ✅ ÉTAPE 10 : Test Final Complet (3 min)

### 10.1 Tester les APIs

```powershell
# Retourner à la racine
cd ..

# Lancer le test
python scripts\test_apis.py
```

**Résultat attendu :**

```
🔍 Testing API Keys and Services Configuration

============================================================

Database (PostgreSQL):
  ✅ PostgreSQL connection successful

Neo4j:
  ✅ Neo4j connection successful

Redis:
  ✅ Redis connection successful

Shodan API:
  ✅ Shodan API key valid

GitHub API:
  ✅ GitHub token valid (user: votre_username)

Hunter.io API:
  ✅ Hunter.io API key valid

VirusTotal API:
  ✅ VirusTotal API key valid

============================================================

📊 Results: 7/7 tests passed
🎉 All tests passed! You're ready to go.
```

**✅ Si tous les tests passent, vous êtes PRÊT !**

---

### 10.2 Tester le workflow complet

```powershell
cd backend
python test_full_workflow.py
```

**Résultat attendu :**

```
======================================================================
🧪 TEST DU WORKFLOW COMPLET
======================================================================

📝 Étape 1 : Création de l'investigation...
✅ Investigation créée : ...
   Target : 8.8.8.8
   Type : ip

🔍 Étape 2 : Lancement du scraper Shodan...
✅ Scraping réussi
   IP : 8.8.8.8
   Organisation : Google LLC
   Pays : United States
   Ports ouverts : [53, 443]
   Score de risque : 6.0/100

💾 Étape 3 : Sauvegarde dans la base de données...

⚠️  Étape 4 : Génération des alertes...
   ✅ Aucune alerte (tout semble normal)

📊 Étape 5 : Mise à jour de l'investigation...
✅ Investigation terminée
   Status : completed
   Risk Score : 6.0/100

======================================================================
✅ TEST COMPLET RÉUSSI !
======================================================================
```

**✅ Si vous voyez ce résultat, TOUT MARCHE !**

---

## 🎊 FÉLICITATIONS !

**Vous avez maintenant :**

✅ Python 3.11.9 installé
✅ Environnement virtuel configuré
✅ Tous les packages Python installés
✅ Docker Desktop opérationnel
✅ PostgreSQL, Neo4j, Redis qui tournent
✅ Base de données initialisée
✅ Clés API configurées
✅ Scrapers fonctionnels
✅ Workflow complet testé

**🚀 Vous êtes PRÊT pour la Phase 2 : Développement !**

---

## 📊 Checklist Finale

Cochez pour vérifier que tout est OK :

- [ ] Python 3.11.9 installé (`python --version`)
- [ ] Venv créé et activé (vous voyez `(venv)`)
- [ ] Packages installés (test import réussi)
- [ ] Docker Desktop installé et lancé
- [ ] 3 conteneurs Docker "Up" (postgres, neo4j, redis)
- [ ] Base de données initialisée (tables créées)
- [ ] Fichier .env configuré avec vos clés
- [ ] `test_apis.py` affiche "All tests passed"
- [ ] `test_full_workflow.py` affiche "TEST COMPLET RÉUSSI"

**Si tout est coché, vous êtes BON ! ✅**

---

## 🆘 Problèmes Courants

### PowerShell : Execution Policy

**Erreur :**
```
venv\Scripts\Activate.ps1 cannot be loaded
```

**Solution :**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

### Docker : Cannot connect to daemon

**Erreur :**
```
Cannot connect to the Docker daemon
```

**Solution :**
1. Ouvrir Docker Desktop manuellement
2. Attendre 1-2 minutes qu'il démarre
3. Réessayer `docker-compose up -d`

---

### Port déjà utilisé

**Erreur :**
```
Port 5432 is already in use
```

**Solution :**
```powershell
# Arrêter tous les conteneurs
docker-compose down

# Redémarrer
docker-compose up -d
```

---

### API Key invalide

**Erreur :**
```
❌ Shodan API key invalid
```

**Solution :**
1. Vérifier que vous avez bien copié TOUTE la clé
2. Vérifier qu'il n'y a pas d'espaces avant/après dans le .env
3. Re-générer une nouvelle clé sur le site

---

## 📚 Prochaines Étapes

Maintenant que tout est installé, vous pouvez :

1. **Lire** `SOCIAL_OSINT_GUIDE.md` pour comprendre les scrapers sociaux
2. **Tester** chaque scraper individuellement :
   ```powershell
   python scrapers\email_scraper.py
   python scrapers\phone_scraper.py
   python scrapers\username_scraper.py
   ```
3. **Commencer** à développer votre propre workflow

---

## 💾 Sauvegarder ce Setup

**Pour ne pas avoir à tout refaire :**

1. **Garder** votre fichier `.env` en lieu sûr (mais NE PAS le commit sur Git !)
2. **Noter** vos clés API quelque part de sécurisé
3. **Documenter** toute modification que vous faites

---

**Bon développement ! 🚀**

*Si votre collègue suit ce guide, il sera exactement au même niveau que vous !*
