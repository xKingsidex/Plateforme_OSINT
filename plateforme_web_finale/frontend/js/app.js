/**
 * ═══════════════════════════════════════════════════════════════
 * OSINT Platform - Main Application
 * Logique principale de l'interface utilisateur
 * ═══════════════════════════════════════════════════════════════
 */

// État de l'application
let currentResults = null;

// ═══════════════════════════════════════════════════════════════
// INITIALISATION
// ═══════════════════════════════════════════════════════════════

document.addEventListener('DOMContentLoaded', () => {
    console.log('🔍 OSINT Platform - Initialized');

    // Vérifier la connexion à l'API
    checkAPIHealth();

    // Attacher les event listeners
    setupEventListeners();
});

/**
 * Vérifie que l'API backend est accessible
 */
async function checkAPIHealth() {
    try {
        await apiClient.healthCheck();
        console.log('✅ API Backend is healthy');
    } catch (error) {
        console.error('❌ API Backend is not reachable:', error);
        showError('Impossible de se connecter au backend. Assurez-vous que le serveur est démarré.');
    }
}

/**
 * Configure les event listeners
 */
function setupEventListeners() {
    const searchForm = document.getElementById('searchForm');
    const searchInput = document.getElementById('searchInput');

    // Soumission du formulaire
    searchForm.addEventListener('submit', handleSearch);

    // Détection automatique pendant la saisie (debounced)
    let detectTimeout;
    searchInput.addEventListener('input', (e) => {
        clearTimeout(detectTimeout);
        detectTimeout = setTimeout(() => {
            if (e.target.value.trim().length > 2) {
                detectInputType(e.target.value.trim());
            }
        }, 500);
    });
}

// ═══════════════════════════════════════════════════════════════
// RECHERCHE
// ═══════════════════════════════════════════════════════════════

/**
 * Gère la soumission du formulaire de recherche
 */
async function handleSearch(event) {
    event.preventDefault();

    const searchInput = document.getElementById('searchInput');
    const deepSearch = document.getElementById('deepSearch');
    const query = searchInput.value.trim();

    if (!query) {
        showError('Veuillez entrer une requête de recherche');
        return;
    }

    // Afficher le loading
    showLoading(true);
    hideResults();

    try {
        // Lancer la recherche
        console.log(`🔍 Searching for: ${query}`);
        const results = await apiClient.search(query, {
            deepSearch: deepSearch.checked
        });

        currentResults = results;

        // Afficher les résultats
        displayResults(results);

    } catch (error) {
        console.error('Search error:', error);
        showError(`Erreur lors de la recherche: ${error.message}`);
    } finally {
        showLoading(false);
    }
}

/**
 * Détecte le type d'input
 */
async function detectInputType(query) {
    try {
        const detection = await apiClient.detectInputType(query);
        displayDetection(detection);
    } catch (error) {
        console.error('Detection error:', error);
    }
}

// ═══════════════════════════════════════════════════════════════
// AFFICHAGE
// ═══════════════════════════════════════════════════════════════

/**
 * Affiche les informations de détection
 */
function displayDetection(detection) {
    const detectionInfo = document.getElementById('detectionInfo');
    const detectionTypes = document.getElementById('detectionTypes');
    const detectionSuggestions = document.getElementById('detectionSuggestions');

    if (detection.detected_types.length === 0) {
        detectionInfo.classList.add('hidden');
        return;
    }

    // Afficher les types détectés
    detectionTypes.innerHTML = detection.detected_types
        .map(type => `<span class="type-badge">${type}</span>`)
        .join('');

    // Afficher les suggestions
    if (detection.suggestions && detection.suggestions.length > 0) {
        detectionSuggestions.innerHTML = `
            <strong>Suggestions:</strong>
            <ul>
                ${detection.suggestions.map(s => `<li>${s}</li>`).join('')}
            </ul>
        `;
    } else {
        detectionSuggestions.innerHTML = '';
    }

    detectionInfo.classList.remove('hidden');
}

/**
 * Affiche les résultats de la recherche
 */
function displayResults(results) {
    const resultsSection = document.getElementById('resultsSection');

    // Afficher le résumé
    displaySummary(results.summary);

    // Afficher les résultats détaillés
    displayDetailedResults(results.results);

    // Afficher la section
    resultsSection.classList.remove('hidden');

    // Scroller vers les résultats
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

/**
 * Affiche le résumé des résultats
 */
function displaySummary(summary) {
    document.getElementById('totalSources').textContent = summary.total_sources || 0;
    document.getElementById('successfulSources').textContent = summary.successful || 0;
    document.getElementById('failedSources').textContent = summary.failed || 0;

    // Afficher les découvertes clés
    const keyFindings = document.getElementById('keyFindings');

    if (summary.key_findings && summary.key_findings.length > 0) {
        keyFindings.innerHTML = `
            <h3>🔑 Découvertes clés</h3>
            ${summary.key_findings.map(finding => `
                <div class="finding ${finding.type}">
                    <strong>${finding.source}:</strong> ${finding.message}
                </div>
            `).join('')}
        `;
    } else {
        keyFindings.innerHTML = '<p>Aucune découverte majeure</p>';
    }
}

/**
 * Affiche les résultats détaillés
 */
function displayDetailedResults(results) {
    const detailedResults = document.getElementById('detailedResults');

    if (!results.sources || Object.keys(results.sources).length === 0) {
        detailedResults.innerHTML = '<p>Aucun résultat trouvé</p>';
        return;
    }

    const html = Object.entries(results.sources)
        .map(([source, data]) => {
            const status = data.status === 'failed' ? '❌' : '✅';
            return `
                <div class="result-item">
                    <h3>${status} ${formatSourceName(source)}</h3>
                    <div class="result-data">
                        <pre>${JSON.stringify(data, null, 2)}</pre>
                    </div>
                </div>
            `;
        })
        .join('');

    detailedResults.innerHTML = html;
}

/**
 * Formate le nom d'une source
 */
function formatSourceName(source) {
    const names = {
        'hunter_verify': 'Hunter.io - Vérification Email',
        'hunter_find': 'Hunter.io - Recherche Email',
        'hibp': 'Have I Been Pwned',
        'github': 'GitHub',
        'virustotal': 'VirusTotal',
        'shodan': 'Shodan',
        'social_media': 'Réseaux Sociaux',
        'sherlock': 'Sherlock'
    };

    return names[source] || source.toUpperCase();
}

// ═══════════════════════════════════════════════════════════════
// UTILITAIRES UI
// ═══════════════════════════════════════════════════════════════

/**
 * Affiche/cache le loading
 */
function showLoading(show) {
    const loadingOverlay = document.getElementById('loadingOverlay');
    const searchBtn = document.getElementById('searchBtn');
    const btnText = document.getElementById('btnText');
    const btnLoader = document.getElementById('btnLoader');

    if (show) {
        loadingOverlay.classList.remove('hidden');
        searchBtn.disabled = true;
        btnText.classList.add('hidden');
        btnLoader.classList.remove('hidden');
    } else {
        loadingOverlay.classList.add('hidden');
        searchBtn.disabled = false;
        btnText.classList.remove('hidden');
        btnLoader.classList.add('hidden');
    }
}

/**
 * Cache les résultats
 */
function hideResults() {
    const resultsSection = document.getElementById('resultsSection');
    resultsSection.classList.add('hidden');
}

/**
 * Affiche une erreur
 */
function showError(message) {
    alert(`❌ Erreur: ${message}`);
}

// ═══════════════════════════════════════════════════════════════
// EXPORT
// ═══════════════════════════════════════════════════════════════

/**
 * Exporte les résultats en JSON
 */
function exportJSON() {
    if (!currentResults) {
        showError('Aucun résultat à exporter');
        return;
    }

    const dataStr = JSON.stringify(currentResults, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });

    const link = document.createElement('a');
    link.href = URL.createObjectURL(dataBlob);
    link.download = `osint_results_${Date.now()}.json`;
    link.click();
}

/**
 * Exporte les résultats en HTML
 */
function exportHTML() {
    if (!currentResults) {
        showError('Aucun résultat à exporter');
        return;
    }

    const html = `
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>OSINT Results - ${currentResults.query}</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 1200px; margin: 0 auto; padding: 20px; }
        h1 { color: #2563eb; }
        .summary { background: #f3f4f6; padding: 20px; border-radius: 8px; margin: 20px 0; }
        .result { background: white; border: 1px solid #e5e7eb; padding: 15px; margin: 10px 0; border-radius: 8px; }
        pre { background: #1f2937; color: #f3f4f6; padding: 15px; border-radius: 8px; overflow-x: auto; }
    </style>
</head>
<body>
    <h1>🔍 OSINT Results</h1>
    <div class="summary">
        <h2>Query: ${currentResults.query}</h2>
        <p>Types: ${currentResults.detected_types.join(', ')}</p>
        <p>Timestamp: ${currentResults.timestamp}</p>
    </div>
    <h2>Results</h2>
    ${Object.entries(currentResults.results.sources)
        .map(([source, data]) => `
            <div class="result">
                <h3>${formatSourceName(source)}</h3>
                <pre>${JSON.stringify(data, null, 2)}</pre>
            </div>
        `).join('')}
</body>
</html>
    `;

    const dataBlob = new Blob([html], { type: 'text/html' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(dataBlob);
    link.download = `osint_results_${Date.now()}.html`;
    link.click();
}
