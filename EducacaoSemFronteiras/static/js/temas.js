/*
 * Lógica da página Matérias, extraída do HTML para static/js/temas.js.
 * Mantém a leitura dinâmica das categorias pela API Flask, que consulta
 * as tabelas do materias.sqlite, e a busca/abertura dos PDFs.
 */

/*
     * Esta página não lê o arquivo SQLite diretamente no navegador.
     * Ela chama a API Flask, que consulta materias.sqlite e devolve apenas
     * os metadados dos PDFs. O arquivo PDF é aberto por uma rota própria.
     */
    let materiaSelecionada = "";

    // Normaliza nomes para comparar tabelas com e sem acentos.
    function normalizarTexto(valor) {
        return String(valor)
            .normalize("NFD")
            .replace(/[\\u0300-\\u036f]/g, "")
            .toLocaleLowerCase("pt-BR");
    }

    // Deixa os nomes das tabelas mais bonitos na interface sem alterar o nome real no banco.
    function nomeExibicao(nome) {
        const conhecidos = {
            "matematica": "Matemática",
            "portugues": "Português",
            "ciencias": "Ciências",
            "fisica": "Física",
            "quimica": "Química",
            "historia": "História",
            "geografia": "Geografia",
            "biologia": "Biologia",
            "artes": "Artes",
            "filosofia": "Filosofia",
            "sociologia": "Sociologia",
            "ingles": "Inglês",
            "educacao fisica": "Educação Física",
            "literatura": "Literatura"
        };
        return conhecidos[normalizarTexto(nome)] || nome;
    }

    // Busca as tabelas do SQLite e cria um botão para cada uma, mesmo sem PDFs cadastrados.
    async function carregarCategorias() {
        const container = document.getElementById("subjects");
        const status = document.getElementById("materias-status");
        try {
            const resposta = await fetch("/api/materias/categorias");
            if (!resposta.ok) throw new Error("Falha ao buscar as matérias.");
            const categorias = await resposta.json();
            container.replaceChildren();

            categorias.forEach((categoria) => {
                const nomeReal = categoria.nome;
                const botao = document.createElement("button");
                botao.type = "button";
                botao.className = "subject materia-filtro";
                botao.dataset.subject = nomeReal;
                botao.setAttribute("aria-pressed", "false");
                botao.textContent = nomeExibicao(nomeReal);
                botao.addEventListener("click", () => {
                    // Clicar na mesma matéria novamente remove o filtro selecionado.
                    materiaSelecionada =
                        normalizarTexto(materiaSelecionada) === normalizarTexto(nomeReal)
                            ? ""
                            : nomeReal;

                    document.querySelectorAll(".materia-filtro").forEach((outro) => {
                        outro.setAttribute(
                            "aria-pressed",
                            String(normalizarTexto(outro.dataset.subject) === normalizarTexto(materiaSelecionada)
                                && materiaSelecionada !== "")
                        );
                    });

                    // Limpa a pesquisa para mostrar somente a matéria clicada.
                    document.getElementById("termo").value = "";
                    carregarMateriais();
                });
                container.appendChild(botao);
            });

            if (categorias.length === 0) {
                status.textContent = "Nenhuma matéria foi cadastrada no materias.sqlite.";
            } else {
                status.textContent = "Selecione uma matéria ou pesquise para visualizar os PDFs.";
            }
        } catch (erro) {
            console.error("Erro ao carregar matérias:", erro);
            status.textContent = "Não foi possível carregar as matérias do banco de dados.";
        }
    }

    // Busca PDFs conforme a matéria selecionada ou o termo digitado.
    async function carregarMateriais() {
        const termo = document.getElementById("termo").value.trim();
        const parametros = new URLSearchParams();
        if (termo) parametros.set("termo", termo);
        if (materiaSelecionada) parametros.set("materia", materiaSelecionada);

        const status = document.getElementById("materias-status");
        const resultado = document.getElementById("resultado-materias");
        resultado.replaceChildren();

        // Não lista PDFs automaticamente quando a página é aberta sem filtro.
        if (!termo && !materiaSelecionada) {
            status.textContent = "Selecione uma matéria ou pesquise para visualizar os PDFs.";
            return;
        }

        status.textContent = "Buscando materiais...";
        try {
            const resposta = await fetch("/api/materias?" + parametros.toString());
            const materiais = await resposta.json();
            if (!resposta.ok || !Array.isArray(materiais)) {
                throw new Error("A API não retornou uma lista válida.");
            }

            if (materiais.length === 0) {
                status.textContent = materiaSelecionada
                    ? "Ainda não há PDFs cadastrados para esta matéria."
                    : "Nenhum PDF encontrado para essa pesquisa.";
                return;
            }

            status.textContent = materiais.length + " material(is) encontrado(s).";
            materiais.forEach((material) => {
                // Criamos elementos DOM e usamos textContent para exibir os dados com segurança.
                const card = document.createElement("article");
                card.className = "material-card";
                const titulo = document.createElement("h3");
                titulo.textContent = material.titulo;
                const descricao = document.createElement("p");
                descricao.textContent = "Matéria: " + nomeExibicao(material.materia);
                const nivel = document.createElement("p");
                nivel.textContent = "Nível: " + (material.nivel || "Não informado");
                const acoes = document.createElement("div");
                acoes.className = "material-actions";

                const abrir = document.createElement("a");
                abrir.className = "material-open";
                abrir.href = "/api/materias/" + encodeURIComponent(material.id) + "/pdf";
                abrir.target = "_blank";
                abrir.rel = "noopener";
                abrir.textContent = "Abrir PDF";

                const baixar = document.createElement("a");
                baixar.className = "material-download";
                baixar.href = abrir.href;
                baixar.download = nomeExibicao(material.materia) + ".pdf";
                baixar.textContent = "Baixar PDF";

                acoes.append(abrir, baixar);
                card.append(titulo, descricao, nivel, acoes);
                resultado.appendChild(card);
            });
        } catch (erro) {
            console.error("Erro ao consultar materiais:", erro);
            status.textContent = "Não foi possível carregar os PDFs. Verifique se o Flask está em execução.";
        }
    }

    // Executa a pesquisa ao clicar na lupa ou pressionar Enter.
    document.getElementById("botao-buscar").addEventListener("click", () => {
        materiaSelecionada = "";
        document.querySelectorAll(".materia-filtro").forEach((botao) => botao.setAttribute("aria-pressed", "false"));
        carregarMateriais();
    });
    document.getElementById("termo").addEventListener("keydown", (evento) => {
        if (evento.key === "Enter") {
            materiaSelecionada = "";
            document.querySelectorAll(".materia-filtro").forEach((botao) => botao.setAttribute("aria-pressed", "false"));
            carregarMateriais();
        }
    });

    // Se vier um termo na URL, pesquisa-o; senão, apenas carrega os botões das tabelas.
    const termoInicial = new URLSearchParams(window.location.search).get("termo");
    if (termoInicial) document.getElementById("termo").value = termoInicial;
    carregarCategorias().then(() => {
        if (termoInicial) carregarMateriais();
    });
