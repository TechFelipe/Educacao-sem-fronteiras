/* Gerenciamento de matérias em temas.html. Cada ação abre seu próprio formulário abaixo dos PDFs. */
(() => {
    const status = document.getElementById('materias-admin-status');
    const painel = document.getElementById('painel-acao-materia');
    if (!status || !painel) return;

    const botoes = [...document.querySelectorAll('[data-acao-materia]')];
    const formularios = [...painel.querySelectorAll('[data-painel]')];
    const formAdicionar = document.getElementById('form-materia-adicionar');
    const formRenomear = document.getElementById('form-materia-renomear');
    const formExcluir = document.getElementById('form-materia-excluir');
    const selectRenomear = document.getElementById('materia-renomear');
    const selectExcluir = document.getElementById('materia-excluir');
    let usuarioLogado = false;
    let materiasCache = [];

    async function api(url, options = {}) {
        const response = await fetch(url, {
            credentials: 'same-origin',
            ...options,
            headers: { Accept: 'application/json', ...(options.headers || {}) }
        });
        const data = response.headers.get('content-type')?.includes('application/json') ? await response.json() : {};
        if (!response.ok) throw new Error(data.erro || data.mensagem || `Falha na operação (${response.status}).`);
        return data;
    }

    function mensagem(texto, erro = false) {
        status.textContent = texto;
        status.classList.toggle('status-error', erro);
    }

    function abrirPainel(acao) {
        if (!usuarioLogado) {
            mensagem('Entre na sua conta para gerenciar matérias.', true);
            return;
        }
        painel.hidden = false;
        formularios.forEach(form => { form.hidden = form.dataset.painel !== acao; });
        botoes.forEach(botao => {
            const ativo = botao.dataset.acaoMateria === acao;
            botao.classList.toggle('is-active', ativo);
            botao.setAttribute('aria-expanded', String(ativo));
        });
        if (acao === 'renomear' || acao === 'excluir') carregarMaterias();
        painel.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }

    async function carregarMaterias() {
        try {
            materiasCache = await api('/api/materias/categorias/gerenciar');
            [selectRenomear, selectExcluir].forEach(select => {
                const valorAnterior = select.value;
                select.replaceChildren(new Option('Selecione uma matéria', ''));
                materiasCache.forEach(materia => {
                    const option = new Option(`${materia.nome} (${materia.pdfs} PDF(s))`, materia.nome);
                    select.add(option);
                });
                if (materiasCache.some(m => m.nome === valorAnterior)) select.value = valorAnterior;
            });
            mensagem(`${materiasCache.length} matéria(s) disponível(is) para gerenciamento.`);
        } catch (error) {
            mensagem(error.message, true);
        }
    }

    botoes.forEach(botao => botao.addEventListener('click', () => abrirPainel(botao.dataset.acaoMateria)));

    formAdicionar.addEventListener('submit', async event => {
        event.preventDefault();
        const nome = document.getElementById('nova-materia').value.trim();
        if (!nome) return mensagem('Informe o nome da matéria.', true);
        try {
            const data = await api('/api/materias/categorias/gerenciar', {
                method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ nome })
            });
            formAdicionar.reset();
            mensagem(data.mensagem || 'Matéria criada com sucesso.');
            await atualizarTela();
        } catch (error) { mensagem(error.message, true); }
    });

    formRenomear.addEventListener('submit', async event => {
        event.preventDefault();
        const atual = selectRenomear.value;
        const novo = document.getElementById('novo-nome-materia').value.trim();
        if (!atual || !novo) return mensagem('Selecione a matéria e informe o novo nome.', true);
        try {
            const data = await api('/api/materias/categorias/gerenciar', {
                method: 'PATCH', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ atual, novo })
            });
            formRenomear.reset();
            mensagem(data.mensagem || 'Matéria renomeada; PDFs preservados.');
            await atualizarTela();
        } catch (error) { mensagem(error.message, true); }
    });

    formExcluir.addEventListener('submit', async event => {
        event.preventDefault();
        const nome = selectExcluir.value;
        const materia = materiasCache.find(item => item.nome === nome);
        if (!materia) return mensagem('Selecione uma matéria válida.', true);
        const aviso = materia.pdfs > 0
            ? `A matéria “${materia.nome}” possui ${materia.pdfs} PDF(s).\n\nSe continuar, TODOS esses PDFs também serão apagados. Essa ação não pode ser desfeita.\n\nDeseja realmente excluir a matéria e seus PDFs?`
            : `Deseja realmente excluir a matéria “${materia.nome}”? Essa ação não pode ser desfeita.`;
        if (!window.confirm(aviso)) {
            mensagem('Exclusão cancelada. Nenhuma alteração foi feita.');
            return;
        }
        try {
            const data = await api('/api/materias/categorias/gerenciar', {
                method: 'DELETE', headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ nome, confirmar: true })
            });
            formExcluir.reset();
            mensagem(data.mensagem || 'Matéria excluída.');
            await atualizarTela();
        } catch (error) { mensagem(error.message, true); }
    });

    async function atualizarTela() {
        await carregarMaterias();
        if (typeof carregarCategorias === 'function') await carregarCategorias();
    }

    async function iniciar() {
        try {
            const response = await fetch('/api/usuario', { credentials: 'same-origin', cache: 'no-store' });
            usuarioLogado = response.ok;
        } catch (_) { usuarioLogado = false; }
        botoes.forEach(botao => { botao.disabled = !usuarioLogado; });
        if (usuarioLogado) {
            await carregarMaterias();
            mensagem('Escolha uma das opções para gerenciar as matérias.');
        } else {
            mensagem('Entre na sua conta para adicionar, renomear ou excluir matérias.', true);
        }
    }
    iniciar();
})();
