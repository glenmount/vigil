(function(){
  fetch("bundles.json", {cache:"no-store"}).then(r=>r.ok?r.json():[])
    .then(b => {
      if (!b || (Array.isArray(b) && b.length===0)) {
        const row = Array.from(document.querySelectorAll("*"))
          .find(n => n.textContent && n.textContent.trim().startsWith("Bundle:"));
        if (row) row.style.display = "none";
      }
    }).catch(()=>{});
})();
