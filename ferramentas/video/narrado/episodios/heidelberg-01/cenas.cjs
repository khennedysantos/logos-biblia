/* Catecismo de Heidelberg, Domingo 1: as cenas do vídeo narrado (ver ../../renderizar.cjs).
   Os instantes vêm do tempos.json (blocos e frases do roteiro.txt casados com a voz pelo alinhar.py),
   então dá para refazer com outra gravação sem mexer aqui. */
const telas = {
  // o plano dos 52 Domingos aberto, com o Domingo 1 expandido
  heidelberg: { url: "/", preparar: async (p) => {
    await p.evaluate(() => { montarPlanos("heidelberg"); alternarPainel("painelPlanos", true); });
    await p.waitForTimeout(1000);
    await p.click(".dia-cat >> nth=0");
  } },
};

function montar({ tempos, LIVRO, tela, cartaoFinal }) {
  const B = tempos.blocos, F = (b) => tempos.frases.filter((f) => f.bloco === b);
  const ini = (b, i = 0) => F(b)[i].ini;                       // início da i-ésima frase do bloco b
  const resp = F(3).slice(1);                                   // a resposta da pergunta 1, sem "E a resposta é esta:"
  const fim = tempos.duracao + 1.6;
  const autor = (n, s, t) => `<div class="autor e" data-t="${t}">${n}<small>${s}</small></div>`;
  return {
    css: `
.pergunta-grande{font:600 104px/1.08 "Cormorant Garamond";color:#F4EFE4}
.pergunta-grande em{font-style:italic;font-weight:500;color:#D4AE6A}
.ano{font:600 170px/1.05 Inter;letter-spacing:-.02em;color:#8C2D23;margin-top:6px}
.autores{display:flex;gap:30px;justify-content:center;margin-top:56px}
.autor{border:1.5px solid #D8CDB6;background:#FBF8F1;border-radius:14px;padding:22px 30px;font:600 46px "Cormorant Garamond"}
.autor small{display:block;font:500 22px Inter;color:#8A8274;margin-top:6px;letter-spacing:.04em}
.nums{display:flex;gap:110px;justify-content:center;align-items:flex-end;margin-top:60px}
.num b{display:block;font:600 200px/1 Inter;letter-spacing:-.03em}
.num span{display:block;font:600 30px Inter;letter-spacing:.12em;text-transform:uppercase;color:#8C2D23;margin-top:10px}
.cal{display:grid;grid-template-columns:repeat(13,46px);gap:12px;justify-content:center;margin-top:70px}
.cal i{width:46px;height:46px;border-radius:10px;background:#E8DFCC}
.cal i.on{background:#8C2D23}
.q4{position:absolute;left:96px;right:96px;top:240px}
.q4 .p{font:600 72px/1.08 "Cormorant Garamond";margin-top:20px}
.resp{position:absolute;left:96px;right:96px;top:590px;font:400 47px/1.52 Cardo;padding-left:36px;border-left:4px solid #B08A4A}
.resp span{color:rgba(29,27,24,.22)}
.resp span.lida{color:#5A544A}
.resp span.agora{color:#1D1B18;background:linear-gradient(transparent 70%,rgba(201,168,106,.4) 70%)}
.resp .intro{font:italic 400 40px Cardo;color:#8C2D23;display:block;margin-bottom:18px}
.nota{position:absolute;left:96px;right:96px;bottom:300px;font:400 24px Inter;color:#8A8274}
.tres{display:flex;flex-direction:column;gap:30px;width:860px;margin-top:60px}
.item{display:flex;align-items:center;gap:34px;background:#FBF8F1;border:1.5px solid #D8CDB6;border-radius:18px;padding:30px 36px;text-align:left}
.item b{flex:0 0 auto;width:96px;height:96px;border-radius:50%;background:#8C2D23;color:#FAF7F0;display:grid;place-items:center;font:600 56px "Cormorant Garamond"}
.item div{font:600 56px/1.05 "Cormorant Garamond"}
.item small{display:block;font:400 26px/1.35 Inter;color:#6D665A;margin-top:8px}
.chips{position:absolute;left:70px;right:70px;top:420px;display:flex;flex-wrap:wrap;gap:14px;justify-content:center}
.chip{font:600 28px Inter;padding:12px 24px;border-radius:999px;background:#8C2D23;color:#FAF7F0}
.chip.claro2{background:#FBF8F1;color:#8C2D23;border:1.5px solid #D8CDB6}`,
    semLegenda: [0, 3],                                         // a pergunta grande e a resposta já são o texto na tela
    cenas: [
      { classe: "escuro", ini: 0, fim: B[1].ini, html: `<div class="mold"></div><div class="centro">
        <p class="rot e" data-t="0.2">Catecismo de Heidelberg · Pergunta 1</p><div class="fio e" data-t="0.4" style="margin:40px auto 50px"></div>
        <p class="pergunta-grande e" data-t="0.3">Qual é o seu único <em>consolo</em>, na vida e na morte?</p></div>` },
      { ini: B[1].ini, fim: B[2].ini, html: `<div class="mold"></div><div class="centro" style="justify-content:flex-start;padding-top:290px">
        <p class="rot e" data-t="${B[1].ini + .2}">A primeira pergunta do</p>
        <p class="titulo e" data-t="${B[1].ini + .5}" style="margin-top:26px">Catecismo de <em>Heidelberg</em></p><div class="fio e" data-t="${B[1].ini + 1}"></div>
        <p class="ano e" data-t="${ini(1, 1)}">1563</p><p class="linha e" data-t="${ini(1, 2)}">Heidelberg, Alemanha</p>
        <div class="autores">${autor("Zacarias Ursino", "1534–1583", ini(1, 3))}${autor("Gaspar Oleviano", "1536–1587", ini(1, 3) + .9)}</div>
        <p class="linha e" data-t="${ini(1, 4)}" style="margin-top:50px;font-size:34px">para ensinar a fé às famílias<br>e às igrejas da Reforma</p></div>` },
      { ini: B[2].ini, fim: B[3].ini, html: `<div class="mold"></div><div class="centro" style="justify-content:flex-start;padding-top:330px">
        <p class="rot e" data-t="${B[2].ini + .1}">Como ele é organizado</p>
        <div class="nums"><div class="num e" data-t="${B[2].ini + .3}"><b id="n129">129</b><span>perguntas e<br>respostas</span></div>
          <div class="num e" data-t="${ini(2, 1)}"><b id="n52">52</b><span>Domingos</span></div></div>
        <div class="cal">${"<i></i>".repeat(52)}</div>
        <p class="linha e" data-t="${ini(2, 2)}" style="margin-top:56px">uma semana de cada vez,<br>ao longo do ano</p></div>` },
      { ini: B[3].ini, fim: B[4].ini, html: `<div class="mold"></div>
        <div class="q4"><p class="rot e" data-t="${B[3].ini + .05}">Pergunta 1</p><p class="p e" data-t="${B[3].ini + .15}">Qual é o teu único consolo na vida e na morte?</p></div>
        <p class="resp e" data-t="${B[3].ini + .25}"><span class="intro">Resposta:</span>${resp.map((r, i) => `<span id="r${i}">${r.texto}</span>`).join(" ")}</p>
        <p class="nota e" data-t="${B[3].ini + .8}">Catecismo de Heidelberg (1563), pergunta 1 (trecho) · tradução do Sola</p>` },
      { ini: B[4].ini, fim: B[5].ini, html: `<div class="mold"></div><div class="centro" style="justify-content:flex-start;padding-top:290px">
        <p class="rot e" data-t="${B[4].ini + .1}">Pergunta 2</p>
        <p class="titulo e" data-t="${B[4].ini + .3}" style="font-size:96px;margin-top:22px">Três coisas para <em>saber</em></p>
        <div class="tres">
          <div class="item e" data-t="${ini(4, 2)}"><b>1</b><div>A nossa miséria<small>quão grandes são o nosso pecado e a nossa miséria</small></div></div>
          <div class="item e" data-t="${ini(4, 3)}"><b>2</b><div>A nossa redenção<small>como somos libertados deles</small></div></div>
          <div class="item e" data-t="${ini(4, 4)}"><b>3</b><div>A nossa gratidão<small>como devemos ser gratos a Deus por essa redenção</small></div></div>
        </div></div>` },
      { ini: B[5].ini, fim: B[6].ini, html: `<div class="mold"></div>
        <div class="marca e" data-t="${B[5].ini + .05}">${LIVRO("#8C2D23", 50)}SOLA</div>
        <p class="rot e" data-t="${B[5].ini + .15}" style="position:absolute;top:350px;left:96px">Tudo isso no Sola</p>
        <div class="chips"><span class="chip e" data-t="${ini(5, 1)}">Heidelberg em 52 Domingos</span><span class="chip claro2 e" data-t="${ini(5, 2)}">Confissão de Westminster</span>
          <span class="chip claro2 e" data-t="${ini(5, 3)}">Catecismos</span><span class="chip claro2 e" data-t="${ini(5, 4)}">Grego e hebraico</span></div>
        <div class="cel e" data-t="${B[5].ini + .35}" style="top:600px"><div><img id="tela" src="${tela("heidelberg")}"></div></div>` },
      { classe: "verm", ini: B[6].ini, fim, html: cartaoFinal(B[6].ini, ini(6, 1), ini(6, 3)) },
    ],
    dados: { b2: B[2].ini, n52: ini(2, 1), resp: resp.map((r) => [r.ini, r.fim]), rolar: B[5].ini + 1.2, rolarDur: B[5].fim - B[5].ini - 1.5 },
    atualizar(t, d) {
      const suave = (x) => x <= 0 ? 0 : x >= 1 ? 1 : 1 - Math.pow(1 - x, 3);
      document.getElementById("n129").textContent = Math.round(129 * suave((t - d.b2 - .3) / 1.8));
      document.getElementById("n52").textContent = Math.round(52 * suave((t - d.n52) / 1.4));
      document.querySelectorAll(".cal i").forEach((c, i) => c.classList.toggle("on", t > d.n52 + .2 + i * .09));
      d.resp.forEach(([a, b], i) => { document.getElementById("r" + i).className = t >= a - .15 && t <= b + .3 ? "agora" : t > b ? "lida" : ""; });
      document.getElementById("tela").style.transform = `translateY(${-suave((t - d.rolar) / d.rolarDur) * 520}px)`;
    },
  };
}
module.exports = { telas, montar };
