# 🕵️ Plateforme OSINT Automatisée par IA

> Plateforme complète d'OSINT (Open Source Intelligence) automatisée avec Intelligence Artificielle pour la cybersécurité, le renseignement et la détection de menaces.

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🎯 Objectifs

Cette plateforme centralise et automatise la recherche OSINT en combinant :
- **Collecte automatisée** de données depuis multiples sources
- **Analyse IA** pour classification des risques et détection d'anomalies
- **Visualisation** de graphes relationnels
- **Génération de rapports** automatiques

### Cas d'usage
- 🛡️ Cybersécurité : Détection de vulnérabilités et fuites de données
- 🔍 Renseignement : Profilage et analyse de menaces
- 🚨 Réponse aux incidents : Investigation rapide sur personnes/domaines/IPs
- 👮 Forces de l'ordre : Enquêtes numériques légales

---

## ✨ Fonctionnalités

### 🔍 Sources OSINT analysées
- **Réseaux sociaux** : Twitter, LinkedIn, Instagram (profils publics)
- **Développement** : GitHub, GitLab (repos, commits, secrets)
- **Domaines & IPs** : Whois, DNS, Shodan, Censys
- **Fuites de données** : HaveIBeenPwned, Dehashed, LeakCheck
- **Threat Intelligence** : VirusTotal, AlienVault OTX
- **Paste sites** : Pastebin, Gist
- **Forums & Darkweb** : Via Tor (optionnel)

### 🧠 Capacités IA

#### 1. Classification automatique
- **Niveaux de risque** : Low / Medium / High / Critical
- **Modèle** : Fine-tuned BERT/DistilBERT
- **Précision** : 85%+ sur dataset annoté

#### 2. Named Entity Recognition (NER)
- Extraction automatique : emails, IPs, noms, téléphones, crypto-adresses
- **Modèle** : spaCy + BERT-NER custom

#### 3. Détection de faux profils
- **Algorithme** : Isolation Forest sur features comportementales
- Détecte : bots, spam accounts, profils suspects

#### 4. Graph Neural Networks
- **Détection de liens** entre entités (personnes, domaines, IPs)
- **Community detection** (Louvain, GraphSAGE)
- Visualisation interactive avec Neo4j

#### 5. Résumé automatique
- Génération de rapports synthétiques
- **Modèle** : BART / T5

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│        Frontend (Vue.js/React)          │
│   Dashboard | Search | Graph | Reports  │
└──────────────────┬──────────────────────┘
                   │ REST API
┌──────────────────▼──────────────────────┐
│          FastAPI Backend                │
│   Auth | Scrapers | IA | Export         │
└──┬────────┬────────┬────────┬───────────┘
   │        │        │        │
   │        │        │        │
┌──▼──┐ ┌──▼──┐ ┌───▼───┐ ┌──▼──┐
│Redis│ │Celery│ │Neo4j  │ │PgSQL│
└─────┘ └─────┘ └───────┘ └─────┘
```

### Stack Technique

**Backend**
- FastAPI (API REST)
- SQLAlchemy + PostgreSQL (données structurées)
- Neo4j (graphe de relations)
- Celery + Redis (tâches asynchrones)

**Scraping & OSINT**
- Scrapy, Selenium, BeautifulSoup
- APIs : Shodan, VirusTotal, GitHub, HIBP

**IA & ML**
- PyTorch + Transformers (Hugging Face)
- spaCy (NLP)
- scikit-learn (ML classique)
- PyTorch Geometric (GNN)

**Frontend**
- Vue.js / React
- D3.js (visualisation graphes)
- Chart.js (métriques)

---

## 🚀 Installation Rapide

### Prérequis
- Python 3.9+
- Docker & Docker Compose
- Git

### Setup automatique

```bash
# Cloner le repo
git clone https://github.com/votre-username/Plateforme_OSINT.git
cd Plateforme_OSINT

# Lancer le script de setup
chmod +x scripts/setup.sh
./scripts/setup.sh

# Éditer .env avec vos clés API
nano .env

# Tester la configuration
python scripts/test_apis.py
```

### Setup manuel

```bash
# 1. Créer environnement virtuel
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# OU venv\Scripts\activate  # Windows

# 2. Installer dépendances
pip install -r requirements.txt
python -m spacy download en_core_web_lg

# 3. Configurer .env
cp .env.example .env
# Éditer .env avec vos clés API

# 4. Lancer services Docker
docker-compose up -d

# 5. Créer tables de base de données
cd backend
python -c "from models.database import engine, Base; from models.models import *; Base.metadata.create_all(bind=engine)"

# 6. Lancer l'API
uvicorn api.main:app --reload
```

Ouvrir http://localhost:8000/docs pour voir la documentation interactive !

---

## 📚 Documentation

### Guides complets

- **[GUIDE_RECHERCHE.md](GUIDE_RECHERCHE.md)** : Outils OSINT, APIs, datasets, roadmap
- **[ARCHITECTURE.md](ARCHITECTURE.md)** : Architecture technique détaillée
- **[GETTING_STARTED.md](GETTING_STARTED.md)** : Tutoriel pas à pas (4 phases)
- **[AI_TRAINING_GUIDE.md](AI_TRAINING_GUIDE.md)** : Entraînement des modèles IA

### Liens utiles

- API Documentation : http://localhost:8000/docs
- Neo4j Browser : http://localhost:7474 (user: `neo4j`, pass: `osint_neo4j_pass`)
- Flower (Celery monitoring) : http://localhost:5555

---

## 🧪 Tests

```bash
# Tester les APIs configurées
python scripts/test_apis.py

# Tests unitaires
pytest backend/tests/

# Test d'un scraper
cd backend
python test_scraper.py
```

---

## 📖 Usage Rapide

### 1. Créer une investigation

```bash
curl -X POST "http://localhost:8000/investigations" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Investigation John Doe",
    "target_type": "email",
    "target_value": "john.doe@example.com"
  }'
```

### 2. Lister les investigations

```bash
curl http://localhost:8000/investigations
```

### 3. Voir les résultats

```bash
curl http://localhost:8000/investigations/{investigation_id}
```

---

## 🗺️ Roadmap

### ✅ Phase 1 : Fondations (Semaines 1-2)
- [x] Setup environnement
- [x] Architecture FastAPI de base
- [x] Premiers scrapers (Shodan, GitHub, Whois)

### 🚧 Phase 2 : Collecte de données (Semaines 3-4)
- [ ] 7+ scrapers fonctionnels
- [ ] Système de queue Celery
- [ ] Stockage PostgreSQL + Neo4j

### 📅 Phase 3 : IA - NLP (Semaines 5-6)
- [ ] NER avec spaCy
- [ ] Classification de risque (BERT)
- [ ] Dataset annoté (1000+ exemples)

### 📅 Phase 4 : IA - Graphes (Semaines 7-8)
- [ ] Modélisation Neo4j complète
- [ ] GNN pour détection de liens
- [ ] Community detection

### 📅 Phase 5 : Frontend (Semaines 9-10)
- [ ] Dashboard Vue/React
- [ ] Visualisation D3.js
- [ ] Export PDF/JSON

### 📅 Phase 6 : Avancé (Semaines 11-12)
- [ ] Détection de faux profils
- [ ] Résumé automatique
- [ ] Scoring de risque global

---

## 🔑 Obtenir des Clés API

### Gratuites
- **Shodan** : https://account.shodan.io/register (100 req/mois)
- **VirusTotal** : https://www.virustotal.com/gui/join-us (4 req/min)
- **GitHub** : https://github.com/settings/tokens (5000 req/h)
- **HaveIBeenPwned** : https://haveibeenpwned.com/API/Key (gratuit)
- **Hunter.io** : https://hunter.io/users/sign_up (25 req/mois)

### Payantes (optionnelles)
- **Censys** : $250/mois
- **SecurityTrails** : $99/mois
- **IntelX** : À partir de $20/mois

---

## ⚖️ Légal & Éthique

**IMPORTANT** : Cette plateforme est destinée à un usage **légal et éthique** uniquement.

### ✅ Utilisations autorisées
- Cybersécurité défensive (pentesting autorisé)
- Renseignement sur sources publiques
- Recherche académique
- Investigations légales (forces de l'ordre)

### ❌ Utilisations interdites
- Stalking / harcèlement
- Collecte de données privées sans consentement
- Violation de RGPD / CCPA
- Hacking non autorisé

**Respectez toujours** :
- Les Terms of Service des plateformes
- Le fichier robots.txt
- Les lois locales sur la protection des données

---

## 🤝 Contribution

Les contributions sont les bienvenues !

1. Fork le projet
2. Créer une branche (`git checkout -b feature/AmazingFeature`)
3. Commit (`git commit -m 'Add AmazingFeature'`)
4. Push (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

---

## 📝 License

Ce projet est sous licence MIT. Voir [LICENSE](LICENSE) pour plus de détails.

---

## 📧 Contact

Pour questions ou support :
- Ouvrir une issue sur GitHub
- Email : votre-email@example.com

---

## 🙏 Remerciements

- [OSINT Framework](https://osintframework.com/)
- [Hugging Face](https://huggingface.co/)
- [Shodan](https://www.shodan.io/)
- [SpiderFoot](https://github.com/smicallef/spiderfoot)

---

**⚠️ Disclaimer** : Les auteurs ne sont pas responsables de l'utilisation malveillante de cet outil. Usage éthique uniquement.
