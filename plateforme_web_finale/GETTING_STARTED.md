# 🚀 Guide de Démarrage Pratique

## 📋 Prérequis

### 1. Environnement de développement

```bash
# Python 3.9+
python --version  # Doit être >= 3.9

# Node.js 16+ (pour le frontend)
node --version

# Docker & Docker Compose
docker --version
docker-compose --version

# Git
git --version
```

### 2. Créer comptes pour APIs gratuites

Créez ces comptes **MAINTENANT** (prend 30 min) :

| Service | URL d'inscription | Clé gratuite |
|---------|-------------------|--------------|
| **Shodan** | https://account.shodan.io/register | ✅ 100 req/mois |
| **VirusTotal** | https://www.virustotal.com/gui/join-us | ✅ 4 req/min |
| **GitHub** | https://github.com/settings/tokens | ✅ 5000 req/h |
| **HaveIBeenPwned** | https://haveibeenpwned.com/API/Key | ✅ Gratuit |
| **Hunter.io** | https://hunter.io/users/sign_up | ✅ 25 req/mois |
| **AlienVault OTX** | https://otx.alienvault.com/ | ✅ Gratuit |

**Sauvegardez toutes vos clés dans un fichier `keys.txt` temporaire !**

---

## 📁 Phase 1 : Setup Initial (30 min)

### Étape 1.1 : Cloner et structurer le projet

```bash
cd Plateforme_OSINT

# Créer structure de dossiers
mkdir -p backend/{api,scrapers,ai,models,tasks,utils,tests}
mkdir -p frontend/{src,public}
mkdir -p data/{raw,processed,models}
mkdir -p logs
mkdir -p docker
mkdir -p notebooks  # Pour expérimentation Jupyter
```

### Étape 1.2 : Créer environnement virtuel Python

```bash
# Créer virtualenv
python -m venv venv

# Activer
source venv/bin/activate  # Linux/Mac
# OU
venv\Scripts\activate  # Windows

# Upgrader pip
pip install --upgrade pip
```

### Étape 1.3 : Installer dépendances Python

```bash
# Créer requirements.txt
cat > requirements.txt << 'EOF'
# API Framework
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
pydantic-settings==2.1.0

# Database
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
neo4j==5.14.0
redis==5.0.1

# Scraping
scrapy==2.11.0
selenium==4.15.2
beautifulsoup4==4.12.2
requests==2.31.0
aiohttp==3.9.0

# OSINT APIs
shodan==1.31.0
python-whois==0.8.0
dnspython==2.4.2

# AI/ML
torch==2.1.0
transformers==4.35.0
sentence-transformers==2.2.2
spacy==3.7.2
scikit-learn==1.3.2
networkx==3.2.1
torch-geometric==2.4.0

# Tasks
celery==5.3.4
flower==2.0.1

# Utils
python-dotenv==1.0.0
pydantic==2.5.0
loguru==0.7.2
pytest==7.4.3

# Export
reportlab==4.0.7
jinja2==3.1.2
EOF

# Installer
pip install -r requirements.txt

# Télécharger modèle spaCy
python -m spacy download en_core_web_lg
```

### Étape 1.4 : Configuration environnement

```bash
# Créer fichier .env
cat > .env << 'EOF'
# Database
DATABASE_URL=postgresql://osint:osint123@localhost:5432/osint_db
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=osint_neo4j_pass
REDIS_URL=redis://localhost:6379

# APIs - REMPLACEZ PAR VOS CLÉS
SHODAN_API_KEY=your_shodan_key_here
VIRUSTOTAL_API_KEY=your_vt_key_here
GITHUB_TOKEN=your_github_token_here
HUNTER_IO_KEY=your_hunter_key_here
HIBP_API_KEY=your_hibp_key_here

# AI
AI_MODEL_PATH=./models
USE_GPU=False

# Celery
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# Security
SECRET_KEY=change_this_to_random_string_in_production
EOF

echo "⚠️  N'oubliez pas de remplacer les clés API dans .env !"
```

### Étape 1.5 : Lancer les services Docker

```bash
# Créer docker-compose.yml simple
cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  postgres:
    image: postgres:15
    container_name: osint_postgres
    environment:
      POSTGRES_DB: osint_db
      POSTGRES_USER: osint
      POSTGRES_PASSWORD: osint123
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  neo4j:
    image: neo4j:5
    container_name: osint_neo4j
    environment:
      NEO4J_AUTH: neo4j/osint_neo4j_pass
    ports:
      - "7474:7474"
      - "7687:7687"
    volumes:
      - neo4j_data:/data

  redis:
    image: redis:7-alpine
    container_name: osint_redis
    ports:
      - "6379:6379"

volumes:
  postgres_data:
  neo4j_data:
EOF

# Lancer les services
docker-compose up -d

# Vérifier que tout tourne
docker-compose ps
```

---

## 🧪 Phase 2 : Premier Scraper (1h)

### Étape 2.1 : Créer le scraper de base

```bash
# Créer structure
touch backend/scrapers/__init__.py
touch backend/scrapers/base_scraper.py
touch backend/scrapers/shodan_scraper.py
```

```python
# backend/scrapers/base_scraper.py
from abc import ABC, abstractmethod
from typing import Dict, Any
import asyncio
from loguru import logger

class BaseScraper(ABC):
    """Classe de base pour tous les scrapers"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.rate_limit = config.get('rate_limit', 1)
        logger.info(f"Initializing {self.__class__.__name__}")

    @abstractmethod
    async def scrape(self, target: str) -> Dict[str, Any]:
        """Collecte les données brutes"""
        pass

    @abstractmethod
    def parse(self, raw_data: Dict) -> Dict[str, Any]:
        """Parse et nettoie les données"""
        pass

    async def process(self, target: str) -> Dict[str, Any]:
        """Pipeline complet : scrape + parse"""
        try:
            logger.info(f"Processing target: {target}")
            raw_data = await self.scrape(target)
            parsed_data = self.parse(raw_data)
            return {
                'status': 'success',
                'target': target,
                'data': parsed_data
            }
        except Exception as e:
            logger.error(f"Error processing {target}: {str(e)}")
            return {
                'status': 'error',
                'target': target,
                'error': str(e)
            }

    async def rate_limit_wait(self):
        """Respect du rate limit"""
        await asyncio.sleep(1 / self.rate_limit)
```

```python
# backend/scrapers/shodan_scraper.py
import shodan
from scrapers.base_scraper import BaseScraper
from typing import Dict, Any
import os

class ShodanScraper(BaseScraper):
    """Scraper pour Shodan API"""

    def __init__(self, api_key: str = None):
        config = {'rate_limit': 1}  # 1 req/sec pour free tier
        super().__init__(config)
        self.api_key = api_key or os.getenv('SHODAN_API_KEY')
        self.api = shodan.Shodan(self.api_key)

    async def scrape(self, ip_address: str) -> Dict[str, Any]:
        """Récupère infos Shodan pour une IP"""
        try:
            await self.rate_limit_wait()
            result = self.api.host(ip_address)
            return result
        except shodan.APIError as e:
            return {'error': str(e)}

    def parse(self, raw_data: Dict) -> Dict[str, Any]:
        """Parse les données Shodan"""
        if 'error' in raw_data:
            return {'error': raw_data['error']}

        return {
            'ip': raw_data.get('ip_str'),
            'ports_open': raw_data.get('ports', []),
            'vulnerabilities': list(raw_data.get('vulns', [])),
            'os': raw_data.get('os'),
            'organization': raw_data.get('org'),
            'country': raw_data.get('country_name'),
            'city': raw_data.get('city'),
            'isp': raw_data.get('isp'),
            'services': [
                {
                    'port': item.get('port'),
                    'protocol': item.get('transport'),
                    'product': item.get('product'),
                    'version': item.get('version')
                }
                for item in raw_data.get('data', [])
            ],
            'risk_score': self._calculate_risk_score(raw_data)
        }

    def _calculate_risk_score(self, data: Dict) -> float:
        """Calcule score de risque basique"""
        score = 0.0

        # Nombre de ports ouverts
        ports_count = len(data.get('ports', []))
        score += min(ports_count * 5, 30)

        # Vulnérabilités connues
        vulns_count = len(data.get('vulns', []))
        score += min(vulns_count * 20, 50)

        # Ports critiques ouverts
        critical_ports = [21, 22, 23, 3389, 445, 1433, 3306]
        open_critical = len(set(data.get('ports', [])) & set(critical_ports))
        score += open_critical * 10

        return min(score, 100)
```

### Étape 2.2 : Tester le scraper

```python
# backend/test_scraper.py
import asyncio
from scrapers.shodan_scraper import ShodanScraper
from dotenv import load_dotenv

load_dotenv()

async def test_shodan():
    scraper = ShodanScraper()

    # Test avec Google DNS (8.8.8.8)
    result = await scraper.process('8.8.8.8')

    print("=" * 50)
    print("RÉSULTAT SHODAN")
    print("=" * 50)
    print(f"Status: {result['status']}")
    print(f"Target: {result['target']}")

    if result['status'] == 'success':
        data = result['data']
        print(f"\nIP: {data['ip']}")
        print(f"Organisation: {data['organization']}")
        print(f"Pays: {data['country']}")
        print(f"Ports ouverts: {data['ports_open']}")
        print(f"Score de risque: {data['risk_score']}/100")

        if data['vulnerabilities']:
            print(f"\n⚠️  VULNÉRABILITÉS DÉTECTÉES:")
            for vuln in data['vulnerabilities']:
                print(f"  - {vuln}")

if __name__ == "__main__":
    asyncio.run(test_shodan())
```

**Lancer le test :**

```bash
cd backend
python test_scraper.py
```

---

## 🗄️ Phase 3 : Base de données (1h)

### Étape 3.1 : Créer le modèle SQLAlchemy

```python
# backend/models/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv('DATABASE_URL')

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

```python
# backend/models/models.py
from sqlalchemy import Column, String, Float, DateTime, JSON, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid
from models.database import Base

class Investigation(Base):
    __tablename__ = 'investigations'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255))
    target_type = Column(String(50))  # 'ip', 'domain', 'email', 'username'
    target_value = Column(String(255))
    status = Column(String(50), default='pending')
    risk_score = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class CollectedData(Base):
    __tablename__ = 'collected_data'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    investigation_id = Column(UUID(as_uuid=True), ForeignKey('investigations.id'))
    source = Column(String(100))  # 'shodan', 'github', etc.
    data_type = Column(String(50))
    raw_data = Column(JSON)
    processed_data = Column(JSON)
    risk_level = Column(String(20))
    collected_at = Column(DateTime, default=datetime.utcnow)
    ai_confidence = Column(Float)

class Alert(Base):
    __tablename__ = 'alerts'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    investigation_id = Column(UUID(as_uuid=True), ForeignKey('investigations.id'))
    severity = Column(String(20))  # 'low', 'medium', 'high', 'critical'
    alert_type = Column(String(100))
    description = Column(String)
    evidence = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
```

### Étape 3.2 : Créer les tables

```python
# backend/create_tables.py
from models.database import engine, Base
from models.models import Investigation, CollectedData, Alert

def create_tables():
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created successfully!")

if __name__ == "__main__":
    create_tables()
```

```bash
cd backend
python create_tables.py
```

### Étape 3.3 : Sauvegarder les données scrapées

```python
# backend/test_db_integration.py
import asyncio
from scrapers.shodan_scraper import ShodanScraper
from models.database import SessionLocal
from models.models import Investigation, CollectedData, Alert
from dotenv import load_dotenv
import uuid

load_dotenv()

async def test_full_pipeline():
    # 1. Créer une investigation
    db = SessionLocal()

    investigation = Investigation(
        name="Test Shodan IP Scan",
        target_type="ip",
        target_value="8.8.8.8"
    )
    db.add(investigation)
    db.commit()
    db.refresh(investigation)

    print(f"✅ Investigation créée: {investigation.id}")

    # 2. Scraper les données
    scraper = ShodanScraper()
    result = await scraper.process('8.8.8.8')

    if result['status'] == 'success':
        data = result['data']

        # 3. Sauvegarder dans collected_data
        collected = CollectedData(
            investigation_id=investigation.id,
            source='shodan',
            data_type='ip_scan',
            raw_data=result,
            processed_data=data,
            risk_level='medium' if data['risk_score'] > 50 else 'low',
            ai_confidence=0.0
        )
        db.add(collected)

        # 4. Créer alerte si vulnérabilités
        if data['vulnerabilities']:
            alert = Alert(
                investigation_id=investigation.id,
                severity='high',
                alert_type='vulnerabilities_detected',
                description=f"{len(data['vulnerabilities'])} vulnerabilities found",
                evidence={'vulns': data['vulnerabilities']}
            )
            db.add(alert)

        # 5. Mettre à jour risk_score
        investigation.risk_score = data['risk_score']
        investigation.status = 'completed'

        db.commit()

        print(f"✅ Données sauvegardées")
        print(f"   Risk Score: {data['risk_score']}/100")
        print(f"   Alerts: {len(data['vulnerabilities'])} vulns")

    db.close()

if __name__ == "__main__":
    asyncio.run(test_full_pipeline())
```

```bash
python test_db_integration.py
```

---

## 🌐 Phase 4 : API FastAPI (1h)

### Étape 4.1 : Créer l'API de base

```python
# backend/api/main.py
from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from models.database import get_db
from models.models import Investigation, CollectedData, Alert
from scrapers.shodan_scraper import ShodanScraper
import uuid

app = FastAPI(
    title="OSINT Platform API",
    description="API pour plateforme OSINT automatisée",
    version="1.0.0"
)

# Schemas Pydantic
class InvestigationCreate(BaseModel):
    name: str
    target_type: str
    target_value: str

class InvestigationResponse(BaseModel):
    id: uuid.UUID
    name: str
    target_type: str
    target_value: str
    status: str
    risk_score: float

    class Config:
        from_attributes = True

# Routes
@app.get("/")
def read_root():
    return {
        "message": "OSINT Platform API",
        "version": "1.0.0",
        "endpoints": ["/investigations", "/health"]
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/investigations", response_model=InvestigationResponse)
async def create_investigation(
    investigation: InvestigationCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Crée une nouvelle investigation"""
    new_inv = Investigation(
        name=investigation.name,
        target_type=investigation.target_type,
        target_value=investigation.target_value
    )
    db.add(new_inv)
    db.commit()
    db.refresh(new_inv)

    # Lancer scraping en background
    background_tasks.add_task(run_scrapers, new_inv.id, investigation.target_value, db)

    return new_inv

@app.get("/investigations", response_model=List[InvestigationResponse])
def list_investigations(db: Session = Depends(get_db)):
    """Liste toutes les investigations"""
    return db.query(Investigation).all()

@app.get("/investigations/{investigation_id}")
def get_investigation(investigation_id: uuid.UUID, db: Session = Depends(get_db)):
    """Récupère une investigation avec toutes ses données"""
    inv = db.query(Investigation).filter(Investigation.id == investigation_id).first()
    if not inv:
        raise HTTPException(status_code=404, detail="Investigation not found")

    data = db.query(CollectedData).filter(CollectedData.investigation_id == investigation_id).all()
    alerts = db.query(Alert).filter(Alert.investigation_id == investigation_id).all()

    return {
        "investigation": inv,
        "collected_data": [d.processed_data for d in data],
        "alerts": [
            {
                "severity": a.severity,
                "type": a.alert_type,
                "description": a.description
            }
            for a in alerts
        ]
    }

async def run_scrapers(investigation_id, target_value, db: Session):
    """Fonction background pour scraping"""
    scraper = ShodanScraper()
    result = await scraper.process(target_value)

    if result['status'] == 'success':
        data = result['data']

        collected = CollectedData(
            investigation_id=investigation_id,
            source='shodan',
            data_type='ip_scan',
            processed_data=data,
            risk_level='high' if data['risk_score'] > 70 else 'medium'
        )
        db.add(collected)

        inv = db.query(Investigation).filter(Investigation.id == investigation_id).first()
        inv.risk_score = data['risk_score']
        inv.status = 'completed'

        db.commit()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### Étape 4.2 : Lancer l'API

```bash
cd backend
uvicorn api.main:app --reload
```

Ouvrir http://localhost:8000/docs pour voir la doc interactive !

### Étape 4.3 : Tester l'API

```bash
# Créer une investigation
curl -X POST "http://localhost:8000/investigations" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Google DNS",
    "target_type": "ip",
    "target_value": "8.8.8.8"
  }'

# Lister les investigations
curl http://localhost:8000/investigations

# Voir les détails (remplacer ID)
curl http://localhost:8000/investigations/<ID>
```

---

## 🎯 Prochaines Étapes

Vous avez maintenant :
- ✅ Environnement configuré
- ✅ Premier scraper Shodan fonctionnel
- ✅ Base de données PostgreSQL
- ✅ API FastAPI opérationnelle

**Continuez avec :**
1. Ajouter d'autres scrapers (GitHub, WhoisXML)
2. Implémenter le module IA NLP
3. Créer le frontend Vue/React
4. Ajouter Celery pour tâches asynchrones

**Besoin d'aide ? Demandez-moi pour la phase suivante !**
