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
