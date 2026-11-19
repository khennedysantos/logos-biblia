# Contas no Sola — como ligar

O projeto no Supabase existe (`rxmxxuyqvetbkjfilayc`) e o login com Google está ligado (`google:true` em `CONTA`,
no `app.js`). Para desligar tudo de conta de uma vez — por exemplo, se o login parar de funcionar — basta voltar
para `google:false`: nada de "Entrar" aparece e o site funciona como sempre, só no aparelho da pessoa.
Os passos abaixo ficam como registro de como foi configurado.

O que a conta faz: guarda anotações, marcações, capítulos lidos, planos e "onde parei" na nuvem, para a
pessoa continuar em qualquer aparelho. Sem conta, o "Meu estudo" continua funcionando, só local.

## 1. Criar o projeto (grátis)

1. Entre em supabase.com com a sua conta do GitHub e crie um projeto (região: São Paulo).
2. Em **SQL Editor → New query**, cole o arquivo `ferramentas/supabase.sql` inteiro e clique em **Run**.
   O arquivo pode rodar de novo sem estragar nada: quando ele mudar (como na página pública do perfil, em
   nov/2026, que criou a tabela `perfis_publicos` e as funções `publicar_perfil`/`despublicar_perfil`), é só
   colar e rodar outra vez.
3. Em **Project Settings → API** (ou "API Keys"), copie:
   - o **Project URL** (`https://xxxx.supabase.co`);
   - a chave **publishable** (nos projetos antigos chama-se `anon` `public`).
   Essa chave é pública de propósito — vai dentro do site. **Nunca** use nem envie a chave `secret` /
   `service_role`: ela ignora as regras de segurança.

## 2. Endereços do site

Em **Authentication → URL Configuration**:

- **Site URL**: `https://solabiblia.com.br`
- **Redirect URLs**: `https://solabiblia.com.br/**` (e `http://localhost:8000/**` se quiser testar no computador)

## 3. Entrar com Google

1. No Google Cloud Console (console.cloud.google.com), crie um projeto, configure a **tela de consentimento
   OAuth** (tipo Externo; nome "Sola"; seu e-mail) e publique o app.
2. Em **Credenciais → Criar credenciais → ID do cliente OAuth → Aplicativo da Web**:
   - Origens JavaScript autorizadas: `https://solabiblia.com.br`
   - URIs de redirecionamento autorizados: o endereço que o Supabase mostra em
     **Authentication → Sign In / Providers → Google** ("Callback URL", algo como
     `https://xxxx.supabase.co/auth/v1/callback`).
3. Copie o **Client ID** e o **Client secret** para essa mesma tela do Supabase e ative o Google.

Só o escopo de e-mail e perfil é pedido. O site não mostra a foto do Google (seria um pedido a terceiros);
usa a inicial do nome.

## 4. Ligar no site

No começo do `app.js`:

```js
const CONTA = { url:"https://rxmxxuyqvetbkjfilayc.supabase.co", chave:"sb_publishable_...", google:true, email:false };
```

Depois `python3 ferramentas/gerar_paginas.py`, commit e push. (Ou mande a URL e a chave publishable para o
Claude, que ele faz e testa.)

## Link por e-mail (opcional, depois)

`email:true` mostra o campo "Receber link por e-mail". Só ligue depois de configurar um SMTP próprio no
Supabase (**Authentication → Emails → SMTP Settings**; o Resend tem plano grátis): o envio embutido do
Supabase é só para teste, com limite de poucos e-mails por hora.

## Como funciona por dentro

- Uma tabela, `itens`: uma linha por coisa (`tipo` + `chave`), com `valor`, `apagado` e `ts`.
  A regra de segurança (RLS) deixa cada pessoa ver e alterar só as próprias linhas.
- O aparelho continua sendo a fonte: tudo é gravado primeiro no navegador (funciona sem internet) e
  sobe depois. `est.sinc.pend` guarda o que falta subir.
- Entre dois aparelhos, no mesmo item vale a alteração mais recente (`ts`). Apagar também é uma alteração.
- Primeira vez num aparelho: o que já existia ali entra na conta. Entrou outra pessoa no mesmo aparelho:
  o site pergunta antes de trocar os dados.
- "Excluir minha conta" apaga o usuário e todas as linhas dele no servidor (função `apagar_conta`).

## O que ainda não foi testado

A sincronização foi testada com um servidor falso que imita a tabela (dois aparelhos, sem rede, conflito,
troca de conta, exclusão). O login de verdade com o Google e as regras do banco só podem ser testados
depois que o projeto existir.

## Página pública do perfil

Quem tem conta pode publicar o perfil em `solabiblia.com.br/perfil/<apelido>/` (aba Perfil → Página pública).
O GitHub Pages responde a esse endereço com o `404.html`, que é o próprio app; o app lê o cartão em
`perfis_publicos` com a chave pública (um `fetch` simples, sem o cliente do Supabase). Ninguém grava direto
na tabela: só pelas funções do `supabase.sql`, cada pessoa no próprio perfil, e o apelido passa por
`apelido_permitido()` (formato, endereços reservados e palavrões — a mesma lista do `app.js`, conferida pelo
`validar_dados.py`). Para tirar do ar um perfil impróprio: **Table Editor → perfis_publicos**, apague a linha.
