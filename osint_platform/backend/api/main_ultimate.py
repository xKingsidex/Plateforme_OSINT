"""
🔍 OSINT Intelligence Platform ULTIMATE - FastAPI Backend
Version ULTIME utilisant TOUS les outils OSINT open source

OUTILS INTÉGRÉS:
✅ Sherlock (300+ sites)
✅ Maigret (400+ sites - meilleur que Sherlock)  
✅ Holehe (120+ sites email)
✅ h8mail (breach hunting)
✅ Socialscan (vérification rapide)
✅ theHarvester (email harvesting)
✅ Sublist3r (subdomain enumeration)
✅ + API keys professionnelles (Hunter, VirusTotal, Shodan, GitHub)
"""
import os
import re
import asyncio
from typing import List, Optional, Dict, Any
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scrapers import (
    EmailScraper, UsernameScraper, PhoneScraper, DomainScraper,
    SherlockScraper, HoleheScraper, SocialscanScraper,
    MaigretScraper, TheHarvesterScraper, H8mailScraper, Sublist3rScraper
)

# Charger les variables d'environnement
load_dotenv()

# ═══════════════════════════════════════════════════════════════
# FASTAPI APP
# ═══════════════════════════════════════════════════════════════

app = FastAPI(
    title="🔍 OSINT Intelligence Platform ULTIMATE",
    description="Maximum OSINT avec TOUS les outils open source",
    version="4.0.0-ULTIMATE",
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
    deep_search: bool = Field(default=False, description="Sherlock + Maigret (TRÈS LENT)")
    ultra_deep: bool = Field(default=False, description="TOUS les outils (MAXIMUM)")
    use_professional_tools: bool = Field(default=True, description="Utiliser tous les outils")

class SearchResponse(BaseModel):
    query: str
    detected_types: List[str]
    results: Dict[str, Any]
    summary: Dict[str, Any]
    tools_used: List[str]

# ═══════════════════════════════════════════════════════════════
# SCRAPERS INSTANCES - TOUS LES OUTILS
# ═══════════════════════════════════════════════════════════════

# Basic scrapers
email_scraper = EmailScraper()
username_scraper = UsernameScraper()
phone_scraper = PhoneScraper()
domain_scraper = DomainScraper()

# Username OSINT - 3 tools
sherlock_scraper = SherlockScraper()      # 300+ sites
maigret_scraper = MaigretScraper()        # 400+ sites (meilleur)
socialscan_scraper = SocialscanScraper()  # Rapide

# Email OSINT - 2 tools
holehe_scraper = HoleheScraper()          # 120+ sites
h8mail_scraper = H8mailScraper()          # Breach hunting

# Domain OSINT - 2 tools
theharvester_scraper = TheHarvesterScraper()  # Email harvesting
sublist3r_scraper = Sublist3rScraper()        # Subdomain enum

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

async def perform_ultimate_osint(
    query: str, 
    search_types: List[str],
    deep_search: bool = False,
    ultra_deep: bool = False,
    use_professional_tools: bool = True
) -> tuple[Dict[str, Any], List[str]]:
    """
    Effectue une recherche OSINT ULTIME avec TOUS les outils
    """
    results = {}
    tools_used = []
    
    # ═══ EMAIL OSINT ═══
    if 'email' in search_types:
        # API-based scraping
        results['email_basic'] = await email_scraper.scrape(query)
        tools_used.append('EmailScraper (API)')
        
        if use_professional_tools:
            # HOLEHE - 120+ sites
            results['email_holehe'] = await holehe_scraper.scrape(query)
            tools_used.append('Holehe (120+ sites)')
            
            # H8MAIL - Breach hunting
            if ultra_deep:
                results['email_h8mail'] = await h8mail_scraper.scrape(query)
                tools_used.append('h8mail (Breach Hunting)')
    
    # ═══ USERNAME OSINT ═══
    if 'username' in search_types:
        username = query.split('@')[0] if '@' in query else query
        
        # Basic API scraping
        results['username_basic'] = await username_scraper.scrape(username)
        tools_used.append('UsernameScraper (API)')
        
        if use_professional_tools:
            # SOCIALSCAN - Rapide
            results['username_socialscan'] = await socialscan_scraper.scrape(username)
            tools_used.append('Socialscan (Fast)')
            
            # SHERLOCK - 300+ sites (LENT)
            if deep_search:
                results['username_sherlock'] = await sherlock_scraper.scrape(username)
                tools_used.append('Sherlock (300+ sites)')
            
            # MAIGRET - 400+ sites (ULTRA LENT mais meilleur)
            if ultra_deep:
                results['username_maigret'] = await maigret_scraper.scrape(username)
                tools_used.append('Maigret (400+ sites - ULTIMATE)')
    
    # ═══ PHONE OSINT ═══
    if 'phone' in search_types:
        results['phone'] = await phone_scraper.scrape(query)
        tools_used.append('PhoneScraper')
    
    # ═══ DOMAIN OSINT ═══
    if 'domain' in search_types:
        domain = query.split('@')[1] if '@' in query else query
        
        # Basic domain scraping
        results['domain_basic'] = await domain_scraper.scrape(domain)
        tools_used.append('DomainScraper (API)')
        
        if use_professional_tools:
            # SUBLIST3R - Subdomain enumeration
            results['domain_sublist3r'] = await sublist3r_scraper.scrape(domain)
            tools_used.append('Sublist3r (Subdomains)')
            
            # THEHARVESTER - Email harvesting
            if deep_search or ultra_deep:
                results['domain_harvester'] = await theharvester_scraper.scrape(domain)
                tools_used.append('theHarvester (Email Harvesting)')
    
    return results, tools_used

def generate_summary(results: Dict[str, Any], tools_used: List[str]) -> Dict[str, Any]:
    """Génère un résumé ULTIMATE des résultats"""
    summary = {
        'total_sources': 0,
        'verified_emails': 0,
        'social_profiles_found': 0,
        'breaches_found': 0,
        'subdomains_found': 0,
        'emails_harvested': 0,
        'confidence_score': 0.0,
        'tools_used_count': len(tools_used),
        'ultimate_mode': 'Maigret' in str(tools_used) or 'h8mail' in str(tools_used)
    }
    
    # Compter les profils (Sherlock, Maigret, Socialscan)
    for key in ['username_sherlock', 'username_maigret', 'username_basic', 'username_socialscan']:
        if key in results:
            summary['social_profiles_found'] += results[key].get('total_found', 0)
    
    # Compter les emails (Holehe, theHarvester)
    if 'email_holehe' in results:
        summary['verified_emails'] += results['email_holehe'].get('total_found', 0)
    
    if 'domain_harvester' in results:
        summary['emails_harvested'] = len(results['domain_harvester'].get('emails', []))
    
    # Compter les breaches
    if 'email_basic' in results:
        breaches = results['email_basic'].get('breaches', [])
        summary['breaches_found'] = len([b for b in breaches if 'error' not in b])
    
    if 'email_h8mail' in results:
        summary['breaches_found'] += results['email_h8mail'].get('total_breaches', 0)
    
    # Compter les subdomains
    if 'domain_sublist3r' in results:
        summary['subdomains_found'] = results['domain_sublist3r'].get('total_found', 0)
    
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
    """Page d'accueil de l'API ULTIMATE"""
    return {
        "message": "🔍 OSINT Intelligence Platform ULTIMATE",
        "version": "4.0.0-ULTIMATE",
        "status": "operational",
        "ultimate_tools": {
            "username_osint": "Sherlock (300+) + Maigret (400+) + Socialscan",
            "email_osint": "Holehe (120+) + h8mail + HaveIBeenPwned",
            "domain_osint": "Sublist3r + theHarvester + VirusTotal",
            "total_sites": "800+ sites couverts"
        },
        "docs": "/docs"
    }

@app.get("/api/health")
async def health_check():
    """Vérifie l'état de l'API ULTIMATE"""
    return {
        "status": "healthy",
        "version": "4.0.0-ULTIMATE",
        "tools_available": {
            "sherlock": "ready",
            "maigret": "ready",
            "holehe": "ready",
            "h8mail": "ready",
            "socialscan": "ready",
            "theharvester": "ready",
            "sublist3r": "ready"
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
        "ultimate_tools_available": True,
        "max_coverage": "800+ sites"
    }

@app.post("/api/search", response_model=SearchResponse)
async def search(request: SearchRequest):
    """
    Effectue une recherche OSINT ULTIMATE avec TOUS les outils
    
    - **query**: La cible (email, username, téléphone, domaine)
    - **deep_search**: Active Sherlock (300+ sites) + theHarvester - LENT (2-3 min)
    - **ultra_deep**: Active Maigret (400+ sites) + h8mail - TRÈS LENT (5-10 min)
    - **use_professional_tools**: Utilise TOUS les outils disponibles
    """
    query = request.query.strip()
    
    if not query:
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    
    # Détecter le type
    search_types = detect_query_type(query)
    
    # Effectuer la recherche ULTIMATE
    try:
        results, tools_used = await perform_ultimate_osint(
            query, 
            search_types,
            deep_search=request.deep_search,
            ultra_deep=request.ultra_deep,
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
    print("║   🔍 OSINT INTELLIGENCE PLATFORM ULTIMATE v4.0.0         ║")
    print("║   Maximum OSINT avec TOUS les outils open source         ║")
    print("╚═══════════════════════════════════════════════════════════╝")
    print(f"\n🚀 Server starting on http://{host}:{port}")
    print(f"📚 API Documentation: http://{host}:{port}/docs\n")
    print("✅ ULTIMATE Tools Enabled:")
    print("   📛 USERNAME: Sherlock (300+) + Maigret (400+) + Socialscan")
    print("   📧 EMAIL: Holehe (120+) + h8mail + HaveIBeenPwned")
    print("   🌐 DOMAIN: Sublist3r + theHarvester + VirusTotal")
    print("   📱 PHONE: Numverify + Phoneinfoga")
    print("\n🎯 TOTAL COVERAGE: 800+ sites web\n")
    print("⚠️  Deep Search: 2-3 minutes")
    print("⚠️  Ultra Deep: 5-10 minutes (Maigret + h8mail)\n")
    
    uvicorn.run(app, host=host, port=port)
