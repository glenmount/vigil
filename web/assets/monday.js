(async function(){
  async function j(p){const r=await fetch(p,{cache:"no-store"}); if(!r.ok) throw new Error(p); return r.json();}
  const host=document.getElementById("monday"); if(!host) return;
  try{
    const m = await j("monday.json");
    const gap = (m.fairness_gap_pp==null) ? "n/a" : (m.fairness_gap_pp.toFixed ? m.fairness_gap_pp.toFixed(1) : m.fairness_gap_pp) + " pp";
    host.innerHTML = `
      <h2 style="margin:16px 0 8px 0">Monday Summary (sandbox)</h2>
      <div style="font-size:14px;color:#333">
        <div>Generated: ${m.generated_at}</div>
        <div style="margin-top:6px">Items: ${m.totals.items} • Handover: ${m.totals.handover} • Bells: ${m.totals.bells} • Breaks: ${m.totals.breaks}</div>
        <div style="margin-top:6px">Fairness gap: ${gap}</div>
      </div>`;
  } catch(e){
    host.innerHTML = "";
  }
})();
