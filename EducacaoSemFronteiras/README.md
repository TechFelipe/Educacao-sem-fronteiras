# Educacao Sem Fronteiras

Plataforma web para preparação para o ENEM, com foco em prática de redações e acompanhamento do desempenho.

## Tecnologias

- Python
- Flask
- Flask-SQLAlchemy
- SQLite
- HTML
- CSS
- JavaScript

## Arquitetura

Controller → Service → Repository → Flask-SQLAlchemy → SQLite

## Banco de dados

O projeto não utiliza mais MySQL nem `mysql-connector-python`.

O banco é um arquivo SQLite localizado em:

`database/enem_plus.db`

As tabelas são criadas automaticamente na primeira execução do `app.py`, e os dados iniciais são inseridos caso ainda não existam.

## Funcionalidades

- Busca de temas por palavra-chave
- Filtro por dificuldade
- Ordenação dos resultados
- Ranking de estudantes
- Relatório individual
- Histórico de evolução
- Consulta das médias das competências
- Cadastro inicial de dados de teste

## Rotas

GET /api/temas/buscar?termo=educacao&dificuldade=Media

POST /api/redacoes

GET /api/redacoes/ranking

GET /api/alunos/<id>/relatorio

GET /api/alunos/<id>/evolucao

GET /api/alunos/<id>/competencia-fraca

## Instalação

1. Instale Python 3.
2. No terminal, execute:

`pip install -r requirements.txt`

3. Execute:

`python app.py`

4. Abra `http://127.0.0.1:5000`

Não é necessário instalar MySQL ou executar nenhum arquivo `.sql`.
