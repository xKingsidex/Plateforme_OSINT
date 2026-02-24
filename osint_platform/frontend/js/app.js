/**
 * ═══════════════════════════════════════════════════════════════
 * OSINT Intelligence Platform - Frontend JavaScript
 * ═══════════════════════════════════════════════════════════════
 */

// Configuration
const API_BASE_URL = 'http://localhost:8000';

// État de l'application
let currentResults = null;

// ═══════════════════════════════════════════════════════════════
// INITIALIZATION
// ═══════════════════════════════════════════════════════════════

document.addEventListener('DOMContentLoaded', () => {
    console.log('🔍 OSINT Platform - Initialized');
    
    // Vérifier la connexion API
    checkAPIHealth();
    
    // Setup event listeners
    setupEventListeners();
});

/**
 * Vérifie l'état de l'API
 */
async function checkAPIHealth() {
    const statusEl = document.getElementById('apiStatus');
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/health`);
        const data = await response.json();
        
        if (data.status === 'healthy') {
            statusEl.classList.remove('disconnected');
            console.log('✅ API Connected');
        } else {
            statusEl.classList.add('disconnected');
        }
    } catch (error) {
        console.error('❌ API Connection Failed:', error);
        statusEl.classList.add('disconnected');
    }
}

/**
 * Configure les event listeners
 */
function setupEventListeners() {
    const searchForm = document.getElementById('searchForm');
    const searchInput = document.getElementById('searchInput');
    const copyBtn = document.getElementById('copyJsonBtn');
    
    // Formulaire de recherche
    searchForm.addEventListener('submit', handleSearch);
    
    // Auto-détection du type avec debounce
    let detectTimeout;
    searchInput.addEventListener('input', (e) => {
        clearTimeout(detectTimeout);
        detectTimeout = setTimeout(() => {
            const query = e.target.value.trim();
            if (query.length > 2) {
                detectType(query);
            } else {
                hideDetectionPanel();
            }
        }, 500);
    });
    
    // Copier le JSON
    if (copyBtn) {
        copyBtn.addEventListener('click', copyRawJSON);
    }
    
    // Enter pour soumettre
    searchInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            e.preventDefault();
            searchForm.dispatchEvent(new Event('submit'));
        }
    });
}

// ═══════════════════════════════════════════════════════════════
// DETECTION
// ═══════════════════════════════════════════════════════════════

/**
 * Détecte automatiquement le type de requête
 */
async function detectType(query) {
    try {
        const response = await fetch(`${API_BASE_URL}/api/detect`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query })
        });
        
        const data = await response.json();
        
        if (data.detected_types && data.detected_types.length > 0) {
            showDetectionPanel(data.detected_types);
        }
    } catch (error) {
        console.error('Detection error:', error);
    }
}

/**
 * Affiche le panneau de détection
 */
function showDetectionPanel(types) {
    const panel = document.getElementById('detectionPanel');
    const badgesContainer = document.getElementById('detectionBadges');
    
    badgesContainer.innerHTML = types.map(type => {
        const icons = {
            'email': '📧',
            'username': '👤',
            'phone': '📱',
            'domain': '🌐',
            'name': '👥'
        };
        
        return `<span class="badge badge-${type}">${icons[type] || '📌'} ${type.toUpperCase()}</span>`;
    }).join('');
    
    panel.classList.add('show');
}

/**
 * Cache le panneau de détection
 */
function hideDetectionPanel() {
    document.getElementById('detectionPanel').classList.remove('show');
}

// ═══════════════════════════════════════════════════════════════
// SEARCH
// ═══════════════════════════════════════════════════════════════

/**
 * Gère la soumission du formulaire de recherche
 */
async function handleSearch(event) {
    event.preventDefault();
    
    const searchInput = document.getElementById('searchInput');
    const searchBtn = document.getElementById('searchBtn');
    const deepSearch = document.getElementById('deepSearch').checked;
    
    const query = searchInput.value.trim();
    
    if (!query) {
        showError('Veuillez entrer une requête !');
        return;
    }
    
    // UI Loading State
    searchBtn.classList.add('loading');
    searchBtn.disabled = true;
    showLoading();
    hideError();
    hideResults();
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/search`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                query: query,
                deep_search: deepSearch
            })
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Erreur API');
        }
        
        const data = await response.json();
        currentResults = data;
        
        displayResults(data);
        
    } catch (error) {
        console.error('Search error:', error);
        showError(`Erreur: ${error.message}`);
    } finally {
        searchBtn.classList.remove('loading');
        searchBtn.disabled = false;
        hideLoading();
    }
}

// ═══════════════════════════════════════════════════════════════
// RESULTS DISPLAY
// ═══════════════════════════════════════════════════════════════

/**
 * Affiche les résultats
 */
function displayResults(data) {
    // Stats
    displayStats(data.summary);
    
    // Résultats par type
    if (data.results.email) {
        displayEmailResults(data.results.email);
    }
    
    if (data.results.username) {
        displayUsernameResults(data.results.username);
    }
    
    if (data.results.phone) {
        displayPhoneResults(data.results.phone);
    }
    
    if (data.results.domain) {
        displayDomainResults(data.results.domain);
    }
    
    // Raw JSON
    displayRawJSON(data);
    
    // Afficher la section résultats
    showResults();
}

/**
 * Affiche les statistiques
 */
function displayStats(summary) {
    const statsGrid = document.getElementById('statsGrid');
    
    const stats = [
        { icon: '📧', label: 'Emails Vérifiés', value: summary.verified_emails || 0 },
        { icon: '👥', label: 'Profils Sociaux', value: summary.social_profiles_found || 0 },
        { icon: '🚨', label: 'Fuites Détectées', value: summary.breaches_found || 0 },
        { icon: '🎯', label: 'Score Confiance', value: `${Math.round((summary.confidence_score || 0) * 100)}%` }
    ];
    
    statsGrid.innerHTML = stats.map(stat => `
        <div class="stat-card">
            <div class="stat-value">${stat.value}</div>
            <div class="stat-label">${stat.icon} ${stat.label}</div>
        </div>
    `).join('');
}

/**
 * Affiche les résultats email
 */
function displayEmailResults(data) {
    const card = document.getElementById('emailResults');
    const content = document.getElementById('emailContent');
    
    let html = `
        <p><strong>Email:</strong> ${data.email}</p>
        <p><strong>Valid:</strong> ${data.valid ? '✅ Oui' : '❌ Non'}</p>
        <p><strong>Domaine:</strong> ${data.domain || 'N/A'}</p>
    `;
    
    // Breaches
    if (data.breaches && data.breaches.length > 0) {
        html += '<h4 style="margin-top: 20px;">🚨 Fuites de données:</h4><ul>';
        data.breaches.forEach(breach => {
            if (!breach.error) {
                html += `<li><strong>${breach.name}</strong> (${breach.date}) - ${breach.data_classes.join(', ')}</li>`;
            }
        });
        html += '</ul>';
    }
    
    // Réputation
    if (data.reputation) {
        html += `<h4 style="margin-top: 20px;">📊 Réputation:</h4>`;
        html += `<p>Score: <strong>${data.reputation.reputation}</strong></p>`;
        html += `<p>Suspicious: ${data.reputation.suspicious ? '⚠️ Oui' : '✅ Non'}</p>`;
    }
    
    content.innerHTML = html;
    card.style.display = 'block';
}

/**
 * Affiche les résultats username
 */
function displayUsernameResults(data) {
    const card = document.getElementById('usernameResults');
    const content = document.getElementById('usernameContent');
    
    let html = `<p><strong>Username:</strong> ${data.username}</p>`;
    html += `<p><strong>Profils trouvés:</strong> ${data.total_found}</p>`;
    
    if (data.github && data.github.found) {
        html += '<h4 style="margin-top: 20px;">💻 GitHub:</h4>';
        html += `<p><strong>Nom:</strong> ${data.github.name || 'N/A'}</p>`;
        html += `<p><strong>Bio:</strong> ${data.github.bio || 'N/A'}</p>`;
        html += `<p><strong>Location:</strong> ${data.github.location || 'N/A'}</p>`;
        html += `<p><strong>Repos:</strong> ${data.github.public_repos || 0}</p>`;
        html += `<p><strong>Followers:</strong> ${data.github.followers || 0}</p>`;
        html += `<p><a href="${data.github.profile_url}" target="_blank" style="color: var(--primary-color);">Voir le profil →</a></p>`;
    }
    
    if (data.social_media && data.social_media.length > 0) {
        html += '<h4 style="margin-top: 20px;">🌐 Réseaux Sociaux:</h4><ul>';
        data.social_media.forEach(profile => {
            html += `<li><strong>${profile.platform}:</strong> <a href="${profile.url}" target="_blank" style="color: var(--primary-color);">${profile.url}</a></li>`;
        });
        html += '</ul>';
    }
    
    content.innerHTML = html;
    card.style.display = 'block';
}

/**
 * Affiche les résultats téléphone
 */
function displayPhoneResults(data) {
    const card = document.getElementById('phoneResults');
    const content = document.getElementById('phoneContent');
    
    let html = `
        <p><strong>Numéro:</strong> ${data.phone}</p>
        <p><strong>Formaté:</strong> ${data.clean_phone}</p>
    `;
    
    if (data.validation) {
        html += '<h4 style="margin-top: 20px;">✅ Validation:</h4>';
        html += `<p><strong>Valide:</strong> ${data.validation.valid ? '✅ Oui' : '❌ Non'}</p>`;
        if (data.validation.country) {
            html += `<p><strong>Pays:</strong> ${data.validation.country} (${data.validation.country_code})</p>`;
        }
        if (data.validation.carrier) {
            html += `<p><strong>Opérateur:</strong> ${data.validation.carrier}</p>`;
        }
        if (data.validation.line_type) {
            html += `<p><strong>Type:</strong> ${data.validation.line_type}</p>`;
        }
    }
    
    content.innerHTML = html;
    card.style.display = 'block';
}

/**
 * Affiche les résultats domaine
 */
function displayDomainResults(data) {
    const card = document.getElementById('domainResults');
    const content = document.getElementById('domainContent');
    
    let html = `<p><strong>Domaine:</strong> ${data.domain}</p>`;
    
    if (data.dns && data.dns.records) {
        html += '<h4 style="margin-top: 20px;">🌐 DNS Records:</h4>';
        html += `<pre>${JSON.stringify(data.dns.records, null, 2)}</pre>`;
    }
    
    if (data.virustotal) {
        html += '<h4 style="margin-top: 20px;">🛡️ VirusTotal:</h4>';
        html += `<p>Malicious: ${data.virustotal.malicious || 0}</p>`;
        html += `<p>Suspicious: ${data.virustotal.suspicious || 0}</p>`;
        html += `<p>Clean: ${data.virustotal.clean || 0}</p>`;
    }
    
    content.innerHTML = html;
    card.style.display = 'block';
}

/**
 * Affiche le JSON brut
 */
function displayRawJSON(data) {
    const pre = document.getElementById('rawJsonData');
    pre.textContent = JSON.stringify(data, null, 2);
}

/**
 * Copie le JSON dans le presse-papiers
 */
function copyRawJSON() {
    if (!currentResults) return;
    
    const text = JSON.stringify(currentResults, null, 2);
    navigator.clipboard.writeText(text).then(() => {
        alert('✅ JSON copié dans le presse-papiers !');
    }).catch(err => {
        console.error('Copy error:', err);
    });
}

// ═══════════════════════════════════════════════════════════════
// UI HELPERS
// ═══════════════════════════════════════════════════════════════

function showLoading() {
    document.getElementById('loadingSection').classList.add('show');
}

function hideLoading() {
    document.getElementById('loadingSection').classList.remove('show');
}

function showResults() {
    document.getElementById('resultsSection').classList.add('show');
}

function hideResults() {
    document.getElementById('resultsSection').classList.remove('show');
}

function showError(message) {
    const errorEl = document.getElementById('errorMessage');
    const errorText = document.getElementById('errorText');
    errorText.textContent = message;
    errorEl.classList.add('show');
}

function hideError() {
    document.getElementById('errorMessage').classList.remove('show');
}
