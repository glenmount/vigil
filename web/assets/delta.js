(async function(){
  const host = document.getElementById("delta");
  if(!host) return;
  try{
    const r = await fetch("delta.json", {cache:"no-store"});
    if(!r.ok) throw new Error("no delta");
    const d = await r.json();
    const rules = d.rules || [];
    const rates = d.cohort_rates || [];
    const topn = d.topn;

    host.innerHTML = `
      <h2 style="margin:16px 0 8px 0">Δ — What changed since last run?</h2>
      <div style="font-size:14px;color:#333;margin-bottom:8px">
        Rules changed: ${d.summary.rules_changed} • Units with rate change: ${d.summary.units_rate_changed} • Top-N changed: ${topn? "yes" : "no"}
      </div>
      ${(topn? `<div style="margin:6px 0 12px">Top-N: ${topn.before} → <b>${topn.after} (${topn.delta>=0?"+":""}${topn.delta})</b></div>` : ``)}
      <div style="display:flex; gap:24px; flex-wrap:wrap">
        <div style="flex:1; min-width:320px">
          <div style="font-weight:600;margin:6px 0">Rule flips / changes</div>
          <table style="border-collapse:collapse;width:100%">
            <thead><tr>
              <th style="text-align:left;border-bottom:1px solid #ddd;padding:8px">Rule</th>
              <th style="text-align:right;border-bottom:1px solid #ddd;padding:8px">OK</th>
              <th style="text-align:right;border-bottom:1px solid #ddd;padding:8px">Observed</th>
            </tr></thead>
            <tbody>
              ${rules.map(r=>`
                <tr>
                  <td style="padding:8px;border-bottom:1px solid #f0f0f0">${r.title}</td>
                  <td style="padding:8px;text-align:right;border-bottom:1px solid #f0f0f0">${r.ok_before===true?"✓":(r.ok_before===false?"✗":"?")} → <b>${r.ok_after===true?"✓":(r.ok_after===false?"✗":"?")}</b></td>
                  <td style="padding:8px;text-align:right;border-bottom:1px solid #f0f0f0">${r.observed_before ?? "—"} → <b>${r.observed_after ?? "—"}</b></td>
                </tr>`).join("") || `<tr><td colspan="3" style="padding:8px;color:#666">No rule changes</td></tr>`}
            </tbody>
          </table>
        </div>
        <div style="flex:1; min-width:320px">
          <div style="font-weight:600;margin:6px 0">Cohort rate changes (pp)</div>
          <table style="border-collapse:collapse;width:100%">
            <thead><tr>
              <th style="text-align:left;border-bottom:1px solid #ddd;padding:8px">Unit</th>
              <th style="text-align:right;border-bottom:1px solid #ddd;padding:8px">Before</th>
              <th style="text-align:right;border-bottom:1px solid #ddd;padding:8px">After</th>
              <th style="text-align:right;border-bottom:1px solid #ddd;padding:8px">Δ</th>
            </tr></thead>
            <tbody>
              ${rates.map(x=>`
                <tr>
                  <td style="padding:8px;border-bottom:1px solid #f0f0f0">${x.unit}</td>
                  <td style="padding:8px;text-align:right;border-bottom:1px solid #f0f0f0">${x.before_pp ?? "—"}</td>
                  <td style="padding:8px;text-align:right;border-bottom:1px solid #f0f0f0">${x.after_pp ?? "—"}</td>
                  <td style="padding:8px;text-align:right;border-bottom:1px solid #f0f0f0"><b>${x.delta_pp>0?"+":""}${x.delta_pp ?? "—"}</b></td>
                </tr>`).join("") || `<tr><td colspan="4" style="padding:8px;color:#666">No rate changes</td></tr>`}
            </tbody>
          </table>
        </div>
      </div>`;
  }catch(e){ host.innerHTML=""; }
})();
