
-- create table -> ok
SET datestyle = "ISO, DMY";
CREATE TABLE pessoa (
  idPessoa serial PRIMARY KEY,
  nome TEXT NOT NULL,
  dataNascimento date NOT NULL,
  salario numeric NOT NULL,
  observacoes TEXT
);
--adicionar colunas ok
ALTER TABLE pessoa
ADD COLUMN nomeMae TEXT,
ADD COLUMN nomePai TEXT,
ADD COLUMN cpf TEXT;



-- criando type com id -> ok
CREATE TYPE pessoa_t_id AS (
    idpessoa integer,
    nome text,
    datanascimento date,
    salario numeric,
    observacoes text,
    nomemae text,
    nomepai text,
    cpf text
);
-- criando type sem id -> ok
CREATE TYPE pessoa_t AS (
    nome text,
    datanascimento date,
    salario numeric,
    observacoes text,
    nomemae text,
    nomepai text,
    cpf text
);


--criando indices para colunas (nome, dataNascimento): ok
CREATE INDEX nome_data_index ON pessoa (nome, dataNascimento);

-- criando indice unico para cpf: -> ok
ALTER TABLE pessoa ADD CONSTRAINT primary_key UNIQUE (cpf);

-- procedure inserção na tabela -> ok
CREATE or replace function inserir(pe pessoa_t) returns  integer as $teste$
declare id integer;
begin
  insert into pessoa(nome, dataNascimento, salario, observacoes, nomemae, nomepai, cpf) 
  values (pe.nome, pe.datanascimento, pe.salario, pe.observacoes, pe.nomemae, pe.nomepai, pe.cpf) RETURNING idPessoa into id;
  RETURN id;
end;
$teste$ LANGUAGE plpgsql;


-- procedure de listagem de todos -> ok
create or replace function listar() returns SETOF pessoa_t_id as $list$
begin
	return query select * from pessoa;
end;
$list$ LANGUAGE plpgsql;

--listar por id -> ok
create or replace function listarUM(id integer) returns table(pe pessoa_t_id) as $um$
begin
	return query select * from pessoa as p where p.idpessoa = id;
	if not found then
		raise exception 'Nenhuma pessoa com id: % encontrada ', id;
	end if;
end;
$um$ language plpgsql;
	
-- atualizar -> ok
create or replace function atualizar(pe pessoa_t_id) returns varchar(2) as $up$
begin

	IF NOT EXISTS (SELECT 1 FROM pessoa WHERE idpessoa = pe.idpessoa) THEN
        RAISE EXCEPTION 'Nenhuma pessoa com id: % encontrada.', pe.idpessoa;
    END IF; 
	
	update pessoa
	set
		nome = pe.nome,
		datanascimento = pe.datanascimento,
		salario = pe.salario,
		observacoes = pe.observacoes,
		nomemae = pe.nomemae,
		nomepai = pe.nomepai,
		cpf = pe.cpf
	where idpessoa = pe.idpessoa;

	return 'OK';
end;
$up$ language plpgsql;

-- deletar -> ok
create or replace function deletar(id integer) returns varchar as $del$
declare 
	linha integer;
begin
	delete from pessoa where idpessoa = id returning idpessoa into linha;
		
	if linha is null then
		return 'NOT FOUND';
		raise exception 'Erro: Nenhum registro encontrado com o ID %. Operação de exclusão falhou.', id;

	else
		return 'OK';

	end if;
end;
$del$ language plpgsql;



-- execuções -> ok
SELECT inserir(row('chefe', '19/01/96', 5300, 'observer', 'mãe', 'pai', '456789'));
SELECT atualizar(ROW(1,'judson alexsander', '19/01/96', 2500, 'teste2', 'luzia', 'jorge', '123')::pessoa_t_id);
select * from listar();
select * from listarUM(1);
select deletar(4)
