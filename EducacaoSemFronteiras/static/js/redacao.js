/*
 * Tela de envio de redação.
 *
 * Fluxo da seleção:
 * 1. O navegador solicita os temas à API Flask: GET /api/temas/buscar.
 * 2. A Controller encaminha a consulta ao TemaService e ao TemaRepository.
 * 3. O backend devolve os temas do banco SQLite em JSON.
 * 4. Este arquivo cria um checkbox para cada tema retornado.
 * 5. Ao marcar um tema, guardamos o ID real no checkbox selecionado e exibimos
 *    o título e a dificuldade. O usuário não precisa digitar o ID.
 */

// Carrega o usuário da sessão para preencher o campo oculto usado no envio.
// A API de redações também pode usar o usuário guardado na sessão do servidor.
document.addEventListener("DOMContentLoaded", async () => {
    // O botão de envio é conectado aqui, sem onclick no HTML.
    document.getElementById("enviar-redacao")?.addEventListener("click", enviar);
    await carregarUsuario();
    await carregarTemas();
});

async function carregarUsuario() {
    try {
        const resposta = await fetch("/api/usuario", {
            credentials: "same-origin"
        });

        if (resposta.ok) {
            const usuario = await resposta.json();
            document.getElementById("usuario").value = usuario.id;
        }
    } catch (erro) {
        // A redação ainda poderá ser enviada se o backend reconhecer a sessão.
        console.error("Não foi possível carregar o usuário da sessão:", erro);
    }
}

// Consulta os temas ao backend Python e cria uma opção de checkbox para cada um.
async function carregarTemas() {
    const lista = document.getElementById("lista-temas");
    const estado = document.getElementById("estado-temas");

    estado.textContent = "Carregando temas...";
    lista.replaceChildren();

    try {
        // Sem filtros, a API retorna todos os temas cadastrados no banco.
        const resposta = await fetch("/api/temas/buscar", {
            credentials: "same-origin"
        });
        const temas = await resposta.json();

        if (!resposta.ok || !Array.isArray(temas)) {
            throw new Error(temas.erro || "A API não retornou uma lista de temas.");
        }

        if (temas.length === 0) {
            estado.textContent = "Nenhum tema cadastrado no momento.";
            return;
        }

        estado.textContent = "Marque um tema para sua redação:";

        temas.forEach((tema) => {
            // Cada opção é montada com elementos DOM, evitando inserir dados da API
            // como HTML interpretável pelo navegador.
            const rotulo = document.createElement("label");
            rotulo.className = "tema-opcao";

            const checkbox = document.createElement("input");
            checkbox.type = "checkbox";
            checkbox.name = "tema_id";
            checkbox.value = String(tema.id);
            checkbox.dataset.titulo = tema.titulo || "Tema sem título";
            checkbox.dataset.dificuldade = tema.dificuldade || "-";

            const texto = document.createElement("span");
            texto.textContent = `${tema.titulo || "Tema sem título"} — dificuldade: ${tema.dificuldade || "-"}`;

            // Embora sejam checkboxes, permitimos apenas um tema marcado por vez.
            // Isso mantém a regra do sistema: uma redação pertence a um tema.
            checkbox.addEventListener("change", () => {
                if (checkbox.checked) {
                    document.querySelectorAll('input[name="tema_id"]').forEach((outro) => {
                        if (outro !== checkbox) outro.checked = false;
                    });
                }
                atualizarResumoTema();
            });

            rotulo.append(checkbox, texto);
            lista.appendChild(rotulo);
        });
    } catch (erro) {
        console.error("Erro ao carregar os temas:", erro);
        estado.textContent = "Não foi possível carregar os temas. Atualize a página e tente novamente.";
    }
}

// Retorna o checkbox marcado, ou null caso o aluno ainda não tenha escolhido um tema.
function obterTemaSelecionado() {
    return document.querySelector('input[name="tema_id"]:checked');
}

// Atualiza o resumo visível com o tema escolhido e o nível de dificuldade.
function atualizarResumoTema() {
    const selecionado = obterTemaSelecionado();
    const titulo = document.getElementById("tema-selecionado");
    const dificuldade = document.getElementById("dificuldade-selecionada");

    if (!selecionado) {
        titulo.textContent = "Tema da redação: nenhum selecionado";
        dificuldade.textContent = "Nível de dificuldade: -";
        return;
    }

    titulo.textContent = `Tema da redação: ${selecionado.dataset.titulo}`;
    dificuldade.textContent = `Nível de dificuldade: ${selecionado.dataset.dificuldade}`;
}

// Envia o texto e o ID do checkbox selecionado para a API Flask.
// O ID continua sendo enviado internamente, mas é escolhido pelo usuário através da interface.
async function enviar() {
    const mensagem = document.getElementById("msg");
    const usuarioId = Number(document.getElementById("usuario").value);
    const temaSelecionado = obterTemaSelecionado();
    const texto = document.getElementById("texto").value.trim();

    // Validações simples no navegador melhoram a experiência; o Service também valida no backend.
    if (!temaSelecionado) {
        mensagem.textContent = "Escolha um tema antes de enviar a redação.";
        mensagem.className = "auth-message error";
        return;
    }

    if (!texto) {
        mensagem.textContent = "Digite o texto da redação antes de enviar.";
        mensagem.className = "auth-message error";
        return;
    }

    const dados = {
        usuario_id: usuarioId || null,
        tema_id: Number(temaSelecionado.value),
        texto: texto
    };

    try {
        const resposta = await fetch("/api/redacoes", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            credentials: "same-origin",
            body: JSON.stringify(dados)
        });

        const json = await resposta.json();
        mensagem.textContent = json.mensagem || json.erro ||
            (resposta.ok ? "Redação enviada com sucesso!" : "Não foi possível enviar a redação.");
        mensagem.className = resposta.ok
            ? "auth-message success"
            : "auth-message error";

        // Se o envio deu certo, limpa o texto, sem apagar a seleção do tema.
        if (resposta.ok) {
            document.getElementById("texto").value = "";
        }
    } catch (erro) {
        console.error("Falha ao enviar a redação:", erro);
        mensagem.textContent = "Falha de comunicação com o servidor.";
        mensagem.className = "auth-message error";
    }
}
