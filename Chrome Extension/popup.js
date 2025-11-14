// =============================================================
// 🧠 MALICIOUS URL DETECTOR — POPUP SCRIPT
// Stable version with safe messaging and color-coded labels
// =============================================================

document.addEventListener("DOMContentLoaded", () => {
  const scanToggle = document.getElementById("scan-toggle");
  const scanButton = document.getElementById("scan-now");
  const pageStatus = document.getElementById("page-status");
  const linkCount = document.getElementById("link-count");
  const maliciousLinks = document.getElementById("malicious-links");

  // --- Helper for safe messaging ---
  function safeSendMessage(message, callback) {
    try {
      chrome.runtime.sendMessage(message, (response) => {
        if (chrome.runtime.lastError) {
          console.warn("⚠️ Message error:", chrome.runtime.lastError.message);
          callback?.(null);
          return;
        }
        callback?.(response);
      });
    } catch (err) {
      console.error("❌ Runtime messaging failed:", err);
      callback?.(null);
    }
  }

  // --- Load scanning toggle state ---
  chrome.storage.local.get("scanningEnabled", (data) => {
    scanToggle.checked = data.scanningEnabled !== false;
  });

  // --- Toggle scanning ---
  scanToggle.addEventListener("change", () => {
    safeSendMessage({ action: "toggleScanning", enabled: scanToggle.checked });
  });

  // --- "Scan Now" button ---
  scanButton.addEventListener("click", () => {
    scanButton.disabled = true;
    scanButton.textContent = "Scanning...";
    safeSendMessage({ action: "scanCurrentPage" }, () => {
      scanButton.disabled = false;
      scanButton.textContent = "Scan Now";
      updatePopup();
    });
  });

  // --- Update popup information ---
  function updatePopup() {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      if (!tabs[0]) {
        pageStatus.textContent = "Error: No active tab";
        return;
      }

      const currentUrl = tabs[0].url;
      safeSendMessage({ action: "checkUrl", url: currentUrl }, (response) => {
        if (!response) {
          pageStatus.textContent = "⚠️ Background inactive";
          pageStatus.className = "text-gray-600 font-medium";
          return;
        }
        const label = response.prediction || (response.malicious ? "MALICIOUS" : "SAFE");
        updatePageStatus(label);
      });

      // Get link results
      safeSendMessage({ action: "getLinkResults" }, (response) => {
        if (!response || !response.results) {
          linkCount.textContent = "0";
          return;
        }

        linkCount.textContent = response.results.filter(r => r.malicious).length;
        maliciousLinks.innerHTML = "";
        response.results
          .filter(r => r.malicious)
          .forEach(r => {
            const li = document.createElement("li");
            li.textContent = `${r.url} (${r.prediction || "MALICIOUS"})`;
            li.className = `p-2 mb-1 rounded break-all ${getLabelColorClass(r.prediction)}`;
            maliciousLinks.appendChild(li);
          });
      });
    });
  }

  // --- Label color mapping ---
  function updatePageStatus(label) {
    pageStatus.textContent = label;
    pageStatus.className = `font-semibold ${getLabelColorClass(label)} text-sm px-2 py-1 rounded`;
  }

  function getLabelColorClass(label) {
    switch ((label || "").toUpperCase()) {
      case "PHISHING": return "bg-red-100 text-red-700";
      case "MALWARE": return "bg-orange-100 text-orange-700";
      case "DEFACEMENT": return "bg-purple-100 text-purple-700";
      case "SAFE": return "bg-green-100 text-green-700";
      default: return "bg-yellow-100 text-yellow-700";
    }
  }

  // --- Initialize popup ---
  updatePopup();
});
