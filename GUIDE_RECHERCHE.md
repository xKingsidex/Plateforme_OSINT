# 📚 Guide de Recherche et Ressources - Plateforme OSINT

## 🎯 Vue d'ensemble du projet

Cette plateforme OSINT automatisée combine collecte de données, analyse IA et visualisation pour identifier des menaces, profils suspects et corrélations.

---

## 🔍 1. OUTILS ET FRAMEWORKS OSINT EXISTANTS

### A. Frameworks complets à étudier
- **Maltego** : Visualisation de relations (commercial mais instructif)
- **SpiderFoot** : Framework OSINT automatisé (Open Source)
- **theHarvester** : Collecte d'emails, domaines, IPs
- **Recon-ng** : Framework modulaire de reconnaissance
- **OSINT Framework** : https://osintframework.com/ (catalogue d'outils)

### B. Outils spécialisés par domaine
```
Réseaux sociaux : Twint (Twitter), Instaloader, Facebook Graph API
GitHub : GitHub API, GitLeaks, TruffleHog
Domaines/IPs : Shodan, Censys, SecurityTrails, VirusTotal
Emails : Hunter.io, HaveIBeenPwned, EmailRep
Fuites de données : Dehashed, IntelX, LeakCheck
Pastebin : PasteBin Scraper, Gist scraping
Darkweb : Ahmia, OnionScan (nécessite Tor)
```

---

## 🔌 2. APIS ET SERVICES DISPONIBLES

### APIs Gratuites (avec limites)
| Service | API | Limite gratuite | Usage |
|---------|-----|-----------------|-------|
| **Shodan** | shodan.io | 100 requêtes/mois | Scan d'appareils IoT/serveurs |
| **VirusTotal** | virustotal.com | 4 req/min | Analyse de fichiers/URLs |
| **HaveIBeenPwned** | haveibeenpwned.com | Gratuit | Vérification fuites emails |
| **Hunter.io** | hunter.io | 25 req/mois | Recherche emails |
| **GitHub API** | api.github.com | 5000 req/h | Scan de repos |
| **WhoisXML** | whoisxmlapi.com | 500 req/mois | Whois enrichi |
| **AlienVault OTX** | otx.alienvault.com | Gratuit | Threat intelligence |

### APIs Payantes (optionnelles pour scale)
- **Censys** : 250$/mois
- **SecurityTrails** : 99$/mois
- **IntelX** : À partir de 20$/mois
- **Dehashed** : 5$/semaine

### Scraping sans API
Pour les sources sans API (forums, réseaux sociaux) :
- **Scrapy** : Framework Python de scraping
- **Selenium** : Automatisation navigateur
- **BeautifulSoup** : Parsing HTML
- **Playwright** : Alternative moderne à Selenium

---

## 🧠 3. INTELLIGENCE ARTIFICIELLE - MODÈLES ET APPROCHES

### A. Tâches IA à implémenter

#### 1️⃣ **Classification de texte (NLP)**
**Objectif** : Classer les informations par risque (faible/moyen/élevé)

**Modèles recommandés** :
- **BERT** (bert-base-uncased) : Classification de texte
- **DistilBERT** : Version allégée de BERT
- **RoBERTa** : Amélioration de BERT
- **Sentence Transformers** : Pour embeddings de texte

**Librairies** :
```python
transformers (Hugging Face)
sentence-transformers
spaCy (NER - Named Entity Recognition)
```

**Datasets d'entraînement** :
- **TweetEval** : Classification de tweets
- **AG News** : Classification d'articles
- **Hate Speech datasets** : Détection de contenu malveillant
- **Phishing datasets** : Classification URLs suspectes

#### 2️⃣ **Détection d'anomalies**
**Objectif** : Identifier comportements suspects, faux profils

**Approches** :
- **Isolation Forest** : Détection anomalies
- **Autoencoders** : Reconstruction d'entités normales
- **One-Class SVM** : Classification binaire

**Datasets** :
- Créer votre propre dataset avec profils normaux vs bots
- **Twitter Bot Detection datasets** (Kaggle, GitHub)

#### 3️⃣ **Graph Neural Networks (GNN)**
**Objectif** : Détecter liens entre personnes/entités

**Modèles** :
- **PyTorch Geometric** : Librairie GNN
- **Neo4j** : Base de données graphe
- **NetworkX** : Analyse de graphes

**Algorithmes** :
- **Graph Convolutional Networks (GCN)**
- **GraphSAGE** : Pour grands graphes
- **Community Detection** : Louvain, Girvan-Newman

#### 4️⃣ **Named Entity Recognition (NER)**
**Objectif** : Extraire noms, emails, IPs, dates

**Modèles** :
- **spaCy** (en_core_web_lg) : NER pré-entraîné
- **BERT-NER** : Fine-tuned sur NER
- **Flair** : Embeddings contextuels

#### 5️⃣ **Résumé automatique**
**Objectif** : Générer rapports synthétiques

**Modèles** :
- **BART** : Résumé extractif/abstractif
- **T5** : Text-to-Text Transfer Transformer
- **Pegasus** : Spécialisé résumé

---

## 📊 4. DATASETS OPEN SOURCE POUR ENTRAÎNEMENT

### A. Datasets publics

#### Sécurité & Cyber
```
- PhishTank : URLs de phishing (phishtank.org)
- Malware Bazaar : Samples de malware (bazaar.abuse.ch)
- URLhaus : URLs malveillantes (urlhaus.abuse.ch)
- Kaggle Security Datasets : kaggle.com/datasets?tags=security
```

#### Réseaux sociaux
```
- Twitter datasets : kaggle.com (chercher "twitter sentiment")
- Reddit datasets : pushshift.io (archives Reddit)
- Facebook Bot Detection : github.com/fb-research
```

#### Text Classification
```
- Hugging Face Datasets : huggingface.co/datasets
- Common Crawl : Données web massives
- OpenWebText : Corpus de texte web
```

### B. Créer vos propres datasets

**Méthode recommandée** :
1. Scraper des données publiques légalement
2. Annoter manuellement (~500-1000 exemples minimum)
3. Utiliser **Label Studio** pour annotation
4. Augmenter avec techniques de data augmentation

**Outils d'annotation** :
- **Label Studio** : label-studio.io
- **Prodigy** : prodi.gy (payant)
- **Doccano** : github.com/doccano

---

## 🛠️ 5. STACK TECHNIQUE RECOMMANDÉE

### Backend
```python
FastAPI         # API REST moderne
SQLAlchemy      # ORM pour PostgreSQL
Celery          # Tâches asynchrones
Redis           # Cache et queue
PostgreSQL      # Base de données principale
Neo4j           # Base graphe pour relations
```

### Scraping & OSINT
```python
Scrapy          # Framework scraping
Selenium/Playwright  # Scraping dynamique
BeautifulSoup   # Parsing HTML
Requests        # HTTP client
aiohttp         # HTTP asynchrone
```

### IA & ML
```python
transformers    # Hugging Face models
torch           # PyTorch
scikit-learn    # ML classique
spaCy           # NLP
sentence-transformers  # Embeddings
pytorch-geometric  # GNN
```

### Frontend
```javascript
Vue.js / React  # Framework UI
D3.js           # Visualisation graphes
Chart.js        # Graphiques
Tailwind CSS    # Styling
```

---

## 🚀 6. ROADMAP DE DÉVELOPPEMENT

### Phase 1 : Fondations (Semaines 1-2)
1. Setup environnement (Docker, PostgreSQL, Redis)
2. Architecture FastAPI de base
3. Premiers scrapers simples (Whois, GitHub)
4. Tests des APIs Shodan, VirusTotal

### Phase 2 : Collecte de données (Semaines 3-4)
1. Implémenter 5-7 scrapers principaux
2. Système de queue avec Celery
3. Stockage structuré dans PostgreSQL
4. Logs et monitoring

### Phase 3 : IA - NLP (Semaines 5-6)
1. Implémenter NER avec spaCy
2. Classification de risque (BERT)
3. Créer dataset annoté (500+ exemples)
4. Fine-tuning du modèle

### Phase 4 : IA - Graphes (Semaines 7-8)
1. Setup Neo4j
2. Modéliser relations (personnes, domaines, IPs)
3. Algorithmes de détection de communautés
4. GNN pour détection de liens

### Phase 5 : Frontend (Semaines 9-10)
1. Dashboard Vue/React
2. Visualisation de graphes (D3.js)
3. Interface de recherche
4. Génération de rapports PDF

### Phase 6 : Avancé (Semaines 11-12)
1. Détection de faux profils
2. Résumé automatique
3. Scoring de risque automatisé
4. Export multi-format

---

## 📖 7. RESSOURCES D'APPRENTISSAGE

### Cours & Tutoriels
- **OSINT** : IntelTechniques.com (Michael Bazzell)
- **NLP** : Hugging Face Course (huggingface.co/course)
- **GNN** : Stanford CS224W (web.stanford.edu/class/cs224w)
- **Scrapy** : docs.scrapy.org/en/latest/intro/tutorial.html

### Livres
- "Open Source Intelligence Techniques" - Michael Bazzell
- "Natural Language Processing with Transformers" - Hugging Face
- "Graph Representation Learning" - William L. Hamilton

### Communautés
- Reddit : r/OSINT, r/cybersecurity
- Discord : OSINT Curious
- GitHub : Awesome OSINT (github.com/jivoi/awesome-osint)

---

## ⚖️ 8. CONSIDÉRATIONS LÉGALES ET ÉTHIQUES

**IMPORTANT** :
- ✅ Scraper uniquement des données **publiques**
- ✅ Respecter robots.txt et Terms of Service
- ✅ Anonymiser les données personnelles si nécessaire
- ✅ Usage défensif uniquement (cybersécurité légitime)
- ❌ Pas de scraping de données privées
- ❌ Pas de violation de RGPD
- ❌ Usage strictement éthique (no stalking, no harassment)

---

## 🎯 NEXT STEPS

1. Lire ce guide en entier
2. Créer comptes APIs (Shodan, VirusTotal, etc.)
3. Setup environnement de développement
4. Commencer par Phase 1 de la roadmap
5. Itérer et améliorer progressivement

---

**Prêt à commencer ? Dites-moi par quelle phase vous voulez démarrer !**
