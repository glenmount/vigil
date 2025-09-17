(async function () {
  async function j(p){const r=await fetch(p,{cache:"no-store"}); if(!r.ok) throw new Error(p); return r.json();}

  async function opps(){
    try{const o=await j("opportunities.json"); if(o?.windows_per_unit) return o.windows_per_unit;}catch(_){}
    try{const l=await j("receipts/labels.json"); const w=l?.handover?.windows_per_unit||l?.windows_per_unit; if(w&&typeof w==="object") return w;}catch(_){}
    try{const s=await j("scoreboard.json"); const w=s?.handover?.windows_per_unit||s?.windows_per_unit; if(w&&typeof w==="object") return w;}catch(_){}
    return {};
  }

  async function acts(){
    // 1) Prefer engine queue (per-unit if emitted; ALL fallback otherwise)
    try{
      const q = await j("queue.json");
      const per={};
      (q.items||q||[]).forEach(it=>{
        if((it.kind||"")!=="handover") return;
        const u = String(it.unit || it.scope || "ALL");
        per[u]=(per[u]||0)+1;
      });
      if(Object.keys(per).length) return per;
    }catch(_){}

    // 2) Fallback: labels snapshot per-unit breach map
    try{
      const l = await j("receipts/labels.json");
      const h = l?.handover||{};
      const ignore=new Set(["windows_per_unit","windows","total","count","summary","breaches_total"]);
      for(const [k,v] of Object.entries(h)){ if(ignore.has(k)) continue;
        if(v && typeof v==="object" && Object.values(v).every(x=>typeof x==="number")) return v;
      }
    }catch(_){}
    return {};
  }

  function render(rows,gapText){
    const host=document.getElementById("cohort-table"); if(!host) return;
    host.innerHTML = `
      <h2 style="margin:16px 0 8px 0">Cohorts (Fairness)</h2>
      <div id="cohort-legend" style="margin:6px 0 8px 0;color:#666;font-size:12px">
        Actions = per-unit handover items; <b>ALL</b> = global items when units are unknown.
      </div>
      <div style="overflow:auto">
        <table style="border-collapse:collapse;width:100%;max-width:960px">
          <thead><tr>
            <th style="text-align:left;border-bottom:1px solid #ddd;padding:8px">Unit</th>
            <th style="text-align:right;border-bottom:1px solid #ddd;padding:8px">Opportunities</th>
            <th style="text-align:right;border-bottom:1px solid #ddd;padding:8px">Actions</th>
            <th style="text-align:right;border-bottom:1px solid #ddd;padding:8px">Rate</th>
          </tr></thead>
          <tbody>${rows.map(r=>`
            <tr>
              <td style="padding:8px;border-bottom:1px solid #f0f0f0">${r.unit}</td>
              <td style="padding:8px;text-align:right;border-bottom:1px solid #f0f0f0">${r.opp ?? "—"}</td>
              <td style="padding:8px;text-align:right;border-bottom:1px solid #f0f0f0">${r.act ?? 0}</td>
              <td style="padding:8px;text-align:right;border-bottom:1px solid #f0f0f0">${r.rate ?? "n/a"}</td>
            </tr>`).join("")}
          </tbody>
        </table>
        <div id="cohort-gap" style="margin-top:8px;color:#666">${gapText}</div>
      </div>`;
  }

  try{
    const [O,A]=await Promise.all([opps(),acts()]);
    const units=Array.from(new Set([...Object.keys(O||{}),...Object.keys(A||{})]));
    let rates=[]; const rows=units.map(u=>{
      const opp = typeof O[u]==="number" ? O[u] : null;
      const act = A[u]||0;
      let rate="n/a"; if(opp!==null && opp>0){ const r=act/opp; rates.push(r); rate=(r*100).toFixed(1)+"%";}
      return {unit:u, opp:opp??"—", act, rate};
    });
    let gap="Fairness gap: n/a";
    if(rates.length>=2){ const mx=Math.max(...rates), mn=Math.min(...rates); gap=`Fairness gap: ${((mx-mn)*100).toFixed(1)} pp`; }
    render(rows,gap);
  }catch(e){ console.warn("[cohorts]", e.message); }
})();
