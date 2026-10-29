/*
 * Desempenho individual do estudante.
 *
 * Primeiro consulta GET /api/usuario. Essa rota retorna o usuário autenticado
 * a partir da sessão Flask criada no login. O ID não é digitado nem escolhido
 * pelo navegador. Só depois de confirmar a sessão, consulta-se o relatório.
 *
 * Todas as áreas da página são atualizadas com createElement/textContent para
 * que os dados vindos da API não sejam interpretados como HTML.
 */

const API_USUARIO_ATUAL = "/api/usuario";
const API_MEU_DESEMPENHO = "/api/alunos/meu-desempenho";

// Cria um elemento definindo seu texto com segurança.
function elementoComTexto(tag, texto, classe = "") {
    const elemento = document.createElement(tag);
    elemento.textContent = texto ?? "";
    if (classe) elemento.className = classe;
    return elemento;
}

// Formata notas para não exibir valores como undefined ou null.
function formatarNota(valor) {
    const numero = Number(valor);
    return Number.isFinite(numero) ? String(Number(numero.toFixed(2))) : "0";
}

// Exibe aviso em uma região da página.
function mostrarAviso(conteiner, mensagem, classe = "notice") {
    conteiner.replaceChildren(elementoComTexto("p", mensagem, classe));
}

// Mostra o nome da conta identificada pela sessão.
function mostrarIdentificacao(usuario) {
    const destino = document.getElementById("identificacao-usuario");
    if (!destino) return;

    const nome = usuario?.nome?.trim();
    destino.textContent = nome
        ? `Desempenho da conta: ${nome}`
        : "Conta identificada com sucesso.";
}

// Informa que é necessário entrar na conta e cria um link para o login.
function pedirLogin() {
    const identificacao = document.getElementById("identificacao-usuario");
    const status = document.getElementById("status-desempenho");
    const relatorio = document.getElementById("relatorio");
    const evolucao = document.getElementById("evolucao");
    const competencias = document.getElementById("fraca");

    if (identificacao) identificacao.textContent = "Nenhuma conta autenticada nesta sessão.";
    if (status) {
        status.replaceChildren(document.createTextNode("Entre na sua conta para consultar seu desempenho. "));
        const linkLogin = elementoComTexto("a", "Entrar na minha conta");
        linkLogin.href = "/login";
        status.appendChild(linkLogin);
    }
    if (relatorio) relatorio.replaceChildren();
    if (evolucao) evolucao.replaceChildren();
    if (competencias) competencias.replaceChildren();
}

// Monta o resumo com as métricas retornadas pelo backend.
function desenharResumo(relatorio) {
    const destino = document.getElementById("relatorio");
    if (!destino) return;
    destino.replaceChildren();

    const grade = document.createElement("div");
    grade.className = "cards";

    const metricas = [
        { titulo: relatorio.nome || "Meu desempenho", rotulo: "Estudante" },
        { titulo: formatarNota(relatorio.total_redacoes), rotulo: "Redações enviadas" },
        { titulo: formatarNota(relatorio.media), rotulo: "Média geral" },
        { titulo: formatarNota(relatorio.melhor_nota), rotulo: "Melhor nota" },
        { titulo: formatarNota(relatorio.menor_nota), rotulo: "Menor nota" }
    ];

    metricas.forEach((metrica) => {
        const cartao = document.createElement("article");
        cartao.className = "card";
        cartao.append(
            elementoComTexto("h2", metrica.titulo),
            elementoComTexto("p", metrica.rotulo)
        );
        grade.appendChild(cartao);
    });
    destino.appendChild(grade);
}

// Lista a evolução das redações do usuário atual.
function desenharEvolucao(evolucao, totalRedacoes) {
    const destino = document.getElementById("evolucao");
    if (!destino) return;
    destino.replaceChildren(elementoComTexto("h2", "Evolução das redações"));

    if (!Array.isArray(evolucao) || evolucao.length === 0) {
        const texto = totalRedacoes > 0
            ? "Ainda não há notas registradas para mostrar a evolução."
            : "Você ainda não possui redações registradas. Envie uma redação para acompanhar sua evolução aqui.";
        destino.appendChild(elementoComTexto("p", texto, "notice"));
        return;
    }

    const lista = document.createElement("div");
    lista.className = "cards";

    evolucao.forEach((item) => {
        const cartao = document.createElement("article");
        cartao.className = "card";
        cartao.append(
            elementoComTexto("h3", item.tema || "Tema não informado"),
            elementoComTexto("p", `Nota: ${formatarNota(item.nota_total)}`),
            elementoComTexto("p", `Data de envio: ${item.data_envio || "Data não informada"}`)
        );
        lista.appendChild(cartao);
    });
    destino.appendChild(lista);
}

// Exibe as médias individuais das cinco competências do ENEM.
function desenharCompetencias(competencias) {
    const destino = document.getElementById("fraca");
    if (!destino) return;
    destino.replaceChildren(elementoComTexto("h2", "Médias por competência"));

    const cartao = document.createElement("article");
    cartao.className = "card";
    const lista = document.createElement("div");
    lista.className = "competencias-lista";

    for (let numero = 1; numero <= 5; numero += 1) {
        const valor = competencias?.[`competencia${numero}`];
        lista.appendChild(
            elementoComTexto("p", `Competência ${numero}: ${formatarNota(valor)}`)
        );
    }

    cartao.appendChild(lista);
    destino.appendChild(cartao);
}

// Confere a sessão pela mesma API usada pelo cabeçalho antes de buscar o relatório.
async function buscarUsuarioAutenticado() {
    const resposta = await fetch(API_USUARIO_ATUAL, {
        method: "GET",
        credentials: "same-origin",
        cache: "no-store",
        headers: { "Accept": "application/json" }
    });

    if (resposta.status === 401) return null;
    if (!resposta.ok) throw new Error("Não foi possível verificar sua sessão de login.");

    const usuario = await resposta.json();
    if (!usuario.logado || !usuario.id) return null;
    return usuario;
}

// Carrega o relatório do usuário já identificado pela sessão Flask.
async function carregarMeuDesempenho() {
    const status = document.getElementById("status-desempenho");
    const identificacao = document.getElementById("identificacao-usuario");
    const botao = document.getElementById("consultar-desempenho");
    const resumo = document.getElementById("relatorio");
    const evolucao = document.getElementById("evolucao");
    const competencias = document.getElementById("fraca");

    if (!status || !botao || !resumo || !evolucao || !competencias) return;

    status.textContent = "Verificando a conta conectada...";
    if (identificacao) identificacao.textContent = "Identificando sua conta...";
    botao.disabled = true;
    resumo.replaceChildren();
    evolucao.replaceChildren();
    competencias.replaceChildren();

    try {
        // Etapa 1: identifica a conta real na sessão do Flask.
        const usuario = await buscarUsuarioAutenticado();
        if (!usuario) {
            pedirLogin();
            return;
        }
        mostrarIdentificacao(usuario);

        // Etapa 2: pede os dados individuais; não envia ID na URL ou no corpo.
        status.textContent = "Conta identificada. Carregando seu desempenho...";
        const resposta = await fetch(API_MEU_DESEMPENHO, {
            method: "GET",
            credentials: "same-origin",
            cache: "no-store",
            headers: { "Accept": "application/json" }
        });
        const dados = await resposta.json();

        if (resposta.status === 401) {
            pedirLogin();
            return;
        }
        if (!resposta.ok) {
            throw new Error(dados.erro || "Não foi possível carregar seu desempenho.");
        }

        const relatorio = dados.relatorio || {};
        desenharResumo(relatorio);
        desenharEvolucao(dados.evolucao || [], Number(relatorio.total_redacoes) || 0);
        desenharCompetencias(dados.competencias || {});
        status.textContent = "Seu desempenho foi atualizado.";
    } catch (erro) {
        console.error("Erro ao carregar desempenho individual:", erro);
        status.textContent = erro.message || "Não foi possível conectar ao servidor.";
    } finally {
        botao.disabled = false;
    }
}

// Ao abrir a página, identifica a sessão e carrega os dados automaticamente.
// O botão permite repetir a consulta sem solicitar o ID do usuário.
document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("consultar-desempenho")
        ?.addEventListener("click", carregarMeuDesempenho);
    carregarMeuDesempenho();
});
