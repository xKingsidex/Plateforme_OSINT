/**
 * ═══════════════════════════════════════════════════════════════
 * OSINT Intelligence Platform PRO - Frontend Logic
 * ═══════════════════════════════════════════════════════════════
 */

const API_BASE_URL = 'http://localhost:8000';

let currentResults = null;

// ═══════════════════════════════════════════════════════════════
// INITIALIZATION
// ═══════════════════════════════════════════════════════════════

document.addEventListener('DOMContentLoaded', () => {
    console.log('[*] Initializing OSINT Platform PRO...');
    
    checkAPIHealth();
    setupEventListeners();
    updateTimestamp();
    setInterval(updateTimestamp, 1000);
});

function updateTimestamp() {
    const now = new Date();
    const timestamp = now.toISOString().replace('T', ' ').split('.')[0];
    const el = document.getElementById('timestamp');
    if (el) el.textContent = `[${timestamp}]`;
}

async function checkAPIHealth() {
    const statusEl = document.getElementById('apiStatus');
    
    addTerminalOutput('[*] Connecting to API backend...', 'info');
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/health`);
        const data = await response.json();
        
        if (data.status === 'healthy') {
            statusEl.textContent = 'CONNECTED ✓';
            statusEl.classList.add('text-success');
            addTerminalOutput('[✓] API backend connected successfully', 'success');
            addTerminalOutput(`[i] Professional tools loaded: ${Object.keys(data.scrapers).length}`, 'info');
        }
    } catch (error) {
        statusEl.textContent = 'OFFLINE ✗';
        statusEl.classList.add('text-error');
        addTerminalOutput('[✗] API backend connection failed', 'error');
    }
}

// ═══════════════════════════════════════════════════════════════
// EVENT LISTENERS
// ═══════════════════════════════════════════════════════════════

function setupEventListeners() {
    const searchForm = document.getElementById('searchForm');
    const searchInput = document.getElementById('searchInput');
    const copyBtn = document.getElementById('copyBtn');
    const downloadBtn = document.getElementById('downloadBtn');
    
    searchForm.addEventListener('submit', handleSearch);
    
    // Auto-detection
    let detectTimeout;
    searchInput.addEventListener('input', (e) => {
        clearTimeout(detectTimeout);
        detectTimeout = setTimeout(() => {
            const query = e.target.value.trim();
            if (query.length > 2) {
                detectType(query);
            } else {
                hideDetectionBanner();
            }
        }, 500);
    });
    
    if (copyBtn) copyBtn.addEventListener('click', copyRawJSON);
    if (downloadBtn) downloadBtn.addEventListener('click', downloadJSON);
}

// ═══════════════════════════════════════════════════════════════
// DETECTION
// ═══════════════════════════════════════════════════════════════

async function detectType(query) {
    try {
        const response = await fetch(`${API_BASE_URL}/api/detect`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query })
        });
        
        const data = await response.json();
        
        if (data.detected_types && data.detected_types.length > 0) {
            showDetectionBanner(data.detected_types);
        }
    } catch (error) {
        console.error('[!] Detection error:', error);
    }
}

function showDetectionBanner(types) {
    const banner = document.getElementById('detectionBanner');
    const typesEl = document.getElementById('detectedTypes');
    
    const icons = {
        'email': '[EMAIL]',
        'username': '[USER]',
        'phone': '[PHONE]',
        'domain': '[DOMAIN]',
        'name': '[NAME]',
        'ip': '[IP]'
    };
    
    typesEl.textContent = types.map(t => icons[t] || `[${t.toUpperCase()}]`).join(' ');
    banner.style.display = 'block';
}

function hideDetectionBanner() {
    document.getElementById('detectionBanner').style.display = 'none';
}

// ═══════════════════════════════════════════════════════════════
// SEARCH
// ═══════════════════════════════════════════════════════════════

async function handleSearch(event) {
    event.preventDefault();
    
    const searchInput = document.getElementById('searchInput');
    const deepSearch = document.getElementById('deepSearch').checked;
    const professionalTools = document.getElementById('professionalTools').checked;
    
    const query = searchInput.value.trim();
    
    if (!query) {
        addTerminalOutput('[!] Error: Query cannot be empty', 'error');
        return;
    }
    
    // Clear previous results
    document.getElementById('resultsContainer').style.display = 'none';
    clearTerminalOutput();
    
    // Start scan
    addTerminalOutput(`[*] TARGET ACQUIRED: ${query}`, 'warning');
    addTerminalOutput(`[*] Deep Scan: ${deepSearch ? 'ENABLED (Sherlock 300+ sites)' : 'DISABLED'}`, 'info');
    addTerminalOutput(`[*] Professional Tools: ${professionalTools ? 'ENABLED' : 'DISABLED'}`, 'info');
    addTerminalOutput('[*] Initiating OSINT reconnaissance...', 'info');
    addTerminalOutput('[~] Please wait, this may take up to 2 minutes' + (deepSearch ? ' (Sherlock scan in progress)' : '') + '...', 'muted');
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/search`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                query: query,
                deep_search: deepSearch,
                use_professional_tools: professionalTools
            })
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'API Error');
        }
        
        const data = await response.json();
        currentResults = data;
        
        addTerminalOutput('[✓] Reconnaissance completed successfully', 'success');
        addTerminalOutput(`[i] Tools used: ${data.tools_used.join(', ')}`, 'info');
        addTerminalOutput(`[i] Total sources: ${data.summary.total_sources}`, 'info');
        addTerminalOutput('[+] Displaying results...', 'success');
        
        displayResults(data);
        
    } catch (error) {
        addTerminalOutput(`[✗] OSINT scan failed: ${error.message}`, 'error');
    }
}

// ═══════════════════════════════════════════════════════════════
// RESULTS DISPLAY
// ═══════════════════════════════════════════════════════════════

function displayResults(data) {
    // Stats
    displayStats(data.summary);
    
    // Detailed results
    displayDetailedResults(data.results, data.tools_used);
    
    // Raw JSON
    displayRawJSON(data);
    
    // Show results container
    document.getElementById('resultsContainer').style.display = 'block';
}

function displayStats(summary) {
    const statsGrid = document.getElementById('statsGrid');
    
    const stats = [
        { label: 'EMAILS VERIFIED', value: summary.verified_emails || 0 },
        { label: 'SOCIAL PROFILES', value: summary.social_profiles_found || 0 },
        { label: 'DATA BREACHES', value: summary.breaches_found || 0 },
        { label: 'CONFIDENCE SCORE', value: `${Math.round((summary.confidence_score || 0) * 100)}%` },
        { label: 'TOOLS USED', value: summary.tools_used_count || 0 },
        { label: 'TOTAL SOURCES', value: summary.total_sources || 0 }
    ];
    
    statsGrid.innerHTML = stats.map(stat => `
        <div class="stat-box">
            <div class="stat-value">${stat.value}</div>
            <div class="stat-label">[${stat.label}]</div>
        </div>
    `).join('');
}

function displayDetailedResults(results, toolsUsed) {
    const container = document.getElementById('resultSections');
    container.innerHTML = '';
    
    // Sherlock Results
    if (results.username_sherlock) {
        const sherlock = results.username_sherlock;
        let html = `
            <div class="terminal-section">
                <div class="section-header">[SHERLOCK] Username found on ${sherlock.total_found} platforms</div>
                <div class="section-content">
        `;
        
        if (sherlock.profiles_found && sherlock.profiles_found.length > 0) {
            sherlock.profiles_found.forEach(profile => {
                html += `<div class="output-line">[+] ${profile.platform}: ${profile.url}</div>`;
            });
        } else {
            html += `<div class="output-line text-muted">[i] No profiles found</div>`;
        }
        
        html += `</div></div>`;
        container.innerHTML += html;
    }
    
    // Holehe Results
    if (results.email_holehe) {
        const holehe = results.email_holehe;
        let html = `
            <div class="terminal-section">
                <div class="section-header">[HOLEHE] Email found on ${holehe.total_found} platforms</div>
                <div class="section-content">
        `;
        
        if (holehe.accounts_found && holehe.accounts_found.length > 0) {
            holehe.accounts_found.forEach(account => {
                html += `<div class="output-line">[+] ${account.platform}: Account exists</div>`;
            });
        } else {
            html += `<div class="output-line text-muted">[i] No accounts found</div>`;
        }
        
        html += `</div></div>`;
        container.innerHTML += html;
    }
    
    // Other results (email, phone, domain, etc.)
    for (const [key, value] of Object.entries(results)) {
        if (key.includes('sherlock') || key.includes('holehe')) continue;
        
        let html = `
            <div class="terminal-section">
                <div class="section-header">[${key.toUpperCase()}]</div>
                <div class="section-content">
                    <pre class="json-output">${JSON.stringify(value, null, 2)}</pre>
                </div>
            </div>
        `;
        
        container.innerHTML += html;
    }
}

function displayRawJSON(data) {
    const pre = document.getElementById('rawJsonData');
    pre.textContent = JSON.stringify(data, null, 2);
}

// ═══════════════════════════════════════════════════════════════
// TERMINAL OUTPUT
// ═══════════════════════════════════════════════════════════════

function addTerminalOutput(message, type = '') {
    const output = document.getElementById('terminalOutput');
    const line = document.createElement('div');
    line.className = `output-line ${type ? 'text-' + type : ''}`;
    line.textContent = message;
    output.appendChild(line);
    output.scrollTop = output.scrollHeight;
}

function clearTerminalOutput() {
    const output = document.getElementById('terminalOutput');
    output.innerHTML = '';
}

// ═══════════════════════════════════════════════════════════════
// EXPORT FUNCTIONS
// ═══════════════════════════════════════════════════════════════

function copyRawJSON() {
    if (!currentResults) return;
    
    const text = JSON.stringify(currentResults, null, 2);
    navigator.clipboard.writeText(text).then(() => {
        addTerminalOutput('[✓] JSON data copied to clipboard', 'success');
    });
}

function downloadJSON() {
    if (!currentResults) return;
    
    const text = JSON.stringify(currentResults, null, 2);
    const blob = new Blob([text], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `osint_results_${Date.now()}.json`;
    a.click();
    URL.revokeObjectURL(url);
    
    addTerminalOutput('[✓] JSON data downloaded successfully', 'success');
}
