// Guarda a página e a planta para funcionar com sinal fraco no campus
const C="onde-fica-v20",F=["./","index.html","planta-campus.webp?v=1.7.1","icone.svg","icone-180.png","manifest.webmanifest","tipografia/hind-latin-400-normal.woff2","tipografia/hind-latin-700-normal.woff2"];
self.addEventListener("install",e=>e.waitUntil(caches.open(C).then(c=>c.addAll(F)).then(()=>self.skipWaiting())));
self.addEventListener("activate",e=>e.waitUntil(caches.keys().then(k=>Promise.all(k.filter(x=>x!==C).map(x=>caches.delete(x)))).then(()=>self.clients.claim())));
self.addEventListener("fetch",e=>{if(e.request.method!=="GET"||new URL(e.request.url).origin!==location.origin)return;
  e.respondWith(fetch(e.request).then(r=>{const cp=r.clone();if(r.ok&&new URL(e.request.url).origin===location.origin)caches.open(C).then(c=>c.put(e.request,cp));return r}).catch(()=>caches.match(e.request,{ignoreSearch:true}).then(r=>r||Response.error())))});
