async function verificarTema() {
    const temaId = document.getElementById("tema").value;
    const mutavel = document.getElementById("mutavel");

    const labels = mutavel.querySelectorAll("label");

    if (temaId === "") {
        labels[0].textContent = "Tema da redação";
        labels[1].textContent = "Nivel de dificuldade";
        return;
    }

    try {
        const resposta = await fetch(
            `/api/temas/${encodeURIComponent(temaId)}`
        );

        if (!resposta.ok) {
            labels[0].textContent = "Tema não encontrado";
            labels[1].textContent = "Nivel de dificuldade: -";
            return;
        }

        const tema = await resposta.json();

        labels[0].textContent = tema.titulo;
        labels[1].textContent = tema.dificuldade;

    } catch (erro) {
        console.error("Erro ao verificar tema:", erro);

        labels[0].textContent = "Erro ao carregar tema";
        labels[1].textContent = "Nivel de dificuldade: -";
    }
}


async function enviar() {
    const dados = {
        usuario_id: Number(
            document.getElementById("usuario").value
        ),
        tema_id: Number(
            document.getElementById("tema").value
        ),
        texto: document.getElementById("texto").value
    };

    const res = await fetch(
        "/api/redacoes",
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(dados)
        }
    );

    const json = await res.json();

    document.getElementById("msg").textContent =
        json.erro || "Redação enviada com sucesso!";
}