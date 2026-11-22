/* Vídeo narrado vertical (Reels/Stories, 1080×1920, 30 qps): cenas animadas no tempo da voz, legendas, trilha de fundo.
   A receita (nov/2026): voz no ElevenLabs (voz "Carlos – Resonant, Majestic Storyteller", Multilingual v2), piano calmo
   do Pixabay Music por baixo, tudo acelerado 12% (a voz sem mudar de tom), música ~12 dB abaixo e abaixando sob a fala.

   uso:  python3 -m http.server 8000                                   (na raiz do site, em outro terminal)
         python3 ferramentas/video/narrado/alinhar.py <episódio>        (tempos.json, a partir da voz)
         node ferramentas/video/narrado/renderizar.cjs <episódio> --previa 2,11,30   (fotos de instantes, para conferir)
         node ferramentas/video/narrado/renderizar.cjs <episódio> [--vel 1.12] [--sem-musica]
   Entrada (fora do git): entrada/<episódio>/voz.mp3 e entrada/<episódio>/musica.mp3 ou entrada/musica.mp3.
   Saída: ferramentas/video/saida/<episódio>.mp4 (~3 min para 85 s de vídeo).

   Cada episódio é uma pasta em episodios/ com roteiro.txt, tempos.json (do alinhar.py) e cenas.cjs, que exporta
   { telas, montar }. telas: fotos do site a tirar antes (nome → { url, preparar(page) }), num celular 390×1150 a 3x.
   montar({ tempos, LIVRO, tela }) devolve { css, cenas: [{ classe, ini, fim, html }], semLegenda: [blocos],
   dados, atualizar(t, dados) }. Elementos com class="e" e data-t="<segundos>" entram com um leve deslize nesse
   instante; o tempo é o do áudio original (antes de acelerar). As legendas vêm de tempos.legendas. */
const fs = require("fs"), path = require("path"), { spawn } = require("child_process");
const { chromium } = require("playwright");
const SITE = process.env.SITE || "http://localhost:8000";
const AQUI = __dirname, SAIDA = path.join(AQUI, "..", "saida");
const QPS = 30, CAUDA = 1.6;
const LIVRO = (cor, tam) => `<svg width="${tam}" height="${tam}" viewBox="0 0 24 24"><g fill="none" stroke="${cor}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" transform="translate(0 1)"><path d="M3 8c3-1.8 6-1.8 9 0c3-1.8 6-1.8 9 0v12c-3-1.8-6-1.8-9 0c-3-1.8-6-1.8-9 0z"/><path d="M12 8v12"/></g><circle cx="12" cy="4.2" r="1.7" fill="${cor}"/></svg>`;
const BASE = `
@font-face{font-family:"Cormorant Garamond";font-weight:600;src:url(/fontes/cormorant-garamond-latin-600-normal.woff2)}
@font-face{font-family:"Cormorant Garamond";font-weight:600;src:url(/fontes/cormorant-garamond-latin-ext-600-normal.woff2);unicode-range:U+0100-024F}
@font-face{font-family:"Cormorant Garamond";font-weight:500;font-style:italic;src:url(/fontes/cormorant-garamond-latin-500-italic.woff2)}
@font-face{font-family:"Cardo";src:url(/fontes/cardo-latin-400-normal.woff2);unicode-range:U+0000-00FF,U+2000-206F}
@font-face{font-family:"Cardo";src:url(/fontes/cardo-latin-ext-400-normal.woff2);unicode-range:U+0100-02FF,U+1E00-1EFF}
@font-face{font-family:"Cardo";font-style:italic;src:url(/fontes/cardo-latin-400-italic.woff2)}
@font-face{font-family:"Cardo";src:url(/fontes/cardo-greek-400-normal.woff2);unicode-range:U+0370-03FF}
@font-face{font-family:"Cardo";src:url(/fontes/cardo-greek-ext-400-normal.woff2);unicode-range:U+1F00-1FFF}
@font-face{font-family:"Cardo";src:url(/fontes/cardo-hebrew-400-normal.woff2);unicode-range:U+0590-05FF,U+FB1D-FB4F}
@font-face{font-family:"Inter";font-weight:100 900;src:url(/fontes/inter-latin-wght-normal.woff2)}
@font-face{font-family:"Inter";font-weight:100 900;src:url(/fontes/inter-latin-ext-wght-normal.woff2);unicode-range:U+0100-024F}
*{box-sizing:border-box;margin:0}
body{width:1080px;height:1920px;overflow:hidden;background:#171613;font-variant-numeric:lining-nums;-webkit-font-smoothing:antialiased}
.s{position:absolute;inset:0;overflow:hidden;opacity:0;font-family:Inter}
.claro{background:linear-gradient(180deg,#FDFBF6,#EFE8DA);color:#1D1B18}
.escuro{background:radial-gradient(ellipse at 50% 40%,#2A2620,#141210 70%);color:#F4EFE4}
.verm{background:linear-gradient(170deg,#9E3429,#6E1F18);color:#FAF7F0}
.mold{position:absolute;inset:30px;border:1.5px solid #C6BBA3;border-radius:6px;z-index:8;pointer-events:none}
.mold::after{content:"";position:absolute;inset:9px;border:1px solid rgba(140,45,35,.22);border-radius:4px}
.escuro .mold{border-color:rgba(212,174,106,.35)} .escuro .mold::after{border-color:rgba(212,174,106,.15)}
.verm .mold{border-color:rgba(244,239,228,.45)} .verm .mold::after{border-color:rgba(244,239,228,.2)}
.marca{position:absolute;top:250px;left:96px;display:flex;align-items:center;gap:18px;font:600 40px "Cormorant Garamond";letter-spacing:.42em}
.rot{font:700 26px Inter;letter-spacing:.22em;text-transform:uppercase;color:#8C2D23}
.escuro .rot{color:#D4AE6A}
.centro{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:0 100px}
.fio{width:340px;height:2px;background:linear-gradient(90deg,transparent,#B08A4A,transparent);margin:44px auto;position:relative}
.fio::after{content:"";position:absolute;left:50%;top:50%;width:14px;height:14px;background:#8C2D23;transform:translate(-50%,-50%) rotate(45deg)}
.titulo{font:600 118px/1 "Cormorant Garamond"}
.titulo em{font-style:italic;font-weight:500;color:#8C2D23}
.linha{font:500 38px/1.4 Inter;color:#454038}
.cel{position:absolute;left:50%;width:560px;height:760px;margin-left:-280px;border-radius:60px;background:#1D1B18;padding:16px;box-shadow:0 30px 90px rgba(60,40,20,.3)}
.cel > div{width:100%;height:100%;border-radius:46px;overflow:hidden;background:#FAF7F0;position:relative}
.cel img{position:absolute;left:-4.75%;top:0;width:109.5%;max-width:none}
/* cartão final, igual em todos os episódios */
.url{font:600 84px "Cormorant Garamond";background:#FAF7F0;color:#8C2D23;padding:16px 52px 26px;border-radius:16px;margin:34px 0 40px}
.verm .linha{color:rgba(250,247,240,.92);font-size:40px}
.siga{margin-top:50px;font:600 34px Inter;letter-spacing:.06em;color:#E4C98E}
.lema{font:500 italic 56px "Cormorant Garamond";color:#FAF7F0;margin-top:40px}
.credito{position:absolute;bottom:250px;left:0;right:0;text-align:center;font:400 22px Inter;color:rgba(250,247,240,.55)}
/* legenda: acima da faixa que o Instagram cobre embaixo */
#leg{position:absolute;left:80px;right:80px;top:1440px;z-index:20;text-align:center;opacity:0}
#leg span{display:inline;font:600 44px/1.5 Inter;color:#FAF7F0;background:rgba(23,22,19,.86);padding:6px 18px;border-radius:10px;
  -webkit-box-decoration-break:clone;box-decoration-break:clone}`;

/* o cartão final do Sola, para os episódios usarem: cartaoFinal(t0, tLema) */
const cartaoFinal = (t, tGratis, tLema) => `<div class="mold"></div><div class="centro">
  <div class="e" data-t="${t + 0.05}">${LIVRO("#FAF7F0", 120)}</div>
  <div class="url e" data-t="${t + 0.15}">solabiblia.com.br</div>
  <p class="linha e" data-t="${tGratis}">Gratuito e sem anúncios</p>
  <p class="lema e" data-t="${tLema}">Sola Scriptura</p>
  <p class="siga e" data-t="${tLema + 0.3}">Siga @projetosolabiblia</p></div>
  <p class="credito e" data-t="${tLema + 0.5}">Voz: ElevenLabs</p>`;

function definir(t, cfg) {
  const suave = (x) => x <= 0 ? 0 : x >= 1 ? 1 : 1 - Math.pow(1 - x, 3), TR = .45;
  document.querySelectorAll(".s").forEach((s, i) => {
    const [a, b] = cfg.cenas[i], ultima = i === cfg.cenas.length - 1;
    let op = 0;
    if (t >= a - (i ? TR : 0) && t <= b + (ultima ? 99 : 0)) op = Math.min(1, i ? (t - (a - TR)) / TR : 1, ultima ? 1 : (b - t) / TR + 1);
    op = Math.max(0, Math.min(1, op));
    s.style.opacity = op; s.style.zIndex = op > 0 ? 10 + i : 0;
    if (op <= 0) return;
    s.querySelectorAll(".e").forEach((el) => {
      const k = suave((t - +el.dataset.t) / .6);
      el.style.opacity = k; el.style.transform = `translateY(${(1 - k) * (el.classList.contains("cel") ? 90 : 30)}px)`;
    });
  });
  const leg = document.getElementById("leg"), l = cfg.legendas.find((x) => t >= x.ini && t < x.fim + .25);
  if (l) { leg.firstChild.textContent = l.texto; leg.style.opacity = Math.min(1, (t - l.ini) / .12, (l.fim + .25 - t) / .12); }
  else leg.style.opacity = 0;
}

(async () => {
  const ep = process.argv[2];
  if (!ep) { console.log("uso: node renderizar.cjs <episódio> [--previa 2,11] [--vel 1.12] [--sem-musica]"); process.exit(1); }
  const arg = (n) => { const i = process.argv.indexOf(n); return i > 0 ? process.argv[i + 1] : null; };
  const VEL = +(arg("--vel") || 1.12), previa = arg("--previa");
  const dir = path.join(AQUI, "episodios", ep);
  const tempos = JSON.parse(fs.readFileSync(path.join(dir, "tempos.json"), "utf8"));
  const voz = path.join(AQUI, "entrada", ep, "voz.mp3");
  const musica = [path.join(AQUI, "entrada", ep, "musica.mp3"), path.join(AQUI, "entrada", "musica.mp3")].find((f) => fs.existsSync(f));
  const roteiro = require(path.join(dir, "cenas.cjs"));
  const nav = await chromium.launch();
  // fotos do site
  const telas = {};
  for (const [nome, { url, preparar }] of Object.entries(roteiro.telas || {})) {
    const c = await nav.newContext({ viewport: { width: 390, height: 1150 }, deviceScaleFactor: 3, serviceWorkers: "block", reducedMotion: "reduce" });
    await c.addInitScript(() => { localStorage.setItem("logos_tema", JSON.stringify("claro")); localStorage.setItem("logos_convite", JSON.stringify({ n: 9, ate: Date.now() + 9e11 })); });
    const p = await c.newPage();
    await p.goto(SITE + url); await p.waitForTimeout(1500);
    if (preparar) await preparar(p);
    await p.waitForTimeout(600);
    telas[nome] = "data:image/png;base64," + (await p.screenshot()).toString("base64");
    await c.close();
  }
  const m = roteiro.montar({ tempos, LIVRO, tela: (n) => telas[n], cartaoFinal });
  const FIM = tempos.duracao + CAUDA;
  const cfg = { cenas: m.cenas.map((c) => [c.ini, c.fim]), legendas: tempos.legendas.filter((l) => !(m.semLegenda || []).includes(l.bloco)) };
  const html = m.cenas.map((c) => `<section class="s ${c.classe || "claro"}">${c.html}</section>`).join("") + `<div id="leg"><span></span></div>`;
  const pg = await nav.newPage({ viewport: { width: 1080, height: 1920 } });
  await pg.goto(SITE + "/robots.txt");
  await pg.evaluate(([css, html]) => { document.open(); document.write(`<!doctype html><meta charset="utf-8"><style>${css}</style><body>${html}</body>`); document.close(); }, [BASE + (m.css || ""), html]);
  await pg.evaluate(() => document.fonts.ready); await pg.evaluate(() => Promise.all([...document.images].map((i) => i.decode())));
  // atualizar pode vir como método ("atualizar(t, d) {…}"): vira function para valer como expressão
  const fn = m.atualizar ? m.atualizar.toString() : "()=>{}", expr = /^(function|\(|\w+\s*=>)/.test(fn) ? fn : "function " + fn;
  await pg.addScriptTag({ content: `window.definir = ${definir.toString()};\nwindow.atualizar = ${expr};` });
  const quadro = (t) => pg.evaluate(([t, cfg, dados]) => { definir(t, cfg); window.atualizar(t, dados); }, [t, cfg, m.dados || {}]);
  fs.mkdirSync(SAIDA, { recursive: true });
  if (previa) {
    for (const t of previa.split(",").map(Number)) { await quadro(t); await pg.screenshot({ path: path.join(SAIDA, `${ep}-previa-${t}.png`) }); }
    console.log("prévias em", SAIDA); await nav.close(); return;
  }
  // um ffmpeg só: quadros pela entrada padrão + voz acelerada (mesmo tom) + música abaixando sob a fala
  const T = (FIM / VEL).toFixed(2), saida = path.join(SAIDA, `${ep}.mp4`);
  const comMusica = musica && !process.argv.includes("--sem-musica");
  const filtro = [`[0:v]setpts=PTS/${VEL},fps=${QPS}[v]`,
    `[1:a]aresample=44100,atempo=${VEL},apad=whole_dur=${T}${comMusica ? ",asplit=2[voz][chave]" : "[a]"}`];
  if (comMusica) filtro.push(
    `[2:a]aresample=44100,pan=mono|c0=0.5*c0+0.5*c1,afade=t=in:st=0:d=1.5,afade=t=out:st=${(T - 3.5).toFixed(2)}:d=3.5,volume=0.17[mus]`,
    `[mus][chave]sidechaincompress=threshold=0.03:ratio=4:attack=60:release=700:makeup=1[musd]`,
    `[voz][musd]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.95[a]`);
  const ff = spawn("ffmpeg", ["-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", String(QPS), "-c:v", "mjpeg", "-i", "-",
    "-i", voz, ...(comMusica ? ["-i", musica] : []), "-filter_complex", filtro.join(";"), "-map", "[v]", "-map", "[a]", "-t", T,
    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "medium", "-crf", "18", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", saida],
    { stdio: ["pipe", "inherit", "inherit"] });
  const N = Math.round(FIM * QPS);
  for (let f = 0; f < N; f++) {
    await quadro(f / QPS);
    const q = await pg.screenshot({ type: "jpeg", quality: 92 });
    if (!ff.stdin.write(q)) await new Promise((r) => ff.stdin.once("drain", r));
    if (f % 300 === 0) console.log(`quadro ${f}/${N}`);
  }
  ff.stdin.end(); await new Promise((r) => ff.on("close", r));
  await nav.close(); console.log(`pronto: ${saida} (${T} s${comMusica ? ", com música" : ""})`);
})();
