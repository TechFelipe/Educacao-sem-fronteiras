/*
 * Eventos da tela do Assistente Virtual.
 * O botão de saída navega para a rota de logout do Flask.
 */
document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("deslogar-assistente")?.addEventListener("click", () => {
        window.location.href = "/logout";
    });
});
