/* Série de Advento, ep. 1 (sábado, 28/11/2026): a primeira promessa, Gênesis 3:15, com o comentário de Calvino.
   Cenas do vídeo narrado (ver ../../renderizar.cjs); os instantes vêm do tempos.json, um bloco do roteiro.txt por cena. */
const telas = {};

function montar({ tempos, LIVRO }) {
  const B = tempos.blocos, F = (b) => tempos.frases.filter((f) => f.bloco === b);
  // início da i-ésima frase do bloco b (se o bloco tiver menos frases, um pouco depois da última)
  const ini = (b, i = 0) => { const f = F(b); return f[i] ? f[i].ini : f[f.length - 1].ini + 1.2 * (i - f.length + 1); };
  const fim = tempos.duracao + 1.6;
  const verso = (ref, html, t, st = "") => `<div class="verso e" data-t="${t}" style="${st}"><p>${html}</p><span>${ref} · Bíblia Livre</span></div>`;
  const topo = (t) => `style="justify-content:flex-start;padding-top:${t}px"`;
  // estrela de Belém (raios girando atrás), poeira dourada e o horizonte de Belém: animados em atualizar()
  const estrela = (id, st) => `<svg id="${id}" class="estrela" viewBox="-100 -100 200 200" style="${st}">
    <defs><radialGradient id="${id}g"><stop offset="0" stop-color="#FFF3D1"/><stop offset=".45" stop-color="#F2D9A6"/><stop offset="1" stop-color="#D4AE6A"/></radialGradient>
      <radialGradient id="${id}h"><stop offset="0" stop-color="#F7E3B5" stop-opacity=".55"/><stop offset="1" stop-color="#F7E3B5" stop-opacity="0"/></radialGradient>
      <linearGradient id="${id}r" x1="0" y1="0" x2="0" y2="-1"><stop offset="0" stop-color="#F7E3B5" stop-opacity=".5"/><stop offset="1" stop-color="#F7E3B5" stop-opacity="0"/></linearGradient></defs>
    <circle r="70" fill="url(#${id}h)" class="halo"/>
    <g class="raios">${Array.from({ length: 12 }, (_, i) => `<path d="M-3 0 L0 -98 L3 0z" fill="url(#${id}r)" transform="rotate(${i * 30})"/>`).join("")}</g>
    <g class="corpo"><path d="M0-62 7-7 62 0 7 7 0 62-7 7-62 0-7-7z" fill="url(#${id}g)"/>
    <path d="M0-30 4-4 30 0 4 4 0 30-4 4-30 0-4-4z" fill="url(#${id}g)" transform="rotate(45)"/></g></svg>`;
  const po = (cor) => `<canvas class="po" width="1080" height="1920" data-cor="${cor}"></canvas>`;
  const belem = `<svg class="belem" viewBox="0 0 1080 260" preserveAspectRatio="none"><path fill="rgba(40,8,6,.32)" d="M0 260V170h60v-30h50v40h40v-70h30l30-30 30 30h20v90h50v-50h70v-40q40-50 80 0v40h40v60h60v-90h20l40-40 40 40h20v60h70v-30h60v70h40v-110h30v-20h30v20h30v70h70v-40h60v120z"/></svg>`;
  return {
    css: `
.abre{font:600 100px/1.12 "Cormorant Garamond";color:#F4EFE4}
.sub0{font:500 40px/1.45 Inter;color:rgba(244,239,228,.8);margin-top:40px}
.abre em{font-style:italic;font-weight:500;color:#D4AE6A}
.verso{width:880px;background:#FBF8F1;border:1.5px solid #D8CDB6;border-radius:22px;padding:46px 52px;text-align:left;margin-top:56px}
.verso p{font:400 52px/1.45 Cardo}
.verso mark{background:linear-gradient(transparent 60%,rgba(201,168,106,.55) 60%);color:#8C2D23}
.verso span{display:block;margin-top:24px;font:600 24px Inter;letter-spacing:.08em;text-transform:uppercase;color:#8A8274}
.frase{font:600 76px/1.12 "Cormorant Garamond";margin-top:34px}
.frase em{font-style:italic;font-weight:500;color:#8C2D23}
.calv{width:880px;text-align:left;border-left:6px solid #B08A4A;padding:10px 0 10px 44px;margin-top:60px}
.calv p{font:400 italic 54px/1.4 Cardo}
.calv span{display:block;margin-top:22px;font:600 26px Inter;letter-spacing:.06em;color:#785C2A}
.duas{display:grid;grid-template-columns:1fr 1fr;gap:30px;width:880px;margin-top:70px}
.golpe{border-radius:22px;padding:44px 30px;border:1.5px solid #D8CDB6;background:#FBF8F1}
.golpe b{display:block;font:600 84px/1 "Cormorant Garamond"}
.golpe span{display:block;font:500 32px/1.4 Inter;color:#6D665A;margin-top:18px}
.golpe.forte{border-color:#8C2D23;background:#F6E4DF}
.golpe.forte b{color:#8C2D23}
.cabeca{font:600 130px/1 "Cormorant Garamond";color:#8C2D23;margin-top:40px}
.cit{font:400 italic 74px/1.3 Cardo;color:#F4EFE4;max-width:900px}
.aut{font:600 30px Inter;letter-spacing:.06em;color:#D4AE6A;margin-top:46px}
.fim1{font:600 96px/1.1 "Cormorant Garamond";color:#FAF7F0}
.fim1 em{font-style:italic;font-weight:500;color:#F2D9A6}
canvas.po,canvas#conv{position:absolute;inset:0;width:1080px;height:1920px}
.estrela{position:absolute;left:50%;width:300px;height:300px;margin-left:-150px;overflow:visible}
.belem{position:absolute;left:0;right:0;bottom:30px;width:1080px;height:260px}
.verso mark{background:linear-gradient(rgba(201,168,106,.55),rgba(201,168,106,.55)) no-repeat 0 92%/0% 40%}
.golpe{position:relative}.golpe b{transform-origin:50% 60%}
.onda{position:absolute;inset:-2px;border-radius:22px;border:4px solid #8C2D23;opacity:0}
.cruz{width:120px;height:150px;margin-top:50px}
.plano{margin-top:70px;font:600 34px Inter;color:#FAF7F0;background:rgba(250,247,240,.12);border:1.5px solid rgba(250,247,240,.35);border-radius:999px;padding:18px 40px}`,
    semLegenda: [1, 6, 7],                     // nos versículos e no fim o texto já está na tela
    cenas: [
      { classe: "escuro", ini: 0, fim: B[1].ini, html: `${po("244,220,170")}<div class="mold"></div>${estrela("est0", "top:300px")}<div class="centro" style="padding-top:240px">
        <p class="rot e" data-t="0.1">Série de Advento · 1</p>
        <p class="abre e" data-t="0.3" style="margin-top:60px">Bem-vindo ao <em>Advento</em></p>
        <p class="sub0 e" data-t="${ini(0, 1)}">o tempo de esperar o Natal<br>pelas promessas de Deus</p>
        <div class="fio e" data-t="${ini(0, 2)}"></div>
        <p class="abre e" data-t="${ini(0, 2)}" style="font-size:76px">A primeira vem<br><em>logo depois da queda</em></p></div>` },
      { ini: B[1].ini, fim: B[2].ini, html: `<div class="mold"></div><div class="centro" ${topo(330)}>
        <p class="rot e" data-t="${B[1].ini + .1}">Gênesis 3:15</p>
        ${verso("Gênesis 3:15", `E inimizade porei entre ti e a mulher, e entre tua descendência e a <mark data-t="${ini(1, 2) + .6}">descendência dela</mark>; esta te ferirá na <mark data-t="${ini(1, 3) + .5}">cabeça</mark>, e tu lhe ferirás no <mark data-t="${ini(1, 4) + .6}">calcanhar</mark>.`, B[1].ini + .4)}</div>` },
      { ini: B[2].ini, fim: B[3].ini, html: `<div class="mold"></div><div class="centro" ${topo(360)}>
        <p class="rot e" data-t="${B[2].ini + .1}">João Calvino, sobre Gênesis 3:15</p>
        <div class="calv e" data-t="${B[2].ini + .4}"><p>“O Senhor não falou por causa da serpente, mas por causa do homem.”</p><span>Comentário de Gênesis</span></div>
        <p class="frase e" data-t="${ini(2, 2)}" style="margin-top:80px">Por trás dela, <em>Satanás</em></p></div>` },
      { ini: B[3].ini, fim: B[4].ini, html: `<div class="mold"></div><div class="centro" ${topo(360)}>
        <p class="rot e" data-t="${B[3].ini + .1}">Os dois saem feridos</p>
        <div class="duas"><div class="golpe e" data-t="${ini(3, 2)}"><b>calcanhar</b><span>a serpente fere</span></div>
          <div class="golpe forte e" data-t="${ini(3, 3)}"><i class="onda" id="onda"></i><b id="cab">cabeça</b><span>a descendência fere</span></div></div>
        <p class="frase e" data-t="${ini(3, 4)}" style="margin-top:80px">Um golpe machuca.</p>
        <p class="frase e" data-t="${ini(3, 5)}" style="margin-top:10px"><em>O outro é derrota.</em></p></div>` },
      { ini: B[4].ini, fim: B[5].ini, html: `<canvas id="conv" width="1080" height="1920"></canvas><div class="mold"></div><div class="centro" ${topo(330)}>
        <p class="rot e" data-t="${B[4].ini + .1}">Quem é a descendência?</p>
        <p class="cabeca e" data-t="${ini(4, 4) + .7}">uma Cabeça única</p>
        ${verso("Gálatas 3:16", `E não diz: “E às descendências” como que falando de muitos, mas sim como a um: “E à tua descendência”, <mark data-t="${ini(4, 6)}">que é Cristo</mark>.`, ini(4, 5), "margin-top:70px")}</div>` },
      { ini: B[5].ini, fim: B[6].ini, html: `<div class="mold"></div><div class="centro" ${topo(330)}>
        <p class="rot e" data-t="${B[5].ini + .1}">Na plenitude dos tempos</p>
        ${verso("Gálatas 4:4", `Mas quando o tempo se completou, Deus enviou o seu Filho, <mark data-t="${ini(5, 2)}">nascido de mulher</mark>, nascido sob a Lei,`, B[5].ini + .3)}
        <svg class="cruz" viewBox="0 0 120 150"><path id="cruz" d="M60 6V144M18 48H102" fill="none" stroke="#8C2D23" stroke-width="7" stroke-linecap="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/></svg>
        <p class="frase e" data-t="${ini(5, 3)}" style="margin-top:20px">ferido na cruz,<br><em>esmagou a cabeça</em></p></div>` },
      { classe: "escuro", ini: B[6].ini, fim: B[7].ini, html: `${po("244,220,170")}<div class="mold"></div><div class="centro">
        <p class="rot e" data-t="${B[6].ini + .05}">A vitória é da Igreja</p>
        <p class="cit e" data-t="${B[6].ini + .2}" style="margin-top:50px">“E o Deus de paz esmagará Satanás em pedaços debaixo dos vossos pés.”</p>
        <p class="aut e" data-t="${B[6].ini + .6}">Romanos 16:20 · Bíblia Livre</p></div>` },
      { classe: "verm", ini: B[7].ini, fim, html: `${po("255,236,200")}${belem}<div class="mold"></div>${estrela("estF", "top:250px")}<div class="centro" style="padding-top:200px">
        <p class="fim1 e" data-t="${B[7].ini + .05}">O Natal não começa<br>em Belém.</p>
        <p class="fim1 e" data-t="${ini(7, 1)}" style="margin-top:30px"><em>Começa no Éden.</em></p>
        <div class="e" data-t="${ini(7, 3)}" style="margin-top:80px">${LIVRO("#FAF7F0", 90)}</div>
        <p class="plano e" data-t="${ini(7, 3) + .1}">Plano Advento com Calvino · solabiblia.com.br</p>
        <p class="siga e" data-t="${ini(7, 3) + .4}">Siga @projetosolabiblia</p></div>
        <p class="credito e" data-t="${ini(7, 3) + .6}">Voz: ElevenLabs</p>` },
    ],
    dados: { est0: 0.2, estF: B[7].ini, cab: ini(3, 3) + .3, c0: B[4].ini + .2, c1: ini(4, 1), c2: ini(4, 4) - .5, cruz: ini(5, 3) - .3 },
    atualizar(t, d) {
      const suave = (x) => x <= 0 ? 0 : x >= 1 ? 1 : 1 - Math.pow(1 - x, 3);
      const r = (i, k) => { const x = Math.sin(i * 127.1 + k * 311.7) * 43758.5453; return x - Math.floor(x); };
      const visivel = (el) => +el.closest(".s").style.opacity > 0;
      // estrelas: nascem, pulsam e os raios giram devagar
      for (const id of ["est0", "estF"]) {
        const s = document.getElementById(id); if (!visivel(s)) continue;
        const k = suave((t - d[id]) / 1.4);
        s.style.opacity = k; s.style.transform = `scale(${(.4 + .6 * k) * (1 + .035 * Math.sin(t * 2.6))})`;
        s.querySelector(".raios").setAttribute("transform", `rotate(${t * 7})`);
        s.querySelector(".halo").setAttribute("r", 62 + 10 * Math.sin(t * 2.1));
      }
      // poeira dourada subindo
      document.querySelectorAll("canvas.po").forEach((c) => {
        if (!visivel(c)) return;
        const g = c.getContext("2d"); g.clearRect(0, 0, 1080, 1920);
        for (let i = 0; i < 70; i++) {
          const sp = 18 + r(i, 2) * 42, y = 1920 - ((r(i, 3) * 2000 + t * sp) % 2000) + 40;
          const x = r(i, 1) * 1080 + Math.sin(t * .4 + i) * 24, tam = 1.4 + r(i, 4) * 3.2;
          const a = (.25 + .75 * (.5 + .5 * Math.sin(t * 2.2 + i * 1.7))) * .75;
          const gr = g.createRadialGradient(x, y, 0, x, y, tam * 4);
          gr.addColorStop(0, `rgba(${c.dataset.cor},${a})`); gr.addColorStop(1, `rgba(${c.dataset.cor},0)`);
          g.fillStyle = gr; g.beginPath(); g.arc(x, y, tam * 4, 0, 7); g.fill();
        }
      });
      // marcas que se pintam no tempo da fala
      document.querySelectorAll("mark[data-t]").forEach((m) => { m.style.backgroundSize = `${100 * suave((t - +m.dataset.t) / .7)}% 40%`; });
      // o golpe na cabeça
      const kc = (t - d.cab) / .9, cab = document.getElementById("cab"), onda = document.getElementById("onda");
      cab.style.transform = kc > 0 && kc < 1 ? `scale(${1 + .14 * Math.sin(kc * Math.PI) * (1 - kc)})` : "";
      onda.style.opacity = kc > 0 && kc < 1 ? 1 - kc : 0; onda.style.transform = `scale(${1 + .18 * Math.max(0, Math.min(1, kc))})`;
      // muitos filhos de Adão -> uma Cabeça única
      const cv = document.getElementById("conv");
      if (visivel(cv)) {
        const g = cv.getContext("2d"); g.clearRect(0, 0, 1080, 1920);
        const ap = suave((t - d.c0) / .8), apaga = suave((t - d.c1) / 1.4), junta = suave((t - d.c2) / 1.3), luz = suave((t - d.c2 - 1) / .8);
        const tx = 540, ty = 470;
        for (let i = 0; i < 90; i++) {
          const x0 = 90 + r(i, 5) * 900, y0 = 620 + r(i, 6) * 760, fica = r(i, 7) < .14;
          const x = x0 + (tx - x0) * junta + Math.sin(t + i) * 6 * (1 - junta), y = y0 + (ty - y0) * junta + Math.cos(t * .8 + i) * 6 * (1 - junta);
          const a = ap * (fica ? 1 : 1 - .85 * apaga) * (1 - luz) * .8;
          g.fillStyle = `rgba(176,138,74,${a})`; g.beginPath(); g.arc(x, y, fica ? 7 : 5, 0, 7); g.fill();
        }
        if (luz > 0) {
          const gr = g.createRadialGradient(tx, ty, 0, tx, ty, 260 * luz);
          gr.addColorStop(0, `rgba(242,217,166,${.75 * luz})`); gr.addColorStop(1, "rgba(242,217,166,0)");
          g.fillStyle = gr; g.beginPath(); g.arc(tx, ty, 260 * luz, 0, 7); g.fill();
        }
      }
      // a cruz se desenha
      document.getElementById("cruz").setAttribute("stroke-dashoffset", 1 - suave((t - d.cruz) / 1.1));
    },
  };
}
module.exports = { telas, montar };
