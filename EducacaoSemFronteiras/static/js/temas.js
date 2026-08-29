async function buscar() {
    const termo = document.getElementById("termo").value.trim();
    const resultado = document.getElementById("resultado");
    const subjects = document.querySelectorAll(".subject");

    if (!termo) {
        resultado.innerHTML = "";
        subjects.forEach(x => x.style.display = "block");
        return;
    }

    const res = await fetch("/api/temas/buscar?termo=" + encodeURIComponent(termo));
    const dados = await res.json();
    subjects.forEach(x => x.style.display = "none");

    resultado.innerHTML = dados.map(t => `
        <div class="card">
            <h2>${escapeHtml(t.titulo)}</h2>
            <p>${escapeHtml(t.descricao || "")}</p>
            <small>Dificuldade: ${escapeHtml(t.dificuldade || "-")}</small>
        </div>
    `).join("") || '<div class="notice">Nenhum material encontrado.</div>';
}
document.querySelectorAll(".subject").forEach(btn => btn.addEventListener("click", e => {
    e.preventDefault();
    const s = btn.dataset.subject;
    if (s === "Ver mais") {
        document.querySelectorAll(".subject").forEach(x => x.style.display = "block");
        return;
    }
    document.getElementById("termo").value = s;
    buscar();
}));
const initial = new URLSearchParams(location.search).get("termo");
if (initial) {
    document.getElementById("termo").value = initial;
    buscar();
}