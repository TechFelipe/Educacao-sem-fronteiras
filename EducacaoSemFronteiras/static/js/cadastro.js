/*
 * Envia o formulário de cadastro à API Flask.
 * A opção "Exibir senha" é controlada pelo common.js através de
 * data-toggle-password, sem handlers inline no HTML.
 */
document.addEventListener("DOMContentLoaded", () => {
    const formulario = document.getElementById("cadastroForm");
    if (!formulario) return;

    formulario.addEventListener("submit", async (evento) => {
        evento.preventDefault();
        const msg = document.getElementById("msg");
        const dados = Object.fromEntries(new FormData(evento.currentTarget));

        try {
            const resposta = await fetch("/api/auth/cadastro", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                credentials: "same-origin",
                body: JSON.stringify(dados)
            });
            const json = await resposta.json();

            if (resposta.ok) {
                msg.textContent = json.mensagem || "Cadastro realizado com sucesso.";
                msg.className = "auth-message success";
                window.setTimeout(() => {
                    window.location.href = "/login";
                }, 1000);
            } else {
                msg.textContent = json.erro || "Não foi possível cadastrar.";
                msg.className = "auth-message error";
            }
        } catch (erro) {
            console.error("Erro ao cadastrar:", erro);
            msg.textContent = "Não foi possível conectar ao servidor.";
            msg.className = "auth-message error";
        }
    });
});
