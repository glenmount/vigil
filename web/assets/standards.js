(async function(){
  const host = document.getElementById("standards");
  if(!host) return;
  try{
    const r = await fetch("standards.json", {cache:"no-store"});
    if (!r.ok) throw new Error("no standards");
    const s = await r.json();
    const {passed, failed, unknown} = s.summary || {};
    host.innerHTML = `
      <h2 style="margin:16px 0 8px 0">Executable Standards (v1)</h2>
      <div style="font-size:14px;color:#333;margin-bottom:8px">
        Passed: ${passed} • Failed: ${failed} • Unknown: ${unknown}
      </div>
      <div style="overflow:auto">
        <table style="border-collapse:collapse;width:100%;max-width:960px">
          <thead><tr>
            <th style="text-align:left;border-bottom:1px solid #ddd;padding:8px">Rule</th>
            <th style="text-align:right;border-bottom:1px solid #ddd;padding:8px">Observed</th>
            <th style="text-align:right;border-bottom:1px solid #ddd;padding:8px">Expected</th>
            <th style="text-align:right;border-bottom:1px solid #ddd;padding:8px">OK</th>
          </tr></thead>
          <tbody>
            ${(s.results||[]).map(r=>`
              <tr>
                <td style="padding:8px;border-bottom:1px solid #f0f0f0">${r.title}</td>
                <td style="padding:8px;text-align:right;border-bottom:1px solid #f0f0f0">${r.observed ?? "—"}</td>
                <td style="padding:8px;text-align:right;border-bottom:1px solid #f0f0f0">${r.expected.op} ${r.expected.value}</td>
                <td style="padding:8px;text-align:right;border-bottom:1px solid #f0f0f0">${r.ok===true?"✓":(r.ok===false?"✗":"?")}</td>
              </tr>`).join("")}
          </tbody>
        </table>
      </div>`;
  }catch(e){
    host.innerHTML = "";
  }
})();
