(function () {
  const KIND_MAP = [
    { test: /handover/i, label: "handover" },
    { test: /break/i,    label: "breaks"   },
    { test: /bell/i,     label: "bells"    },
  ];
  function classify(text) {
    for (const r of KIND_MAP) if (r.test(text)) return r.label;
    return null;
  }
  function pill(text, title) {
    const span = document.createElement("span");
    span.textContent = text;
    span.style.cssText = "display:inline-block;margin-left:8px;padding:2px 6px;border-radius:10px;border:1px solid #ddd;font-size:12px;color:#333;vertical-align:middle;";
    if (title) span.title = title; // hover
    return span;
  }

  // Try to load local receipts (viewer stays receipt-free on Pages; this only works locally)
  let receipts = null;
  fetch("receipts.jsonl", { cache: "no-store" })
    .then(r => r.ok ? r.text() : Promise.reject())
    .then(t => {
      receipts = t.trim().split(/\n+/).map(l => { try { return JSON.parse(l); } catch { return null; } }).filter(Boolean);
    })
    .catch(()=>{ /* no local receipts, hover will be empty */ });

  function topCitationTitle(kindGuess) {
    if (!receipts) return null;
    // Find the first matching receipt with citations
    const rec = receipts.find(r => r.kind && (!kindGuess || (r.kind||"").toLowerCase().includes(kindGuess)));
    const c = rec && Array.isArray(rec.citations) && rec.citations[0];
    if (!c) return null;
    const file = (c.doc_id || "").split("/").pop() || "policy.pdf";
    const page = c.page != null ? ` p.${c.page}` : "";
    return `${file}${page}`;
  }

  function enhanceQueue() {
    // Be permissive in selecting queue titles
    const col = document.querySelector(".queue, .live-queue, #live-queue, main");
    if (!col) return;
    const nodes = col.querySelectorAll("li, .item, .queue-item, h3, h4, .title");
    nodes.forEach(n => {
      if (n.dataset.badged) return;
      const txt = (n.textContent || "").trim();
      const label = classify(txt);
      if (label) {
        const hover = topCitationTitle(label); // e.g., "handover" → find a handover receipt
        n.appendChild(pill(label, hover));
        n.dataset.badged = "1";
      }
    });
  }

  const obs = new MutationObserver(() => enhanceQueue());
  obs.observe(document.body, { childList: true, subtree: true });
  enhanceQueue();
})();
