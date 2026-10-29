/*
 * Eventos da página inicial.
 * A pesquisa pode ser enviada pelo botão ou pela tecla Enter.
 */
function searchHome() {
    const campo = document.getElementById("homeSearch");
    const termo = campo ? campo.value.trim() : "";
    window.location.href = "/temas?termo=" + encodeURIComponent(termo);
}

document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("botao-buscar-home")?.addEventListener("click", searchHome);
    document.getElementById("homeSearch")?.addEventListener("keydown", (evento) => {
        if (evento.key === "Enter") searchHome();
    });
});
