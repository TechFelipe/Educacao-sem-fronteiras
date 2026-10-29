/*
 * Executado dentro de cabecalho.html.
 * Consulta o usuário da sessão Flask e comunica o clique no hambúrguer
 * à página principal. O menu é criado fora do iframe para poder sobrepor
 * o conteúdo, sem ficar cortado pelos limites do iframe.
 */

async function carregarUsuarioDoCabecalho() {
    const area = document.getElementById("user-area");
    if (!area) return;

    try {
        const resposta = await fetch("/api/usuario", {
            credentials: "same-origin",
            cache: "no-store",
            headers: { "Accept": "application/json" }
        });

        if (resposta.ok) {
            const usuario = await resposta.json();
            const inicial = (usuario.nome || "U").trim().charAt(0).toUpperCase() || "U";
            const sair = document.createElement("a");
            sair.className = "user-button";
            sair.href = "/logout";
            sair.target = "_top";
            sair.title = `Sair da conta de ${usuario.nome || "usuário"}`;
            sair.setAttribute("aria-label", "Sair da conta");
            sair.textContent = inicial;
            area.replaceChildren(sair);
        } else {
            const login = document.createElement("a");
            login.className = "user-button login-placeholder";
            login.href = "/login";
            login.target = "_top";
            login.setAttribute("aria-label", "Entrar");
            login.textContent = "♙";
            area.replaceChildren(login);
        }
    } catch (erro) {
        console.error("Não foi possível identificar o usuário no cabeçalho:", erro);
    }
}

document.addEventListener("DOMContentLoaded", () => {
    carregarUsuarioDoCabecalho();

    const botao = document.getElementById("toggle-side-menu");
    botao?.addEventListener("click", () => {
        // Comunica apenas para a página que incorporou este iframe.
        window.parent.postMessage(
            { tipo: "educacao:alternar-menu-lateral" },
            window.location.origin
        );
    });
});
