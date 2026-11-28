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
.plano{margin-top:70px;font:600 34px Inter;color:#FAF7F0;background:rgba(250,247,240,.12);border:1.5px solid rgba(250,247,240,.35);border-radius:999px;padding:18px 40px}`,
    semLegenda: [1, 6],                        // nos versículos o texto já está na tela
    cenas: [
      { classe: "escuro", ini: 0, fim: B[1].ini, html: `<div class="mold"></div><div class="centro">
        <p class="rot e" data-t="0.1">Série de Advento · 1</p>
        <p class="abre e" data-t="0.3" style="margin-top:60px">Bem-vindo ao <em>Advento</em></p>
        <p class="sub0 e" data-t="${ini(0, 1)}">o tempo de esperar o Natal<br>pelas promessas de Deus</p>
        <div class="fio e" data-t="${ini(0, 2)}"></div>
        <p class="abre e" data-t="${ini(0, 2)}" style="font-size:76px">A primeira vem<br><em>logo depois da queda</em></p></div>` },
      { ini: B[1].ini, fim: B[2].ini, html: `<div class="mold"></div><div class="centro" ${topo(330)}>
        <p class="rot e" data-t="${B[1].ini + .1}">Gênesis 3:15</p>
        ${verso("Gênesis 3:15", "E inimizade porei entre ti e a mulher, e entre tua descendência e a <mark>descendência dela</mark>; esta te ferirá na <mark>cabeça</mark>, e tu lhe ferirás no <mark>calcanhar</mark>.", B[1].ini + .4)}</div>` },
      { ini: B[2].ini, fim: B[3].ini, html: `<div class="mold"></div><div class="centro" ${topo(360)}>
        <p class="rot e" data-t="${B[2].ini + .1}">João Calvino, sobre Gênesis 3:15</p>
        <div class="calv e" data-t="${B[2].ini + .4}"><p>“O Senhor não falou por causa da serpente, mas por causa do homem.”</p><span>Comentário de Gênesis</span></div>
        <p class="frase e" data-t="${ini(2, 2)}" style="margin-top:80px">Por trás dela, <em>Satanás</em></p></div>` },
      { ini: B[3].ini, fim: B[4].ini, html: `<div class="mold"></div><div class="centro" ${topo(360)}>
        <p class="rot e" data-t="${B[3].ini + .1}">Os dois saem feridos</p>
        <div class="duas"><div class="golpe e" data-t="${ini(3, 2)}"><b>calcanhar</b><span>a serpente fere</span></div>
          <div class="golpe forte e" data-t="${ini(3, 3)}"><b>cabeça</b><span>a descendência fere</span></div></div>
        <p class="frase e" data-t="${ini(3, 4)}" style="margin-top:80px">Um golpe machuca.</p>
        <p class="frase e" data-t="${ini(3, 5)}" style="margin-top:10px"><em>O outro é derrota.</em></p></div>` },
      { ini: B[4].ini, fim: B[5].ini, html: `<div class="mold"></div><div class="centro" ${topo(330)}>
        <p class="rot e" data-t="${B[4].ini + .1}">Quem é a descendência?</p>
        <p class="cabeca e" data-t="${ini(4, 4)}">uma Cabeça única</p>
        ${verso("Gálatas 3:16", "E não diz: “E às descendências” como que falando de muitos, mas sim como a um: “E à tua descendência”, <mark>que é Cristo</mark>.", ini(4, 5), "margin-top:70px")}</div>` },
      { ini: B[5].ini, fim: B[6].ini, html: `<div class="mold"></div><div class="centro" ${topo(330)}>
        <p class="rot e" data-t="${B[5].ini + .1}">Na plenitude dos tempos</p>
        ${verso("Gálatas 4:4", "Mas quando o tempo se completou, Deus enviou o seu Filho, <mark>nascido de mulher</mark>, nascido sob a Lei,", B[5].ini + .3)}
        <p class="frase e" data-t="${ini(5, 3)}" style="margin-top:80px">ferido na cruz,<br><em>esmagou a cabeça</em></p></div>` },
      { classe: "escuro", ini: B[6].ini, fim: B[7].ini, html: `<div class="mold"></div><div class="centro">
        <p class="rot e" data-t="${B[6].ini + .05}">A vitória é da Igreja</p>
        <p class="cit e" data-t="${B[6].ini + .2}" style="margin-top:50px">“E o Deus de paz esmagará Satanás em pedaços debaixo dos vossos pés.”</p>
        <p class="aut e" data-t="${B[6].ini + .6}">Romanos 16:20 · Bíblia Livre</p></div>` },
      { classe: "verm", ini: B[7].ini, fim, html: `<div class="mold"></div><div class="centro">
        <p class="fim1 e" data-t="${B[7].ini + .05}">O Natal não começa<br>em Belém.</p>
        <p class="fim1 e" data-t="${ini(7, 1)}" style="margin-top:30px"><em>Começa no Éden.</em></p>
        <div class="e" data-t="${ini(7, 3)}" style="margin-top:80px">${LIVRO("#FAF7F0", 90)}</div>
        <p class="plano e" data-t="${ini(7, 3) + .1}">Plano Advento com Calvino · solabiblia.com.br</p>
        <p class="siga e" data-t="${ini(7, 3) + .4}">Siga @projetosolabiblia</p></div>
        <p class="credito e" data-t="${ini(7, 3) + .6}">Voz: ElevenLabs</p>` },
    ],
  };
}
module.exports = { telas, montar };
