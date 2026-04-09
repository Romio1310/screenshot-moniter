// ═══ Initialize ═══
document.addEventListener('DOMContentLoaded', () => {
    loadStatus();
    checkServer();

    // Attach event listeners (Manifest V3 blocks inline onclick handlers)
    document.getElementById('save-url').addEventListener('click', saveUrl);
    document.getElementById('capture-btn').addEventListener('click', captureNow);
    document.getElementById('auto-btn').addEventListener('click', toggleAuto);
});

// ═══ Load Status ═══
function loadStatus() {
    chrome.runtime.sendMessage({ action: 'getStatus' }, (response) => {
        if (response) {
            document.getElementById('server-url').value = response.serverUrl || 'http://localhost:5005';
            document.getElementById('capture-count').textContent = response.captureCount || 0;

            const autoBtn = document.getElementById('auto-btn');
            const autoStatus = document.getElementById('auto-status');

            if (response.autoCapture) {
                autoBtn.classList.add('active');
                autoBtn.querySelector('.btn-text').textContent = '⏹ Stop Auto-Capture';
                autoStatus.textContent = 'ON';
            } else {
                autoBtn.classList.remove('active');
                autoBtn.querySelector('.btn-text').textContent = '⏱️ Auto-Capture (Every 5s)';
                autoStatus.textContent = 'OFF';
            }
        }
    });
}

// ═══ Check Server ═══
async function checkServer() {
    let urlInput = document.getElementById('server-url');
    let url = urlInput.value.trim() || 'http://localhost:5005';
    if (url.endsWith('/')) {
        url = url.slice(0, -1);
    }

    try {
        const res = await fetch(`${url}/`, { method: 'GET' });
        const data = await res.json();

        document.getElementById('status-dot').classList.add('connected');
        document.getElementById('status-text').textContent =
            `Connected — ${data.screenshot_count || 0} screenshots`;
        
        // SYNC: Update the big counter in the extension UI and storage
        if (data.screenshot_count !== undefined) {
            document.getElementById('capture-count').textContent = data.screenshot_count;
            chrome.runtime.sendMessage({ action: 'syncCount', count: data.screenshot_count });
        }
    } catch {
        document.getElementById('status-dot').classList.remove('connected');
        document.getElementById('status-text').textContent = 'Server offline (CORS/URL issue)';
    }
}

// ═══ Save URL ═══
function saveUrl() {
    let url = document.getElementById('server-url').value.trim();
    if (url.endsWith('/')) {
        url = url.slice(0, -1);
    }
    document.getElementById('server-url').value = url;
    
    if (url) {
        chrome.runtime.sendMessage({ action: 'setServerUrl', url });
        showFeedback('Server URL saved', 'success');
        checkServer();
    }
}

// ═══ Manual Capture ═══
function captureNow() {
    const btn = document.getElementById('capture-btn');
    btn.classList.add('loading');

    chrome.runtime.sendMessage({ action: 'captureScreenshot' }, (response) => {
        btn.classList.remove('loading');

        if (response && response.success) {
            showFeedback('✓ Screenshot captured and uploaded!', 'success');
            loadStatus(); // Refresh count
        } else {
            showFeedback(`✗ ${response?.error || 'Capture failed'}`, 'error');
        }
    });
}

// ═══ Toggle Auto-Capture ═══
function toggleAuto() {
    chrome.runtime.sendMessage({ action: 'getStatus' }, (response) => {
        if (response.autoCapture) {
            chrome.runtime.sendMessage({ action: 'stopAutoCapture' }, () => {
                showFeedback('Auto-capture stopped', 'success');
                loadStatus();
            });
        } else {
            chrome.runtime.sendMessage({ action: 'startAutoCapture' }, () => {
                showFeedback('Auto-capture started (every 5s)', 'success');
                loadStatus();
            });
        }
    });
}

// ═══ Feedback Toast ═══
function showFeedback(message, type) {
    const fb = document.getElementById('feedback');
    fb.textContent = message;
    fb.className = `feedback ${type}`;
    setTimeout(() => { fb.className = 'feedback'; }, 3000);
}
