// ============= SAFE CONTENT SCRIPT =============
// Prevents "Extension context invalidated" errors when tab reloads or extension reloads

function safeGetStorage(key, callback) {
  try {
    if (!chrome || !chrome.storage || !chrome.storage.local) {
      console.warn("⚠️ Chrome storage not available yet — retrying...");
      setTimeout(() => safeGetStorage(key, callback), 500);
      return;
    }

    chrome.storage.local.get(key, (data) => {
      if (chrome.runtime?.lastError) {
        console.warn("⚠️ chrome.runtime.lastError:", chrome.runtime.lastError.message);
        setTimeout(() => safeGetStorage(key, callback), 500);
        return;
      }
      callback(data);
    });
  } catch (err) {
    console.error("❌ Storage access failed:", err);
    setTimeout(() => safeGetStorage(key, callback), 500);
  }
}

// ============= MAIN LINK SCANNER =============
function scanLinks() {
  safeGetStorage('scanningEnabled', (data) => {
    if (data.scanningEnabled === false) return;

    const links = Array.from(document.querySelectorAll('a'))
      .map(a => a.href)
      .filter(href => href);

    if (links.length === 0) return;

    chrome.runtime.sendMessage({ action: "checkLinks", links: links }, (response) => {
      if (chrome.runtime.lastError) {
        console.warn('⚠️ Error sending checkLinks message:', chrome.runtime.lastError.message);
        return;
      }

      if (response && response.results) {
        response.results.forEach(result => {
          if (result.malicious) {
            highlightLink(result.url, result.prediction || "MALICIOUS");
          }
        });
      }
    });
  });
}

// ============= LINK HIGHLIGHT FUNCTION =============
function highlightLink(url, label) {
  const anchors = document.querySelectorAll(`a[href="${url}"]`);
  let color = "#ef4444";
  let labelText = label.toUpperCase();

  switch (labelText) {
    case "PHISHING": color = "#ef4444"; break;
    case "MALWARE": color = "#f97316"; break;
    case "DEFACEMENT": color = "#8b5cf6"; break;
    case "SAFE": color = "#22c55e"; break;
    default: color = "#eab308"; // yellow fallback
  }

  anchors.forEach(a => {
    a.style.backgroundColor = `${color}20`;
    a.style.border = `2px solid ${color}`;
    a.style.padding = "2px";
    a.style.borderRadius = "4px";
    a.style.transition = "all 0.3s ease-in-out";
    a.title = `⚠️ ${labelText} link detected`;
    a.classList.add("cursor-not-allowed");
  });
}

// ============= MONITORING =============
window.addEventListener('load', () => {
  setTimeout(scanLinks, 1000); // small delay for stability
});

const observer = new MutationObserver(() => {
  setTimeout(scanLinks, 500);
});
observer.observe(document.body, { childList: true, subtree: true });

// Allow popup-triggered rescans
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "rescanLinks") {
    scanLinks();
    sendResponse({});
  }
  return true;
});
