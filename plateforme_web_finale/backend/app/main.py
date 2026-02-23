#!/usr/bin/env python3
"""
🔥 OSINT Platform - FastAPI Backend
Main application entry point
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, Dict, List
import uvicorn
from datetime import datetime

from app.services.detector import InputDetector
from app.services.aggregator import OSINTAggregator

# ═══════════════════════════════════════════════════════════════
# FASTAPI APP
# ═══════════════════════════════════════════════════════════════

app = FastAPI(
    title="OSINT Platform API",
    description="Plateforme d'automatisation OSINT - Recherche sur email, téléphone, nom, username, IP, domaine",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS - Permettre les requêtes depuis le frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En production, spécifier les domaines autorisés
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ═══════════════════════════════════════════════════════════════
# MODELS PYDANTIC
# ═══════════════════════════════════════════════════════════════

class SearchRequest(BaseModel):
    """Requête de recherche OSINT"""
    query: str
    search_types: Optional[List[str]] = None  # ['email', 'social', 'github', etc.]
    deep_search: bool = False  # Active Sherlock et recherches approfondies


class SearchResponse(BaseModel):
    """Réponse de recherche OSINT"""
    query: str
    detected_types: List[str]
    timestamp: str
    results: Dict
    summary: Dict


# ═══════════════════════════════════════════════════════════════
# ROUTES
# ═══════════════════════════════════════════════════════════════

@app.get("/")
async def root():
    """Page d'accueil de l'API"""
    return {
        "name": "OSINT Platform API",
        "version": "1.0.0",
        "status": "online",
        "timestamp": datetime.now().isoformat(),
        "endpoints": {
            "search": "/api/search",
            "detect": "/api/detect",
            "health": "/api/health",
            "docs": "/api/docs"
        }
    }


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }


@app.post("/api/detect")
async def detect_input_type(request: SearchRequest):
    """
    Détecte automatiquement le type d'input
    (email, phone, name, username, IP, domain)
    """
    try:
        detector = InputDetector()
        result = detector.detect(request.query)

        return {
            "query": request.query,
            "detected_types": result["types"],
            "confidence": result.get("confidence", {}),
            "suggestions": result.get("suggestions", [])
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/search", response_model=SearchResponse)
async def search_osint(request: SearchRequest):
    """
    Lance une recherche OSINT complète

    Détecte automatiquement le type d'input et lance toutes les recherches pertinentes :
    - Email → Hunter.io, HIBP, validation
    - Téléphone → NumVerify, recherche opérateur
    - Nom → Recherche sociale, Google Dorks
    - Username → 30+ plateformes, Sherlock (si deep_search=True)
    - IP → Shodan, géolocalisation
    - Domaine → VirusTotal, WHOIS, DNS
    """
    try:
        # 1. Détecter le type d'input
        detector = InputDetector()
        detection = detector.detect(request.query)

        # 2. Lancer les recherches
        aggregator = OSINTAggregator()
        results = await aggregator.search(
            query=request.query,
            detected_types=detection["types"],
            search_types=request.search_types,
            deep_search=request.deep_search
        )

        # 3. Générer un résumé
        summary = aggregator.generate_summary(results)

        return SearchResponse(
            query=request.query,
            detected_types=detection["types"],
            timestamp=datetime.now().isoformat(),
            results=results,
            summary=summary
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la recherche: {str(e)}")


@app.get("/api/search/history")
async def get_search_history(limit: int = 10):
    """Récupère l'historique des recherches (à implémenter avec DB)"""
    # TODO: Implémenter avec PostgreSQL
    return {
        "message": "Historique non encore implémenté",
        "limit": limit
    }


# ═══════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("🚀 Démarrage de l'OSINT Platform API...")
    print("📡 API disponible sur: http://localhost:8000")
    print("📚 Documentation: http://localhost:8000/api/docs")

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
