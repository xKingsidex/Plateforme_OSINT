# 🚀 OSINT Platform - Quick Start Guide

## 🎯 Plateforme d'automatisation OSINT tout-en-un

Cette plateforme vous permet de faire des recherches OSINT automatisées sur :
- ✅ **Emails** (Hunter.io, HIBP, validation)
- ✅ **Téléphones** (NumVerify, opérateur, pays)
- ✅ **Noms** (Réseaux sociaux, Google Dorks)
- ✅ **Usernames** (30+ plateformes, Sherlock, GitHub)
- ✅ **IPs** (Shodan, géolocalisation)
- ✅ **Domaines** (VirusTotal, WHOIS, DNS)

---

## ⚡ Démarrage en 3 étapes

### 1️⃣ Configuration des API Keys

Éditer le fichier `.env` avec vos clés API :

```bash
# Copier le fichier exemple
cp .env.example .env

# Éditer avec vos clés
nano .env
```

**Clés API recommandées :**
- `HUNTER_API_KEY` - https://hunter.io (email)
- `HIBP_API_KEY` - https://haveibeenpwned.com/API/Key (fuites)
- `SHODAN_API_KEY` - https://shodan.io (IP)
- `VIRUSTOTAL_API_KEY` - https://virustotal.com (domaines)
- `GITHUB_TOKEN` - https://github.com/settings/tokens (GitHub)
- `NUMVERIFY_API_KEY` - https://numverify.com (téléphones)

### 2️⃣ Lancer la plateforme avec Docker

```bash
# Construire et démarrer tous les services
docker-compose up -d

# Vérifier que tout est OK
docker-compose ps
```

### 3️⃣ Accéder à la plateforme

- **🌐 Interface Web** : http://localhost:3000
- **📚 API Docs** : http://localhost:8000/api/docs
- **🔍 API Health** : http://localhost:8000/api/health

---

## 🎨 Utilisation

### Via l'interface web

1. Ouvrir http://localhost:3000
2. Entrer n'importe quoi : email, téléphone, nom, username, IP, domaine
3. La plateforme détecte automatiquement le type
4. Cliquer sur "Rechercher"
5. Voir les résultats en temps réel
6. Exporter en JSON ou HTML

### Via l'API

```bash
# Exemple : Recherche sur un email
curl -X POST "http://localhost:8000/api/search" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "john@example.com",
    "deep_search": false
  }'

# Exemple : Recherche approfondie sur un username
curl -X POST "http://localhost:8000/api/search" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "johndoe",
    "deep_search": true
  }'
```

### Via les scripts CLI (ancienne méthode)

```bash
# Recherche sur une personne
python3 osint_person_search.py john@example.com

# Recherche réseaux sociaux
python3 osint_social_search.py johndoe
```

---

## 📊 Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    OSINT PLATFORM                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐      ┌──────────────┐                   │
│  │   Frontend   │─────▶│   Backend    │                   │
│  │  (React/JS)  │      │  (FastAPI)   │                   │
│  │  Port 3000   │      │  Port 8000   │                   │
│  └──────────────┘      └──────────────┘                   │
│                               │                             │
│                               ├─────▶ PostgreSQL           │
│                               ├─────▶ Redis                │
│                               └─────▶ Modules OSINT        │
│                                       (Hunter, HIBP,       │
│                                        Shodan, etc.)       │
└─────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Commandes utiles

### Docker

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

# Nettoyer tout
docker-compose down -v
```

### Développement

```bash
# Backend seulement (mode dev)
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload

# Tester le détecteur
python3 backend/app/services/detector.py

# Tester l'agrégateur
python3 backend/app/services/aggregator.py
```

---

## 📋 Fonctionnalités

### ✅ Détection automatique
- Email, téléphone, nom, username, IP, domaine, URL

### ✅ Sources OSINT
- **Hunter.io** : Recherche et validation d'emails
- **HIBP** : Fuites de données (Have I Been Pwned)
- **GitHub** : Profils utilisateurs et repos
- **Shodan** : Scanner d'IPs et ports
- **VirusTotal** : Réputation de domaines
- **30+ Réseaux sociaux** : Twitter, Instagram, LinkedIn, etc.
- **Sherlock** : 300+ sites (si deep_search activé)
- **Google Dorks** : Recherches avancées

### ✅ Export
- JSON
- HTML
- Dashboard interactif

---

## 🔧 Troubleshooting

### Le backend ne démarre pas
```bash
# Vérifier les logs
docker-compose logs backend

# Vérifier que PostgreSQL est prêt
docker-compose ps postgres

# Rebuild
docker-compose up -d --build backend
```

### Le frontend ne se connecte pas au backend
```bash
# Vérifier que le backend est accessible
curl http://localhost:8000/api/health

# Vérifier les logs Nginx
docker-compose logs frontend
```

### Les API keys ne fonctionnent pas
```bash
# Vérifier que le .env est chargé
docker-compose exec backend env | grep API_KEY

# Relancer après modification du .env
docker-compose down
docker-compose up -d
```

---

## 📚 Documentation complète

- **GETTING_STARTED.md** : Guide détaillé
- **ARCHITECTURE.md** : Architecture technique
- **API Docs** : http://localhost:8000/api/docs

---

## 🎯 Prochaines étapes

1. Configurer toutes vos API keys dans `.env`
2. Lancer la plateforme avec `docker-compose up -d`
3. Tester sur http://localhost:3000
4. Consulter les résultats et exporter

---

**Bonne recherche OSINT ! 🔍**
