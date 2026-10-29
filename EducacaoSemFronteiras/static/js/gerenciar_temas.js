/*
 * Gerenciamento dos temas.
 * Todas as interações são ligadas por addEventListener e os dados da API
 * são inseridos usando textContent, sem handlers inline na marcação.
 */

// Busca temas na API e constrói os cartões de forma segura.
async function carregarTemas() {
    const lista = document.getElementById("listaTemas");
    if (!lista) return;

    try {
        const resposta = await fetch("/api/temas/buscar");
        const temas = await resposta.json();
        if (!resposta.ok) throw new Error(temas.erro || "Falha ao listar temas.");

        lista.replaceChildren();

        if (!temas.length) {
            lista.textContent = "Nenhum tema cadastrado.";
            return;
        }

        temas.forEach((tema) => {
            const cartao = document.createElement("article");
            cartao.className = "card";

            const titulo = document.createElement("h3");
            titulo.textContent = tema.titulo || "Tema sem título";

            const descricao = document.createElement("p");
            descricao.textContent = tema.descricao || "Sem descrição";

            const dificuldade = document.createElement("p");
            dificuldade.textContent = `Dificuldade: ${tema.dificuldade || "-"}`;

            const editar = document.createElement("button");
            editar.type = "button";
            editar.dataset.acao = "editar";
            editar.dataset.id = String(tema.id);
            editar.textContent = "Editar";

            const excluir = document.createElement("button");
            excluir.type = "button";
            excluir.dataset.acao = "excluir";
            excluir.dataset.id = String(tema.id);
            excluir.textContent = "Excluir";

            cartao.append(titulo, descricao, dificuldade, editar, document.createTextNode(" "), excluir);
            lista.appendChild(cartao);
        });
    } catch (erro) {
        lista.textContent = erro.message;
    }
}

// Busca um tema pelo ID e preenche o formulário para edição.
async function editarTema(id) {
    try {
        const resposta = await fetch(`/api/temas/${encodeURIComponent(id)}`);
        const tema = await resposta.json();

        if (!resposta.ok) {
            mostrarMensagem(tema.erro || "Tema não encontrado.", true);
            return;
        }

        document.getElementById("temaId").value = tema.id;
        document.getElementById("titulo").value = tema.titulo || "";
        document.getElementById("descricao").value = tema.descricao || "";
        document.getElementById("dificuldade").value = tema.dificuldade || "Facil";
        window.scrollTo({ top: 0, behavior: "smooth" });
    } catch (erro) {
        mostrarMensagem("Não foi possível buscar o tema.", true);
    }
}

// Envia POST para criar um tema ou PUT para alterar um tema existente.
async function salvarTema() {
    const id = document.getElementById("temaId").value;
    const dados = {
        titulo: document.getElementById("titulo").value.trim(),
        descricao: document.getElementById("descricao").value.trim(),
        dificuldade: document.getElementById("dificuldade").value
    };

    try {
        const resposta = await fetch(
            id ? `/api/temas/${encodeURIComponent(id)}` : "/api/temas",
            {
                method: id ? "PUT" : "POST",
                headers: { "Content-Type": "application/json" },
                credentials: "same-origin",
                body: JSON.stringify(dados)
            }
        );
        const resultado = await resposta.json();

        if (!resposta.ok) {
            throw new Error(resultado.erro || "Não foi possível salvar o tema.");
        }

        mostrarMensagem(id ? "Tema atualizado com sucesso." : "Tema cadastrado com sucesso.");
        limparFormulario();
        await carregarTemas();
    } catch (erro) {
        mostrarMensagem(erro.message, true);
    }
}

// Pede confirmação antes de excluir um tema.
async function excluirTema(id) {
    if (!window.confirm("Deseja realmente excluir este tema? Temas ligados a redações não podem ser excluídos.")) {
        return;
    }

    try {
        const resposta = await fetch(`/api/temas/${encodeURIComponent(id)}`, {
            method: "DELETE",
            credentials: "same-origin"
        });
        const resultado = await resposta.json();

        if (!resposta.ok) {
            mostrarMensagem(resultado.erro || "Não foi possível excluir.", true);
            return;
        }

        mostrarMensagem("Tema excluído com sucesso.");
        await carregarTemas();
    } catch (erro) {
        mostrarMensagem("Não foi possível conectar ao servidor.", true);
    }
}

// Limpa o formulário e prepara a tela para um novo cadastro.
function limparFormulario() {
    document.getElementById("temaId").value = "";
    document.getElementById("titulo").value = "";
    document.getElementById("descricao").value = "";
    document.getElementById("dificuldade").value = "Facil";
}

// Apresenta mensagens de sucesso e erro ao usuário.
function mostrarMensagem(texto, erro = false) {
    const alvo = document.getElementById("mensagem");
    if (!alvo) return;

    alvo.textContent = texto;
    alvo.className = erro ? "auth-message error" : "auth-message success";
}

// Liga os controles fixos e os botões criados dinamicamente.
function inicializarGerenciamentoTemas() {
    document.getElementById("salvar-tema")?.addEventListener("click", salvarTema);
    document.getElementById("limpar-formulario")?.addEventListener("click", limparFormulario);

    const lista = document.getElementById("listaTemas");
    lista?.addEventListener("click", (evento) => {
        const botao = evento.target.closest("button[data-acao][data-id]");
        if (!botao) return;

        const id = Number(botao.dataset.id);
        if (!Number.isInteger(id) || id <= 0) return;

        if (botao.dataset.acao === "editar") {
            editarTema(id);
        } else if (botao.dataset.acao === "excluir") {
            excluirTema(id);
        }
    });

    carregarTemas();
}

document.addEventListener("DOMContentLoaded", inicializarGerenciamentoTemas);
