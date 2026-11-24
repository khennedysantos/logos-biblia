/* Catecismo de Heidelberg, Domingo 2 (perguntas 3 a 5): as cenas do vídeo narrado (ver ../../renderizar.cjs).
   Os instantes vêm do tempos.json; ini(b, i) = início da i-ésima frase do bloco b do roteiro.txt. */
const telas = {
  // o plano dos 52 Domingos com o Domingo 2 aberto
  heidelberg: { url: "/", preparar: async (p) => {
    await p.evaluate(() => { montarPlanos("heidelberg"); alternarPainel("painelPlanos", true); });
    await p.waitForTimeout(1000);
    await p.click(".dia-cat >> nth=1");
    await p.waitForTimeout(400);
    await p.evaluate(() => document.querySelectorAll(".dia-cat")[1].scrollIntoView({ block: "start" }));
  } },
};

function montar({ tempos, tela, cartaoFinal }) {
  const B = tempos.blocos, F = (b) => tempos.frases.filter((f) => f.bloco === b);
  const ini = (b, i = 0) => F(b)[i].ini;
  const fim = tempos.duracao + 1.6;
  return {
    css: `
.pergunta-grande{font:600 110px/1.08 "Cormorant Garamond";color:#F4EFE4}
.pergunta-grande em{font-style:italic;font-weight:500;color:#D4AE6A}
.dom{font:600 200px/1 Inter;letter-spacing:-.03em;color:#8C2D23}
.sub2{font:600 40px Inter;color:#1D1B18;margin-top:18px} .sub2 span{font-weight:500;color:#8A8274}
.tres{display:flex;flex-direction:column;gap:26px;width:860px;margin-top:70px}
.item{display:flex;align-items:center;gap:34px;background:#FBF8F1;border:1.5px solid #D8CDB6;border-radius:18px;padding:28px 36px;text-align:left;transition:none}
.item b{flex:0 0 auto;width:90px;height:90px;border-radius:50%;background:#C9BFAB;color:#FAF7F0;display:grid;place-items:center;font:600 52px "Cormorant Garamond"}
.item div{font:600 56px/1.05 "Cormorant Garamond";color:#9A9284}
.item.on{border-color:#8C2D23;background:#FFF;box-shadow:0 10px 40px rgba(140,45,35,.15)}
.item.on b{background:#8C2D23} .item.on div{color:#1D1B18}
.qa{position:absolute;left:96px;right:96px;top:250px}
.qa .p{font:600 76px/1.08 "Cormorant Garamond";margin-top:18px}
.qa .r{font:600 italic 96px/1.1 "Cormorant Garamond";color:#8C2D23;margin-top:46px}
.qa .r small{display:block;font:700 24px Inter;letter-spacing:.22em;text-transform:uppercase;color:#8A8274;font-style:normal;margin-bottom:10px}
.verso{background:#FBF8F1;border:1.5px solid #D8CDB6;border-radius:22px;padding:40px 48px;text-align:left;margin-top:70px}
.verso p{font:400 48px/1.45 Cardo}
.verso mark{background:linear-gradient(transparent 60%,rgba(201,168,106,.55) 60%);color:#8C2D23}
.verso span{display:block;margin-top:22px;font:600 24px Inter;letter-spacing:.08em;text-transform:uppercase;color:#8A8274}
.mand{position:absolute;left:96px;right:96px;top:470px;display:flex;flex-direction:column;gap:26px}
.tab{background:#FBF8F1;border:1.5px solid #D8CDB6;border-radius:22px;padding:30px 40px;text-align:left}
.tab h3{font:600 58px/1.1 "Cormorant Garamond"} .tab h3 i{font-style:normal;color:#8C2D23}
.tab .chips{display:flex;flex-wrap:wrap;gap:12px;margin-top:20px}
.tab .chip{font:600 28px Inter;padding:10px 22px;border-radius:999px;background:#8C2D23;color:#FAF7F0}
.coracao{font:600 italic 64px/1.15 "Cormorant Garamond";color:#8C2D23;text-align:center;margin-top:16px}
.ref{font:600 24px Inter;letter-spacing:.08em;text-transform:uppercase;color:#8A8274}
.nao{font:600 300px/1 "Cormorant Garamond";color:#D4AE6A;margin-top:30px}
.resp5{font:400 52px/1.45 Cardo;color:#F4EFE4;max-width:860px;margin-top:30px}
.linha2{font:600 76px/1.15 "Cormorant Garamond"} .linha2 em{font-style:italic;font-weight:500;color:#8C2D23}
.cel{top:560px}`,
    semLegenda: [0, 2, 4, 5, 6],              // o que a voz diz já está escrito na tela
    cenas: [
      { classe: "escuro", ini: 0, fim: B[1].ini, html: `<div class="mold"></div><div class="centro">
        <p class="rot e" data-t="0.1">Catecismo de Heidelberg · Domingo 2</p><div class="fio e" data-t="0.2" style="margin:40px auto 50px"></div>
        <p class="pergunta-grande e" data-t="0.15">Como você conhece a sua <em>miséria</em>?</p></div>` },
      { ini: B[1].ini, fim: B[2].ini, html: `<div class="mold"></div><div class="centro" style="justify-content:flex-start;padding-top:280px">
        <p class="rot e" data-t="${B[1].ini + .1}">Domingo</p><p class="dom e" data-t="${B[1].ini + .25}">2</p>
        <p class="sub2 e" data-t="${B[1].ini + .5}">perguntas 3 a 5 <span>· de 129 do catecismo</span></p>
        <p class="linha e" data-t="${ini(1, 1)}" style="margin-top:30px">das três coisas que precisamos saber</p>
        <div class="tres"><div class="item e" id="i1" data-t="${ini(1, 1) + .3}"><b>1</b><div>A nossa miséria</div></div>
          <div class="item e" data-t="${ini(1, 1) + .5}"><b>2</b><div>A nossa redenção</div></div>
          <div class="item e" data-t="${ini(1, 1) + .7}"><b>3</b><div>A nossa gratidão</div></div></div></div>` },
      { ini: B[2].ini, fim: B[3].ini, html: `<div class="mold"></div>
        <div class="qa"><p class="rot e" data-t="${B[2].ini + .05}">Catecismo · Pergunta 3 de 129</p><p class="p e" data-t="${ini(2, 1)}">Como conheces a tua miséria?</p>
          <p class="r e" data-t="${ini(2, 3)}"><small>Resposta</small>Pela Lei de Deus.</p>
          <div class="verso e" data-t="${ini(2, 4) + .2}"><p>Assim, ninguém será justificado diante dele pelas obras da Lei, porque o que vem pela Lei é o <mark>conhecimento do pecado</mark>.</p><span>Romanos 3:20 · Bíblia Livre</span></div></div>` },
      { ini: B[3].ini, fim: B[4].ini, html: `<div class="mold"></div>
        <div class="qa"><p class="rot e" data-t="${B[3].ini + .05}">Catecismo · Pergunta 4 de 129</p><p class="p e" data-t="${ini(3, 1)}">Que exige de nós a Lei de Deus?</p></div>
        <div class="mand">
          <div class="tab e" data-t="${ini(3, 3)}"><h3><i>1.</i> Amarás o Senhor teu Deus</h3><div class="chips">${["de todo o coração", "de toda a alma", "de todo o entendimento", "de todas as forças"].map((c, i) => `<span class="chip e" data-t="${[ini(3, 3) + .5, ini(3, 4), ini(3, 5), ini(3, 5) + 1.4][i]}">${c}</span>`).join("")}</div></div>
          <div class="tab e" data-t="${ini(3, 6)}"><h3><i>2.</i> Amarás o teu próximo como a ti mesmo</h3></div>
          <p class="ref e" data-t="${ini(3, 6) + .4}" style="text-align:center">Mateus 22:37-40</p>
          <p class="coracao e" data-t="${ini(3, 8)}">não só atos:<br>o coração inteiro</p></div>` },
      { classe: "escuro", ini: B[4].ini, fim: B[5].ini, html: `<div class="mold"></div><div class="centro" style="justify-content:flex-start;padding-top:300px">
        <p class="rot e" data-t="${B[4].ini + .05}">Catecismo · Pergunta 5 de 129</p>
        <p class="pergunta-grande e" data-t="${ini(4, 1)}" style="font-size:84px;margin-top:24px">Podes guardar tudo isso perfeitamente?</p>
        <p class="nao e" data-t="${ini(4, 2)}">Não.</p>
        <p class="resp5 e" data-t="${ini(4, 3)}">Por natureza estou inclinado a odiar a Deus e ao meu próximo.</p></div>` },
      { ini: B[5].ini, fim: B[6].ini, html: `<div class="mold"></div><div class="centro" style="justify-content:flex-start;padding-top:420px">
        <p class="linha2 e" data-t="${B[5].ini + .1}">Uma resposta dura.</p><div class="fio e" data-t="${ini(5, 1)}"></div>
        <p class="linha2 e" data-t="${ini(5, 1)}">o <em>diagnóstico</em><br>antes do <em>remédio</em></p>
        <p class="linha e" data-t="${ini(5, 2)}" style="margin-top:56px">Só quem conhece a doença<br>procura o médico.</p></div>` },
      { ini: B[6].ini, fim: B[7].ini, html: `<div class="mold"></div>
        <p class="rot e" data-t="${B[6].ini + .05}" style="position:absolute;top:290px;left:0;right:0;text-align:center">No Sola</p>
        <p class="linha2 e" data-t="${B[6].ini + .15}" style="position:absolute;top:350px;left:0;right:0;text-align:center;font-size:64px">Heidelberg em <em>52 Domingos</em></p>
        <div class="cel e" data-t="${B[6].ini + .25}"><div><img id="tela" src="${tela("heidelberg")}"></div></div>` },
      { classe: "verm", ini: B[7].ini, fim, html: cartaoFinal(B[7].ini, ini(7, 1), ini(7, 3)) },
    ],
    dados: { mis: ini(1, 3), rolar: B[6].ini + .8, rolarDur: B[7].ini - B[6].ini - 1 },
    atualizar(t, d) {
      const suave = (x) => x <= 0 ? 0 : x >= 1 ? 1 : 1 - Math.pow(1 - x, 3);
      document.getElementById("i1").classList.toggle("on", t >= d.mis);
      document.getElementById("tela").style.transform = `translateY(${-suave((t - d.rolar) / d.rolarDur) * 300}px)`;
    },
  };
}
module.exports = { telas, montar };
