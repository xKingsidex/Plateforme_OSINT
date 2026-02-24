"""
🔍 OSINT Intelligence Platform - FastAPI Backend
API professionnelle pour recherches OSINT complètes
"""
import os
import re
from typing import List, Optional, Dict, Any
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scrapers import EmailScraper, UsernameScraper, PhoneScraper, DomainScraper

# Charger les variables d'environnement
load_dotenv()

# ═══════════════════════════════════════════════════════════════
# FASTAPI APP
# ═══════════════════════════════════════════════════════════════

app = FastAPI(
    title="🔍 OSINT Intelligence Platform",
    description="Professional Grade OSINT Intelligence Gathering API",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En production: spécifier les domaines autorisés
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ═══════════════════════════════════════════════════════════════
# MODELS
# ═══════════════════════════════════════════════════════════════

class DetectionRequest(BaseModel):
    query: str = Field(..., description="La requête à analyser")

class SearchRequest(BaseModel):
    query: str = Field(..., description="La cible OSINT (email, nom, username, etc.)")
    search_types: Optional[List[str]] = Field(default=None, description="Types de recherche spécifiques")
    deep_search: bool = Field(default=False, description="Recherche approfondie (plus lent)")

class SearchResponse(BaseModel):
    query: str
    detected_types: List[str]
    results: Dict[str, Any]
    summary: Dict[str, Any]

# ═══════════════════════════════════════════════════════════════
# SCRAPERS INSTANCES
# ═══════════════════════════════════════════════════════════════

email_scraper = EmailScraper()
username_scraper = UsernameScraper()
phone_scraper = PhoneScraper()
domain_scraper = DomainScraper()

# ═══════════════════════════════════════════════════════════════
# UTILITY FUNCTIONS
# ═══════════════════════════════════════════════════════════════

def detect_query_type(query: str) -> List[str]:
    """Détecte automatiquement le type de la requête"""
    types = []
    
    # Email
    if re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', query):
        types.append('email')
        
    # Téléphone (format international ou français)
    if re.match(r'^\+?[\d\s\-\(\)]{10,}$', query):
        types.append('phone')
        
    # Domaine
    if re.match(r'^[a-zA-Z0-9][a-zA-Z0-9-]{0,61}[a-zA-Z0-9]?\.[a-zA-Z]{2,}$', query) and '@' not in query:
        types.append('domain')
        
    # Username (si rien d'autre ne correspond)
    if not types:
        types.append('username')
        
    # Nom complet (si contient un espace)
    if ' ' in query:
        types.append('name')
    
    return types

async def perform_osint_search(query: str, search_types: List[str]) -> Dict[str, Any]:
    """Effectue la recherche OSINT selon les types détectés"""
    results = {}
    
    if 'email' in search_types:
        results['email'] = await email_scraper.scrape(query)
        
    if 'username' in search_types:
        # Extraire le username si c'est un email
        username = query.split('@')[0] if '@' in query else query
        results['username'] = await username_scraper.scrape(username)
        
    if 'phone' in search_types:
        results['phone'] = await phone_scraper.scrape(query)
        
    if 'domain' in search_types:
        domain = query.split('@')[1] if '@' in query else query
        results['domain'] = await domain_scraper.scrape(domain)
    
    return results

def generate_summary(results: Dict[str, Any]) -> Dict[str, Any]:
    """Génère un résumé des résultats"""
    summary = {
        'total_sources': 0,
        'verified_emails': 0,
        'social_profiles_found': 0,
        'breaches_found': 0,
        'confidence_score': 0.0
    }
    
    # Email
    if 'email' in results:
        email_data = results['email']
        if email_data.get('valid'):
            summary['verified_emails'] = 1
        breaches = email_data.get('breaches', [])
        summary['breaches_found'] = len([b for b in breaches if 'error' not in b])
        
    # Username/Social
    if 'username' in results:
        username_data = results['username']
        summary['social_profiles_found'] = username_data.get('total_found', 0)
        
    # Calcul du score de confiance
    total_data_points = 0
    valid_data_points = 0
    
    for key, data in results.items():
        if isinstance(data, dict):
            total_data_points += len(data)
            valid_data_points += sum(1 for v in data.values() if v and v != 'unknown')
    
    if total_data_points > 0:
        summary['confidence_score'] = valid_data_points / total_data_points
    
    summary['total_sources'] = len(results)
    
    return summary

# ═══════════════════════════════════════════════════════════════
# API ENDPOINTS
# ═══════════════════════════════════════════════════════════════

@app.get("/")
async def root():
    """Page d'accueil de l'API"""
    return {
        "message": "🔍 OSINT Intelligence Platform API",
        "version": "2.0.0",
        "status": "operational",
        "docs": "/docs",
        "endpoints": {
            "health": "/api/health",
            "detect": "/api/detect",
            "search": "/api/search"
        }
    }

@app.get("/api/health")
async def health_check():
    """Vérifie l'état de l'API"""
    return {
        "status": "healthy",
        "version": "2.0.0",
        "scrapers": {
            "email": "operational",
            "username": "operational",
            "phone": "operational",
            "domain": "operational"
        }
    }

@app.post("/api/detect")
async def detect_type(request: DetectionRequest):
    """Détecte automatiquement le type de requête"""
    query = request.query.strip()
    
    if not query:
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    
    detected_types = detect_query_type(query)
    
    return {
        "query": query,
        "detected_types": detected_types,
        "suggestions": {
            "email": "email" in detected_types,
            "username": "username" in detected_types,
            "phone": "phone" in detected_types,
            "domain": "domain" in detected_types,
            "name": "name" in detected_types
        }
    }

@app.post("/api/search", response_model=SearchResponse)
async def search(request: SearchRequest):
    """
    Effectue une recherche OSINT complète
    
    - **query**: La cible à rechercher (email, username, téléphone, domaine)
    - **search_types**: Types de recherche spécifiques (optionnel)
    - **deep_search**: Recherche approfondie sur 300+ sites (plus lent)
    """
    query = request.query.strip()
    
    if not query:
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    
    # Détecter le type si non spécifié
    search_types = request.search_types or detect_query_type(query)
    
    # Effectuer la recherche
    try:
        results = await perform_osint_search(query, search_types)
        summary = generate_summary(results)
        
        return SearchResponse(
            query=query,
            detected_types=search_types,
            results=results,
            summary=summary
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search error: {str(e)}")

@app.get("/api/stats")
async def get_stats():
    """Statistiques de la plateforme"""
    return {
        "total_searches": 0,  # À implémenter avec une DB
        "scrapers_available": 4,
        "api_keys_configured": sum([
            bool(os.getenv('HIBP_API_KEY')),
            bool(os.getenv('HUNTER_IO_KEY')),
            bool(os.getenv('NUMVERIFY_API_KEY')),
            bool(os.getenv('VIRUSTOTAL_API_KEY')),
            bool(os.getenv('GITHUB_TOKEN')),
        ]),
        "version": "2.0.0"
    }

# ═══════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import uvicorn
    
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    
    print("╔═══════════════════════════════════════════════════════════╗")
    print("║   🔍 OSINT INTELLIGENCE PLATFORM - BACKEND API           ║")
    print("╚═══════════════════════════════════════════════════════════╝")
    print(f"\n🚀 Server starting on http://{host}:{port}")
    print(f"📚 API Documentation: http://{host}:{port}/docs")
    print(f"🔄 Alternative Docs: http://{host}:{port}/redoc\n")
    
    uvicorn.run(app, host=host, port=port)
