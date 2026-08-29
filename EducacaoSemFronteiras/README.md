# EducacaoSemFronteiras — HTML puro + JavaScript + Flask-SQLAlchemy

Esta versão remove o Jinja do frontend. Os arquivos HTML não usam `{% ... %}` nem `{{ ... }}`.

## Como funciona

O navegador usa `fetch()` para consultar as APIs do Flask. O Flask usa Flask-SQLAlchemy para acessar `database/enem_plus.db`.

- `GET /api/usuario` — informa se existe usuário logado e devolve seus dados.
- `POST /api/auth/login` — autentica e cria a sessão.
- `POST /api/auth/cadastro` — cadastra usuário no SQLite.
- `GET /api/temas/buscar?termo=...` — consulta temas no banco.
- `POST /api/redacoes` — salva a redação.
- `GET /api/redacoes/temas` — consulta Tema.
- `GET /api/redacoes/temas` — consulta Dificuldade.
-  FUNC /static/js/redacoes/temas` — Atualiza a pagina redacao.html
- `GET /api/redacoes/ranking` — consulta ranking.
- `GET /api/alunos/<id>/relatorio` — relatório.
- `GET /api/alunos/<id>/evolucao` — evolução.
- `GET /api/alunos/<id>/competencia-fraca` — competências.

## Executar

Na pasta `EducacaoSemFronteiras`:

```bash
pip install -r requirements.txt
python app.py
```

O banco usado é `database/enem_plus.db`.

Usuário de teste criado automaticamente:
- e-mail: `aluno@teste.com`
- senha: `123456`
