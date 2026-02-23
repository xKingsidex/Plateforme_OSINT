# 🗺️ Roadmap de Développement Détaillée

## Vue d'ensemble

Ce document détaille le plan de développement étape par étape de la plateforme OSINT.

---

## 📊 Phase 1 : Fondations (Semaines 1-2)

### Objectifs
Mettre en place l'infrastructure de base et les premiers scrapers fonctionnels.

### Tâches

#### Semaine 1 : Setup
- [x] Initialiser structure du projet
- [x] Configurer Docker (PostgreSQL, Neo4j, Redis)
- [x] Créer environnement virtuel Python
- [x] Installer dépendances
- [ ] Configurer variables d'environnement (.env)
- [ ] Obtenir clés API (Shodan, VirusTotal, GitHub)
- [ ] Créer modèles de base de données (SQLAlchemy)
- [ ] Setup FastAPI basique

**Livrables** :
- ✅ Environnement de développement fonctionnel
- ✅ Services Docker opérationnels
- ⏳ API FastAPI avec endpoint `/health`

#### Semaine 2 : Premiers Scrapers
- [ ] Implémenter `BaseScraper` (classe abstraite)
- [ ] Scraper Shodan (IPs)
- [ ] Scraper GitHub (profils, repos, secrets)
- [ ] Scraper Whois (domaines)
- [ ] Tests unitaires pour chaque scraper
- [ ] Endpoint `/scrape` dans API

**Livrables** :
- 3 scrapers fonctionnels
- Tests passés
- Documentation API

**Test de validation** :
```bash
python backend/test_scraper.py
curl -X POST http://localhost:8000/scrape -d '{"target": "8.8.8.8", "type": "ip"}'
```

---

## 📦 Phase 2 : Collecte de Données (Semaines 3-4)

### Objectifs
Élargir les sources OSINT et automatiser la collecte avec Celery.

### Tâches

#### Semaine 3 : Scrapers Avancés
- [ ] Scraper Twitter (via API ou scraping)
- [ ] Scraper LinkedIn (profils publics)
- [ ] Scraper HaveIBeenPwned (fuites d'emails)
- [ ] Scraper VirusTotal (URLs/fichiers)
- [ ] Scraper Pastebin (recherche par keywords)
- [ ] Rate limiting et gestion d'erreurs

**Livrables** :
- 5 nouveaux scrapers
- Gestion des quotas API
- Logging structuré

#### Semaine 4 : Automatisation avec Celery
- [ ] Configuration Celery + Redis
- [ ] Créer tâches asynchrones pour scrapers
- [ ] Queue de priorité (high/medium/low)
- [ ] Retry logic avec backoff exponentiel
- [ ] Interface Flower pour monitoring
- [ ] Endpoints API pour lancer/monitorer jobs

**Livrables** :
- Système de queue fonctionnel
- Dashboard Flower accessible
- Scraping parallèle de 5+ sources

**Test de validation** :
```bash
# Lancer investigation complète
curl -X POST http://localhost:8000/investigations -d '{
  "name": "Test Investigation",
  "target_type": "email",
  "target_value": "test@example.com"
}'

# Vérifier progression dans Flower
open http://localhost:5555
```

---

## 🧠 Phase 3 : IA - NLP (Semaines 5-6)

### Objectifs
Implémenter les modèles d'IA pour analyse de texte et classification.

### Tâches

#### Semaine 5 : NER et Préparation Données
- [ ] Configurer Hugging Face Hub
- [ ] Implémenter NER avec spaCy (emails, IPs, noms, téléphones)
- [ ] Custom NER pour patterns OSINT (CVEs, API keys, credentials)
- [ ] Fine-tuning spaCy sur dataset custom
- [ ] Créer dataset de classification de risque (500+ exemples)
- [ ] Annoter avec Label Studio
- [ ] Data augmentation (synonymes, back-translation)

**Livrables** :
- NER extrayant 10+ types d'entités
- Dataset annoté (1000 exemples)
- Pipeline de data augmentation

#### Semaine 6 : Classification de Risque
- [ ] Fine-tuning DistilBERT sur dataset de risque
- [ ] 4 classes : low/medium/high/critical
- [ ] Évaluation (accuracy, F1-score, confusion matrix)
- [ ] Intégration dans pipeline de scraping
- [ ] Génération automatique d'alertes (high/critical)
- [ ] Endpoint `/analyze` pour analyse de texte

**Livrables** :
- Modèle de classification (F1 > 0.85)
- API d'analyse en temps réel
- Alertes automatiques

**Test de validation** :
```bash
curl -X POST http://localhost:8000/analyze -d '{
  "text": "Plain text password admin123 found in public GitHub repo"
}'
# Devrait retourner: {"risk_level": "critical", "confidence": 0.95}
```

---

## 🕸️ Phase 4 : IA - Graphes (Semaines 7-8)

### Objectifs
Modéliser les relations entre entités et détecter des patterns cachés.

### Tâches

#### Semaine 7 : Modélisation Neo4j
- [ ] Schéma de graphe complet (Person, Email, Domain, IP, etc.)
- [ ] Script de migration PostgreSQL → Neo4j
- [ ] Relations automatiques (OWNS, REGISTERED_ON, RESOLVES_TO)
- [ ] Requêtes Cypher pour patterns communs
- [ ] Visualisation basique dans Neo4j Browser
- [ ] Endpoint `/graph/{investigation_id}`

**Livrables** :
- Schéma Neo4j documenté
- Script de peuplement automatique
- API de requête graphe

#### Semaine 8 : GNN et Community Detection
- [ ] Setup PyTorch Geometric
- [ ] Algorithme de community detection (Louvain)
- [ ] Calcul de centralité (betweenness, PageRank)
- [ ] GNN pour link prediction
- [ ] Détection d'anomalies dans graphe
- [ ] Export graphe (JSON, GraphML)

**Livrables** :
- Détection de communautés
- Identification de nœuds centraux
- Score de similarité entre entités

**Test de validation** :
```bash
# Construire graphe pour investigation
curl http://localhost:8000/graph/build/{inv_id}

# Détecter communautés
curl http://localhost:8000/graph/communities/{inv_id}
# Devrait retourner: {"communities": [[person1, person2], [person3, person4]]}
```

---

## 🎨 Phase 5 : Frontend (Semaines 9-10)

### Objectifs
Créer interface utilisateur intuitive avec visualisations.

### Tâches

#### Semaine 9 : Dashboard et Recherche
- [ ] Setup Vue.js / React
- [ ] Page d'accueil / Dashboard
- [ ] Liste des investigations
- [ ] Formulaire de création d'investigation
- [ ] Page de détails d'investigation
- [ ] Affichage des données collectées (cartes, tableaux)
- [ ] Filtres et recherche

**Livrables** :
- Application frontend fonctionnelle
- CRUD investigations
- UI/UX moderne

#### Semaine 10 : Visualisation et Export
- [ ] Intégration D3.js pour graphe interactif
- [ ] Zoom, pan, filtres sur graphe
- [ ] Timeline des événements
- [ ] Graphiques de métriques (Chart.js)
- [ ] Export PDF de rapports
- [ ] Export JSON/CSV des données
- [ ] Dark mode

**Livrables** :
- Visualisation graphe interactive
- Rapports PDF générés
- Export multi-format

**Test de validation** :
```bash
npm run dev
# Ouvrir http://localhost:3000
# Créer investigation, visualiser graphe, exporter rapport
```

---

## 🚀 Phase 6 : Fonctionnalités Avancées (Semaines 11-12)

### Objectifs
Ajouter détection de faux profils, résumé IA et scoring global.

### Tâches

#### Semaine 11 : Détection de Faux Profils
- [ ] Collecte de features profils sociaux
- [ ] Entraînement Isolation Forest
- [ ] Dataset profils réels vs bots (1000+)
- [ ] Calcul de scores d'anomalie
- [ ] Red flags automatiques (pas de photo, ratio followers, etc.)
- [ ] Endpoint `/detect-fake-profile`

**Livrables** :
- Modèle de détection (precision > 0.90)
- API de détection temps réel

#### Semaine 12 : Résumé IA et Finalisation
- [ ] Fine-tuning BART/T5 pour résumé
- [ ] Génération de rapports narratifs
- [ ] Calcul de score de risque global (0-100)
- [ ] Recommandations automatiques
- [ ] Tests end-to-end
- [ ] Documentation complète
- [ ] Déploiement production (Docker Compose)

**Livrables** :
- Génération de rapports automatiques
- Score de risque global
- Plateforme production-ready

**Test de validation** :
```bash
# Test complet de bout en bout
curl -X POST http://localhost:8000/investigations -d '{
  "name": "Complete Test",
  "target_type": "person",
  "target_value": "John Doe"
}'

# Attendre 30s, puis récupérer rapport
curl http://localhost:8000/investigations/{id}/report
# Devrait retourner: rapport PDF avec graphe, résumé IA, score de risque
```

---

## 📈 Phase 7 : Production & Scaling (Semaines 13+)

### Objectifs optionnels pour mise en production
- [ ] Authentification JWT
- [ ] RBAC (roles: admin, analyst, viewer)
- [ ] Rate limiting API
- [ ] Monitoring (Prometheus, Grafana)
- [ ] CI/CD (GitHub Actions)
- [ ] Kubernetes deployment
- [ ] Backup automatique (PostgreSQL, Neo4j)
- [ ] Tests de charge

---

## 📊 Métriques de Succès

### Phase 1-2
- ✅ 8+ scrapers fonctionnels
- ✅ 100% tests passés
- ✅ API docs complète

### Phase 3-4
- 🎯 F1-score > 0.85 (classification)
- 🎯 NER precision > 0.90
- 🎯 Détection communautés < 5s

### Phase 5-6
- 🎯 Frontend responsive
- 🎯 Export PDF < 2s
- 🎯 Détection fake profiles precision > 0.90

---

## 🎯 Jalons (Milestones)

| Milestone | Date cible | Livrables |
|-----------|------------|-----------|
| MVP (Phase 1-2) | Semaine 4 | 3+ scrapers, API, DB |
| IA v1 (Phase 3) | Semaine 6 | NER, Classification |
| Graphes (Phase 4) | Semaine 8 | Neo4j, GNN |
| Frontend v1 (Phase 5) | Semaine 10 | Dashboard, Viz |
| Production (Phase 6) | Semaine 12 | Plateforme complète |

---

## 💡 Ressources par Phase

### Phase 1-2
- [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/)
- [Celery Docs](https://docs.celeryproject.org/)
- [Scrapy Tutorial](https://docs.scrapy.org/)

### Phase 3-4
- [Hugging Face Course](https://huggingface.co/course)
- [spaCy NER](https://spacy.io/usage/training#ner)
- [Neo4j Graph Data Science](https://neo4j.com/docs/graph-data-science/)

### Phase 5-6
- [Vue.js Guide](https://vuejs.org/guide/)
- [D3.js Gallery](https://observablehq.com/@d3/gallery)
- [Scikit-learn Isolation Forest](https://scikit-learn.org/stable/modules/outlier_detection.html)

---

**Prêt à commencer ? Choisissez votre phase et lancez-vous ! 🚀**
