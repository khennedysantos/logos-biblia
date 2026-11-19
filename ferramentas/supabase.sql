-- Sola — contas e sincronização (Supabase)
--
-- Cole este arquivo inteiro no SQL Editor do projeto (painel do Supabase → SQL Editor → New query → Run).
-- Pode rodar mais de uma vez sem estragar nada.
--
-- O que ele cria: uma tabela só, "itens". Cada linha é uma coisa do estudo de uma pessoa:
--   tipo = nota | marca | plano | lido | estado       chave = "JHN.3.16", "anual.12", "JHN.3", "ultimo"
--   valor = o conteúdo (texto da anotação, cor da marcação...)     apagado = a pessoa removeu
--   ts = quando foi alterado, no relógio do aparelho (milissegundos) — entre dois aparelhos, vale o mais recente
-- A regra de segurança (RLS) faz cada pessoa ver e alterar só as próprias linhas; sem ela, a chave
-- pública que vai no site deixaria qualquer um ler tudo. Não desligue o RLS desta tabela.

create table if not exists public.itens (
  user_id       uuid        not null default auth.uid() references auth.users (id) on delete cascade,
  tipo          text        not null check (tipo in ('nota', 'marca', 'plano', 'lido', 'estado')),
  chave         text        not null check (char_length(chave) between 1 and 80),
  valor         jsonb                check (valor is null or pg_column_size(valor) < 60000),
  apagado       boolean     not null default false,
  ts            bigint      not null default 0,
  atualizado_em timestamptz not null default now(),
  primary key (user_id, tipo, chave)
);

create index if not exists itens_por_data on public.itens (user_id, atualizado_em);

alter table public.itens enable row level security;

drop policy if exists "cada pessoa só mexe no que é seu" on public.itens;
create policy "cada pessoa só mexe no que é seu" on public.itens
  for all to authenticated
  using ((select auth.uid()) = user_id)
  with check ((select auth.uid()) = user_id);

revoke all on public.itens from anon;
grant select, insert, update, delete on public.itens to authenticated;

-- a data de alteração é sempre a do servidor (é por ela que cada aparelho pede "o que mudou desde...")
create or replace function public.itens_carimbar() returns trigger
  language plpgsql set search_path = '' as $$
begin
  new.atualizado_em := now();
  return new;
end $$;

drop trigger if exists itens_carimbar on public.itens;
create trigger itens_carimbar before insert or update on public.itens
  for each row execute function public.itens_carimbar();

-- limite de linhas por pessoa (1.189 capítulos + anotações e marcações cabem com muita folga)
create or replace function public.itens_limite() returns trigger
  language plpgsql security definer set search_path = '' as $$
begin
  if (select count(*) from public.itens where user_id = new.user_id) >= 40000 then
    raise exception 'limite de itens por conta atingido';
  end if;
  return new;
end $$;

drop trigger if exists itens_limite on public.itens;
create trigger itens_limite before insert on public.itens
  for each row execute function public.itens_limite();

-- "Excluir minha conta" (botão em Meu estudo): apaga o usuário, e a tabela vai junto (on delete cascade)
create or replace function public.apagar_conta() returns void
  language sql security definer set search_path = '' as $$
  delete from auth.users where id = (select auth.uid());
$$;

revoke all on function public.apagar_conta() from public, anon;
grant execute on function public.apagar_conta() to authenticated;

-- ------------------------------------------------------------------------------------------------------------------
-- Página pública do perfil (opcional): solabiblia.com.br/perfil/<apelido>/
--
-- Só existe para quem liga "Publicar perfil" na aba Perfil do app. Uma linha por pessoa: o apelido (o endereço) e
-- um retrato do cartão do perfil (nome, avatar, capa, bio, versículo de vida e, se a pessoa escolher, os números do
-- estudo, as conquistas e a prateleira). Qualquer visitante lê, porque a pessoa decidiu tornar público; gravar e
-- apagar, só pelas funções publicar_perfil() e despublicar_perfil(), cada um o seu. Anotações, marcações e o resto
-- do estudo continuam só em "itens", privados. Excluir a conta apaga a página junto (on delete cascade).
-- Para tirar do ar um perfil impróprio: Table Editor → perfis_publicos → apagar a linha.

create table if not exists public.perfis_publicos (
  user_id       uuid        primary key references auth.users (id) on delete cascade,
  apelido       text        not null unique,
  dados         jsonb       not null check (pg_column_size(dados) < 60000),
  atualizado_em timestamptz not null default now()
);

alter table public.perfis_publicos enable row level security;

drop policy if exists "perfis publicados são públicos" on public.perfis_publicos;
create policy "perfis publicados são públicos" on public.perfis_publicos
  for select to anon, authenticated using (true);

-- ninguém grava direto na tabela, e quem lê vê só o apelido e o cartão (nunca o user_id)
revoke all on public.perfis_publicos from anon, authenticated;
grant select (apelido, dados, atualizado_em) on public.perfis_publicos to anon, authenticated;

-- Regras do apelido: 3 a 30 letras minúsculas sem acento, números e hífens (sem hífen no começo, no fim ou dobrado),
-- fora os endereços reservados e os palavrões. A mesma lista está no app.js (APELIDO_*): mudou aqui, mude lá.
create or replace function public.apelido_permitido(a text) returns boolean
  language sql immutable set search_path = '' as $$
  select a ~ '^[a-z0-9][a-z0-9-]{1,28}[a-z0-9]$' and position('--' in a) = 0
    and a <> all (array['sola','solabiblia','sola-biblia','admin','administrador','administracao','suporte','contato',
      'ajuda','oficial','equipe','moderador','moderacao','root','sistema','perfil','perfis','biblia','api','www','null',
      'undefined','deus','jesus','cristo','jesus-cristo','espirito-santo','senhor','igreja'])
    and not exists (
      select 1 from unnest(string_to_array(a, '-')) as s
      where s = any (array['puta','puto','putas','putos','merda','porra','foda','fodase','foder','fodido','fodida','cu',
          'cus','cuzao','cuzinho','bosta','piroca','corno','viado','vadia','vagabunda','vagabundo','otario','babaca',
          'imbecil','cacete','buceta','boceta','xoxota','xereca','punheta','prostituta','prostituto','nazi','nazista',
          'hitler','satanas','satan','diabo','lucifer','demonio','sexo','porno','porn','xxx','anal','nude','nudes',
          'fuck','fucker','fucking','shit','bitch','cunt','dick','cock','pussy','whore','slut','fag','faggot','nigger',
          'nigga','rape','rapist','asshole','bastard','kkk','mierda','joder','cono','pendejo','pendeja','cabron',
          'cabrona','verga','chinga','chingar','maricon','culo','zorra','perra','gilipollas','hijueputa'])
         or s ~ '^(arromb|vagabund|prostitut|punhet|fodid|caralh|bucet|bocet|xoxot|putari|pornog|fuck|nigg|faggot|pendej|chingad|hijueput|gilipoll|retardad|nazis|satanis)')
    and replace(a, '-', '') !~ '(caralho|buceta|boceta|punheta|xoxota|fuck|nigger|nigga|faggot|hitler|putaria|putinha|putona)';
$$;

create or replace function public.publicar_perfil(p_apelido text, p_dados jsonb) returns void
  language plpgsql security definer set search_path = '' as $$
declare
  eu uuid := (select auth.uid());
begin
  if eu is null then raise exception 'sem_conta'; end if;
  if not public.apelido_permitido(p_apelido) then raise exception 'apelido_invalido'; end if;
  if jsonb_typeof(p_dados) <> 'object' or pg_column_size(p_dados) >= 60000 then raise exception 'dados_invalidos'; end if;
  insert into public.perfis_publicos (user_id, apelido, dados) values (eu, p_apelido, p_dados)
  on conflict (user_id) do update set apelido = excluded.apelido, dados = excluded.dados, atualizado_em = now();
exception when unique_violation then
  raise exception 'apelido_em_uso';
end $$;

create or replace function public.despublicar_perfil() returns void
  language sql security definer set search_path = '' as $$
  delete from public.perfis_publicos where user_id = (select auth.uid());
$$;

revoke all on function public.publicar_perfil(text, jsonb) from public, anon;
revoke all on function public.despublicar_perfil() from public, anon;
grant execute on function public.publicar_perfil(text, jsonb) to authenticated;
grant execute on function public.despublicar_perfil() to authenticated;
