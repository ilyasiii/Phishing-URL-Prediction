// API URL - uses same origin in production, localhost for development
const API_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' 
    ? 'http://127.0.0.1:8000' 
    : window.location.origin;
let history = [];

// Check URL
async function checkURL() {
    const input = document.getElementById('urlInput');
    const url = input.value.trim();
    
    if (!url) {
        showError('Please enter a URL to check');
        return;
    }

    // Basic URL validation
    if (!url.match(/^https?:\/\/.+/i) && !url.match(/^[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,}/i)) {
        showError('Please enter a valid URL (e.g., https://example.com)');
        return;
    }

    // Add protocol if missing
    let fullURL = url;
    if (!url.match(/^https?:\/\//i)) {
        fullURL = 'https://' + url;
    }

    setLoading(true);
    hideError();
    hideResult();

    try {
        const response = await fetch(`${API_URL}/predict`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ urls: [fullURL] }),
        });

        if (!response.ok) {
            throw new Error('API request failed');
        }

        const data = await response.json();
        showResult(fullURL, data);
        addToHistory(fullURL, data);
    } catch (error) {
        console.error('Error:', error);
        showError('Failed to connect to API. Make sure the server is running on port 8000.');
    } finally {
        setLoading(false);
    }
}

// Test URL from quick test buttons
function testURL(url) {
    document.getElementById('urlInput').value = url;
    checkURL();
}

// Show result
function showResult(url, data) {
    const resultSection = document.getElementById('result');
    const resultCard = resultSection.querySelector('.result-card');
    const resultIcon = document.getElementById('resultIcon');
    const resultLabel = document.getElementById('resultLabel');
    const resultURL = document.getElementById('resultURL');
    const confidencePercent = document.getElementById('confidencePercent');
    const progressFill = document.getElementById('progressFill');

    const isPhishing = data.predictions[0] === 1;
    const probability = data.probabilities[0];
    const confidence = isPhishing ? probability : (1 - probability);

    // Update classes
    resultCard.className = `result-card ${isPhishing ? 'danger' : 'safe'}`;
    resultIcon.className = `result-icon ${isPhishing ? 'danger' : 'safe'}`;
    resultLabel.className = isPhishing ? 'danger' : 'safe';
    progressFill.className = `progress-fill ${isPhishing ? 'danger' : 'safe'}`;

    // Update content
    resultIcon.innerHTML = isPhishing ? `
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="#ff4757" stroke-width="2">
            <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path>
            <line x1="12" y1="9" x2="12" y2="13"></line>
            <line x1="12" y1="17" x2="12.01" y2="17"></line>
        </svg>
    ` : `
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="#00ff88" stroke-width="2">
            <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
            <polyline points="22 4 12 14.01 9 11.01"></polyline>
        </svg>
    `;

    resultLabel.textContent = isPhishing ? '⚠️ Phishing Detected!' : '✓ Safe Website';
    resultURL.textContent = url;
    confidencePercent.textContent = `${(confidence * 100).toFixed(1)}%`;
    progressFill.style.width = `${confidence * 100}%`;

    resultSection.style.display = 'block';
}

// Hide result
function hideResult() {
    document.getElementById('result').style.display = 'none';
}

// Show error
function showError(message) {
    const errorSection = document.getElementById('error');
    const errorMessage = document.getElementById('errorMessage');
    errorMessage.textContent = message;
    errorSection.style.display = 'block';
}

// Hide error
function hideError() {
    document.getElementById('error').style.display = 'none';
}

// Set loading state
function setLoading(loading) {
    const btn = document.getElementById('checkBtn');
    const btnText = btn.querySelector('.btn-text');
    const btnLoader = btn.querySelector('.btn-loader');
    
    if (loading) {
        btnText.style.display = 'none';
        btnLoader.style.display = 'block';
        btn.disabled = true;
    } else {
        btnText.style.display = 'block';
        btnLoader.style.display = 'none';
        btn.disabled = false;
    }
}

// Add to history
function addToHistory(url, data) {
    const isPhishing = data.predictions[0] === 1;
    
    // Add to beginning
    history.unshift({ url, isPhishing });
    
    // Keep only last 5
    if (history.length > 5) {
        history.pop();
    }

    renderHistory();
}

// Render history
function renderHistory() {
    const historyContainer = document.getElementById('history');
    
    if (history.length === 0) {
        historyContainer.innerHTML = '<p class="empty-history">No URLs checked yet</p>';
        return;
    }

    historyContainer.innerHTML = history.map(item => `
        <div class="history-item">
            <div class="history-dot ${item.isPhishing ? 'danger' : 'safe'}"></div>
            <span class="history-url">${item.url}</span>
            <span class="history-label ${item.isPhishing ? 'danger' : 'safe'}">
                ${item.isPhishing ? 'Phishing' : 'Safe'}
            </span>
        </div>
    `).join('');
}

// Enter key handler
document.getElementById('urlInput').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        checkURL();
    }
});

// Initialize
renderHistory();
