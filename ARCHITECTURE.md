# 🏗️ Architecture Technique - Plateforme OSINT

## 📐 Vue d'ensemble

```
┌─────────────────────────────────────────────────────────────┐
│                    FRONTEND (Vue.js/React)                  │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │Dashboard │  │ Search   │  │  Graph   │  │ Reports  │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
└─────────────────────────────┬───────────────────────────────┘
                              │ REST API
┌─────────────────────────────▼───────────────────────────────┐
│                    API GATEWAY (FastAPI)                    │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │  Auth    │  │  Search  │  │   IA     │  │  Export  │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
└───────┬────────────────┬────────────────┬──────────────────┘
        │                │                │
┌───────▼─────┐  ┌───────▼─────┐  ┌──────▼───────┐
│   CELERY    │  │   REDIS     │  │  PostgreSQL  │
│   Workers   │  │   Cache     │  │   + Neo4j    │
└───────┬─────┘  └─────────────┘  └──────────────┘
        │
┌───────▼──────────────────────────────────────────────┐
│              SCRAPERS & COLLECTORS                   │
│  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐       │
│  │Shodan  │ │GitHub  │ │Social  │ │Whois   │       │
│  └────────┘ └────────┘ └────────┘ └────────┘       │
└──────────────────────────────────────────────────────┘
        │
┌───────▼──────────────────────────────────────────────┐
│              IA PROCESSING PIPELINE                  │
│  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐       │
│  │  NER   │ │Classify│ │  GNN   │ │Summary │       │
│  └────────┘ └────────┘ └────────┘ └────────┘       │
└──────────────────────────────────────────────────────┘
```

---

## 🗄️ Modèle de Données

### PostgreSQL (Données structurées)

```sql
-- Table principale des enquêtes
CREATE TABLE investigations (
    id UUID PRIMARY KEY,
    name VARCHAR(255),
    target_type VARCHAR(50), -- 'person', 'domain', 'ip', 'email'
    target_value TEXT,
    status VARCHAR(50),
    risk_score FLOAT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- Données collectées
CREATE TABLE collected_data (
    id UUID PRIMARY KEY,
    investigation_id UUID REFERENCES investigations(id),
    source VARCHAR(100), -- 'shodan', 'github', 'twitter'
    data_type VARCHAR(50), -- 'profile', 'post', 'leak'
    raw_data JSONB,
    processed_data JSONB,
    risk_level VARCHAR(20), -- 'low', 'medium', 'high', 'critical'
    collected_at TIMESTAMP,
    ai_confidence FLOAT
);

-- Entités extraites (NER)
CREATE TABLE entities (
    id UUID PRIMARY KEY,
    investigation_id UUID REFERENCES investigations(id),
    entity_type VARCHAR(50), -- 'person', 'email', 'ip', 'phone', 'location'
    entity_value TEXT,
    source_data_id UUID REFERENCES collected_data(id),
    confidence FLOAT,
    created_at TIMESTAMP
);

-- Alertes générées par l'IA
CREATE TABLE alerts (
    id UUID PRIMARY KEY,
    investigation_id UUID REFERENCES investigations(id),
    severity VARCHAR(20),
    alert_type VARCHAR(100), -- 'leaked_password', 'exposed_port', 'suspicious_activity'
    description TEXT,
    evidence JSONB,
    created_at TIMESTAMP
);

-- Jobs de scraping
CREATE TABLE scraping_jobs (
    id UUID PRIMARY KEY,
    investigation_id UUID REFERENCES investigations(id),
    scraper_name VARCHAR(100),
    status VARCHAR(50), -- 'pending', 'running', 'completed', 'failed'
    params JSONB,
    results_count INT,
    error_message TEXT,
    started_at TIMESTAMP,
    completed_at TIMESTAMP
);
```

### Neo4j (Graphe de relations)

```cypher
// Nœuds
(:Person {name, emails[], phones[], risk_score})
(:Email {address, leaked, first_seen})
(:Domain {name, registrar, creation_date})
(:IPAddress {ip, country, ports[], services[]})
(:SocialProfile {platform, username, url, is_fake_probability})
(:Organization {name, industry})

// Relations
(:Person)-[:OWNS]->(:Email)
(:Person)-[:WORKS_AT]->(:Organization)
(:Email)-[:REGISTERED_ON]->(:Domain)
(:Domain)-[:RESOLVES_TO]->(:IPAddress)
(:Person)-[:HAS_PROFILE]->(:SocialProfile)
(:Person)-[:KNOWS]->(:Person)
(:Person)-[:ASSOCIATED_WITH]->(:IPAddress)
```

---

## 🔄 Architecture des Scrapers

### Structure modulaire

```python
# base_scraper.py
from abc import ABC, abstractmethod

class BaseScraper(ABC):
    def __init__(self, config):
        self.config = config
        self.rate_limit = config.get('rate_limit', 1)  # req/sec

    @abstractmethod
    async def scrape(self, target):
        """Collecte les données"""
        pass

    @abstractmethod
    def parse(self, raw_data):
        """Parse les données brutes"""
        pass

    async def process(self, target):
        """Pipeline complet"""
        raw = await self.scrape(target)
        parsed = self.parse(raw)
        enriched = await self.enrich(parsed)
        return enriched

    async def enrich(self, data):
        """Enrichissement avec IA"""
        # Appel au module IA
        return data
```

### Exemples de scrapers

```python
# scrapers/shodan_scraper.py
import shodan

class ShodanScraper(BaseScraper):
    def __init__(self, api_key):
        self.api = shodan.Shodan(api_key)

    async def scrape(self, ip_address):
        try:
            result = self.api.host(ip_address)
            return {
                'ip': result['ip_str'],
                'ports': result.get('ports', []),
                'vulns': result.get('vulns', []),
                'os': result.get('os'),
                'org': result.get('org'),
                'country': result.get('country_name')
            }
        except shodan.APIError as e:
            return {'error': str(e)}

# scrapers/github_scraper.py
from github import Github

class GitHubScraper(BaseScraper):
    def __init__(self, token):
        self.gh = Github(token)

    async def scrape(self, username):
        user = self.gh.get_user(username)
        repos = user.get_repos()

        # Recherche de secrets dans repos
        secrets_found = []
        for repo in repos[:10]:  # Limite à 10 repos
            secrets = self.scan_for_secrets(repo)
            if secrets:
                secrets_found.append({
                    'repo': repo.full_name,
                    'secrets': secrets
                })

        return {
            'username': user.login,
            'name': user.name,
            'email': user.email,
            'repos_count': user.public_repos,
            'followers': user.followers,
            'secrets_found': secrets_found
        }

    def scan_for_secrets(self, repo):
        # Utiliser TruffleHog ou regex
        patterns = {
            'AWS_KEY': r'AKIA[0-9A-Z]{16}',
            'API_KEY': r'api[_-]?key["\']?\s*[:=]\s*["\']?([a-zA-Z0-9]{32,})',
        }
        # Implementation...
```

---

## 🧠 Pipeline IA

### 1. NER (Named Entity Recognition)

```python
# ai/ner_extractor.py
import spacy
from transformers import pipeline

class NERExtractor:
    def __init__(self):
        self.spacy_model = spacy.load("en_core_web_lg")
        self.transformer_ner = pipeline("ner", model="dslim/bert-base-NER")

    def extract_entities(self, text):
        """Extrait entités avec spaCy + BERT"""
        entities = {
            'persons': [],
            'emails': [],
            'phones': [],
            'ips': [],
            'locations': []
        }

        # spaCy
        doc = self.spacy_model(text)
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                entities['persons'].append(ent.text)
            elif ent.label_ == "GPE":
                entities['locations'].append(ent.text)

        # Regex pour emails, IPs
        entities['emails'] = self._extract_emails(text)
        entities['ips'] = self._extract_ips(text)

        return entities
```

### 2. Classification de risque

```python
# ai/risk_classifier.py
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

class RiskClassifier:
    def __init__(self, model_path='./models/risk_classifier'):
        self.tokenizer = AutoTokenizer.from_pretrained('distilbert-base-uncased')
        self.model = AutoModelForSequenceClassification.from_pretrained(
            model_path,
            num_labels=4  # low, medium, high, critical
        )

    def classify(self, text):
        """Classifie le risque d'une information"""
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
        outputs = self.model(**inputs)
        probs = torch.softmax(outputs.logits, dim=1)

        risk_levels = ['low', 'medium', 'high', 'critical']
        predicted_class = torch.argmax(probs).item()
        confidence = probs[0][predicted_class].item()

        return {
            'risk_level': risk_levels[predicted_class],
            'confidence': confidence,
            'probabilities': {
                level: prob.item() for level, prob in zip(risk_levels, probs[0])
            }
        }
```

### 3. Détection de faux profils

```python
# ai/fake_profile_detector.py
from sklearn.ensemble import IsolationForest
import numpy as np

class FakeProfileDetector:
    def __init__(self):
        self.model = IsolationForest(contamination=0.1, random_state=42)
        self.is_trained = False

    def extract_features(self, profile):
        """Extrait features d'un profil social"""
        return np.array([
            profile.get('followers_count', 0),
            profile.get('following_count', 0),
            profile.get('posts_count', 0),
            profile.get('account_age_days', 0),
            profile.get('avg_post_length', 0),
            profile.get('follower_following_ratio', 0),
            int(profile.get('has_profile_picture', False)),
            int(profile.get('has_bio', False)),
            profile.get('posts_per_day', 0)
        ]).reshape(1, -1)

    def predict(self, profile):
        """Prédit si profil est fake"""
        features = self.extract_features(profile)
        prediction = self.model.predict(features)
        score = self.model.score_samples(features)

        return {
            'is_fake': prediction[0] == -1,
            'anomaly_score': abs(score[0]),
            'confidence': min(abs(score[0]) * 100, 100)
        }
```

### 4. Graph Neural Network pour relations

```python
# ai/graph_analyzer.py
import networkx as nx
from neo4j import GraphDatabase
from torch_geometric.nn import GCNConv
import torch

class GraphAnalyzer:
    def __init__(self, neo4j_uri, user, password):
        self.driver = GraphDatabase.driver(neo4j_uri, auth=(user, password))
        self.nx_graph = nx.Graph()

    def build_graph(self, investigation_id):
        """Construit graphe depuis Neo4j"""
        with self.driver.session() as session:
            # Récupérer nœuds et relations
            result = session.run("""
                MATCH (n)-[r]->(m)
                WHERE n.investigation_id = $inv_id
                RETURN n, r, m
            """, inv_id=investigation_id)

            for record in result:
                # Ajouter au graphe NetworkX
                self.nx_graph.add_edge(
                    record['n'].id,
                    record['m'].id,
                    relationship=record['r'].type
                )

    def detect_communities(self):
        """Détecte communautés (groupes liés)"""
        from networkx.algorithms import community
        communities = community.louvain_communities(self.nx_graph)
        return [list(comm) for comm in communities]

    def find_central_nodes(self):
        """Trouve nœuds centraux (personnes clés)"""
        centrality = nx.betweenness_centrality(self.nx_graph)
        sorted_nodes = sorted(centrality.items(), key=lambda x: x[1], reverse=True)
        return sorted_nodes[:10]
```

### 5. Résumé automatique

```python
# ai/summarizer.py
from transformers import pipeline

class ReportSummarizer:
    def __init__(self):
        self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

    def generate_summary(self, investigation_data):
        """Génère résumé d'une enquête"""
        # Compiler toutes les données
        full_text = self._compile_investigation(investigation_data)

        # Résumer en chunks
        max_length = 1024
        chunks = [full_text[i:i+max_length] for i in range(0, len(full_text), max_length)]

        summaries = []
        for chunk in chunks[:5]:  # Max 5 chunks
            summary = self.summarizer(chunk, max_length=150, min_length=50)
            summaries.append(summary[0]['summary_text'])

        return ' '.join(summaries)

    def _compile_investigation(self, data):
        """Compile données en texte narratif"""
        text = f"Investigation on {data['target_value']}.\n"
        text += f"Risk score: {data['risk_score']}/100.\n"
        text += f"Alerts: {len(data['alerts'])} alerts generated.\n"
        # Ajouter détails...
        return text
```

---

## ⚙️ Configuration API

### Structure du fichier config

```python
# config.py
from pydantic import BaseSettings

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql://user:pass@localhost/osint_db"
    NEO4J_URI: str = "bolt://localhost:7687"
    NEO4J_USER: str = "neo4j"
    NEO4J_PASSWORD: str = "password"
    REDIS_URL: str = "redis://localhost:6379"

    # APIs
    SHODAN_API_KEY: str
    VIRUSTOTAL_API_KEY: str
    GITHUB_TOKEN: str
    HUNTER_IO_KEY: str

    # AI Models
    AI_MODEL_PATH: str = "./models"
    USE_GPU: bool = True

    # Celery
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"

    class Config:
        env_file = ".env"

settings = Settings()
```

### FastAPI Routes

```python
# api/main.py
from fastapi import FastAPI, BackgroundTasks
from api.routes import investigations, scrapers, ai_analysis

app = FastAPI(title="OSINT Platform API")

app.include_router(investigations.router, prefix="/api/investigations")
app.include_router(scrapers.router, prefix="/api/scrapers")
app.include_router(ai_analysis.router, prefix="/api/ai")

# api/routes/investigations.py
from fastapi import APIRouter, Depends
from typing import List
from tasks.scraping_tasks import launch_investigation

router = APIRouter()

@router.post("/")
async def create_investigation(target: str, target_type: str, background_tasks: BackgroundTasks):
    """Crée une nouvelle enquête"""
    investigation_id = generate_uuid()

    # Lancer scrapers en tâche de fond
    background_tasks.add_task(launch_investigation, investigation_id, target, target_type)

    return {"id": investigation_id, "status": "pending"}

@router.get("/{investigation_id}")
async def get_investigation(investigation_id: str):
    """Récupère résultats d'enquête"""
    # Query DB + Neo4j
    return investigation_data

@router.get("/{investigation_id}/graph")
async def get_investigation_graph(investigation_id: str):
    """Récupère graphe de relations"""
    # Query Neo4j
    return graph_data
```

---

## 🐳 Déploiement Docker

```yaml
# docker-compose.yml
version: '3.8'

services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: osint_db
      POSTGRES_USER: osint
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  neo4j:
    image: neo4j:5
    environment:
      NEO4J_AUTH: neo4j/${NEO4J_PASSWORD}
    volumes:
      - neo4j_data:/data
    ports:
      - "7474:7474"
      - "7687:7687"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  api:
    build: ./backend
    command: uvicorn api.main:app --host 0.0.0.0 --port 8000
    volumes:
      - ./backend:/app
    ports:
      - "8000:8000"
    depends_on:
      - postgres
      - redis
      - neo4j
    env_file:
      - .env

  celery_worker:
    build: ./backend
    command: celery -A tasks.celery_app worker --loglevel=info
    volumes:
      - ./backend:/app
    depends_on:
      - redis
      - postgres
    env_file:
      - .env

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    depends_on:
      - api

volumes:
  postgres_data:
  neo4j_data:
```

---

## 📊 Monitoring et Logs

```python
# utils/logger.py
import logging
from logging.handlers import RotatingFileHandler

def setup_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    handler = RotatingFileHandler(
        f'logs/{name}.log',
        maxBytes=10000000,  # 10MB
        backupCount=5
    )

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger
```

---

**Cette architecture est modulaire, scalable et prête pour la production !**
