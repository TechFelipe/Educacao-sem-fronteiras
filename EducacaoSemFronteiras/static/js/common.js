async function carregarUsuario() {
    const userArea = document.getElementById("user-area");
    const sideAuth = document.getElementById("side-auth");
    if (!userArea || !sideAuth) return;

    try {
        const resposta = await fetch("/api/usuario", {
            credentials: "same-origin"
        });

        if (resposta.ok) {
            const usuario = await resposta.json();
            const inicial = (usuario.nome || "?").charAt(0).toUpperCase();

            userArea.innerHTML = `
                <button class="user-button" onclick="location.href='/logout'" aria-label="Sair">
                    ${inicial}
                </button>
            `;

            sideAuth.innerHTML = `
                <a href="/logout">Sair (${escapeHtml(usuario.nome)})</a>
            `;
        } else {
            userArea.innerHTML = `
                <button class="icon-button" onclick="openLogin()" aria-label="Login">♙</button>
            `;

            sideAuth.innerHTML = `
                <a href="/login">Login</a>
                <a href="/cadastro">Cadastrar</a>
            `;
        }
    } catch (erro) {
        console.error("Não foi possível consultar o usuário:", erro);
        userArea.innerHTML = `
            <button class="icon-button" onclick="openLogin()" aria-label="Login">♙</button>
        `;
        sideAuth.innerHTML = `
            <a href="/login">Login</a>
            <a href="/cadastro">Cadastrar</a>
        `;
    }
}

function escapeHtml(value) {
    const div = document.createElement("div");
    div.textContent = value ?? "";
    return div.innerHTML;
}

function toggleMenu() {
    document.getElementById("sideMenu")?.classList.toggle("open");
    document.getElementById("menuBackdrop")?.classList.toggle("show");
}

function openLogin() {
    document.getElementById("authOverlay")?.classList.add("show");
}

function closeLogin(event) {
    const overlay = document.getElementById("authOverlay");
    if (!event || event.target === overlay) {
        overlay?.classList.remove("show");
    }
}

function togglePassword(id) {
    const el = document.getElementById(id);
    if (el) el.type = el.type === "password" ? "text" : "password";
}

function renderLayout() {
    const header = document.getElementById("site-header");
    if (!header) return;

    header.innerHTML = `
        <header class="topbar">
            <a class="brand" href="/dashboard" aria-label="Biblioteca digital Estudantil">
                <span class="brand-logo" aria-hidden="true"><span>📖</span></span>
                <span>Biblioteca digital Estudantil</span>
            </a>
            <div class="top-actions">
                <div id="user-area"></div>
                <button class="icon-button sparkle" onclick="location.href='/assistente'" aria-label="Assistente">✧</button>
                <button class="hamburger" onclick="toggleMenu()" aria-label="Abrir menu">
                    <span></span><span></span><span></span>
                </button>
            </div>
        </header>

        <nav class="main-nav" id="mainNav">
            <a href="/dashboard">Início</a>
            <a href="/temas">Matérias</a>
            <a href="/assistente">Assistente Virtual</a>
        </nav>

        <div class="side-menu" id="sideMenu">
            <button class="close-menu" onclick="toggleMenu()">×</button>
            <a href="/dashboard">Início</a>
            <a href="/temas">Matérias</a>
            <a href="/assistente">Assistente Virtual</a>
            <div id="side-auth"></div>
        </div>

        <div class="menu-backdrop" id="menuBackdrop" onclick="toggleMenu()"></div>

        <div class="auth-overlay" id="authOverlay" onclick="closeLogin(event)">
            <div class="auth-panel" onclick="event.stopPropagation()">
                <button class="auth-close" onclick="closeLogin()">×</button>
                <div class="auth-form">
                    <h1>Fazer login</h1>
                    <form id="quickLoginForm" class="auth-form-fields">
                        <label>Email<input name="email" id="loginEmail" type="email" autocomplete="email" required></label>
                        <label>Senha<input name="senha" id="loginSenha" type="password" autocomplete="current-password" required></label>
                        <label class="check"><input type="checkbox" onclick="togglePassword('loginSenha')"> Exibir senha</label>
                        <button class="orange-btn" type="submit">Entrar</button>
                        <p id="quickLoginMsg"></p>
                    </form>
                    <p>Não possui uma conta?<br><a href="/cadastro">Cadastre-se</a> agora!</p>
                </div>
                <div class="auth-art"><div class="big-logo">📖</div></div>
            </div>
        </div>
    `;

    document.getElementById("quickLoginForm")?.addEventListener("submit", async (event) => {
        event.preventDefault();
        const form = event.currentTarget;
        const msg = document.getElementById("quickLoginMsg");
        const dados = Object.fromEntries(new FormData(form));

        const resposta = await fetch("/api/auth/login", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            credentials: "same-origin",
            body: JSON.stringify(dados)
        });

        const json = await resposta.json();

        if (resposta.ok) {
            location.reload();
        } else {
            msg.textContent = json.erro || "Não foi possível fazer login.";
            msg.className = "auth-message error";
        }
    });

    carregarUsuario();
}

document.addEventListener("DOMContentLoaded", renderLayout);
