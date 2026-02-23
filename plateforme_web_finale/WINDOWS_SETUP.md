# 🪟 Guide d'Installation Windows

Ce guide résout les problèmes courants d'installation sur Windows.

---

## ⚠️ Problèmes Courants sur Windows

### 1. Erreur psycopg2-binary

**Symptôme :**
```
Error: pg_config executable not found.
ERROR: Failed to build 'psycopg2-binary'
```

**✅ Solution :**

```powershell
# Option A : Installer la version la plus récente (sans version fixe)
pip install psycopg2-binary

# Option B : Utiliser une roue pré-compilée
pip install --only-binary :all: psycopg2-binary

# Option C : Utiliser psycopg3 (plus moderne)
pip install "psycopg[binary]"
```

Si vous utilisez l'option C (psycopg3), modifiez `backend/models/database.py` :
```python
# Changer l'import (si vous utilisez psycopg3)
# from psycopg2 import ...
# EN
# from psycopg import ...
```

---

### 2. Erreur torch (PyTorch trop lourd)

**Symptôme :**
```
Downloading torch-2.1.0... (2.5 GB)
```

**✅ Solution : Installer séparément (optionnel pour démarrer)**

```powershell
# N'installez torch QUE si vous allez utiliser l'IA deep learning
# Pour commencer, vous n'en avez PAS besoin

# Si vraiment nécessaire plus tard :
pip install torch --index-url https://download.pytorch.org/whl/cpu
```

---

### 3. Installation Complète Simplifiée

**ÉTAPE PAR ÉTAPE :**

#### Étape 1 : Installer les dépendances de base

```powershell
# 1. Créer et activer le venv
python -m venv venv
venv\Scripts\Activate.ps1

# 2. Mettre à jour pip
pip install --upgrade pip

# 3. Installer psycopg2 d'abord (séparément)
pip install psycopg2-binary

# 4. Installer les packages essentiels (SANS torch pour l'instant)
pip install fastapi uvicorn[standard] pydantic pydantic-settings
pip install sqlalchemy neo4j redis alembic
pip install scrapy selenium beautifulsoup4 requests aiohttp
pip install shodan python-whois dnspython
pip install spacy scikit-learn networkx
pip install celery python-dotenv loguru pytest
pip install reportlab jinja2 matplotlib

# 5. Télécharger le modèle spaCy
python -m spacy download en_core_web_lg
```

---

## 🚀 Installation Rapide (Recommandée)

**Utilisez le fichier Windows-compatible :**

```powershell
# Utiliser le requirements-windows.txt
pip install -r requirements-windows.txt

# Télécharger spaCy
python -m spacy download en_core_web_lg
```

---

## 🐳 Docker sur Windows

### Prérequis
- **Docker Desktop** : https://www.docker.com/products/docker-desktop/
- Activer **WSL 2** (Windows Subsystem for Linux)

### Installation Docker Desktop

1. Télécharger Docker Desktop
2. Installer et redémarrer Windows
3. Ouvrir Docker Desktop
4. Attendre que "Docker Desktop is running" apparaisse

### Vérifier Docker

```powershell
# Vérifier que Docker tourne
docker --version
docker-compose --version

# Lancer les services
docker-compose up -d

# Vérifier les conteneurs
docker-compose ps
```

---

## 🔧 Problèmes Docker sur Windows

### Erreur : "Cannot connect to Docker daemon"

**✅ Solution :**
1. Ouvrir Docker Desktop manuellement
2. Attendre 1-2 minutes qu'il démarre complètement
3. Relancer `docker-compose up -d`

### Erreur : "Port already in use"

**✅ Solution :**
```powershell
# Voir quel processus utilise le port (exemple: 5432)
netstat -ano | findstr :5432

# Tuer le processus (remplacer PID)
taskkill /PID <numero_PID> /F

# Relancer Docker
docker-compose restart
```

---

## 📁 Chemins de Fichiers Windows

**IMPORTANT :** Utilisez des backslash `\` ou des raw strings sur Windows

```python
# ❌ Mauvais
path = "C:\Users\enzo\Documents\file.txt"  # Erreur d'échappement

# ✅ Bon
path = r"C:\Users\enzo\Documents\file.txt"  # Raw string
# OU
path = "C:\\Users\\enzo\\Documents\\file.txt"  # Double backslash
# OU
from pathlib import Path
path = Path("C:/Users/enzo/Documents/file.txt")  # Forward slash marche aussi
```

---

## 🧪 Tester l'Installation

```powershell
# 1. Vérifier Python
python --version

# 2. Vérifier les packages
python -c "import fastapi; import spacy; import sqlalchemy; print('✅ OK')"

# 3. Vérifier Docker
docker-compose ps

# 4. Tester le scraper
cd backend
python scrapers\shodan_scraper.py

# 5. Initialiser la DB
python init_db.py
```

---

## 📋 Checklist Complète

- [ ] Python 3.9+ installé
- [ ] Docker Desktop installé et démarré
- [ ] Environnement virtuel créé (`venv`)
- [ ] `venv` activé (`venv\Scripts\Activate.ps1`)
- [ ] psycopg2-binary installé
- [ ] Autres dépendances installées
- [ ] spaCy en_core_web_lg téléchargé
- [ ] Docker containers running (postgres, neo4j, redis)
- [ ] Fichier `.env` configuré avec les clés API
- [ ] Test scraper réussi
- [ ] Base de données initialisée

---

## 🆘 Aide Supplémentaire

### Erreur PowerShell Execution Policy

**Symptôme :**
```
venv\Scripts\Activate.ps1 cannot be loaded because running scripts is disabled
```

**✅ Solution :**
```powershell
# Exécuter en tant qu'administrateur
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Puis réessayer
venv\Scripts\Activate.ps1
```

### Vérifier que venv est activé

Votre prompt doit montrer `(venv)` au début :
```powershell
(venv) PS C:\Users\enzo\...\Plateforme_OSINT>
```

---

## 🎯 Commandes Rapides Windows

```powershell
# Activer venv
venv\Scripts\Activate.ps1

# Désactiver venv
deactivate

# Lister les packages installés
pip list

# Mettre à jour un package
pip install --upgrade nom-du-package

# Désinstaller un package
pip uninstall nom-du-package

# Nettoyer le cache pip
pip cache purge
```

---

## 🚀 Prêt !

Une fois tout installé, continuez avec le **GETTING_STARTED.md** à partir du Jour 2.

**Bon développement ! 💪**
