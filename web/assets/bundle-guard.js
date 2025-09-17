(function(){
  fetch("bundles.json",{cache:"no-store"})
    .then(r=>r.ok?r.json():[])
    .then(b=>{
      if (!b || (Array.isArray(b)&&b.length===0)){
        const n=[...document.querySelectorAll("*")].find(x=>x.textContent?.trim().startsWith("Bundle:"));
        if (n) n.style.display="none";
      }
    }).catch(()=>{});
})();
