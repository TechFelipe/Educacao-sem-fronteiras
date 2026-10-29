# Guia dos arquivos do Educação sem Fronteiras

Este documento descreve os arquivos mantidos após a limpeza e a função de cada um.
A aplicação está organizada em Frontend (HTML/CSS/JavaScript) e Backend (Flask,
Controllers, Services, Models e Repositories), além de dois bancos SQLite.

## Fluxo geral da aplicação

1. O navegador abre uma página HTML na pasta `frontend/`.
2. O HTML carrega estilos de `static/css/` e scripts de `static/js/`.
3. O JavaScript chama os endpoints definidos em `app.py` e nos Controllers.
4. A Controller interpreta a requisição e chama o Service apropriado.
5. O Service valida os dados e coordena o caso de uso.
6. A Model representa uma entidade e permite persistência ORM; o Repository trata
   consultas específicas e agregações.
7. Os dados são lidos ou gravados nos bancos SQLite e a API responde em JSON.

---

## Arquivos da raiz

- **`app.py`** — ponto de entrada da aplicação Flask. Inicializa o banco principal,
  registra as Controllers/Blueprints e disponibiliza as páginas HTML, incluindo a rota
  `/gerenciar-materiais`. O gerenciamento dos PDFs é delegado à Controller, Service e
  Repository de materiais. Também contém a rota de logout e o tratamento de erros HTTP.
- **`requirements.txt`** — lista as bibliotecas Python necessárias. Deve ser usado com
  `pip install -r requirements.txt`.
- **`README.md`** — instruções para instalar e executar a aplicação, funcionalidades,
  rotas e informações da arquitetura. Aponta para este guia e o diagrama de classes.

## Configuração

- **`config/__init__.py`** — marca `config` como pacote Python. Não tem lógica própria,
  mas mantém a organização dos imports.
- **`config/database.py`** — cria a instância compartilhada do Flask-SQLAlchemy, define
  o caminho de `database/enem_plus.db`, oferece uma conexão SQLite para consultas
  específicas e inicializa as tabelas e os dados de demonstração.

## Controllers

Cada Controller recebe requisições HTTP e devolve respostas da API. As regras de
negócio devem ficar nos Services, não nas Controllers.

- **`controllers/__init__.py`** — marcador do pacote Python `controllers`.
- **`controllers/usuario_controller.py`** — endpoints de cadastro, login e consulta
  do usuário da sessão. No login, guarda os dados públicos da conta na sessão Flask.
- **`controllers/tema_controller.py`** — endpoints para pesquisar/listar temas,
  consultar tema por ID, cadastrar, atualizar e excluir temas.
- **`controllers/redacao_controller.py`** — recebe o envio de redação e fornece o
  endpoint de ranking.
- **`controllers/relatorio_controller.py`** — endpoints para relatório consolidado,
  evolução e médias de competências. Também oferece `/api/alunos/meu-desempenho`,
  que usa o ID da sessão autenticada em vez de pedir um ID no navegador.
- **`controllers/material_controller.py`** — endpoints para listar, cadastrar, editar, excluir, abrir e substituir PDFs; exige sessão autenticada nas operações que alteram dados.

## Services

Cada Service coordena um caso de uso, valida dados e chama Models/Repositories.

- **`services/__init__.py`** — marcador do pacote Python `services`.
- **`services/auth_service.py`** — valida cadastro, verifica e-mail duplicado,
  gera hash de senha e autentica o usuário comparando o hash.
- **`services/tema_service.py`** — coordena pesquisa, criação, consulta, atualização
  e exclusão dos temas, validando os dados recebidos.
- **`services/redacao_service.py`** — valida e coordena a criação de redações e a
  consulta do ranking.
- **`services/relatorio_service.py`** — valida o identificador e reúne resumo,
  evolução e médias por competência para a tela de desempenho.
- **`services/material_service.py`** — valida título, matéria, níveis de ensino, extensão e assinatura de PDF; coordena os casos de uso de materiais.

## Models

As Models representam as entidades e definem campos, chaves estrangeiras e
relacionamentos do banco principal. Também possuem operações de persistência ORM.

- **`models/__init__.py`** — importa e expõe as quatro Models, garantindo que o
  SQLAlchemy conheça as entidades antes de criar as tabelas.
- **`models/usuario_model.py`** — entidade `Usuario`, associada à tabela `usuarios`;
  armazena nome, e-mail e hash da senha. A serialização pública não expõe a senha.
- **`models/tema_model.py`** — entidade `Tema`, associada à tabela `temas`; armazena
  título, descrição, dificuldade e relacionamento com as redações.
- **`models/redacao_model.py`** — entidade `Redacao`, associada à tabela `redacoes`;
  guarda autor, tema, texto, nota total e data de envio, além dos relacionamentos.
- **`models/nota_competencia_model.py`** — entidade `NotaCompetencia`, que guarda as
  notas das cinco competências associadas a uma redação.
- **`models/material_model.py`** — representa os metadados do material e define os níveis permitidos: Ensino Fundamental, Ensino Médio e Faculdade.

## Repositories

Os Repositories isolam consultas SQL específicas e operações de consulta usadas
pelos Services. O projeto usa `config/database.py` para abrir conexões SQLite.

- **`repositories/__init__.py`** — marcador do pacote Python `repositories`.
- **`repositories/usuario_repository.py`** — localiza usuários por e-mail e cria
  registros de usuário no banco principal.
- **`repositories/tema_repository.py`** — lista e filtra temas, busca tema por ID,
  cria, atualiza e exclui registros relacionados a temas.
- **`repositories/redacao_repository.py`** — grava redações e constrói o ranking.
- **`repositories/relatorio_repository.py`** — executa consultas agregadas de relatório,
  evolução de notas e médias das cinco competências.
- **`repositories/material_repository.py`** — lê os PDFs das tabelas antigas e guarda os novos PDFs, os níveis e os títulos no `materias.sqlite`, preservando os outros campos das linhas antigas.

## Páginas HTML

Os HTMLs fornecem a estrutura das telas. O comportamento interativo fica nos
arquivos JavaScript correspondentes em `static/js/`.

- **`frontend/index.html`** — página de entrada do site.
- **`frontend/dashboard.html`** — página inicial após entrada, com atalhos para matérias,
  assistente, redação e desempenho.
- **`frontend/temas.html`** — página de matérias; os botões são criados dinamicamente
  a partir das tabelas detectadas em `materias.sqlite`; os PDFs aparecem após seleção
  da matéria ou pesquisa.
- **`frontend/gerenciar_temas.html`** — formulário e lista para cadastrar, editar e
  excluir temas de redação.
- **`frontend/gerenciar_materiais.html`** — tela para adicionar, editar, substituir, abrir/baixar e excluir PDFs; inclui os três níveis de ensino.
- **`frontend/redacao.html`** — tela para escolher um tema por checkbox e enviar o texto
  da redação.
- **`frontend/desempenho.html`** — tela de desempenho individual; apresenta áreas que
  o JavaScript preenche com dados do usuário autenticado.
- **`frontend/ranking.html`** — tela que exibe o ranking calculado pela API.
- **`frontend/login.html`** — formulário de autenticação.
- **`frontend/cadastro.html`** — formulário de criação de conta.
- **`frontend/assistente.html`** — interface visual do assistente de estudos. Nesta versão
  há a interface e seus controles básicos; não se deve presumir que exista uma integração
  funcional com uma LLM/IA sem configuração adicional.

## JavaScript do frontend

- **`static/js/common.js`** — compartilhado entre as telas: insere o cabeçalho, navegação
  e menu; consulta `/api/usuario`; apresenta os controles de login e implementa menu,
  janela de login e exibição/ocultação de senha.
- **`static/js/dashboard.js`** — encaminha a busca da página inicial para a página Matérias.
- **`static/js/temas.js`** — solicita `/api/materias/categorias`, cria um botão para cada
  tabela/matéria, normaliza nomes, filtra materiais e apresenta links para abrir ou baixar PDFs.
- **`static/js/gerenciar_temas.js`** — consulta a lista de temas, preenche o formulário
  para edição e envia requisições de criação, atualização e exclusão.
- **`static/js/gerenciar_materiais.js`** — controla o formulário CRUD de PDF, filtro de materiais, seleção para edição e chamadas da API.
- **`static/js/redacao.js`** — carrega o usuário e os temas, controla o checkbox de tema,
  mostra o título/dificuldade selecionados e envia a redação à API.
- **`static/js/desempenho.js`** — verifica a sessão, solicita o relatório individual sem
  ID informado pelo usuário e desenha resumo, evolução e competências.
- **`static/js/ranking.js`** — consulta o endpoint de ranking e apresenta os resultados.
- **`static/js/login.js`** — envia as credenciais de login para a API e mostra mensagens
  de sucesso ou falha.
- **`static/js/cadastro.js`** — envia o formulário de cadastro e apresenta as respostas da API.
- **`static/js/assistente.js`** — conecta o botão de saída da tela do assistente à rota `/logout`.

## CSS

- **`static/css/style.css`** — folhas de estilo global: cabeçalho, menu, formulários,
  botões, cartões, páginas e componentes compartilhados.
- **`static/css/temas.css`** — estilos adicionais específicos da página Matérias, como
  grade de matérias, pesquisa e cartões de PDF.
- **`static/css/gerenciar_materiais.css`** — estilos da tela de administração dos PDFs e formulário de nível/matéria/arquivo.

## Bancos de dados e arquivos de documentação

- **`database/enem_plus.db`** — banco SQLite principal da aplicação. Guarda usuários,
  temas, redações e notas por competência. É usado por `config/database.py`.
- **`database/materias.sqlite`** — banco SQLite separado que armazena as tabelas das
  matérias e os PDFs como dados binários (BLOB). É consultado por
  `repositories/material_repository.py`, que cria as tabelas auxiliares de gerenciamento.
- **`docs/diagrama_classes.md`** — diagrama textual das Models e dos relacionamentos
  de domínio usado na documentação do projeto.
- **`docs/GUIA_ARQUIVOS.md`** — este inventário, para localizar e compreender cada arquivo.

## O que foi removido na limpeza

- Pastas `__pycache__/` e arquivos `.pyc`/`.pyo`: são caches gerados automaticamente
  pelo Python e serão recriados quando a aplicação for executada.
- `database/enem_plus.sql`: dump SQL sem referências no código de execução. A aplicação
  inicializa o banco ativo `enem_plus.db` por meio de `config/database.py`.

Os bancos `.db` e `.sqlite` foram preservados. Eles contêm dados da aplicação e materiais
didáticos, por isso não devem ser apagados como se fossem arquivos temporários.
