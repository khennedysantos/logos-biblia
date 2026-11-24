/* Palavra da semana: hesed (H2617). Cenas do vídeo narrado (ver ../../renderizar.cjs).
   Os instantes vêm do tempos.json; cada bloco do roteiro.txt é uma cena (o 5º, Salmo 136 + Lamentações, vira duas). */
const telas = {
  // Miqueias 6:8 no interlinear, com o cartão do léxico de hesed aberto (o mesmo que o mantenedor mostrou)
  miqueias: { url: "/biblia/miqueias/6/", preparar: async (p) => {
    await p.evaluate(() => document.getElementById("v8").scrollIntoView({ block: "start" }));
    await p.click("#v8 > p"); await p.waitForTimeout(400);
    await p.click('#v8 [data-acao="original"]'); await p.waitForTimeout(1200);
    await p.click('#v8 .inter-palavra[data-strong^="H2617"]'); await p.waitForTimeout(800);
    await p.evaluate(() => { const r = document.querySelector('#v8 .inter-palavra[data-strong^="H2617"]').getBoundingClientRect(); window.scrollBy(0, r.top - 120); });
  } },
};

function montar({ tempos, tela, cartaoFinal }) {
  const B = tempos.blocos, F = (b) => tempos.frases.filter((f) => f.bloco === b);
  const ini = (b, i = 0) => F(b)[i].ini;
  const fim = tempos.duracao + 1.6;
  const verso = (ref, html, t) => `<div class="verso e" data-t="${t}"><p>${html}</p><span>${ref} · Bíblia Livre</span></div>`;
  return {
    css: `
.heb{font:400 300px/1 Cardo;color:#F4EFE4;direction:rtl}
.tr{font:500 italic 74px "Cormorant Garamond";color:#D4AE6A;margin-top:30px}
.sub{font:500 38px/1.4 Inter;color:rgba(244,239,228,.8);margin-top:60px}
.num b{display:block;font:600 230px/1 Inter;letter-spacing:-.03em;color:#8C2D23}
.num span{display:block;font:600 30px Inter;letter-spacing:.12em;text-transform:uppercase;color:#6D665A;margin-top:12px}
.barra{width:760px;height:26px;border-radius:13px;background:#E8DFCC;margin:56px auto 14px;overflow:hidden}
.barra i{display:block;height:100%;width:0;background:#B08A4A;border-radius:13px}
.barra-rot{font:500 30px Inter;color:#6D665A}
.trads{display:flex;flex-wrap:wrap;gap:18px;justify-content:center;margin-top:70px;max-width:860px}
.trad{font:600 56px "Cormorant Garamond";padding:12px 34px;border-radius:999px;background:#FBF8F1;border:1.5px solid #D8CDB6;color:#8C2D23}
.frase{font:600 76px/1.12 "Cormorant Garamond";margin-top:34px}
.frase em{font-style:italic;font-weight:500;color:#8C2D23}
.verso{width:880px;background:#FBF8F1;border:1.5px solid #D8CDB6;border-radius:22px;padding:46px 52px;text-align:left;margin-top:56px}
.verso p{font:400 52px/1.45 Cardo}
.verso mark{background:linear-gradient(transparent 60%,rgba(201,168,106,.55) 60%);color:#8C2D23}
.verso span{display:block;margin-top:24px;font:600 24px Inter;letter-spacing:.08em;text-transform:uppercase;color:#8A8274}
.contexto{font:500 30px Inter;color:#6D665A;margin-top:20px}
.refrao{display:flex;flex-direction:column;gap:6px;margin-top:40px}
.refrao div{font:400 italic 40px Cardo;color:#8C2D23;opacity:.18}
.refrao div.on{opacity:1}
.n26{font:600 150px/1 Inter;color:#1D1B18}
.tres3{display:flex;flex-direction:column;gap:22px;width:860px;margin-top:56px}
.tres3 div{font:600 58px "Cormorant Garamond";background:#FBF8F1;border:1.5px solid #D8CDB6;border-radius:18px;padding:24px 34px;text-align:left}
.tres3 div.ouro{border-color:#B08A4A;background:#F6EBD3;color:#8C2D23}
.cel{top:430px}`,
    semLegenda: [0, 3, 4, 5],                 // nas cenas de versículo o texto já está na tela
    cenas: [
      { classe: "escuro", ini: 0, fim: B[1].ini, html: `<div class="mold"></div><div class="centro">
        <p class="rot e" data-t="0.1">Palavra da semana · hebraico</p>
        <p class="heb e" data-t="0.3" style="margin-top:60px">חֶסֶד</p>
        <p class="tr e" data-t="${ini(0, 1) - .2}">hesed</p>
        <p class="sub e" data-t="${ini(0, 1) + .2}">a palavra que nenhuma<br>tradução diz inteira</p></div>` },
      { ini: B[1].ini, fim: B[2].ini, html: `<div class="mold"></div><div class="centro" style="justify-content:flex-start;padding-top:300px">
        <div class="num e" data-t="${B[1].ini + .1}"><b id="n250">250</b><span>vezes no Antigo Testamento</span></div>
        <div class="barra e" data-t="${ini(1, 1)}"><i id="barra"></i></div><p class="barra-rot e" data-t="${ini(1, 1) + .2}">mais da metade nos Salmos</p>
        <p class="rot e" data-t="${ini(1, 2)}" style="margin-top:80px">As Bíblias traduzem</p>
        <div class="trads">${["bondade", "misericórdia", "benignidade", "lealdade"].map((w, i) => `<span class="trad e" data-t="${ini(1, 2 + i) + (i ? 0 : 1.2)}">${w}</span>`).join("")}</div></div>` },
      { ini: B[2].ini, fim: B[3].ini, html: `<div class="mold"></div><div class="centro" style="justify-content:flex-start;padding-top:330px">
        <p class="rot e" data-t="${B[2].ini + .1}">Mais que um sentimento</p>
        <p class="frase e" data-t="${ini(2, 1)}">o amor de quem fez<br>uma <em>aliança</em></p>
        <p class="frase e" data-t="${ini(2, 1) + 1.6}">e não volta atrás</p><div class="fio e" data-t="${ini(2, 2)}"></div>
        <p class="frase e" data-t="${ini(2, 2)}" style="font-size:64px">um amor <em>leal</em>, que permanece<br>quando o outro falha</p></div>` },
      { ini: B[3].ini, fim: B[4].ini, html: `<div class="mold"></div><div class="centro" style="justify-content:flex-start;padding-top:330px">
        <p class="rot e" data-t="${B[3].ini + .1}">Êxodo 34 · no Sinai</p>
        <p class="contexto e" data-t="${B[3].ini + .3}">logo depois do bezerro de ouro</p>
        ${verso("Êxodo 34:6", "SENHOR, SENHOR, forte, misericordioso, e piedoso; tardio para a ira, e grande em <mark>benignidade</mark> e verdade", ini(3, 1))}</div>` },
      { ini: B[4].ini, fim: ini(4, 3), html: `<div class="mold"></div><div class="centro" style="justify-content:flex-start;padding-top:300px">
        <p class="rot e" data-t="${B[4].ini + .1}">Salmo 136</p>
        <div class="e" data-t="${ini(4, 1)}"><span class="n26" id="n26">26</span><p class="contexto">vezes o mesmo refrão</p></div>
        <div class="refrao">${"<div>porque a sua bondade dura para sempre</div>".repeat(8)}</div></div>` },
      { ini: ini(4, 3), fim: B[5].ini, html: `<div class="mold"></div><div class="centro" style="justify-content:flex-start;padding-top:330px">
        <p class="rot e" data-t="${ini(4, 3) + .1}">Lamentações 3</p>
        <p class="contexto e" data-t="${ini(4, 4)}">nas ruínas de Jerusalém</p>
        ${verso("Lamentações 3:22-23", "É pelas <mark>bondades</mark> do SENHOR que não somos consumidos [...] Elas são novas a cada manhã", ini(4, 5))}</div>` },
      { ini: B[5].ini, fim: B[6].ini, html: `<div class="mold"></div><div class="centro" style="justify-content:flex-start;padding-top:330px">
        <p class="rot e" data-t="${B[5].ini + .1}">Miqueias 6:8</p>
        <p class="frase e" data-t="${B[5].ini + .3}" style="font-size:70px">E Deus pede o mesmo <em>de nós</em></p>
        <div class="tres3"><div class="e" data-t="${ini(5, 2)}">fazer o que é justo</div><div class="ouro e" data-t="${ini(5, 3)}">amar a bondade <span style="font:400 40px Cardo">· חֶסֶד</span></div>
          <div class="e" data-t="${ini(5, 4)}">andar humildemente com o teu Deus</div></div></div>` },
      { ini: B[6].ini, fim: B[7].ini, html: `<div class="mold"></div>
        <p class="rot e" data-t="${B[6].ini + .05}" style="position:absolute;top:290px;left:0;right:0;text-align:center">Miqueias 6:8 no interlinear do Sola</p>
        <div class="cel e" data-t="${B[6].ini + .2}"><div><img id="tela" src="${tela("miqueias")}"></div></div>` },
      { classe: "verm", ini: B[7].ini, fim, html: cartaoFinal(B[7].ini, ini(7, 1), ini(7, 3)) },
    ],
    dados: { b1: B[1].ini, barra: ini(1, 1), b4: ini(4, 1), b4f: ini(4, 3), rolar: B[6].ini + 1.2, rolarDur: B[7].ini - B[6].ini - 1.4 },
    atualizar(t, d) {
      const suave = (x) => x <= 0 ? 0 : x >= 1 ? 1 : 1 - Math.pow(1 - x, 3);
      document.getElementById("n250").textContent = Math.round(250 * suave((t - d.b1 - .1) / 1.6));
      document.getElementById("barra").style.width = (100 * 127 / 247 * suave((t - d.barra) / 1.2)) + "%";
      const k = suave((t - d.b4) / (d.b4f - d.b4 - .4));
      document.getElementById("n26").textContent = Math.max(1, Math.round(26 * k));
      document.querySelectorAll(".refrao div").forEach((el, i) => el.classList.toggle("on", k * 8 > i));
      document.getElementById("tela").style.transform = `translateY(${-suave((t - d.rolar) / d.rolarDur) * 260}px)`;
    },
  };
}
module.exports = { telas, montar };
