# 🔍 OSINT Intelligence Platform PRO v3.0

**Version Professionnelle avec Sherlock, Holehe, et Socialscan**

Une plateforme OSINT de niveau professionnel utilisant les **vrais outils** de reconnaissance :
- ✅ **Sherlock** - Recherche username sur 300+ sites
- ✅ **Holehe** - Vérification email sur 120+ sites  
- ✅ **Socialscan** - Vérification rapide username/email
- ✅ **Design Terminal Cybersécurité** - Interface hacker-style avec animations Matrix

---

## 🎯 NOUVEAUTÉS PRO

### 🛠️ Vrais Outils OSINT Intégrés
- **Sherlock**: Recherche exhaustive sur 300+ plateformes sociales
- **Holehe**: Détecte les comptes email sur 120+ services
- **Socialscan**: Vérification ultra-rapide en temps réel
- **API Professionnelles**: HaveIBeenPwned, Hunter.io, VirusTotal, etc.

### 🎨 Design Cybersécurité Pro
- Interface terminal style "hacker"
- Animation Matrix en background
- Effet scanline CRT vintage
- ASCII art et glitch effects
- Theme vert monochrome terminal

### ⚡ Performance
- Recherches parallèles asynchrones
- Rate limiting intelligent
- Cache et optimisations
- Export JSON/PDF des résultats

---

## 📦 INSTALLATION

### 1️⃣ Prérequis
```bash
Python 3.8+
pip (gestionnaire de paquets Python)
```

### 2️⃣ Installation des Dépendances

```bash
cd osint_platform

# Installation des outils OSINT réels
pip install -r requirements_pro.txt

# OU utiliser le script automatique
bash install_osint_tools.sh
```

### 3️⃣ Configuration des Clés API

**Copiez et éditez le fichier `.env`:**
```bash
cp .env.example .env
nano .env  # ou notepad .env sur Windows
```

**Ajoutez vos clés API dans `.env`:**
```env
# Email OSINT
HIBP_API_KEY=votre_cle_haveibeenpwned
HUNTER_IO_KEY=votre_cle_hunter_io

# Phone OSINT
NUMVERIFY_API_KEY=votre_cle_numverify

# Domain/IP OSINT
SHODAN_API_KEY=votre_cle_shodan
VIRUSTOTAL_API_KEY=votre_cle_virustotal

# Social OSINT
GITHUB_TOKEN=ghp_votre_token_github
```

> ⚠️ **IMPORTANT**: Sans clés API, Sherlock/Holehe/Socialscan fonctionneront quand même !

---

## 🚀 LANCEMENT

### Terminal 1 - Backend PRO API
```bash
cd osint_platform/backend/api
python main_pro.py
```

**Vous devriez voir:**
```
╔═══════════════════════════════════════════════════════════╗
║   🔍 OSINT INTELLIGENCE PLATFORM PRO v3.0.0              ║
║   Professional Grade avec Sherlock + Holehe + Socialscan║
╚═══════════════════════════════════════════════════════════╝

🚀 Server starting on http://0.0.0.0:8000
📚 API Documentation: http://0.0.0.0:8000/docs

✅ Professional Tools Enabled:
   - Sherlock (300+ sites)
   - Holehe (120+ sites)
   - Socialscan (fast check)
```

### Terminal 2 - Frontend Terminal PRO
```bash
cd osint_platform/frontend
python -m http.server 3000
```

---

## 🌐 ACCÈS

**Ouvrez votre navigateur:**
- **Interface Terminal**: http://localhost:3000/index_pro.html
- **API Docs**: http://localhost:8000/docs

---

## 🎯 UTILISATION

### Interface Terminal

1. Ouvrez http://localhost:3000/index_pro.html
2. Vous verrez l'interface terminal style "hacker"
3. Tapez votre requête (email, username, téléphone, domaine)
4. Options:
   - **[DEEP SCAN]**: Active Sherlock sur 300+ sites (⚠️ LENT - 2-3 minutes)
   - **[PRO TOOLS]**: Utilise Holehe + Socialscan
5. Appuyez sur ENTRÉE
6. Attendez les résultats (affichés en temps réel dans le terminal)

### Exemples de Recherches

```
# Email
test@example.com

# Username
torvalds

# Téléphone
+33612345678

# Domaine
example.com
```

### Mode Deep Scan

⚠️ **ATTENTION**: Le mode Deep Scan avec Sherlock peut prendre **2-3 minutes** car il interroge 300+ sites web.

**Quand l'utiliser ?**
- Recherche exhaustive d'un username
- Investigation approfondie
- Vous avez le temps d'attendre

**Quand NE PAS l'utiliser ?**
- Test rapide
- Démonstration
- Recherche préliminaire

---

## 📊 RÉSULTATS

### Ce que vous obtenez:

#### 📧 Email OSINT
- Validation de l'email
- **Holehe**: Comptes trouvés sur 120+ sites (Discord, Spotify, Netflix, etc.)
- **HaveIBeenPwned**: Fuites de données
- Réputation email (spam score)

#### 👤 Username OSINT
- **Sherlock** (Deep Scan): 300+ plateformes
  - GitHub, Twitter, Instagram, Reddit
  - Facebook, LinkedIn, TikTok
  - Steam, Twitch, YouTube
  - + 290 autres sites
- **Socialscan**: Vérification rapide (6 sites majeurs)
- Profil GitHub complet

#### 📱 Téléphone OSINT
- Validation du numéro
- Pays et opérateur
- Type de ligne (mobile/fixe)

#### 🌐 Domaine OSINT
- Enregistrements DNS
- Réputation VirusTotal
- Certificat SSL/TLS
- WHOIS (si disponible)

---

## 🔑 CLÉS API - Où les obtenir ?

| Service | URL | Prix | Limite Gratuite |
|---------|-----|------|-----------------|
| **Sherlock** | - | ✅ GRATUIT | Illimité |
| **Holehe** | - | ✅ GRATUIT | Illimité |
| **Socialscan** | - | ✅ GRATUIT | Illimité |
| **HaveIBeenPwned** | https://haveibeenpwned.com/API/Key | $3.50/mois | - |
| **Hunter.io** | https://hunter.io/ | ✅ GRATUIT | 50/mois |
| **Numverify** | https://numverify.com/ | ✅ GRATUIT | 100/mois |
| **Shodan** | https://account.shodan.io/ | ✅ GRATUIT | 1 scan/mois |
| **VirusTotal** | https://www.virustotal.com/ | ✅ GRATUIT | 4 req/min |
| **GitHub** | https://github.com/settings/tokens | ✅ GRATUIT | 5000/h |

> 💡 **BON À SAVOIR**: Sherlock, Holehe et Socialscan sont 100% gratuits et fonctionnent sans clés API !

---

## 🛠️ DÉPANNAGE

### Sherlock ne fonctionne pas
```bash
# Vérifier l'installation
sherlock --version

# Réinstaller si nécessaire
pip install sherlock-project --upgrade
```

### Holehe ne fonctionne pas
```bash
# Vérifier l'installation
holehe --version

# Réinstaller si nécessaire
pip install holehe --upgrade
```

### Le frontend ne charge pas
- Vérifiez que vous utilisez `index_pro.html` et pas `index.html`
- URL correcte: http://localhost:3000/index_pro.html

### Le backend ne démarre pas
```bash
# Vérifier les dépendances
pip install -r requirements_pro.txt

# Lancer avec plus de logs
cd backend/api
python main_pro.py
```

---

## 📁 STRUCTURE DU PROJET

```
osint_platform/
├── README_PRO.md                    # Ce fichier
├── requirements_pro.txt             # Dépendances avec outils OSINT
├── install_osint_tools.sh           # Script d'installation auto
│
├── backend/
│   ├── api/
│   │   ├── main.py                 # API basique
│   │   └── main_pro.py             # 🔥 API PRO avec Sherlock/Holehe
│   │
│   └── scrapers/
│       ├── email_scraper.py
│       ├── username_scraper.py
│       ├── phone_scraper.py
│       ├── domain_scraper.py
│       ├── sherlock_scraper.py     # 🔥 Intégration Sherlock
│       ├── holehe_scraper.py       # 🔥 Intégration Holehe
│       └── socialscan_scraper.py   # 🔥 Intégration Socialscan
│
└── frontend/
    ├── index.html                   # Interface basique
    ├── index_pro.html               # 🔥 Interface Terminal PRO
    ├── css/
    │   ├── style.css
    │   └── style_pro.css            # 🔥 Design cybersécurité
    └── js/
        ├── app.js
        ├── app_pro.js               # 🔥 Logique PRO
        └── matrix.js                # 🔥 Animation Matrix
```

---

## ⚡ PERFORMANCES

### Temps de Recherche

| Mode | Outils | Temps Moyen |
|------|--------|-------------|
| **Quick** | APIs basiques + Socialscan | 5-10 secondes |
| **Normal** | APIs + Holehe + Socialscan | 30-60 secondes |
| **Deep Scan** | APIs + Holehe + Sherlock | 2-3 minutes |

### Optimisations

- Requêtes parallèles asynchrones (asyncio)
- Rate limiting automatique
- Cache des résultats (si configuré)
- Timeout intelligent par outil

---

## 📜 EXEMPLES D'UTILISATION

### 1. Recherche Email Rapide
```
Query: john.doe@example.com
Options: ☐ Deep Scan  ☑ Pro Tools
Temps: ~30 secondes
Résultats:
  - Holehe: 15 comptes trouvés
  - HaveIBeenPwned: 3 fuites
  - EmailRep: Score de réputation
```

### 2. Recherche Username Exhaustive
```
Query: johndoe123
Options: ☑ Deep Scan  ☑ Pro Tools
Temps: ~2 minutes
Résultats:
  - Sherlock: 45 profils trouvés sur 300+ sites
  - GitHub: Profil complet
  - Socialscan: Vérification rapide
```

### 3. Recherche Téléphone
```
Query: +33612345678
Options: ☐ Deep Scan  ☑ Pro Tools
Temps: ~5 secondes
Résultats:
  - Numverify: Validé, France, Mobile
  - Opérateur détecté
```

---

## ⚠️ AVERTISSEMENT LÉGAL

Cette plateforme est destinée à:
- ✅ Recherches OSINT légales et éthiques
- ✅ Tests de sécurité autorisés
- ✅ Investigation professionnelle
- ✅ Recherche académique
- ✅ Vérification de sa propre empreinte numérique

**STRICTEMENT INTERDIT:**
- ❌ Harcèlement ou stalking
- ❌ Usurpation d'identité
- ❌ Accès non autorisé
- ❌ Utilisation malveillante
- ❌ Violation de vie privée

---

## 🤝 SUPPORT

**Problèmes ?** Vérifiez:
1. Les dépendances sont installées (`pip list`)
2. Le backend tourne sur le port 8000
3. Le frontend charge bien `index_pro.html`
4. Les logs du backend pour les erreurs

---

## 🎯 ROADMAP

- [ ] Export PDF des résultats
- [ ] Graphe de relations (NetworkX)
- [ ] Timeline des découvertes
- [ ] Support de theHarvester
- [ ] Support de Spiderfoot
- [ ] Mode batch (fichiers CSV)

---

**🔍 OSINT Intelligence Platform PRO v3.0.0**  
*Professional Grade Intelligence Gathering with Real OSINT Tools*

**Made with ❤️ for Cybersecurity Professionals**
