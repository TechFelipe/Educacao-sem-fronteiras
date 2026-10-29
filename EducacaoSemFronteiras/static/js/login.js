/*
 * Controla o envio do formulário da página de login.
 * O JavaScript fica aqui em static/js/login.js, e o HTML contém apenas
 * a estrutura do formulário e a referência a este arquivo.
 */
document.addEventListener("DOMContentLoaded", () => {
    const formulario = document.getElementById("loginForm");
    if (!formulario) return;

    formulario.addEventListener("submit", async (evento) => {
        evento.preventDefault();

        const mensagem = document.getElementById("msg");
        const dados = Object.fromEntries(new FormData(evento.currentTarget));

        try {
            const resposta = await fetch("/api/auth/login", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                credentials: "same-origin",
                body: JSON.stringify(dados)
            });
            const resultado = await resposta.json();

            if (resposta.ok) {
                window.location.href = "/dashboard";
            } else {
                mensagem.textContent = resultado.erro || "Erro ao fazer login.";
                mensagem.className = "auth-message error";
            }
        } catch (erro) {
            console.error("Erro ao conectar com a API de login:", erro);
            mensagem.textContent = "Não foi possível conectar ao servidor.";
            mensagem.className = "auth-message error";
        }
    });
});
