/*
 * JavaScript compartilhado do documento principal.
 *
 * O cabeçalho antigo (faixa laranja + navegação vermelha) está em um iframe.
 * O botão hambúrguer dentro do iframe envia uma mensagem via postMessage.
 * Este arquivo cria o painel lateral no documento principal para que o menu
 * possa abrir por cima do conteúdo sem ficar recortado pelo iframe.
 */


// Função compartilhada para páginas que precisam do ID do usuário autenticado,
// como o formulário de redação. O ID é obtido pela sessão do Flask.
async function carregarUsuario() {
    try {
        const resposta = await fetch("/api/usuario", {
            credentials: "same-origin",
            cache: "no-store",
            headers: { "Accept": "application/json" }
        });

        if (!resposta.ok) return null;

        const usuario = await resposta.json();
        const campoId = document.getElementById("usuario");

        // Algumas telas usam um campo oculto para preencher o autor da redação.
        if (campoId && usuario.id) {
            campoId.value = usuario.id;
        }

        return usuario;
    } catch (erro) {
        console.error("Não foi possível consultar o usuário conectado:", erro);
        return null;
    }
}

// Escapa nomes antes de usá-los em marcação HTML criada para o menu.
function escaparTexto(valor) {
    const div = document.createElement("div");
    div.textContent = valor ?? "";
    return div.innerHTML;
}

// Abre/fecha o menu e sincroniza os atributos de acessibilidade.
function definirMenuLateralAberto(aberto) {
    const menu = document.getElementById("globalSideMenu");
    const fundo = document.getElementById("globalSideMenuBackdrop");
    if (!menu || !fundo) return;

    menu.classList.toggle("open", aberto);
    fundo.classList.toggle("show", aberto);
    menu.setAttribute("aria-hidden", String(!aberto));
    fundo.setAttribute("aria-hidden", String(!aberto));
}

// Cria o painel lateral uma vez, diretamente no documento da página principal.
function criarMenuLateral() {
    if (document.getElementById("globalSideMenu")) return;

    const fundo = document.createElement("div");
    fundo.id = "globalSideMenuBackdrop";
    fundo.className = "global-menu-backdrop";
    fundo.setAttribute("aria-hidden", "true");

    const menu = document.createElement("aside");
    menu.id = "globalSideMenu";
    menu.className = "global-side-menu";
    menu.setAttribute("aria-label", "Menu lateral");
    menu.setAttribute("aria-hidden", "true");

    menu.innerHTML = `
        <button type="button" class="global-menu-close" aria-label="Fechar menu">×</button>
        <h2>Menu</h2>
        <nav aria-label="Mais opções">
            <a href="/redacao">Escrever redação</a>
            <a href="/desempenho">Meu desempenho</a>
            <a href="/ranking">Ranking</a>
            <a href="/gerenciar-materiais">Gerenciar PDFs</a>
        </nav>
        <div id="globalSideAuth"></div>
    `;

    document.body.append(fundo, menu);

    fundo.addEventListener("click", () => definirMenuLateralAberto(false));
    menu.querySelector(".global-menu-close").addEventListener("click", () => {
        definirMenuLateralAberto(false);
    });

    // Ao pressionar Escape, fecha o painel.
    document.addEventListener("keydown", (evento) => {
        if (evento.key === "Escape") definirMenuLateralAberto(false);
    });

    // Obtém login/sair da sessão, para manter o menu consistente com o cabeçalho.
    carregarAcoesDaConta();
}

// Preenche os links de login/sair dentro do menu, usando a sessão Flask.
async function carregarAcoesDaConta() {
    const area = document.getElementById("globalSideAuth");
    if (!area) return;

    try {
        const resposta = await fetch("/api/usuario", {
            credentials: "same-origin",
            cache: "no-store",
            headers: { "Accept": "application/json" }
        });

        if (resposta.ok) {
            const usuario = await resposta.json();
            area.replaceChildren();

            const nome = document.createElement("p");
            nome.className = "global-side-user";
            nome.textContent = `Conectado como ${usuario.nome || "usuário"}`;

            const sair = document.createElement("a");
            sair.href = "/logout";
            sair.textContent = "Sair da conta";

            area.append(nome, sair);
        } else {
            area.replaceChildren();

            const login = document.createElement("a");
            login.href = "/login";
            login.textContent = "Entrar";

            const cadastro = document.createElement("a");
            cadastro.href = "/cadastro";
            cadastro.textContent = "Criar uma conta";

            area.append(login, cadastro);
        }
    } catch (erro) {
        console.error("Erro ao carregar as opções da conta:", erro);
    }
}

// Recebe o clique do botão hambúrguer que existe dentro do iframe do cabeçalho.
// Valida a origem e a janela de origem para ignorar mensagens externas.
window.addEventListener("message", (evento) => {
    if (evento.origin !== window.location.origin) return;
    if (evento.data?.tipo !== "educacao:alternar-menu-lateral") return;

    const iframe = document.querySelector("iframe.header-frame");
    if (!iframe || evento.source !== iframe.contentWindow) return;

    const menu = document.getElementById("globalSideMenu");
    definirMenuLateralAberto(!menu?.classList.contains("open"));
});

// Continua permitindo mostrar/ocultar senhas em formulários.
function togglePassword(id) {
    const campo = document.getElementById(id);
    if (campo) {
        campo.type = campo.type === "password" ? "text" : "password";
    }
}

document.addEventListener("change", (evento) => {
    const controle = evento.target.closest("[data-toggle-password]");
    if (controle) togglePassword(controle.dataset.togglePassword);
});

document.addEventListener("DOMContentLoaded", () => {
    criarMenuLateral();
});
