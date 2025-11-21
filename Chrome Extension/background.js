// =============================================================
// 🧠 BACKGROUND SERVICE WORKER — connects Chrome Extension to FastAPI model
// =============================================================

const API_URL = "https://malurl-final.onrender.com/predict"; // Render backend

let lastResults = [];

// Utility: POST to FastAPI
async function fetchPrediction(url) {
  try {
    const response = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url })
    });

    if (!response.ok) throw new Error(`HTTP ${response.status}`);

    const data = await response.json();
    const label = (data.prediction || "").toUpperCase();

    return {
      url,
      prediction: label,
      malicious: label !== "SAFE",
      probabilities: data.probabilities || {}
    };
  } catch (err) {
    console.error("❌ API error:", err);
    return { url, prediction: "UNKNOWN", malicious: false, error: err.message };
  }
}

// =============================================================
// 🔁 Handle Messages from Popup or Content Scripts
// =============================================================
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  (async () => {
    switch (message.action) {
      case "checkUrl":
        sendResponse(await fetchPrediction(message.url));
        break;

      case "checkLinks":
        if (!message.links || !message.links.length) {
          sendResponse({ results: [] });
          return;
        }

        const results = [];
        for (const link of message.links) {
          const r = await fetchPrediction(link);
          results.push(r);
        }
        lastResults = results;
        sendResponse({ results });
        break;

      case "getLinkResults":
        sendResponse({ results: lastResults });
        break;

      case "scanCurrentPage":
        chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
          if (tabs[0]) chrome.tabs.sendMessage(tabs[0].id, { action: "rescanLinks" });
        });
        sendResponse({});
        break;

      case "toggleScanning":
        chrome.storage.local.set({ scanningEnabled: message.enabled });
        sendResponse({});
        break;

      default:
        console.warn("⚠️ Unknown action:", message);
        sendResponse({});
    }
  })();

  return true; // Keeps sendResponse async
});
