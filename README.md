# Educação sem Fronteiras

Aplicação educacional com frontend HTML/CSS/JavaScript, API Flask e banco SQLite. A arquitetura separa Controllers (HTTP), Services (regras de negócio), Models (entidades ORM) e Repositories (consultas específicas).

## Requisitos
- Python 3.10 ou superior
- Dependências listadas em `requirements.txt`

## Como executar
Na pasta `EducacaoSemFronteiras`:

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python app.py
```
Abra `http://127.0.0.1:5000`.

Conta de demonstração: `aluno@teste.com` / `123456`.

## Seleção do tema na tela de redação

Na página `/redacao`, os temas são carregados dinamicamente pela API Flask `GET /api/temas/buscar`. O navegador apresenta um checkbox para cada tema; o aluno marca uma opção e o JavaScript envia o ID correspondente no cadastro da redação. A interface não exige digitação manual do ID. O fluxo está documentado com comentários em `static/js/redacao.js` e `frontend/redacao.html`.

## Funcionalidades Implementadas
1. Cadastrar conta de aluno (validação de campos e e-mail duplicado).
2. Autenticar aluno com senha armazenada em hash.
3. Consultar estado da sessão do usuário.
4. Encerrar sessão de usuário.
5. Listar temas de redação.
6. Pesquisar temas por título ou descrição.
7. Filtrar temas por dificuldade via API.
8. Consultar detalhes de um tema por ID.
9. Cadastrar tema de redação pela API.
10. Atualizar tema de redação pela API.
11. Excluir tema sem redações vinculadas pela interface e API.
12. Enviar redação associada a um aluno e tema.
13. Validar campos e tamanho mínimo do texto da redação.
14. Consultar ranking de alunos por média das redações.
15. Consultar relatório consolidado do aluno.
16. Consultar evolução das notas de redação.
17. Consultar médias das cinco competências.
18. Exibir dashboard e navegação entre as páginas.
19. Preencher tema e dificuldade selecionados na tela de redação.
20. Exibir mensagens de sucesso/erro retornadas pela API.
21. Abrir formulário de gerenciamento de temas.
22. Carregar lista de temas no gerenciamento.
23. Preencher formulário ao escolher editar tema.
24. Confirmar exclusão de tema antes da requisição.
25. Validar e informar falhas de tema associado a redações.

A tela de gerenciamento de temas fica em `/gerenciar-temas` e permite cadastrar, listar, editar e excluir temas usando a API.

## Arquitetura
- `controllers/`: classes baseadas em `MethodView`, responsáveis por HTTP e respostas JSON.
- `services/`: validação e coordenação dos casos de uso.
- `models/`: entidades ORM `db.Model` e operações de persistência comuns.
- `repositories/`: consultas especiais e agregações SQL.
- `frontend/`: páginas HTML.
- `static/js/`: consumo da API pelo navegador.
- `config/database.py`: configuração de SQLAlchemy, conexão SQLite e dados de demonstração.

## Diagrama de classes
O diagrama está em [`docs/diagrama_classes.md`](docs/diagrama_classes.md). Ele representa as quatro entidades ORM e os relacionamentos entre aluno, redação, tema e notas por competência.

## Rotas principais
- `POST /api/auth/cadastro`
- `POST /api/auth/login`
- `GET /api/usuario`
- `GET /api/temas/buscar?termo=educação&dificuldade=Media`
- `GET /api/temas/<id>`
- `POST /api/temas`
- `PUT /api/temas/<id>`
- `DELETE /api/temas/<id>`
- `POST /api/redacoes`
- `GET /api/redacoes/ranking`
- `GET /api/alunos/<id>/relatorio`
- `GET /api/alunos/<id>/evolucao`
- `GET /api/alunos/<id>/competencia-fraca`

## Segurança e limitações
Defina `SECRET_KEY` por variável de ambiente em ambientes reais. O usuário de teste existe apenas para demonstração local. Antes de produção, restrinja a criação/edição/exclusão de temas a usuários autorizados e associe envios exclusivamente à sessão autenticada.


## Materiais em PDF

A página `/temas` pesquisa os PDFs armazenados como BLOB no arquivo `database/materias.sqlite`.
A API `GET /api/materias` localiza automaticamente os valores que começam com `%PDF-` e retorna
metadados para pesquisa e filtro. A rota `GET /api/materias/<id>/pdf` entrega o arquivo ao navegador.

A tela `/gerenciar-materiais` permite adicionar PDFs, editar título/matéria/nível, substituir o arquivo
e excluir materiais. Os níveis permitidos são `Ensino Fundamental`, `Ensino Médio` e `Faculdade`.
Para alterar os materiais, é necessário entrar em uma conta. Novos PDFs ficam armazenados na tabela
`_materiais_gerenciados`, criada automaticamente no próprio `materias.sqlite`. Para os PDFs antigos,
o título e o nível são guardados em `_materiais_metadados`; ao excluí-los, apenas a coluna que contém
o PDF é esvaziada, preservando os outros campos da linha original.

Operações da API de materiais:
- `GET /api/materias?administracao=1` — lista todos os PDFs para a tela de gerenciamento.
- `POST /api/materias` — adiciona um PDF (`multipart/form-data`: `materia`, `titulo`, `nivel`, `arquivo`).
- `PATCH /api/materias/<id>` — edita título, matéria (em arquivos novos) e nível (`application/json`).
- `PUT /api/materias/<id>/pdf` — substitui o arquivo PDF (`multipart/form-data`: `arquivo`).
- `DELETE /api/materias/<id>` — exclui um material.
- `GET /api/materias/categorias` — lista as matérias disponíveis.
A tela de gerenciamento também permite cadastrar uma nova matéria digitando seu nome; nesse caso, os PDFs
ficam na tabela `_materiais_gerenciados`. As tabelas antigas (por exemplo, `Portugues` ou `Matematica`)
continuam sendo detectadas automaticamente, sem alteração no JavaScript. Os PDFs precisam estar salvos no
banco para aparecerem na biblioteca.


## Organização do JavaScript do frontend

Os comportamentos das páginas ficam em arquivos separados na pasta `static/js/`.
Os arquivos HTML contêm apenas a estrutura visual e referências com `<script src="...">`.
Os eventos de interface são conectados com `addEventListener`, sem atributos JavaScript
inline (`onclick`, por exemplo). A página `temas.html` carrega `static/js/temas.js`,
que consulta a API Flask para listar dinamicamente as tabelas de matérias do `materias.sqlite`.


## Desempenho individual

A página `/desempenho` carrega automaticamente as estatísticas do usuário autenticado, sem solicitar o ID.
O frontend chama `GET /api/alunos/meu-desempenho`; a Controller obtém o ID da sessão Flask e delega ao
`RelatorioService`, que reúne o resumo, a evolução das redações e as médias das cinco competências.
Se não houver uma sessão autenticada, a API retorna HTTP 401 e a tela orienta o usuário a entrar na conta.


## Cabeçalho compartilhado e menu lateral

O conteúdo compartilhado está em `frontend/cabecalho.html`, que contém o cabeçalho e o painel lateral.
Cada página possui um elemento `<div id="site-header"></div>` e carrega `static/js/common.js`,
que busca o fragmento pela rota `/cabecalho` e o insere no documento atual. Isso permite que o menu
lateral apareça por cima do conteúdo da página, sem a limitação de altura de um iframe.
O painel abre pelo botão hambúrguer, fecha pelo botão `×`, pelo fundo escurecido ou pela tecla Escape.
O compartilhamento de HTML sem template server-side precisa de um mecanismo de inclusão; neste projeto,
a inclusão é feita pelo `common.js`, mas o HTML do cabeçalho continua em um único arquivo.

## Cabeçalho antigo via iframe com menu lateral

O cabeçalho completo (faixa laranja e navegação vermelha) é servido em `frontend/cabecalho.html`
pela rota `/cabecalho` e mostrado nas demais páginas através de `<iframe class="header-frame">`.
O script `static/js/cabecalho.js` trata o usuário e envia uma mensagem `postMessage` quando o
botão hambúrguer é clicado. O script `static/js/common.js`, na página principal, recebe essa
mensagem e abre/fecha um menu lateral que pertence ao documento principal. Assim, o painel
pode sobrepor o conteúdo da página, apesar do cabeçalho permanecer dentro de um iframe.

## Cabeçalho fixo durante a rolagem

O `iframe.header-frame` usa `position: sticky; top: 0` em `static/css/style.css`. Assim, as faixas laranja e vermelha permanecem no topo durante a rolagem, mantendo o menu lateral alinhado logo abaixo do cabeçalho.

## Separação das funções de PDF

As rotas e operações de PDF estão organizadas em `controllers/pdf_controller.py`, `services/pdf_service.py` e `repositories/pdf_repository.py`. Os arquivos `material_controller.py`, `material_service.py` e `material_repository.py` foram mantidos como compatibilidade para imports antigos.

Os PDFs cadastrados são armazenados na tabela da matéria, na coluna correspondente ao nível (`Ensino Fundamental`, `Ensino Medio`/`Ensino Médio` ou `Faculdade`). A listagem identifica o nível pela coluna. Em colunas SQLite `TEXT` de tabelas `STRICT`, o conteúdo do PDF é codificado em Base64 com prefixo interno para preservar os bytes e permitir leitura, substituição e exclusão.
