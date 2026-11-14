/* Tira as fotos do site que entram no vídeo de apresentação (celular, 390×844, 3x).
   uso:  python3 -m http.server 8000         (na raiz do site, em outro terminal)
         node ferramentas/video/capturar.cjs
   Grava em ferramentas/video/telas/ (fora do git) as imagens e o medidas.json com as posições
   dos botões, que a animação usa para rolar a tela e mostrar os toques. */
const fs = require("fs"), path = require("path");
const { chromium } = require("playwright");
const SITE = process.env.SITE || "http://localhost:8000";
const TELAS = path.join(__dirname, "telas");
const L = 390, A = 844;

(async () => {
  fs.mkdirSync(TELAS, { recursive: true });
  const nav = await chromium.launch(), medidas = {};
  const novo = async (comEstudo) => {
    const c = await nav.newContext({ viewport: { width: L, height: A }, deviceScaleFactor: 3, isMobile: true, hasTouch: true,
      serviceWorkers: "block", reducedMotion: "reduce", colorScheme: "light" });
    await c.addInitScript((comEstudo) => {
      localStorage.setItem("logos_convite", JSON.stringify({ n: 3, ate: Date.now() + 9e9 }));   // sem o convite de login nas fotos
      if (!comEstudo || localStorage.getItem("logos_lidos")) return;
      const dia = 864e5, agora = Date.now(), lidos = {};
      const por = (l, n, d0) => { for (let i = 1; i <= n; i++) lidos[l + "." + i] = agora - dia * Math.max(0, d0 - Math.floor(i / 3)); };
      por("JHN", 21, 9); por("ROM", 11, 5); por("PSA", 34, 11); por("GEN", 18, 10); por("EPH", 6, 2); por("PHP", 4, 1);
      localStorage.setItem("logos_lidos", JSON.stringify(lidos));
      localStorage.setItem("logos_marcas", JSON.stringify({ "JHN.3.16": "ouro", "ROM.8.28": "verde", "PSA.23.1": "ouro", "EPH.2.8": "rosa", "ROM.5.1": "azul", "JHN.14.6": "ouro" }));
      localStorage.setItem("logos_notas", JSON.stringify({ "JHN.3.16": "O amor de Deus é a causa da salvação.", "ROM.8.28": "Todas as coisas.", "EPH.2.8": "Graça, fé, dom." }));
    }, comEstudo);
    const p = await c.newPage();
    p.on("pageerror", (e) => console.log("ERRO NA PÁGINA", e.message));
    return p;
  };
  const foto = (p, nome, op = {}) => p.screenshot({ path: path.join(TELAS, nome + ".png"), ...op });
  // faixa comprida da página, para rolar dentro do celular; os botões fixos de baixo sairiam no meio dela
  const faixa = async (p, nome, y, alt) => {
    const estilo = await p.addStyleTag({ content: ".rodape-nav{visibility:hidden!important}" });
    await foto(p, nome, { fullPage: true, clip: { x: 0, y, width: L, height: alt } });
    await estilo.evaluate((el) => el.remove());
  };
  const centro = (loc, s) => loc.evaluate((el, s) => { const r = el.getBoundingClientRect(); return [Math.round(r.left + r.width / 2), Math.round(r.top + scrollY + r.height / 2 - s)]; }, s);
  const abrirVerso = async (p, endereco) => {
    await p.goto(SITE + endereco); await p.waitForSelector(".verso.ativo"); await p.waitForTimeout(500);
    const v = p.locator(".verso.ativo");
    const s = await v.evaluate((el) => Math.round(el.getBoundingClientRect().top + scrollY - 104));
    await p.evaluate((s) => scrollTo(0, s), s); await p.waitForTimeout(200);
    return [v, s];
  };

  // 1. página inicial (visitante novo)
  let p = await novo(false);
  await p.goto(SITE + "/"); await p.waitForSelector("#versoDia:not(:empty)"); await p.waitForTimeout(500);
  medidas.cabInicio = await p.evaluate(() => Math.round(document.querySelector(".topo").getBoundingClientRect().bottom));
  await foto(p, "inicio");
  await faixa(p, "inicio-rolo", 0, 1500);

  // 2. João 1: do alto do capítulo até o versículo 14, depois o original e o léxico
  await p.goto(SITE + "/biblia/joao/1/"); await p.waitForSelector(".verso .barra", { state: "attached" }); await p.waitForTimeout(400);
  medidas.cab = await p.evaluate(() => Math.round(document.querySelector(".topo").getBoundingClientRect().bottom));
  await foto(p, "cap");
  let [v, s] = await abrirVerso(p, "/biblia/joao/1/#v14");
  medidas.s = s; const ALT = 1500;
  medidas.toqueVerso = await centro(v.locator("p").first(), s);
  await faixa(p, "j1-ativo", s, ALT);
  await p.goto(SITE + "/biblia/joao/1/"); await p.waitForSelector(".verso .barra", { state: "attached" }); await p.waitForTimeout(400);
  await faixa(p, "j1-rolo", 0, s + ALT);
  [v, s] = await abrirVerso(p, "/biblia/joao/1/#v14");
  medidas.toqueOriginal = await centro(v.locator('.acao[data-acao="original"]'), s);
  await v.locator('.acao[data-acao="original"]').evaluate((el) => el.click()); await p.waitForSelector(".inter-palavra"); await p.waitForTimeout(600);
  await faixa(p, "j1-original", s, ALT);
  const ultima = v.locator(".inter-palavra").last();
  medidas.toquePalavra = await centro(ultima, s);
  await ultima.evaluate((el) => el.click()); await p.waitForSelector(".lex-caixa:not(:empty)"); await p.waitForTimeout(600);
  medidas.lexico = await v.locator(".lex-caixa").evaluate((el, s) => { const r = el.getBoundingClientRect(); return [Math.round(r.top + scrollY - s), Math.round(r.height)]; }, s);
  await faixa(p, "j1-lexico", s, ALT);

  // 3. hebraico: Salmo 23
  [v, s] = await abrirVerso(p, "/biblia/salmos/23/#v1");
  await v.locator('.acao[data-acao="original"]').evaluate((el) => el.click()); await p.waitForSelector(".inter-palavra"); await p.waitForTimeout(600);
  await p.evaluate((s) => scrollTo(0, s), s); await p.waitForTimeout(200); await foto(p, "hebraico");

  // 4. João 3:16: comentário e referências
  [v, s] = await abrirVerso(p, "/biblia/joao/3/#v16");
  medidas.toqueComentario = await centro(v.locator('.acao[data-acao="comentario"]'), s);
  medidas.toqueRefs = await centro(v.locator('.acao[data-acao="referencias"]'), s);
  await foto(p, "j3-ativo");
  for (const a of ["comentario", "referencias"]) {
    await v.locator(`.acao[data-acao="${a}"]`).evaluate((el) => el.click()); await p.waitForTimeout(800);
    await p.evaluate((s) => scrollTo(0, s), s); await p.waitForTimeout(200); await foto(p, "j3-" + a);
  }

  // 5. "Meu estudo" de quem já leu bastante, e a aba Perfil
  p = await novo(true);
  await p.goto(SITE + "/biblia/joao/3/"); await p.waitForSelector(".verso .barra", { state: "attached" });
  await p.evaluate(() => document.getElementById("btnMeuEstudo").click()); await p.waitForSelector(".estudo-numeros"); await p.waitForTimeout(900);
  await foto(p, "estudo");
  await p.click('#abasEstudo .aba[data-aba="perfil"]'); await p.waitForSelector(".perfil-topo"); await p.waitForTimeout(600);
  await foto(p, "perfil");

  fs.writeFileSync(path.join(TELAS, "medidas.js"), "window.MEDIDAS = " + JSON.stringify(medidas) + ";\n");
  console.log(medidas);
  await nav.close();
})();
