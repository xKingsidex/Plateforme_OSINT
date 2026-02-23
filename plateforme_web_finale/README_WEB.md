# 🌐 OSINT Platform - VERSION WEB COMPLÈTE

> **📁 Dossier:** `Plateforme_OSINT_Web/`
>
> Ce dossier contient la **version web complète** de la plateforme OSINT avec Docker.
>
> Le dossier `Plateforme_OSINT/` contient les **scripts CLI de base** (étape par étape).

---

## 🎯 Quelle est la différence ?

### 📂 `Plateforme_OSINT/` (Base - Scripts CLI)
- ✅ Scripts Python en ligne de commande
- ✅ `osint_person_search.py` - Recherche sur une personne
- ✅ `osint_social_search.py` - Recherche réseaux sociaux
- ✅ Modules OSINT individuels
- ✅ Utilisable directement avec Python

### 🌐 `Plateforme_OSINT_Web/` (Web - Cette version)
- ✅ **Interface web moderne** (HTML/CSS/JS)
- ✅ **API REST** (FastAPI)
- ✅ **Docker Compose** (déploiement facile)
- ✅ **PostgreSQL** (base de données)
- ✅ **Redis** (cache)
- ✅ **Dashboard interactif**
- ✅ **Export JSON/HTML**
- ✅ **Tous les modules CLI intégrés**

---

## 🚀 Démarrage rapide

### 1️⃣ Configuration
```bash
# Vérifier que Docker est installé
docker --version
docker-compose --version

# Configurer les API keys
nano .env
```

### 2️⃣ Lancer la plateforme
```bash
# Option 1: Script automatique
./start.sh

# Option 2: Manuel
docker-compose up -d
```

### 3️⃣ Accéder à la plateforme
- **🌐 Interface Web** : http://localhost:3000
- **📚 API Docs** : http://localhost:8000/api/docs
- **🔍 Health Check** : http://localhost:8000/api/health

---

## 📊 Architecture de cette version

```
Plateforme_OSINT_Web/
├── 🎨 frontend/              # Interface web
│   ├── index.html           # Page principale
│   ├── css/style.css        # Styles modernes
│   ├── js/
│   │   ├── app.js           # Logique UI
│   │   └── api.js           # Client API
│   ├── nginx.conf           # Config Nginx
│   └── Dockerfile           # Image Docker
│
├── ⚙️ backend/               # API FastAPI
│   ├── app/
│   │   ├── main.py          # Application principale
│   │   ├── services/
│   │   │   ├── detector.py  # Détection auto
│   │   │   └── aggregator.py # Agrégation OSINT
│   │   ├── api/
│   │   ├── models/
│   │   └── utils/
│   ├── requirements.txt
│   └── Dockerfile
│
├── 🐳 docker-compose.yml     # Orchestration
├── 📚 QUICKSTART.md         # Guide rapide
├── 🚀 start.sh              # Script de démarrage
└── 🧪 test_platform.py      # Tests

Services Docker:
├── backend (FastAPI:8000)
├── frontend (Nginx:3000)
├── postgres (PostgreSQL:5432)
└── redis (Redis:6379)
```

---

## 🎨 Utilisation de l'interface web

1. **Ouvrir** http://localhost:3000
2. **Entrer** n'importe quoi dans le champ :
   - 📧 `john@example.com` (email)
   - 📱 `+33612345678` (téléphone)
   - 👤 `John Doe` (nom)
   - 🔤 `johndoe` (username)
   - 🌐 `8.8.8.8` (IP)
   - 🔗 `example.com` (domaine)
3. **Détection automatique** du type
4. **Cliquer** sur "🔍 Rechercher"
5. **Voir** les résultats en temps réel
6. **Exporter** en JSON ou HTML

---

## 📡 Utilisation de l'API

### Recherche simple
```bash
curl -X POST "http://localhost:8000/api/search" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "john@example.com",
    "deep_search": false
  }'
```

### Recherche approfondie (avec Sherlock)
```bash
curl -X POST "http://localhost:8000/api/search" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "johndoe",
    "deep_search": true
  }'
```

### Détection automatique
```bash
curl -X POST "http://localhost:8000/api/detect" \
  -H "Content-Type: application/json" \
  -d '{"query": "test@example.com"}'
```

---

## 🔧 Commandes Docker utiles

```bash
# Démarrer
docker-compose up -d

# Arrêter
docker-compose down

# Voir les logs
docker-compose logs -f

# Logs d'un service spécifique
docker-compose logs -f backend
docker-compose logs -f frontend

# Rebuild après modifications
docker-compose up -d --build

# Redémarrer un service
docker-compose restart backend

# Nettoyer complètement
docker-compose down -v
```

---

## 🛠️ Développement

### Backend seulement
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend seulement
```bash
cd frontend
# Ouvrir index.html dans un navigateur
# Ou utiliser un serveur HTTP simple:
python3 -m http.server 3000
```

---

## 📋 Modules OSINT intégrés

Cette version web intègre **TOUS** les modules CLI :

- ✅ **Hunter.io** - Recherche et validation d'emails
- ✅ **HIBP** - Fuites de données (Have I Been Pwned)
- ✅ **Shodan** - Scanner d'IPs et ports ouverts
- ✅ **VirusTotal** - Réputation de domaines
- ✅ **GitHub** - Profils utilisateurs et repos
- ✅ **30+ Réseaux sociaux** - Twitter, Instagram, LinkedIn, etc.
- ✅ **Sherlock** - Recherche sur 300+ sites (si deep_search)
- ✅ **Google Dorks** - Recherches avancées

---

## 🎯 Différences techniques

| Fonctionnalité | Version CLI | Version Web |
|---------------|-------------|-------------|
| Interface | ❌ Terminal | ✅ Web moderne |
| Détection auto | ⚠️ Manuelle | ✅ Automatique |
| Recherche parallèle | ⚠️ Limitée | ✅ Complète |
| Export | ✅ JSON | ✅ JSON + HTML |
| Dashboard | ❌ Non | ✅ Oui |
| API REST | ❌ Non | ✅ Oui |
| Base de données | ❌ Non | ✅ PostgreSQL |
| Cache | ❌ Non | ✅ Redis |
| Docker | ❌ Non | ✅ Oui |
| Déploiement | ⚠️ Manuel | ✅ 1 commande |

---

## 📚 Documentation

- **QUICKSTART.md** - Guide de démarrage rapide
- **README.md** - Documentation générale du projet
- **ARCHITECTURE.md** - Architecture technique détaillée
- **API Docs** - http://localhost:8000/api/docs (auto-générée)

---

## 🔄 Retour à la version CLI

Pour utiliser les scripts CLI de base :

```bash
# Retourner au dossier de base
cd ../Plateforme_OSINT/

# Utiliser les scripts
python3 osint_person_search.py john@example.com
python3 osint_social_search.py johndoe
```

---

## 🎉 C'est fait !

Cette version web est **100% fonctionnelle** et prête à l'emploi !

```bash
# Démarrer maintenant
./start.sh

# Ou manuellement
docker-compose up -d

# Accéder à l'interface
xdg-open http://localhost:3000  # Linux
open http://localhost:3000      # macOS
start http://localhost:3000     # Windows
```

**Bonne recherche OSINT ! 🔍🚀**
