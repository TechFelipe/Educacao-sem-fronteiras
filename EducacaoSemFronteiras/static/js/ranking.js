(() => {
    const status = document.getElementById("ranking-status");
    const lista = document.getElementById("ranking-list");
    const total = document.getElementById("ranking-total");

    // Evita que nomes vindos do banco sejam interpretados como HTML.
    function escaparHtml(valor) {
        return String(valor ?? "").replace(/[&<>"']/g, caractere => ({
            "&": "&amp;",
            "<": "&lt;",
            ">": "&gt;",
            '"': "&quot;",
            "'": "&#39;"
        })[caractere]);
    }

    function formatarNota(valor) {
        const nota = Number(valor);
        return Number.isFinite(nota)
            ? nota.toLocaleString("pt-BR", {
                minimumFractionDigits: 2,
                maximumFractionDigits: 2
            })
            : "0,00";
    }

    function criarLinha(estudante, indice) {
        const posicao = indice + 1;
        const classes = ["top-one", "top-two", "top-three"];
        const medalhas = ["🥇", "🥈", "🥉"];
        const classeDestaque = classes[indice] || "";
        const medalha = medalhas[indice]
            ? `<span class="rank-medal" aria-label="${posicao}º lugar">${medalhas[indice]}</span>`
            : "";

        const nome = String(estudante.nome || "Estudante").trim();
        const inicial = nome.charAt(0).toLocaleUpperCase("pt-BR");

        return `
            <article class="rank-card ${classeDestaque}">
                <span class="rank-number">${posicao}º</span>
                <div class="rank-avatar" aria-hidden="true">${escaparHtml(inicial || "?")}</div>
                <div class="rank-student">
                    <strong>${escaparHtml(nome)} ${medalha}</strong>
                    <small>${Number(estudante.quantidade_redacoes) || 0} redação(ões) enviada(s)</small>
                </div>
                <div class="rank-score">
                    <strong>${formatarNota(estudante.media)}</strong>
                    <small>média</small>
                </div>
                <div class="rank-best">
                    <strong>${formatarNota(estudante.melhor_nota)}</strong>
                    <small>melhor nota</small>
                </div>
            </article>
        `;
    }

    async function carregarRanking() {
        try {
            const resposta = await fetch("/api/redacoes/ranking");
            if (!resposta.ok) throw new Error("Falha ao consultar o ranking");

            const dados = await resposta.json();

            if (!Array.isArray(dados) || dados.length === 0) {
                total.textContent = "0";
                status.textContent = "Ainda não há redações avaliadas para formar o ranking.";
                status.classList.add("ranking-empty");
                lista.innerHTML = "";
                return;
            }

            total.textContent = dados.length.toLocaleString("pt-BR");
            status.textContent = "Ranking global ordenado pela média das notas. Em caso de empate, a quantidade de redações enviadas define a posição.";
            status.classList.add("ranking-info");

            lista.innerHTML = dados.map(criarLinha).join("");
        } catch (erro) {
            console.error("Erro ao carregar ranking:", erro);
            status.textContent = "Não foi possível carregar o ranking. Tente atualizar a página.";
            status.classList.add("ranking-error");
            total.textContent = "—";
        }
    }

    carregarRanking();
})();
