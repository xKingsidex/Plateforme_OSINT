"""
🔍 OSINT Intelligence Platform PRO - FastAPI Backend
Version professionnelle utilisant les vrais outils OSINT
- Sherlock (300+ sites)
- Holehe (120+ sites)
- Socialscan (vérification rapide)
- + API keys professionnelles
"""
import os
import re
import asyncio
from typing import List, Optional, Dict, Any
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scrapers import (
    EmailScraper, UsernameScraper, PhoneScraper, DomainScraper,
    SherlockScraper, HoleheScraper, SocialscanScraper
)

# Charger les variables d'environnement
load_dotenv()

# ═══════════════════════════════════════════════════════════════
# FASTAPI APP
# ═══════════════════════════════════════════════════════════════

app = FastAPI(
    title="🔍 OSINT Intelligence Platform PRO",
    description="Professional Grade OSINT with Sherlock, Holehe, and more",
    version="3.0.0-PRO",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
    query: str = Field(..., description="La cible OSINT")
    deep_search: bool = Field(default=False, description="Recherche approfondie (Sherlock + Holehe)")
    use_professional_tools: bool = Field(default=True, description="Utiliser Sherlock/Holehe")

class SearchResponse(BaseModel):
    query: str
    detected_types: List[str]
    results: Dict[str, Any]
    summary: Dict[str, Any]
    tools_used: List[str]

# ═══════════════════════════════════════════════════════════════
# SCRAPERS INSTANCES
# ═══════════════════════════════════════════════════════════════

email_scraper = EmailScraper()
username_scraper = UsernameScraper()
phone_scraper = PhoneScraper()
domain_scraper = DomainScraper()

# PROFESSIONAL TOOLS
sherlock_scraper = SherlockScraper()
holehe_scraper = HoleheScraper()
socialscan_scraper = SocialscanScraper()

# ═══════════════════════════════════════════════════════════════
# UTILITY FUNCTIONS
# ═══════════════════════════════════════════════════════════════

def detect_query_type(query: str) -> List[str]:
    """Détecte automatiquement le type de la requête"""
    types = []
    
    if re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', query):
        types.append('email')
        
    if re.match(r'^\+?[\d\s\-\(\)]{10,}$', query):
        types.append('phone')
        
    if re.match(r'^[a-zA-Z0-9][a-zA-Z0-9-]{0,61}[a-zA-Z0-9]?\.[a-zA-Z]{2,}$', query) and '@' not in query:
        types.append('domain')
        
    if not types:
        types.append('username')
        
    if ' ' in query:
        types.append('name')
    
    return types

async def perform_professional_osint(
    query: str, 
    search_types: List[str],
    deep_search: bool = False,
    use_professional_tools: bool = True
) -> tuple[Dict[str, Any], List[str]]:
    """
    Effectue une recherche OSINT PROFESSIONNELLE avec les vrais outils
    """
    results = {}
    tools_used = []
    
    # ═══ EMAIL OSINT ═══
    if 'email' in search_types:
        # API-based scraping
        results['email_basic'] = await email_scraper.scrape(query)
        tools_used.append('EmailScraper')
        
        # HOLEHE - Check sur 120+ sites (PRO)
        if use_professional_tools:
            results['email_holehe'] = await holehe_scraper.scrape(query)
            tools_used.append('Holehe (120+ sites)')
    
    # ═══ USERNAME OSINT ═══
    if 'username' in search_types:
        username = query.split('@')[0] if '@' in query else query
        
        # Basic API scraping
        results['username_basic'] = await username_scraper.scrape(username)
        tools_used.append('UsernameScraper')
        
        # SOCIALSCAN - Vérification rapide
        if use_professional_tools:
            results['username_socialscan'] = await socialscan_scraper.scrape(username)
            tools_used.append('Socialscan')
        
        # SHERLOCK - 300+ sites (SLOW mais complet)
        if deep_search and use_professional_tools:
            results['username_sherlock'] = await sherlock_scraper.scrape(username)
            tools_used.append('Sherlock (300+ sites)')
    
    # ═══ PHONE OSINT ═══
    if 'phone' in search_types:
        results['phone'] = await phone_scraper.scrape(query)
        tools_used.append('PhoneScraper')
    
    # ═══ DOMAIN OSINT ═══
    if 'domain' in search_types:
        domain = query.split('@')[1] if '@' in query else query
        results['domain'] = await domain_scraper.scrape(domain)
        tools_used.append('DomainScraper')
    
    return results, tools_used

def generate_summary(results: Dict[str, Any], tools_used: List[str]) -> Dict[str, Any]:
    """Génère un résumé PRO des résultats"""
    summary = {
        'total_sources': 0,
        'verified_emails': 0,
        'social_profiles_found': 0,
        'breaches_found': 0,
        'confidence_score': 0.0,
        'tools_used_count': len(tools_used),
        'sherlock_enabled': 'Sherlock' in str(tools_used),
        'holehe_enabled': 'Holehe' in str(tools_used)
    }
    
    # Compter les profils Sherlock
    if 'username_sherlock' in results:
        summary['social_profiles_found'] += results['username_sherlock'].get('total_found', 0)
    
    # Compter les comptes Holehe
    if 'email_holehe' in results:
        summary['verified_emails'] += results['email_holehe'].get('total_found', 0)
    
    # Compter les autres profils
    if 'username_basic' in results:
        summary['social_profiles_found'] += results['username_basic'].get('total_found', 0)
    
    if 'username_socialscan' in results:
        summary['social_profiles_found'] += results['username_socialscan'].get('total_found', 0)
    
    # Breaches
    if 'email_basic' in results:
        breaches = results['email_basic'].get('breaches', [])
        summary['breaches_found'] = len([b for b in breaches if 'error' not in b])
    
    # Score de confiance
    total_data_points = sum(1 for r in results.values() if isinstance(r, dict) and not r.get('error'))
    summary['confidence_score'] = total_data_points / max(len(results), 1)
    summary['total_sources'] = len(results)
    
    return summary

# ═══════════════════════════════════════════════════════════════
# API ENDPOINTS
# ═══════════════════════════════════════════════════════════════

@app.get("/")
async def root():
    """Page d'accueil de l'API PRO"""
    return {
        "message": "🔍 OSINT Intelligence Platform PRO",
        "version": "3.0.0-PRO",
        "status": "operational",
        "professional_tools": {
            "sherlock": "✅ 300+ sites",
            "holehe": "✅ 120+ sites",
            "socialscan": "✅ Fast check"
        },
        "docs": "/docs"
    }

@app.get("/api/health")
async def health_check():
    """Vérifie l'état de l'API PRO"""
    return {
        "status": "healthy",
        "version": "3.0.0-PRO",
        "scrapers": {
            "basic": "operational",
            "sherlock": "ready",
            "holehe": "ready",
            "socialscan": "ready"
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
        "professional_tools_available": True
    }

@app.post("/api/search", response_model=SearchResponse)
async def search(request: SearchRequest):
    """
    Effectue une recherche OSINT PROFESSIONNELLE
    
    - **query**: La cible (email, username, téléphone, domaine)
    - **deep_search**: Active Sherlock (300+ sites) - LENT
    - **use_professional_tools**: Utilise Holehe/Sherlock/Socialscan
    """
    query = request.query.strip()
    
    if not query:
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    
    # Détecter le type
    search_types = detect_query_type(query)
    
    # Effectuer la recherche PRO
    try:
        results, tools_used = await perform_professional_osint(
            query, 
            search_types,
            deep_search=request.deep_search,
            use_professional_tools=request.use_professional_tools
        )
        
        summary = generate_summary(results, tools_used)
        
        return SearchResponse(
            query=query,
            detected_types=search_types,
            results=results,
            summary=summary,
            tools_used=tools_used
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search error: {str(e)}")

# ═══════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import uvicorn
    
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    
    print("╔═══════════════════════════════════════════════════════════╗")
    print("║   🔍 OSINT INTELLIGENCE PLATFORM PRO v3.0.0              ║")
    print("║   Professional Grade avec Sherlock + Holehe + Socialscan║")
    print("╚═══════════════════════════════════════════════════════════╝")
    print(f"\n🚀 Server starting on http://{host}:{port}")
    print(f"📚 API Documentation: http://{host}:{port}/docs\n")
    print("✅ Professional Tools Enabled:")
    print("   - Sherlock (300+ sites)")
    print("   - Holehe (120+ sites)")
    print("   - Socialscan (fast check)\n")
    
    uvicorn.run(app, host=host, port=port)
