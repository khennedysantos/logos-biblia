/* Transforma o video.html em MP4: tira uma foto de cada quadro e junta com o ffmpeg.
   uso:  python3 -m http.server 8000                 (na raiz do site, em outro terminal)
         node ferramentas/video/capturar.cjs          (fotos do site; só quando o site mudar)
         node ferramentas/video/renderizar.cjs        (uns 2 minutos)
   Sai em ferramentas/video/saida/sola-apresentacao.mp4 (1080×1920, 30 qps, H.264, trilha de áudio muda).
   Para conferir instantes sem gerar o vídeo:  node ferramentas/video/renderizar.cjs --fotos 2,6,13.5 */
const fs = require("fs"), path = require("path"), { execFileSync } = require("child_process");
const { chromium } = require("playwright");
const SITE = process.env.SITE || "http://localhost:8000";
const QPS = 30, ABAS = 4;
const QUADROS = path.join(__dirname, "quadros"), SAIDA = path.join(__dirname, "saida");

(async () => {
  const iFotos = process.argv.indexOf("--fotos");
  const fotos = iFotos > 0 ? process.argv[iFotos + 1].split(",").map(Number) : null;
  fs.rmSync(QUADROS, { recursive: true, force: true });
  fs.mkdirSync(QUADROS, { recursive: true }); fs.mkdirSync(SAIDA, { recursive: true });
  const nav = await chromium.launch();
  const ctx = await nav.newContext({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1, serviceWorkers: "block" });
  const abrir = async () => {
    const p = await ctx.newPage();
    p.on("pageerror", (e) => { console.error("ERRO NA PÁGINA", e.message); process.exitCode = 1; });
    p.on("requestfailed", (r) => console.error("não carregou:", r.url()));
    p.on("response", (r) => { if (r.status() >= 400) { console.error(r.status(), r.url()); process.exitCode = 1; } });
    await p.goto(SITE + "/ferramentas/video/video.html?quadros");
    await p.evaluate(() => window.pronto);
    return p;
  };
  const quadro = async (p, ms, arquivo, tipo) => {
    await p.evaluate((ms) => { window.irPara(ms); return new Promise((ok) => requestAnimationFrame(() => requestAnimationFrame(ok))); }, ms);
    await p.screenshot(tipo === "png" ? { path: arquivo } : { path: arquivo, type: "jpeg", quality: 97 });
  };

  if (fotos) {
    const p = await abrir();
    for (const s of fotos) await quadro(p, s * 1000, path.join(SAIDA, `foto-${s.toFixed(2).padStart(5, "0")}.png`), "png");
    await nav.close(); return;
  }

  const paginas = await Promise.all(Array.from({ length: ABAS }, abrir));
  const total = Math.round((await paginas[0].evaluate(() => window.DURACAO)) * QPS);
  let feitos = 0; const inicio = Date.now();
  await Promise.all(paginas.map(async (p, k) => {
    for (let i = k; i < total; i += ABAS) {
      await quadro(p, (i * 1000) / QPS, path.join(QUADROS, `q${String(i).padStart(5, "0")}.jpg`));
      if (++feitos % 150 === 0) console.log(`${feitos}/${total} quadros (${Math.round((Date.now() - inicio) / 1000)} s)`);
    }
  }));
  await nav.close();
  const mp4 = path.join(SAIDA, "sola-apresentacao.mp4");
  execFileSync("ffmpeg", ["-y", "-loglevel", "error", "-framerate", String(QPS), "-i", path.join(QUADROS, "q%05d.jpg"),
    "-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=44100", "-shortest",
    "-c:v", "libx264", "-preset", "slow", "-crf", "17", "-pix_fmt", "yuv420p", "-profile:v", "high", "-level", "4.2",
    "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
    "-c:a", "aac", "-b:a", "96k", "-movflags", "+faststart", mp4], { stdio: "inherit" });
  fs.rmSync(QUADROS, { recursive: true, force: true });
  console.log(`pronto: ${mp4} (${(fs.statSync(mp4).size / 1048576).toFixed(1)} MB, ${total} quadros)`);
})();
