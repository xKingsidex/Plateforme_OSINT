/**
 * ═══════════════════════════════════════════════════════════════
 * OSINT Platform - API Client
 * Gère toutes les communications avec le backend
 * ═══════════════════════════════════════════════════════════════
 */

// Configuration de l'API
const API_CONFIG = {
    baseURL: window.location.hostname === 'localhost'
        ? 'http://localhost:8000'
        : 'http://backend:8000',
    timeout: 120000 // 2 minutes
};

/**
 * Client API pour la plateforme OSINT
 */
class OSINTAPIClient {
    constructor(baseURL = API_CONFIG.baseURL) {
        this.baseURL = baseURL;
    }

    /**
     * Effectue une requête HTTP
     */
    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        const config = {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        };

        try {
            const response = await fetch(url, config);

            if (!response.ok) {
                const error = await response.json().catch(() => ({}));
                throw new Error(error.detail || `HTTP ${response.status}: ${response.statusText}`);
            }

            return await response.json();
        } catch (error) {
            console.error('API Request Error:', error);
            throw error;
        }
    }

    /**
     * GET request
     */
    async get(endpoint) {
        return this.request(endpoint, { method: 'GET' });
    }

    /**
     * POST request
     */
    async post(endpoint, data) {
        return this.request(endpoint, {
            method: 'POST',
            body: JSON.stringify(data)
        });
    }

    /**
     * Vérifie le statut de l'API
     */
    async healthCheck() {
        return this.get('/api/health');
    }

    /**
     * Détecte le type d'input
     */
    async detectInputType(query) {
        return this.post('/api/detect', { query });
    }

    /**
     * Lance une recherche OSINT
     */
    async search(query, options = {}) {
        const payload = {
            query,
            search_types: options.searchTypes || null,
            deep_search: options.deepSearch || false
        };

        return this.post('/api/search', payload);
    }

    /**
     * Récupère l'historique des recherches
     */
    async getSearchHistory(limit = 10) {
        return this.get(`/api/search/history?limit=${limit}`);
    }
}

// Instance globale du client API
const apiClient = new OSINTAPIClient();
