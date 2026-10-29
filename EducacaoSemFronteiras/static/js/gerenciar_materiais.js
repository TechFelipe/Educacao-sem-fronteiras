/* Interface de administração dos PDFs. A persistência é feita pela API Flask. */
(() => {
    const form = document.getElementById("form-material");
    const campoTitulo = document.getElementById("material-titulo");
    const campoMateria = document.getElementById("material-materia");
    const campoNivel = document.getElementById("material-nivel");
    const campoArquivo = document.getElementById("material-arquivo");
    const lista = document.getElementById("lista-materiais");
    const listaVazia = document.getElementById("lista-vazia");
    const status = document.getElementById("admin-status");
    const avisoLogin = document.getElementById("aviso-login");
    const listaMaterias = document.getElementById("lista-materias");
    const filtro = document.getElementById("filtro-materiais");
    const botaoAdicionar = document.getElementById("adicionar-material");
    const botaoSalvar = document.getElementById("salvar-edicao");
    const botaoSubstituir = document.getElementById("substituir-pdf");
    const botaoCancelar = document.getElementById("cancelar-edicao");

    let materiais = [];
    let materialSelecionado = null;
    let usuarioLogado = false;

    function mostrarStatus(mensagem, erro = false) {
        status.textContent = mensagem;
        status.classList.toggle("status-error", erro);
    }

    async function respostaApi(url, opcoes = {}) {
        const resposta = await fetch(url, {
            credentials: "same-origin",
            ...opcoes,
            headers: {
                ...(opcoes.headers || {}),
                "Accept": "application/json"
            }
        });
        let dados = {};
        const tipo = resposta.headers.get("content-type") || "";
        if (tipo.includes("application/json")) dados = await resposta.json();
        if (!resposta.ok) throw new Error(dados.erro || dados.mensagem || `A operação falhou (${resposta.status}).`);
        return dados;
    }

    async function verificarUsuario() {
        try {
            const resposta = await fetch("/api/usuario", { credentials: "same-origin", cache: "no-store" });
            usuarioLogado = resposta.ok;
        } catch (erro) {
            usuarioLogado = false;
        }
        avisoLogin.hidden = usuarioLogado;
        atualizarBotoes();
    }

    function atualizarBotoes() {
        botaoAdicionar.disabled = !usuarioLogado;
        botaoSalvar.disabled = !usuarioLogado || !materialSelecionado;
        botaoSubstituir.disabled = !usuarioLogado || !materialSelecionado;
        botaoCancelar.disabled = !materialSelecionado;
    }

    function limparFormulario() {
        materialSelecionado = null;
        form.reset();
        document.getElementById("form-title").textContent = "Adicionar PDF";
        campoMateria.readOnly = false;
        campoArquivo.required = false;
        campoArquivo.value = "";
        atualizarBotoes();
    }

    function criarBotao(texto, classe, acao, desabilitado = false) {
        const botao = document.createElement("button");
        botao.type = "button";
        botao.className = `admin-card-button ${classe}`;
        botao.textContent = texto;
        botao.disabled = desabilitado;
        botao.addEventListener("click", acao);
        return botao;
    }

    function selecionarMaterial(material) {
        materialSelecionado = material;
        campoTitulo.value = material.titulo || "";
        campoMateria.value = material.materia || "";
        campoNivel.value = material.nivel || "";
        campoMateria.readOnly = material.origem === "legado";
        campoArquivo.value = "";
        campoArquivo.required = false;
        document.getElementById("form-title").textContent = "Editar PDF selecionado";
        atualizarBotoes();
        document.querySelector(".admin-panel").scrollIntoView({ behavior: "smooth", block: "start" });
        mostrarStatus(`Editando: ${material.titulo}. Ajuste os campos e escolha a operação desejada.`);
    }

    async function excluirMaterial(material) {
        const confirmado = window.confirm(`Deseja excluir o PDF “${material.titulo}”? Esta ação não pode ser desfeita.`);
        if (!confirmado) return;
        try {
            const dados = await respostaApi(`/api/materias/${encodeURIComponent(material.id)}`, { method: "DELETE" });
            mostrarStatus(dados.mensagem || "PDF excluído.");
            if (materialSelecionado?.id === material.id) limparFormulario();
            await carregarMateriais();
            await carregarCategorias();
        } catch (erro) {
            mostrarStatus(erro.message, true);
        }
    }

    function renderizarMateriais() {
        const termo = filtro.value.trim().toLocaleLowerCase("pt-BR");
        const filtrados = materiais.filter((material) =>
            `${material.titulo} ${material.materia} ${material.nivel || ""}`.toLocaleLowerCase("pt-BR").includes(termo)
        );
        lista.replaceChildren();
        listaVazia.hidden = filtrados.length > 0;

        filtrados.forEach((material) => {
            const card = document.createElement("article");
            card.className = "admin-material-card";
            const titulo = document.createElement("h3");
            titulo.textContent = material.titulo;
            const materia = document.createElement("p");
            materia.textContent = `Matéria: ${material.materia}`;
            const nivel = document.createElement("p");
            nivel.className = "admin-material-meta";
            nivel.textContent = `Nível: ${material.nivel || "Não informado"}`;
            const origem = document.createElement("p");
            origem.className = "admin-material-meta";
            origem.textContent = material.origem === "legado" ? "Arquivo já existente no banco" : "Arquivo gerenciado pela aplicação";

            const acoes = document.createElement("div");
            acoes.className = "admin-material-actions";
            const abrir = document.createElement("a");
            abrir.href = `/api/materias/${encodeURIComponent(material.id)}/pdf`;
            abrir.target = "_blank";
            abrir.rel = "noopener";
            abrir.textContent = "Abrir PDF";
            const baixar = document.createElement("a");
            baixar.href = abrir.href;
            baixar.download = material.nome_arquivo || "material.pdf";
            baixar.className = "download-link";
            baixar.textContent = "Baixar";
            acoes.append(abrir, baixar);
            acoes.append(
                criarBotao("Editar", "edit", () => selecionarMaterial(material), !usuarioLogado),
                criarBotao("Excluir", "delete", () => excluirMaterial(material), !usuarioLogado)
            );
            card.append(titulo, materia, nivel, origem, acoes);
            lista.appendChild(card);
        });
    }

    async function carregarMateriais() {
        try {
            materiais = await respostaApi("/api/materias?administracao=1");
            if (!Array.isArray(materiais)) throw new Error("A API não retornou uma lista de PDFs.");
            renderizarMateriais();
            mostrarStatus(`${materiais.length} PDF(s) encontrado(s).`);
        } catch (erro) {
            mostrarStatus(erro.message || "Não foi possível carregar os PDFs.", true);
        }
    }

    async function carregarCategorias() {
        try {
            const categorias = await respostaApi("/api/materias/categorias");
            listaMaterias.replaceChildren();
            categorias.forEach((categoria) => {
                const opcao = document.createElement("option");
                opcao.value = categoria.nome;
                listaMaterias.appendChild(opcao);
            });
        } catch (erro) {
            console.error("Não foi possível listar as matérias:", erro);
        }
    }

    form.addEventListener("submit", async (evento) => {
        evento.preventDefault();
        if (!usuarioLogado) {
            mostrarStatus("Entre na sua conta antes de adicionar um PDF.", true);
            return;
        }
        if (!campoArquivo.files?.[0]) {
            mostrarStatus("Selecione o arquivo PDF que deseja adicionar.", true);
            campoArquivo.focus();
            return;
        }
        const dados = new FormData();
        dados.append("titulo", campoTitulo.value.trim());
        dados.append("materia", campoMateria.value.trim());
        dados.append("nivel", campoNivel.value);
        dados.append("arquivo", campoArquivo.files[0]);
        try {
            const retorno = await respostaApi("/api/materias", { method: "POST", body: dados });
            mostrarStatus(retorno.mensagem || "PDF adicionado com sucesso.");
            limparFormulario();
            await carregarMateriais();
            await carregarCategorias();
        } catch (erro) {
            mostrarStatus(erro.message, true);
        }
    });

    botaoSalvar.addEventListener("click", async () => {
        if (!materialSelecionado || !usuarioLogado) return;
        const dados = {
            titulo: campoTitulo.value.trim(),
            nivel: campoNivel.value
        };
        if (materialSelecionado.pode_editar_materia) dados.materia = campoMateria.value.trim();
        try {
            const retorno = await respostaApi(`/api/materias/${encodeURIComponent(materialSelecionado.id)}`, {
                method: "PATCH",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(dados)
            });
            mostrarStatus(retorno.mensagem || "Edição salva.");
            limparFormulario();
            await carregarMateriais();
            await carregarCategorias();
        } catch (erro) {
            mostrarStatus(erro.message, true);
        }
    });

    botaoSubstituir.addEventListener("click", async () => {
        if (!materialSelecionado || !usuarioLogado) return;
        if (!campoArquivo.files?.[0]) {
            mostrarStatus("Selecione o novo arquivo PDF antes de substituí-lo.", true);
            campoArquivo.focus();
            return;
        }
        const dados = new FormData();
        dados.append("arquivo", campoArquivo.files[0]);
        try {
            const retorno = await respostaApi(`/api/materias/${encodeURIComponent(materialSelecionado.id)}/pdf`, {
                method: "PUT",
                body: dados
            });
            mostrarStatus(retorno.mensagem || "Arquivo substituído.");
            limparFormulario();
            await carregarMateriais();
        } catch (erro) {
            mostrarStatus(erro.message, true);
        }
    });

    botaoCancelar.addEventListener("click", limparFormulario);
    filtro.addEventListener("input", renderizarMateriais);

    async function iniciar() {
        await verificarUsuario();
        await Promise.all([carregarCategorias(), carregarMateriais()]);
    }
    iniciar();
})();
