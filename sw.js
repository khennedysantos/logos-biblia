/* Sola — service worker: deixa o site abrir e os capítulos já lidos funcionarem sem internet.
   A linha VERSAO é carimbada por ferramentas/gerar_paginas.py a cada mudança no app. */
const VERSAO = "784ff2bfc0";
const CACHE_APP = "sola-app-" + VERSAO;
const CACHE_DADOS = "sola-dados-v1";   // o mesmo nome está no app.js (botão "Baixar a Bíblia")
const BASE = ["/", "/data/books.json", "/favicon.svg", "/manifest.webmanifest",
  "/fontes/cardo-latin-400-normal.woff2", "/fontes/inter-latin-wght-normal.woff2",
  "/fontes/cormorant-garamond-latin-500-normal.woff2", "/fontes/cormorant-garamond-latin-600-normal.woff2"];

self.addEventListener("install", (e)=>{
  e.waitUntil(caches.open(CACHE_APP).then(async (c)=>{
    const inicio = await fetch("/", { cache: "reload" });
    const html = await inicio.clone().text();
    await c.put("/", inicio);
    // o app.js e o style.css com a versão que esta página usa
    const versionados = [...html.matchAll(/(?:src|href)="(\/(?:app\.js|style\.css)[^"]*)"/g)].map(m=>m[1]);
    await Promise.all(BASE.slice(1).concat(versionados).map(u=>c.add(u).catch(()=>{})));
  }).then(()=>self.skipWaiting()));
});

self.addEventListener("activate", (e)=>{
  e.waitUntil(caches.keys()
    .then(nomes=>Promise.all(nomes.filter(n=>n.startsWith("sola-app-") && n !== CACHE_APP).map(n=>caches.delete(n))))
    .then(()=>self.clients.claim()));
});

async function guardar(nomeCache, pedido, resposta){
  if(resposta && resposta.ok) (await caches.open(nomeCache)).put(pedido, resposta.clone());
  return resposta;
}

self.addEventListener("fetch", (e)=>{
  const pedido = e.request, url = new URL(pedido.url);
  if(pedido.method !== "GET" || url.origin !== location.origin) return;   // mapa (OpenStreetMap) e o resto: direto na rede

  // páginas: sempre a versão nova da rede; sem rede, a página guardada (o app lê o endereço e abre o capítulo certo)
  if(pedido.mode === "navigate"){
    e.respondWith(fetch(pedido).catch(()=>caches.match("/")));
    return;
  }
  // dados (Bíblia, interlinear, comentários…): responde do que está guardado e atualiza por trás
  if(url.pathname.startsWith("/data/")){
    e.respondWith(caches.match(pedido).then(guardado=>{
      const rede = fetch(pedido).then(r=>guardar(CACHE_DADOS, pedido, r));
      if(guardado){ rede.catch(()=>{}); return guardado; }
      return rede;
    }));
    return;
  }
  // app.js, style.css (têm a versão no endereço), fontes, ícones e mapa: o guardado serve; senão rede
  e.respondWith(caches.match(pedido).then(guardado=>guardado || fetch(pedido).then(r=>guardar(CACHE_APP, pedido, r))));
});
