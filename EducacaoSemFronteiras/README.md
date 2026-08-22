# ENEM+

Plataforma web para preparação para o ENEM, com foco em prática de redações e acompanhamento do desempenho.

## Tecnologias

- Python
- Flask
- MySQL
- HTML
- CSS
- JavaScript

## Arquitetura

Controller → Service → Repository → Procedure → MySQL

## Funcionalidades além do CRUD

- Busca de temas por palavra-chave
- Filtro por dificuldade
- Ordenação dos resultados
- Ranking de estudantes
- Relatório individual
- Histórico de evolução
- Consulta das médias das competências

## Procedures

- buscar_temas
- criar_redacao
- ranking_alunos
- relatorio_aluno
- evolucao_aluno
- competencia_fraca

## Rotas

GET /api/temas/buscar?termo=educacao&dificuldade=Media

POST /api/redacoes

GET /api/redacoes/ranking

GET /api/alunos/<id>/relatorio

GET /api/alunos/<id>/evolucao

GET /api/alunos/<id>/competencia-fraca

## Instalação

1. Instale Python 3.
2. Instale MySQL.
3. Execute database/enem_plus.sql no MySQL.
4. Abra config/database.py e altere SUA_SENHA.
5. No terminal, execute:

pip install -r requirements.txt

6. Execute:

python app.py

7. Abra http://127.0.0.1:5000

## Observação

A tela de envio de redação cria o registro e deixa a nota inicialmente em 0. A avaliação por competências pode ser adicionada como próxima etapa do projeto.
