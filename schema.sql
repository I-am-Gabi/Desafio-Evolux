drop table if exists entries;
create table bares (
  id integer primary key autoincrement,
  nome string not null,
  descricao string not null,
  endereco string not null,
  especialidade string not null,
  telefone string not null,
  foto BLOB
);