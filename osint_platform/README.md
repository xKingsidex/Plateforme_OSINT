# 🔍 OSINT Intelligence Platform - Professional Grade

Plateforme OSINT professionnelle pour la collecte d'intelligence sur des personnes, emails, usernames, téléphones et domaines.

## ✨ Fonctionnalités

### 🎯 Recherches OSINT
- **📧 Email**: Vérification, fuites de données (HaveIBeenPwned), réputation
- **👤 Username**: Recherche sur GitHub, Twitter, LinkedIn, Instagram, Reddit, etc.
- **📱 Téléphone**: Validation, opérateur, localisation
- **🌐 Domaine**: DNS, VirusTotal, SSL, WHOIS

### 🚀 Caractéristiques
- ✅ Interface web professionnelle et moderne
- ✅ API REST FastAPI
- ✅ Détection automatique du type de requête
- ✅ Recherche parallèle multi-sources
- ✅ Résultats détaillés et exportables (JSON)
- ✅ Support de 300+ plateformes sociales

---

## 📦 Installation

### 1️⃣ Prérequis
- Python 3.8+
- pip

### 2️⃣ Installation des dépendances

```bash
cd osint_platform
pip install -r requirements.txt
```

### 3️⃣ Configuration des clés API

**Copiez le fichier `.env.example` vers `.env`:**

```bash
cp .env.example .env
```

**Éditez `.env` et ajoutez vos clés API:**

```env
# Email & Breach Detection
HIBP_API_KEY=votre_cle_haveibeenpwned

# Email Discovery
HUNTER_IO_KEY=votre_cle_hunter_io

# Phone Number Verification
NUMVERIFY_API_KEY=votre_cle_numverify

# Network & Security
SHODAN_API_KEY=votre_cle_shodan
VIRUSTOTAL_API_KEY=votre_cle_virustotal

# GitHub
GITHUB_TOKEN=ghp_votre_token_github
```

#### 🔑 Où obtenir les clés API ?

| Service | URL | Gratuit ? |
|---------|-----|-----------|
| HaveIBeenPwned | https://haveibeenpwned.com/API/Key | ❌ Payant ($3.50/mois) |
| Hunter.io | https://hunter.io/users/sign_up | ✅ 50 recherches/mois |
| Numverify | https://numverify.com/product | ✅ 100 requêtes/mois |
| Shodan | https://account.shodan.io/ | ✅ 1 scan/mois |
| VirusTotal | https://www.virustotal.com/gui/join-us | ✅ 4 requêtes/min |
| GitHub | https://github.com/settings/tokens | ✅ 5000 requêtes/h |

---

## 🚀 Lancement de la plateforme

### Option 1: Lancement simple (recommandé)

**Terminal 1 - Backend API:**
```bash
cd osint_platform/backend/api
python main.py
```

**Terminal 2 - Frontend:**
```bash
cd osint_platform/frontend
python -m http.server 3000
```

### Option 2: Lancement avec uvicorn

**Terminal 1:**
```bash
cd osint_platform/backend/api
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**Terminal 2:**
```bash
cd osint_platform/frontend
python -m http.server 3000
```

---

## 🌐 Accès à la plateforme

Une fois lancé, ouvrez votre navigateur:

- **Frontend Web:** http://localhost:3000
- **API Backend:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs
- **API ReDoc:** http://localhost:8000/redoc

---

## 📖 Utilisation

### Interface Web

1. Ouvrez http://localhost:3000
2. Entrez votre requête (email, username, téléphone, domaine)
3. Le type est détecté automatiquement
4. Cliquez sur "🔍 Analyser"
5. Consultez les résultats détaillés

### API REST

**Détection de type:**
```bash
curl -X POST http://localhost:8000/api/detect \
  -H "Content-Type: application/json" \
  -d '{"query": "john.doe@example.com"}'
```

**Recherche OSINT:**
```bash
curl -X POST http://localhost:8000/api/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "john.doe@example.com",
    "deep_search": false
  }'
```

---

## 📁 Structure du projet

```
osint_platform/
├── backend/
│   ├── api/
│   │   └── main.py          # API FastAPI
│   ├── scrapers/
│   │   ├── base_scraper.py  # Classe de base
│   │   ├── email_scraper.py # Scraper email
│   │   ├── username_scraper.py
│   │   ├── phone_scraper.py
│   │   └── domain_scraper.py
│   └── utils/
├── frontend/
│   ├── index.html
│   ├── css/
│   │   └── style.css        # Design professionnel
│   └── js/
│       └── app.js           # Logique frontend
├── data/                    # Résultats (optionnel)
├── .env                     # Vos clés API (à créer)
├── .env.example             # Template
├── requirements.txt
└── README.md
```

---

## 🛠️ Dépannage

### Le backend ne démarre pas
- Vérifiez que Python 3.8+ est installé: `python --version`
- Installez les dépendances: `pip install -r requirements.txt`

### Le frontend ne se connecte pas à l'API
- Vérifiez que le backend tourne sur http://localhost:8000
- Vérifiez les CORS dans `backend/api/main.py`

### Erreurs "API Key manquante"
- Vérifiez que le fichier `.env` existe
- Vérifiez que les clés API sont correctement configurées
- **Note:** Certaines fonctionnalités marchent sans clés API (recherche username basique)

---

## ⚠️ Avertissement légal

Cette plateforme est destinée à:
- ✅ Recherches OSINT légales
- ✅ Tests de sécurité autorisés
- ✅ Investigation professionnelle
- ✅ Recherche académique

**INTERDIT:**
- ❌ Harcèlement
- ❌ Usurpation d'identité
- ❌ Accès non autorisé
- ❌ Utilisation malveillante

---

## 📝 Licence

MIT License - Utilisation à des fins éducatives et professionnelles uniquement.

---

## 🤝 Support

Pour toute question ou problème, créez une issue sur GitHub.

---

**🔍 OSINT Intelligence Platform v2.0.0**
*Professional Grade Intelligence Gathering*
