/* Especial de Advento e Natal (domingo, 29/11/2026): o plano "Advento com Calvino" e as leituras de /natal/.
   Cenas do vídeo narrado (ver ../../renderizar.cjs); os instantes vêm do tempos.json, um bloco do roteiro.txt por cena. */
const telas = {
  // o plano do Advento aberto no painel de planos (abre no dia de hoje enquanto nada foi marcado)
  advento: { url: "/", preparar: async (p) => {
    await p.evaluate(() => { montarPlanos("advento"); alternarPainel("painelPlanos", true); });
    await p.waitForTimeout(1200);
  } },
  natal: { url: "/natal/" },
};

function montar({ tempos, tela }) {
  const B = tempos.blocos, F = (b) => tempos.frases.filter((f) => f.bloco === b);
  // início da i-ésima frase do bloco b (se o bloco tiver menos frases, um pouco depois da última)
  const ini = (b, i = 0) => { const f = F(b); return f[i] ? f[i].ini : f[f.length - 1].ini + 1.2 * (i - f.length + 1); };
  const fim = tempos.duracao + 1.6;
  const grupo = (rot, itens, t, dt) => `<div class="grupo e" data-t="${t}"><p class="rot">${rot}</p>${
    itens.map((x, i) => `<div class="it e" data-t="${t + .25 + i * dt}">${x}</div>`).join("")}</div>`;
  return {
    css: `
.abre{font:600 104px/1.12 "Cormorant Garamond";color:#F4EFE4}
.abre em{font-style:italic;font-weight:500;color:#D4AE6A}
.verso{width:880px;background:#FBF8F1;border:1.5px solid #D8CDB6;border-radius:22px;padding:46px 52px;text-align:left;margin-top:56px}
.verso p{font:400 52px/1.45 Cardo}
.verso mark{background:linear-gradient(transparent 60%,rgba(201,168,106,.55) 60%);color:#8C2D23}
.verso span{display:block;margin-top:24px;font:600 24px Inter;letter-spacing:.08em;text-transform:uppercase;color:#8A8274}
.frase{font:600 76px/1.12 "Cormorant Garamond";margin-top:34px}
.frase em{font-style:italic;font-weight:500;color:#8C2D23}
.n27 b{display:block;font:600 260px/1 Inter;letter-spacing:-.03em;color:#8C2D23}
.n27 span{display:block;font:600 32px Inter;letter-spacing:.12em;text-transform:uppercase;color:#6D665A;margin-top:14px}
.datas{font:500 italic 80px "Cormorant Garamond";color:#1D1B18;margin-top:50px}
.grupos{display:flex;flex-direction:column;gap:34px;width:880px;margin-top:20px;text-align:left}
.grupo .rot{margin-bottom:14px}
.grupo{display:flex;flex-wrap:wrap;gap:12px 14px;align-items:center}
.grupo .rot{flex:0 0 100%}
.it{font:600 46px "Cormorant Garamond";background:#FBF8F1;border:1.5px solid #D8CDB6;border-radius:999px;padding:8px 28px}
.it.ouro{border-color:#B08A4A;background:#F6EBD3;color:#8C2D23}
.cartoes{display:flex;flex-direction:column;gap:34px;width:880px;margin-top:60px}
.cartao{text-align:left;border:1.5px solid rgba(212,174,106,.4);background:rgba(212,174,106,.07);border-radius:22px;padding:40px 46px}
.cartao b{display:block;font:600 70px/1.05 "Cormorant Garamond";color:#F4EFE4}
.cartao span{display:block;font:500 32px/1.4 Inter;color:rgba(244,239,228,.75);margin-top:12px}
.cartao i{display:inline-block;font:700 26px Inter;font-style:normal;letter-spacing:.1em;color:#D4AE6A;margin-bottom:12px}
.cit{font:400 italic 82px/1.3 Cardo;color:#F4EFE4;max-width:880px}
.aut{font:600 32px Inter;letter-spacing:.06em;color:#D4AE6A;margin-top:50px}
.url2{font:600 72px "Cormorant Garamond";background:#FAF7F0;color:#8C2D23;padding:16px 46px 24px;border-radius:16px;margin:34px 0 40px}
.cel{top:400px}`,
    semLegenda: [6],                           // a citação de Gregório já está na tela
    cenas: [
      { classe: "escuro", ini: 0, fim: B[1].ini, html: `<div class="mold"></div><div class="centro">
        <p class="rot e" data-t="0.1">Especial de Advento</p>
        <p class="abre e" data-t="0.3" style="margin-top:60px">O Natal não começa<br>em Belém.</p>
        <p class="abre e" data-t="${ini(0, 1) - .1}" style="margin-top:40px"><em>Começa no Éden.</em></p></div>` },
      { ini: B[1].ini, fim: B[2].ini, html: `<div class="mold"></div><div class="centro" style="justify-content:flex-start;padding-top:330px">
        <p class="rot e" data-t="${B[1].ini + .1}">Gênesis 3:15 · a primeira promessa</p>
        <div class="verso e" data-t="${B[1].ini + .4}"><p>E inimizade porei entre ti e a mulher, e entre tua descendência e a descendência dela; <mark>esta te ferirá na cabeça</mark>, e tu lhe ferirás no calcanhar.</p><span>Gênesis 3:15 · Bíblia Livre</span></div></div>` },
      { ini: B[2].ini, fim: B[3].ini, html: `<div class="mold"></div><div class="centro" style="justify-content:flex-start;padding-top:330px">
        <p class="rot e" data-t="${B[2].ini + .1}">Hoje começa o Advento</p>
        <p class="frase e" data-t="${ini(2, 1)}" style="font-size:96px">Advento com <em>Calvino</em></p>
        <div class="n27 e" data-t="${ini(2, 2)}" style="margin-top:70px"><b id="n27">27</b><span>dias de leitura</span></div>
        <p class="datas e" data-t="${ini(2, 2) + .8}">29 nov → 25 dez</p></div>` },
      { ini: B[3].ini, fim: B[4].ini, html: `<div class="mold"></div><div class="centro" style="justify-content:flex-start;padding-top:300px"><div class="grupos">
        ${grupo("As promessas", ["Abraão", "o cetro de Judá", "a estrela de Jacó"], B[3].ini + .1, .55)}
        ${grupo("Os profetas", ["Emanuel", "o Menino que nos nasceu", "o Servo ferido", "Belém Efrata"], ini(3, 1), .6)}
        ${grupo("O nascimento", ["o anúncio a Maria", "os pastores", `<span style="color:#8C2D23">o Verbo se fez carne</span>`], ini(3, 2), .7)}
        </div></div>` },
      { ini: B[4].ini, fim: B[5].ini, html: `<div class="mold"></div>
        <p class="rot e" data-t="${B[4].ini + .05}" style="position:absolute;top:290px;left:0;right:0;text-align:center">Um tema e Calvino em cada dia</p>
        <div class="cel e" data-t="${B[4].ini + .2}"><div><img id="tela" src="${tela("advento")}"></div></div>` },
      { classe: "escuro", ini: B[5].ini, fim: B[6].ini, html: `<div class="mold"></div><div class="centro" style="justify-content:flex-start;padding-top:330px">
        <p class="rot e" data-t="${B[5].ini + .1}">Leituras de Natal · em português</p>
        <div class="cartoes">
          <div class="cartao e" data-t="${ini(5, 0) + 2.6}"><i>ANO 380</i><b>Gregório de Nazianzo</b><span>Sermão 38, sobre o Natal de Cristo</span></div>
          <div class="cartao e" data-t="${ini(5, 0) + 5}"><i>1855</i><b>Charles H. Spurgeon</b><span>A encarnação e o nascimento de Cristo, sobre Miqueias 5:2</span></div>
        </div></div>` },
      { classe: "escuro", ini: B[6].ini, fim: B[7].ini, html: `<div class="mold"></div><div class="centro">
        <p class="cit e" data-t="${B[6].ini + .1}">“Cristo nasce: glorificai-o.</p>
        <p class="cit e" data-t="${ini(6, 1) - .1}" style="margin-top:24px">Cristo vem do céu: saí ao seu encontro.”</p>
        <p class="aut e" data-t="${ini(6, 1) + .4}">Gregório de Nazianzo, Natal de 380</p></div>` },
      { classe: "verm", ini: B[7].ini, fim, html: `<div class="mold"></div><div class="centro">
        <p class="lema e" data-t="${B[7].ini + .05}" style="margin-top:0">Especial de Natal</p>
        <div class="url2 e" data-t="${B[7].ini + .15}">solabiblia.com.br/natal</div>
        <p class="linha e" data-t="${ini(7, 1)}">Gratuito e sem anúncios</p>
        <p class="lema e" data-t="${ini(7, 2)}">Sola Scriptura</p>
        <p class="siga e" data-t="${ini(7, 2) + .3}">Siga @projetosolabiblia</p></div>
        <p class="credito e" data-t="${ini(7, 2) + .5}">Voz: ElevenLabs</p>` },
    ],
    dados: { n27: ini(2, 2), rolar: B[4].ini + 1, rolarDur: B[5].ini - B[4].ini - 1.2 },
    atualizar(t, d) {
      const suave = (x) => x <= 0 ? 0 : x >= 1 ? 1 : 1 - Math.pow(1 - x, 3);
      document.getElementById("n27").textContent = Math.max(1, Math.round(27 * suave((t - d.n27) / 1.4)));
      document.getElementById("tela").style.transform = `translateY(${-suave((t - d.rolar) / d.rolarDur) * 900}px)`;
    },
  };
}
module.exports = { telas, montar };
