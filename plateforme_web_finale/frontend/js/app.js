/**
 * ═══════════════════════════════════════════════════════════════
 * OSINT INTELLIGENCE PLATFORM - Main Application
 * Enhanced UI Logic with Toast Notifications
 * ═══════════════════════════════════════════════════════════════
 */

// Application state
let currentResults = null;

// ═══════════════════════════════════════════════════════════════
// INITIALIZATION
// ═══════════════════════════════════════════════════════════════

document.addEventListener('DOMContentLoaded', () => {
    console.log('🎯 OSINT Intelligence Platform - Initialized');

    // Check API health
    checkAPIHealth();

    // Setup event listeners
    setupEventListeners();

    // Initialize tooltips and animations
    initializeUI();
});

/**
 * Check if API backend is reachable
 */
async function checkAPIHealth() {
    try {
        await apiClient.healthCheck();
        console.log('✅ API Backend is healthy');
        showToast('API Backend Connected', 'success');
    } catch (error) {
        console.error('❌ API Backend is not reachable:', error);
        showToast('API Backend Connection Failed', 'error');
    }
}

/**
 * Setup all event listeners
 */
function setupEventListeners() {
    const searchForm = document.getElementById('searchForm');
    const searchInput = document.getElementById('searchInput');

    // Form submission
    searchForm.addEventListener('submit', handleSearch);

    // Auto-detection with debounce
    let detectTimeout;
    searchInput.addEventListener('input', (e) => {
        clearTimeout(detectTimeout);
        detectTimeout = setTimeout(() => {
            if (e.target.value.trim().length > 2) {
                detectInputType(e.target.value.trim());
            } else {
                // Hide detection panel if input is too short
                document.getElementById('detectionInfo').classList.add('hidden');
            }
        }, 500);
    });

    // Enhanced input effects
    searchInput.addEventListener('focus', () => {
        searchInput.parentElement.classList.add('focused');
    });

    searchInput.addEventListener('blur', () => {
        searchInput.parentElement.classList.remove('focused');
    });
}

/**
 * Initialize UI enhancements
 */
function initializeUI() {
    // Add smooth scroll behavior
    document.documentElement.style.scrollBehavior = 'smooth';

    // Add keyboard shortcuts
    document.addEventListener('keydown', (e) => {
        // Ctrl/Cmd + K to focus search
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            document.getElementById('searchInput').focus();
        }
    });
}

// ═══════════════════════════════════════════════════════════════
// SEARCH FUNCTIONALITY
// ═══════════════════════════════════════════════════════════════

/**
 * Handle search form submission
 */
async function handleSearch(event) {
    event.preventDefault();

    const searchInput = document.getElementById('searchInput');
    const deepSearch = document.getElementById('deepSearch');
    const query = searchInput.value.trim();

    if (!query) {
        showToast('Please enter a search query', 'warning');
        return;
    }

    // Show loading state
    showLoading(true);
    hideResults();

    try {
        console.log(`🔍 Executing search for: ${query}`);

        const results = await apiClient.search(query, {
            deepSearch: deepSearch.checked
        });

        currentResults = results;

        // Display results
        displayResults(results);
        showToast('Search completed successfully', 'success');

    } catch (error) {
        console.error('Search error:', error);
        showToast(`Search failed: ${error.message}`, 'error');
    } finally {
        showLoading(false);
    }
}

/**
 * Detect input type automatically
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
// DISPLAY FUNCTIONS
// ═══════════════════════════════════════════════════════════════

/**
 * Display detection information
 */
function displayDetection(detection) {
    const detectionInfo = document.getElementById('detectionInfo');
    const detectionTypes = document.getElementById('detectionTypes');
    const detectionSuggestions = document.getElementById('detectionSuggestions');

    if (detection.detected_types.length === 0) {
        detectionInfo.classList.add('hidden');
        return;
    }

    // Display detected types
    detectionTypes.innerHTML = detection.detected_types
        .map(type => `<span class="type-badge">${formatTypeName(type)}</span>`)
        .join('');

    // Display suggestions
    if (detection.suggestions && detection.suggestions.length > 0) {
        detectionSuggestions.innerHTML = `
            <strong>Recommended searches:</strong>
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
 * Display search results
 */
function displayResults(results) {
    const resultsSection = document.getElementById('resultsSection');

    // Display summary stats
    displaySummary(results.summary);

    // Display key findings
    displayKeyFindings(results.summary);

    // Display detailed results
    displayDetailedResults(results.results);

    // Show results section
    resultsSection.classList.remove('hidden');

    // Smooth scroll to results
    setTimeout(() => {
        resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }, 100);
}

/**
 * Display summary statistics
 */
function displaySummary(summary) {
    document.getElementById('totalSources').textContent = summary.total_sources || 0;
    document.getElementById('successfulSources').textContent = summary.successful || 0;
    document.getElementById('failedSources').textContent = summary.failed || 0;

    // Animate numbers
    animateValue('totalSources', 0, summary.total_sources || 0, 1000);
    animateValue('successfulSources', 0, summary.successful || 0, 1000);
    animateValue('failedSources', 0, summary.failed || 0, 1000);
}

/**
 * Display key findings
 */
function displayKeyFindings(summary) {
    const keyFindings = document.getElementById('keyFindings');

    if (summary.key_findings && summary.key_findings.length > 0) {
        keyFindings.innerHTML = summary.key_findings.map((finding, index) => `
            <div class="finding ${finding.type}" style="animation-delay: ${index * 0.1}s">
                <strong>${formatSourceName(finding.source)}:</strong> ${finding.message}
            </div>
        `).join('');
    } else {
        keyFindings.innerHTML = '';
    }
}

/**
 * Display detailed results
 */
function displayDetailedResults(results) {
    const detailedResults = document.getElementById('detailedResults');

    if (!results.sources || Object.keys(results.sources).length === 0) {
        detailedResults.innerHTML = `
            <div style="text-align: center; padding: 2rem; color: var(--text-secondary);">
                <svg style="width: 64px; height: 64px; margin-bottom: 1rem; opacity: 0.5;" viewBox="0 0 24 24" fill="none">
                    <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2"/>
                    <path d="M12 8V12M12 16H12.01" stroke="currentColor" stroke-width="2"/>
                </svg>
                <p>No results found for this query</p>
            </div>
        `;
        return;
    }

    const html = Object.entries(results.sources)
        .map(([source, data]) => {
            const status = data.status === 'failed' ? '❌' : '✅';
            const statusClass = data.status === 'failed' ? 'status-failed' : 'status-success';

            return `
                <div class="result-item ${statusClass}">
                    <h3>${status} ${formatSourceName(source)}</h3>
                    ${data.status === 'failed' && data.error ? `
                        <p style="color: var(--cyber-error); margin: 0.5rem 0;">${data.error}</p>
                    ` : ''}
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
 * Format source name for display
 */
function formatSourceName(source) {
    const names = {
        'hunter_verify': '🔍 Hunter.io - Email Verification',
        'hunter_find': '🔍 Hunter.io - Email Finder',
        'hibp': '🔒 Have I Been Pwned',
        'github': '💻 GitHub Profile',
        'virustotal': '🛡️ VirusTotal',
        'shodan': '🌐 Shodan',
        'social_media': '📱 Social Media',
        'sherlock': '🕵️ Sherlock Username Search'
    };

    return names[source] || `📊 ${source.toUpperCase()}`;
}

/**
 * Format type name for badges
 */
function formatTypeName(type) {
    const names = {
        'email': '📧 Email',
        'phone': '📱 Phone',
        'username': '👤 Username',
        'ip': '🌐 IP Address',
        'domain': '🌍 Domain',
        'url': '🔗 URL',
        'person': '👤 Person Name'
    };

    return names[type] || type;
}

// ═══════════════════════════════════════════════════════════════
// UI UTILITIES
// ═══════════════════════════════════════════════════════════════

/**
 * Show/hide loading overlay
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
 * Hide results section
 */
function hideResults() {
    const resultsSection = document.getElementById('resultsSection');
    resultsSection.classList.add('hidden');
}

/**
 * Show toast notification
 */
function showToast(message, type = 'info') {
    const toastContainer = document.getElementById('toastContainer');

    const toast = document.createElement('div');
    toast.className = 'toast';

    const icons = {
        success: '✅',
        error: '❌',
        warning: '⚠️',
        info: 'ℹ️'
    };

    const colors = {
        success: 'var(--cyber-success)',
        error: 'var(--cyber-error)',
        warning: 'var(--cyber-warning)',
        info: 'var(--cyber-primary)'
    };

    toast.innerHTML = `
        <div style="display: flex; align-items: center; gap: 0.75rem;">
            <span style="font-size: 1.5rem;">${icons[type]}</span>
            <span style="flex: 1; color: var(--text-primary);">${message}</span>
        </div>
    `;

    toast.style.borderLeft = `4px solid ${colors[type]}`;

    toastContainer.appendChild(toast);

    // Auto remove after 5 seconds
    setTimeout(() => {
        toast.style.animation = 'slideOutRight 0.3s ease-out';
        setTimeout(() => {
            toastContainer.removeChild(toast);
        }, 300);
    }, 5000);
}

/**
 * Animate number counter
 */
function animateValue(elementId, start, end, duration) {
    const element = document.getElementById(elementId);
    const range = end - start;
    const increment = range / (duration / 16);
    let current = start;

    const timer = setInterval(() => {
        current += increment;
        if ((increment > 0 && current >= end) || (increment < 0 && current <= end)) {
            current = end;
            clearInterval(timer);
        }
        element.textContent = Math.floor(current);
    }, 16);
}

// ═══════════════════════════════════════════════════════════════
// EXPORT FUNCTIONS
// ═══════════════════════════════════════════════════════════════

/**
 * Export results as JSON
 */
function exportJSON() {
    if (!currentResults) {
        showToast('No results to export', 'warning');
        return;
    }

    const dataStr = JSON.stringify(currentResults, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });

    const link = document.createElement('a');
    link.href = URL.createObjectURL(dataBlob);
    link.download = `osint_results_${Date.now()}.json`;
    link.click();

    showToast('JSON export successful', 'success');
}

/**
 * Export results as HTML
 */
function exportHTML() {
    if (!currentResults) {
        showToast('No results to export', 'warning');
        return;
    }

    const html = `
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OSINT Results - ${currentResults.query}</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: #0a0e1a;
            color: #e8edf4;
            padding: 2rem;
            line-height: 1.6;
        }
        .container { max-width: 1200px; margin: 0 auto; }
        h1 {
            font-size: 2.5rem;
            margin-bottom: 1rem;
            background: linear-gradient(135deg, #00f7ff, #7d5fff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .meta {
            background: rgba(21, 27, 43, 0.7);
            padding: 1.5rem;
            border-radius: 12px;
            margin: 2rem 0;
            border: 1px solid rgba(127, 95, 255, 0.2);
        }
        .meta-item { margin: 0.5rem 0; color: #a0aec0; }
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin: 2rem 0;
        }
        .stat-card {
            background: rgba(21, 27, 43, 0.7);
            padding: 1.5rem;
            border-radius: 12px;
            text-align: center;
            border: 1px solid rgba(127, 95, 255, 0.2);
        }
        .stat-value {
            font-size: 2.5rem;
            font-weight: 800;
            color: #00f7ff;
        }
        .stat-label {
            color: #a0aec0;
            font-size: 0.875rem;
            text-transform: uppercase;
            margin-top: 0.5rem;
        }
        .result {
            background: rgba(21, 27, 43, 0.7);
            border: 1px solid rgba(127, 95, 255, 0.2);
            border-radius: 12px;
            padding: 1.5rem;
            margin: 1rem 0;
        }
        .result h3 {
            color: #00f7ff;
            margin-bottom: 1rem;
        }
        pre {
            background: #0f1420;
            border: 1px solid rgba(127, 95, 255, 0.2);
            border-radius: 8px;
            padding: 1rem;
            overflow-x: auto;
            font-family: 'JetBrains Mono', 'Courier New', monospace;
            font-size: 0.875rem;
            color: #a0aec0;
        }
        .footer {
            text-align: center;
            margin-top: 3rem;
            padding-top: 2rem;
            border-top: 1px solid rgba(127, 95, 255, 0.2);
            color: #64748b;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎯 OSINT Intelligence Report</h1>

        <div class="meta">
            <div class="meta-item"><strong>Query:</strong> ${currentResults.query}</div>
            <div class="meta-item"><strong>Types:</strong> ${currentResults.detected_types.join(', ')}</div>
            <div class="meta-item"><strong>Timestamp:</strong> ${currentResults.timestamp}</div>
        </div>

        <div class="stats">
            <div class="stat-card">
                <div class="stat-value">${currentResults.summary.total_sources || 0}</div>
                <div class="stat-label">Total Sources</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" style="color: #00ff9d">${currentResults.summary.successful || 0}</div>
                <div class="stat-label">Successful</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" style="color: #ff3366">${currentResults.summary.failed || 0}</div>
                <div class="stat-label">Failed</div>
            </div>
        </div>

        <h2 style="margin: 2rem 0 1rem; color: #00f7ff;">Detailed Results</h2>
        ${Object.entries(currentResults.results.sources)
            .map(([source, data]) => `
                <div class="result">
                    <h3>${formatSourceName(source)}</h3>
                    <pre>${JSON.stringify(data, null, 2)}</pre>
                </div>
            `).join('')}

        <div class="footer">
            <p>Generated by OSINT Intelligence Platform</p>
            <p>Report Date: ${new Date().toLocaleString()}</p>
        </div>
    </div>
</body>
</html>
    `;

    const dataBlob = new Blob([html], { type: 'text/html' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(dataBlob);
    link.download = `osint_report_${Date.now()}.html`;
    link.click();

    showToast('HTML report exported successfully', 'success');
}

// ═══════════════════════════════════════════════════════════════
// KEYBOARD SHORTCUTS INFO
// ═══════════════════════════════════════════════════════════════

console.log(`
╔═══════════════════════════════════════════════════════════════╗
║         OSINT INTELLIGENCE PLATFORM - KEYBOARD SHORTCUTS      ║
╠═══════════════════════════════════════════════════════════════╣
║  Ctrl/Cmd + K  │  Focus search input                          ║
║  Enter         │  Execute search                              ║
╚═══════════════════════════════════════════════════════════════╝
`);
