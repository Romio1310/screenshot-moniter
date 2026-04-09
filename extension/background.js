/**
 * Screenshot Monitor — Background Service Worker
 *
 * Handles auto-capture alarms and screenshot transmission to the backend.
 */

// ─── Timer-based Auto Capture (Fast 5s) ─────────────────
let captureIntervalId = null;

async function runAutoCapture() {
  console.log("[Screenshot Monitor] Auto-capture triggered");
  try {
    await captureAndSend();
  } catch (err) {
    console.error("[Screenshot Monitor] Auto-capture failed:", err);
  }
}

// ─── Message Handler (from popup) ───────────────────────

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === "captureScreenshot") {
    captureAndSend()
      .then((result) => sendResponse({ success: true, ...result }))
      .catch((err) => sendResponse({ success: false, error: err.message }));
    return true; // Keep message channel open for async response
  }

  if (message.action === "startAutoCapture") {
    if (!captureIntervalId) {
      captureIntervalId = setInterval(runAutoCapture, 5000);
    }
    chrome.storage.local.set({ autoCapture: true });
    console.log("[Screenshot Monitor] Auto-capture started (every 5s)");
    sendResponse({ success: true, status: "started" });
  }

  if (message.action === "stopAutoCapture") {
    if (captureIntervalId) {
      clearInterval(captureIntervalId);
      captureIntervalId = null;
    }
    chrome.storage.local.set({ autoCapture: false });
    console.log("[Screenshot Monitor] Auto-capture stopped");
    sendResponse({ success: true, status: "stopped" });
  }

  if (message.action === "getStatus") {
    chrome.storage.local.get(["autoCapture", "serverUrl", "captureCount"], (data) => {
      sendResponse({
        autoCapture: data.autoCapture || false,
        serverUrl: data.serverUrl || "http://localhost:5005",
        captureCount: data.captureCount || 0,
      });
    });
    return true;
  }

  if (message.action === "setServerUrl") {
    chrome.storage.local.set({ serverUrl: message.url });
    sendResponse({ success: true });
  }
});

// ─── Core: Capture Tab & Send to Server ─────────────────

async function captureAndSend() {
  // Get the active tab
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

  if (!tab || !tab.id || !tab.url) {
    throw new Error("No active tab found");
  }

  // Soft-fail for protected pages to avoid red extension console errors
  if (tab.url.startsWith("chrome://") || tab.url.startsWith("edge://") || tab.url.startsWith("about:")) {
    console.warn("[Screenshot Monitor] Skipping protected browser page.");
    return { success: false, ignored: true };
  }

  // Capture visible tab as PNG data URL
  const dataUrl = await chrome.tabs.captureVisibleTab(null, {
    format: "png",
    quality: 100,
  });

  // Convert data URL to blob
  const blob = dataURLtoBlob(dataUrl);

  // Get server URL from storage
  const { serverUrl } = await chrome.storage.local.get("serverUrl");
  let baseUrl = serverUrl ? serverUrl.trim() : "http://localhost:5005";
  if (baseUrl.endsWith('/')) {
    baseUrl = baseUrl.slice(0, -1);
  }

  // Create form data
  const formData = new FormData();
  const filename = `screenshot_${Date.now()}.png`;
  formData.append("file", blob, filename);

  // Send to backend
  const response = await fetch(`${baseUrl}/upload`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.error || `Server responded with ${response.status}`);
  }

  const result = await response.json();

  // Update capture count
  const { captureCount } = await chrome.storage.local.get("captureCount");
  chrome.storage.local.set({ captureCount: (captureCount || 0) + 1 });

  console.log("[Screenshot Monitor] Screenshot sent:", result.screenshot?.filename);
  return result;
}

// ─── Utility: Data URL to Blob ──────────────────────────

function dataURLtoBlob(dataUrl) {
  const parts = dataUrl.split(",");
  const mime = parts[0].match(/:(.*?);/)[1];
  const binary = atob(parts[1]);
  const array = new Uint8Array(binary.length);
  for (let i = 0; i < binary.length; i++) {
    array[i] = binary.charCodeAt(i);
  }
  return new Blob([array], { type: mime });
}

// ─── Install Handler ────────────────────────────────────

chrome.runtime.onInstalled.addListener(() => {
  chrome.storage.local.set({
    autoCapture: false,
    serverUrl: "http://localhost:5005",
    captureCount: 0,
  });
  console.log("[Screenshot Monitor] Extension installed and configured");
});
