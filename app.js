/* Logos — Estudo Bíblico. SPA em JS puro, sem dependências. */
"use strict";

/* ---------- textos da interface ---------- */
const UI = {
  pt: { idioma:"Idioma", traducao:"Tradução", comparar:"Comparar com…", semComparar:"Sem comparação",
    livros:"Livros", buscar:"Buscar", notas:"Minhas anotações", marcar:"Marcar",
    original:"Original", comentario:"Comentário", anotacao:"Anotação", copiar:"Copiar", copiado:"Copiado!",
    grego:"Grego — Textus Receptus", hebraico:"Hebraico — Códice de Leningrado",
    lexDef:"Definição (Strong)", lexKjv:"Como a KJV traduz", lexFonte:"Léxico de Strong (1890) · Texto marcado: STEPBible/Tyndale House (CC BY)",
    semOriginal:"Texto original indisponível para este versículo.",
    semComentario:"Ainda não há comentário para este versículo.",
    avisoIdiomaComentario:"Comentário exibido no original em inglês — tradução em andamento.",
    fonte:"Fonte", salvar:"Salvar", cancelar:"Cancelar", excluir:"Excluir", fechar:"Fechar",
    escrevaNota:"Escreva sua reflexão sobre este versículo…",
    semNotas:"Você ainda não tem anotações. Toque em um versículo e escolha “Anotação”.",
    bibliaToda:"Buscar na Bíblia toda", buscarNoLivro:"Este livro", carregando:"Carregando…",
    buscando:"Buscando", resultados:"resultado(s)", nadaEncontrado:"Nada encontrado.",
    digiteBusca:"Digite ao menos 3 letras.", at:"Antigo Testamento", nt:"Novo Testamento",
    exPlaceholder:"ex.: graça e verdade" },
  en: { idioma:"Language", traducao:"Translation", comparar:"Compare with…", semComparar:"No comparison",
    livros:"Books", buscar:"Search", notas:"My notes", marcar:"Highlight",
    original:"Original", comentario:"Commentary", anotacao:"Note", copiar:"Copy", copiado:"Copied!",
    grego:"Greek — Textus Receptus", hebraico:"Hebrew — Leningrad Codex",
    lexDef:"Definition (Strong)", lexKjv:"KJV renderings", lexFonte:"Strong's Lexicon (1890) · Tagged text: STEPBible/Tyndale House (CC BY)",
    semOriginal:"Original text unavailable for this verse.",
    semComentario:"No commentary available for this verse yet.",
    avisoIdiomaComentario:"Commentary shown in the original English.",
    fonte:"Source", salvar:"Save", cancelar:"Cancel", excluir:"Delete", fechar:"Close",
    escrevaNota:"Write your reflection on this verse…",
    semNotas:"No notes yet. Tap a verse and choose “Note”.",
    bibliaToda:"Search the whole Bible", buscarNoLivro:"This book", carregando:"Loading…",
    buscando:"Searching", resultados:"result(s)", nadaEncontrado:"Nothing found.",
    digiteBusca:"Type at least 3 letters.", at:"Old Testament", nt:"New Testament",
    exPlaceholder:"e.g. grace and truth" },
  es: { idioma:"Idioma", traducao:"Traducción", comparar:"Comparar con…", semComparar:"Sin comparación",
    livros:"Libros", buscar:"Buscar", notas:"Mis notas", marcar:"Resaltar",
    original:"Original", comentario:"Comentario", anotacao:"Nota", copiar:"Copiar", copiado:"¡Copiado!",
    grego:"Griego — Textus Receptus", hebraico:"Hebreo — Códice de Leningrado",
    lexDef:"Definición (Strong)", lexKjv:"Traducciones en la KJV", lexFonte:"Léxico de Strong (1890) · Texto marcado: STEPBible/Tyndale House (CC BY)",
    semOriginal:"Texto original no disponible para este versículo.",
    semComentario:"Aún no hay comentario para este versículo.",
    avisoIdiomaComentario:"Comentario mostrado en el inglés original.",
    fonte:"Fuente", salvar:"Guardar", cancelar:"Cancelar", excluir:"Eliminar", fechar:"Cerrar",
    escrevaNota:"Escribe tu reflexión sobre este versículo…",
    semNotas:"Aún no tienes notas. Toca un versículo y elige “Nota”.",
    bibliaToda:"Buscar en toda la Biblia", buscarNoLivro:"Este libro", carregando:"Cargando…",
    buscando:"Buscando", resultados:"resultado(s)", nadaEncontrado:"No se encontró nada.",
    digiteBusca:"Escribe al menos 3 letras.", at:"Antiguo Testamento", nt:"Nuevo Testamento",
    exPlaceholder:"ej.: gracia y verdad" },
};
const CORES = ["ouro","verde","azul","rosa"];

/* ---------- estado ---------- */
const est = {
  meta:null, idioma:"pt", traducao:"blivre", comparar:"",
  livro:"JHN", cap:1, tema:"claro",
  marcas: lerLS("logos_marcas", {}), notas: lerLS("logos_notas", {}),
  cacheBiblia:{}, cacheComent:{}, versoAtivo:null, gaveta:null, // {tipo, verso}
};
function lerLS(k, padrao){ try{ return JSON.parse(localStorage.getItem(k)) ?? padrao; }catch(e){ return padrao; } }
function gravarLS(k, v){ try{ localStorage.setItem(k, JSON.stringify(v)); }catch(e){} }
function t(){ return UI[est.idioma]; }
const $ = (id)=>document.getElementById(id);

/* ---------- dados ---------- */
async function json(url){ const r = await fetch(url); if(!r.ok) throw new Error(url); return r.json(); }
async function carregarLivro(trad, usfm){
  const chave = trad+"/"+usfm;
  if(!est.cacheBiblia[chave]){
    try{ est.cacheBiblia[chave] = await json(`data/bibles/${trad}/${usfm}.json`); }
    catch(e){ est.cacheBiblia[chave] = null; }
  }
  return est.cacheBiblia[chave];
}
async function carregarComentario(usfm, cap){
  const chave = usfm+"/"+cap;
  if(!(chave in est.cacheComent)){
    try{ est.cacheComent[chave] = await json(`data/commentaries/calvin/${usfm}/${cap}.json`); }
    catch(e){ est.cacheComent[chave] = null; }
  }
  return est.cacheComent[chave];
}
est.cacheInter = {}; est.cacheLex = {};
async function carregarInterlinear(usfm, cap){
  const chave = usfm+"/"+cap;
  if(!(chave in est.cacheInter)){
    try{ est.cacheInter[chave] = await json(`data/interlinear/${usfm}/${cap}.json`); }
    catch(e){ est.cacheInter[chave] = null; }
  }
  return est.cacheInter[chave];
}
async function carregarLexico(letra){
  if(!est.cacheLex[letra]){
    try{ est.cacheLex[letra] = await json(`data/strongs/${letra}.json`); }
    catch(e){ est.cacheLex[letra] = null; }
  }
  return est.cacheLex[letra];
}
function infoLivro(usfm){ return est.meta.books.find(b=>b.id===usfm); }
function nomeLivro(usfm){ return infoLivro(usfm)[est.idioma] || infoLivro(usfm).pt; }
function refStr(usfm, cap, v){ return `${nomeLivro(usfm)} ${cap}:${v}`; }

/* ---------- interface base ---------- */
function aplicarTextos(){
  const x = t();
  $("lblIdioma").textContent = x.idioma;
  $("lblTraducao").textContent = x.traducao;
  $("lblComparar").textContent = x.comparar;
  $("tituloLivros").textContent = x.livros;
  $("tituloBusca").textContent = x.buscar;
  $("tituloNotas").textContent = x.notas;
  $("lblBibliaToda").textContent = x.bibliaToda;
  $("campoBusca").placeholder = x.exPlaceholder;
}
function preencherTraducoes(){
  const doIdioma = est.meta.translations.filter(tr=>tr.lang===est.idioma);
  if(!doIdioma.find(tr=>tr.id===est.traducao)) est.traducao = doIdioma[0].id;
  $("selTraducao").innerHTML = doIdioma.map(tr=>`<option value="${tr.id}">${tr.name}</option>`).join("");
  $("selTraducao").value = est.traducao;
  const outras = est.meta.translations.filter(tr=>tr.id!==est.traducao);
  $("selComparar").innerHTML = `<option value="">${t().semComparar}</option>` +
    outras.map(tr=>`<option value="${tr.id}">${tr.name}</option>`).join("");
  $("selComparar").value = outras.find(tr=>tr.id===est.comparar) ? est.comparar : "";
  if(!outras.find(tr=>tr.id===est.comparar)) est.comparar = "";
}

/* ---------- leitura ---------- */
async function renderizarCapitulo(){
  const x = t(), leitor = $("leitor");
  leitor.innerHTML = `<p class="sub-cap">${x.carregando}</p>`;
  const [livro, livroComp] = await Promise.all([
    carregarLivro(est.traducao, est.livro),
    est.comparar ? carregarLivro(est.comparar, est.livro) : null,
  ]);
  const info = infoLivro(est.livro);
  if(est.cap > info.ch) est.cap = 1;
  const versos = livro ? livro[est.cap-1] || [] : [];
  const versosComp = livroComp ? (livroComp[est.cap-1]||[]) : null;
  const nomeTrad = est.meta.translations.find(tr=>tr.id===est.traducao).name;

  let html = `<h1 class="titulo-cap escritura">${nomeLivro(est.livro)} ${est.cap}</h1>
    <p class="sub-cap">${nomeTrad}${est.comparar ? " · " + est.meta.translations.find(tr=>tr.id===est.comparar).name : ""}</p>`;
  versos.forEach((texto, i)=>{
    if(!texto && !(versosComp && versosComp[i])) return;
    const v = i+1, chave = `${est.livro}.${est.cap}.${v}`;
    const marca = est.marcas[chave] ? " m-"+est.marcas[chave] : "";
    const temNota = est.notas[chave] ? `<span class="indicadores" title="${t().anotacao}">✎</span>` : "";
    html += `<div class="verso${marca}" data-v="${v}">
      <p class="escritura"><sup>${v}</sup>${esc(texto)}${temNota}</p>
      ${versosComp && versosComp[i] ? `<p class="comparado escritura">${esc(versosComp[i])}</p>` : ""}
      <div class="barra" role="toolbar"></div>
      <div class="gavetas"></div>
    </div>`;
  });
  leitor.innerHTML = html;
  leitor.querySelectorAll(".verso").forEach(el=>{
    el.addEventListener("mouseenter", ()=>ativarVerso(el));
    el.addEventListener("click", (e)=>{ if(e.target.closest(".barra,.gavetas")) return; ativarVerso(el, true); });
  });
  atualizarNav();
  $("lblLivroAtual").textContent = `${nomeLivro(est.livro)} ${est.cap}`;
  document.title = `${nomeLivro(est.livro)} ${est.cap} — Logos`;
  location.hash = `#/${est.livro}/${est.cap}`;
  window.scrollTo({top:0});
}
function esc(s){ const d=document.createElement("div"); d.textContent=s; return d.innerHTML; }

function ativarVerso(el, toque){
  if(est.versoAtivo && est.versoAtivo!==el){ est.versoAtivo.classList.remove("ativo"); fecharGavetas(est.versoAtivo); }
  est.versoAtivo = el;
  el.classList.add("ativo");
  montarBarra(el);
}
function fecharGavetas(el){ el.querySelector(".gavetas").innerHTML=""; est.gaveta=null; }

function montarBarra(el){
  const v = +el.dataset.v, chave = `${est.livro}.${est.cap}.${v}`, x = t();
  const barra = el.querySelector(".barra");
  if(barra.dataset.pronta) return;
  barra.dataset.pronta = "1";
  barra.innerHTML =
    CORES.map(c=>`<button class="cor m-btn-${c}" data-cor="${c}" title="${x.marcar}" style="background:var(--m-${c})"></button>`).join("") +
    `<span class="sep"></span>
     <button class="acao" data-acao="original">${x.original}</button>
     <button class="acao" data-acao="comentario">${x.comentario}</button>
     <button class="acao" data-acao="anotacao">${x.anotacao}</button>
     <button class="acao" data-acao="copiar">${x.copiar}</button>`;
  barra.querySelectorAll(".cor").forEach(b=>{
    if(est.marcas[chave]===b.dataset.cor) b.classList.add("sel");
    b.addEventListener("click", ()=>{
      const c = b.dataset.cor;
      if(est.marcas[chave]===c){ delete est.marcas[chave]; } else { est.marcas[chave]=c; }
      gravarLS("logos_marcas", est.marcas);
      el.className = "verso ativo" + (est.marcas[chave] ? " m-"+est.marcas[chave] : "");
      barra.querySelectorAll(".cor").forEach(o=>o.classList.toggle("sel", est.marcas[chave]===o.dataset.cor));
    });
  });
  barra.querySelectorAll(".acao").forEach(b=>b.addEventListener("click", ()=>acaoVerso(el, v, b.dataset.acao, b)));
}

async function acaoVerso(el, v, acao, botao){
  const x = t(), chave = `${est.livro}.${est.cap}.${v}`;
  const gavetas = el.querySelector(".gavetas");
  if(acao==="copiar"){
    const texto = el.querySelector("p.escritura").innerText.replace(/^\d+\s*/,"").replace(/✎$/,"").trim();
    if(navigator.clipboard) navigator.clipboard.writeText(`"${texto}" — ${refStr(est.livro, est.cap, v)}`).catch(()=>{});
    const rot = botao.textContent; botao.textContent = x.copiado;
    setTimeout(()=>{ botao.textContent = rot; }, 1400);
    return;
  }
  if(est.gaveta && est.gaveta.tipo===acao && est.gaveta.verso===v){ fecharGavetas(el); return; }
  est.gaveta = {tipo:acao, verso:v};

  if(acao==="original"){
    const ehAT = infoLivro(est.livro).t==="AT";
    const rotulo = ehAT ? x.hebraico : x.grego;
    const inter = await carregarInterlinear(est.livro, est.cap);
    const palavras = inter && inter[v-1] && inter[v-1].length ? inter[v-1] : null;
    if(palavras){
      const grid = palavras.map((p,pi)=>
        `<button class="inter-palavra" data-pi="${pi}" data-strong="${p[2]||""}">
           <span class="ip-surf escritura" ${ehAT?'dir="rtl" lang="he"':'lang="grc"'}>${esc(p[0])}</span>
           <span class="ip-translit">${esc(p[1])}</span>
           <span class="ip-gloss">${esc(p[3])}</span>
           <span class="ip-strong">${p[2]||""}</span>
         </button>`).join("");
      gavetas.innerHTML = gaveta(rotulo,
        `<div class="inter-grid" ${ehAT?'dir="rtl"':''}>${grid}</div>
         <div class="lex-caixa oculto"></div>
         <p class="fonte">${x.lexFonte}</p>`);
      gavetas.querySelectorAll(".inter-palavra").forEach(btn=>btn.addEventListener("click", async ()=>{
        const caixa = gavetas.querySelector(".lex-caixa");
        const strong = btn.dataset.strong;
        gavetas.querySelectorAll(".inter-palavra").forEach(o=>o.classList.remove("sel"));
        if(!strong || caixa.dataset.atual===strong && !caixa.classList.contains("oculto")){
          caixa.classList.add("oculto"); caixa.dataset.atual=""; return;
        }
        btn.classList.add("sel");
        caixa.dataset.atual = strong;
        caixa.classList.remove("oculto");
        caixa.innerHTML = `<em>${x.carregando}</em>`;
        const lex = await carregarLexico(strong[0]);
        const ent = lex && lex[strong];
        if(!ent){ caixa.innerHTML = ""; caixa.classList.add("oculto"); return; }
        caixa.innerHTML = `
          <div class="lex-topo"><span class="escritura lex-lemma">${esc(ent.lemma)}</span>
            <span class="lex-translit">${esc(ent.translit)}</span>
            <span class="lex-num">${strong}</span></div>
          <p class="lex-def"><strong>${x.lexDef}:</strong> ${esc(ent.defpt || ent.def)}</p>
          ${ent.kjv ? `<p class="lex-def"><strong>${x.lexKjv}:</strong> ${esc(ent.kjv)}</p>` : ""}`;
      }));
    } else {
      const orig = await carregarLivro("orig", est.livro);
      const texto = orig && orig[est.cap-1] ? orig[est.cap-1][v-1] : "";
      gavetas.innerHTML = gaveta(rotulo,
        texto ? `<p class="original-texto" dir="${ehAT?"rtl":"ltr"}" lang="${ehAT?"he":"grc"}">${esc(texto)}</p>`
              : `<p class="comentario-texto">${x.semOriginal}</p>`);
    }
  }
  if(acao==="comentario"){
    const com = await carregarComentario(est.livro, est.cap);
    const texto = com ? com[String(v)] : null;
    gavetas.innerHTML = gaveta(x.comentario,
      texto ? `<p class="comentario-texto">${esc(texto)}</p>
               <p class="fonte">${x.fonte}: João Calvino (1509–1564), domínio público</p>
               ${est.idioma!=="en" && !com.__pt ? `<p class="aviso-idioma">${x.avisoIdiomaComentario}</p>` : ""}`
            : `<p class="comentario-texto">${x.semComentario}</p>`);
  }
  if(acao==="anotacao"){
    gavetas.innerHTML = gaveta(x.anotacao,
      `<textarea id="campoNota" placeholder="${x.escrevaNota}">${esc(est.notas[chave]||"")}</textarea>
       <div class="acoes">
         <button class="cancelar">${x.cancelar}</button>
         <button class="salvar">${x.salvar}</button>
       </div>`, true);
    gavetas.querySelector(".cancelar").addEventListener("click", ()=>fecharGavetas(el));
    gavetas.querySelector(".salvar").addEventListener("click", ()=>{
      const valor = gavetas.querySelector("#campoNota").value.trim();
      if(valor) est.notas[chave] = valor; else delete est.notas[chave];
      gravarLS("logos_notas", est.notas);
      fecharGavetas(el);
      renderizarCapitulo();
    });
    gavetas.querySelector("#campoNota").focus();
  }
  const fechaBtn = gavetas.querySelector(".rotulo button");
  if(fechaBtn) fechaBtn.addEventListener("click", ()=>fecharGavetas(el));
}
function gaveta(rotulo, corpo, destaque){
  return `<div class="gaveta${destaque?" destaque":""}">
    <div class="rotulo"><span>${rotulo}</span><button>✕ ${t().fechar}</button></div>${corpo}</div>`;
}

/* ---------- navegação ---------- */
function atualizarNav(){
  const idx = est.meta.books.findIndex(b=>b.id===est.livro);
  const info = est.meta.books[idx];
  const ant = est.cap>1 ? {l:est.livro, c:est.cap-1}
            : idx>0 ? {l:est.meta.books[idx-1].id, c:est.meta.books[idx-1].ch} : null;
  const pro = est.cap<info.ch ? {l:est.livro, c:est.cap+1}
            : idx<est.meta.books.length-1 ? {l:est.meta.books[idx+1].id, c:1} : null;
  const bA = $("btnAnterior"), bP = $("btnProximo");
  bA.disabled = !ant; bP.disabled = !pro;
  if(ant){ bA.querySelector("span").textContent = `${nomeLivro(ant.l)} ${ant.c}`; bA.onclick = ()=>irPara(ant.l, ant.c); }
  if(pro){ bP.querySelector("span").textContent = `${nomeLivro(pro.l)} ${pro.c}`; bP.onclick = ()=>irPara(pro.l, pro.c); }
}
function irPara(usfm, cap){ est.livro=usfm; est.cap=cap; renderizarCapitulo(); }

function montarListaLivros(){
  const x = t();
  let html = `<div class="grupo">${x.at}</div>`;
  est.meta.books.forEach(b=>{
    if(b.id==="MAT") html += `<div class="grupo">${x.nt}</div>`;
    html += `<button data-livro="${b.id}">${b[est.idioma]||b.pt}</button>`;
  });
  $("listaLivros").innerHTML = html;
  $("listaLivros").classList.remove("oculto");
  $("listaCapitulos").classList.add("oculto");
  $("listaLivros").querySelectorAll("button").forEach(btn=>btn.addEventListener("click", ()=>{
    const info = infoLivro(btn.dataset.livro);
    $("listaLivros").classList.add("oculto");
    const caps = Array.from({length:info.ch},(_,i)=>`<button data-cap="${i+1}">${i+1}</button>`).join("");
    $("listaCapitulos").innerHTML = caps;
    $("listaCapitulos").classList.remove("oculto");
    $("listaCapitulos").querySelectorAll("button").forEach(cb=>cb.addEventListener("click", ()=>{
      alternarPainel("painelLivros", false);
      irPara(info.id, +cb.dataset.cap);
    }));
  }));
}

/* ---------- busca ---------- */
async function buscar(){
  const x = t(), termo = $("campoBusca").value.trim();
  const res = $("buscaResultados"), status = $("buscaStatus");
  res.innerHTML = "";
  if(termo.length < 3){ status.textContent = x.digiteBusca; return; }
  const norm = (s)=>s.normalize("NFD").replace(/[\u0300-\u036f]/g,"").toLowerCase();
  const alvo = norm(termo);
  const livros = $("chkBibliaToda").checked ? est.meta.books.map(b=>b.id) : [est.livro];
  let achados = [], n = 0;
  for(const usfm of livros){
    n++;
    if(livros.length>1) status.textContent = `${x.buscando}… ${nomeLivro(usfm)} (${n}/${livros.length})`;
    const livro = await carregarLivro(est.traducao, usfm);
    if(!livro) continue;
    livro.forEach((capversos, ci)=>{
      capversos.forEach((texto, vi)=>{
        if(texto && norm(texto).includes(alvo)) achados.push({usfm, cap:ci+1, v:vi+1, texto});
      });
    });
    if(achados.length > 400) break;
  }
  status.textContent = achados.length ? `${achados.length} ${x.resultados}` : x.nadaEncontrado;
  const re = new RegExp("("+termo.replace(/[.*+?^${}()|[\]\\]/g,"\\$&")+")","gi");
  res.innerHTML = achados.slice(0,400).map((a,i)=>
    `<div class="res" data-i="${i}"><div class="ref">${refStr(a.usfm,a.cap,a.v)}</div>
     <p>${esc(a.texto).replace(re,"<mark>$1</mark>")}</p></div>`).join("");
  res.querySelectorAll(".res").forEach(el=>el.addEventListener("click", ()=>{
    const a = achados[+el.dataset.i];
    alternarPainel("painelBusca", false);
    irPara(a.usfm, a.cap);
  }));
}

/* ---------- anotações ---------- */
function montarNotas(){
  const x = t(), alvo = $("listaNotas");
  const chaves = Object.keys(est.notas);
  if(!chaves.length){ alvo.innerHTML = `<p class="vazio">${x.semNotas}</p>`; return; }
  alvo.innerHTML = chaves.map(k=>{
    const [usfm, cap, v] = k.split(".");
    return `<div class="nota" data-k="${k}">
      <div class="ref"><span>${refStr(usfm,+cap,+v)}</span><button>${x.excluir}</button></div>
      <p>${esc(est.notas[k])}</p></div>`;
  }).join("");
  alvo.querySelectorAll(".nota").forEach(el=>{
    el.querySelector("button").addEventListener("click", (e)=>{
      e.stopPropagation();
      delete est.notas[el.dataset.k]; gravarLS("logos_notas", est.notas); montarNotas();
    });
    el.addEventListener("click", ()=>{
      const [usfm, cap] = el.dataset.k.split(".");
      alternarPainel("painelNotas", false);
      irPara(usfm, +cap);
    });
  });
}

/* ---------- painéis e tema ---------- */
function alternarPainel(id, abrir){
  const p = $(id);
  const mostrar = abrir!==undefined ? abrir : p.classList.contains("oculto");
  document.querySelectorAll(".painel").forEach(o=>o.classList.add("oculto"));
  if(mostrar) p.classList.remove("oculto");
}
function aplicarTema(){
  document.documentElement.dataset.tema = est.tema==="escuro" ? "escuro" : "claro";
  $("btnTema").textContent = est.tema==="escuro" ? "☀" : "☾";
  gravarLS("logos_tema", est.tema);
}

/* ---------- inicialização ---------- */
async function iniciar(){
  est.meta = await json("data/books.json");
  est.idioma = lerLS("logos_idioma","pt");
  est.traducao = lerLS("logos_trad","blivre");
  est.tema = lerLS("logos_tema", matchMedia("(prefers-color-scheme: dark)").matches ? "escuro":"claro");
  const m = location.hash.match(/^#\/([A-Z0-9]{3})\/(\d+)/);
  if(m && infoLivro(m[1])){ est.livro=m[1]; est.cap=+m[2]; }

  $("selIdioma").value = est.idioma;
  aplicarTextos(); preencherTraducoes(); aplicarTema();
  await renderizarCapitulo();

  $("selIdioma").addEventListener("change", (e)=>{
    est.idioma = e.target.value; gravarLS("logos_idioma", est.idioma);
    aplicarTextos(); preencherTraducoes(); gravarLS("logos_trad", est.traducao);
    renderizarCapitulo();
  });
  $("selTraducao").addEventListener("change", (e)=>{
    est.traducao = e.target.value; gravarLS("logos_trad", est.traducao);
    preencherTraducoes(); renderizarCapitulo();
  });
  $("selComparar").addEventListener("change", (e)=>{ est.comparar = e.target.value; renderizarCapitulo(); });
  $("btnLivros").addEventListener("click", ()=>{ montarListaLivros(); alternarPainel("painelLivros"); });
  $("btnBusca").addEventListener("click", ()=>{ alternarPainel("painelBusca"); $("campoBusca").focus(); });
  $("btnNotas").addEventListener("click", ()=>{ montarNotas(); alternarPainel("painelNotas"); });
  $("btnTema").addEventListener("click", ()=>{ est.tema = est.tema==="escuro"?"claro":"escuro"; aplicarTema(); });
  $("btnBuscar").addEventListener("click", buscar);
  $("campoBusca").addEventListener("keydown", (e)=>{ if(e.key==="Enter") buscar(); });
  document.querySelectorAll(".fechar").forEach(b=>b.addEventListener("click", ()=>alternarPainel(b.dataset.fecha, false)));
  document.querySelectorAll(".painel").forEach(p=>p.addEventListener("click", (e)=>{ if(e.target===p) p.classList.add("oculto"); }));
  window.addEventListener("hashchange", ()=>{
    const h = location.hash.match(/^#\/([A-Z0-9]{3})\/(\d+)/);
    if(h && infoLivro(h[1]) && (h[1]!==est.livro || +h[2]!==est.cap)){ est.livro=h[1]; est.cap=+h[2]; renderizarCapitulo(); }
  });
}
iniciar();
