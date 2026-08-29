
async function carregar() {
    const id = document.getElementById("usuario").value;
    if (!id) return;
    const [r,e,c] = await Promise.all([
        fetch(`/api/alunos/${id}/relatorio`).then(x=>x.json()),
        fetch(`/api/alunos/${id}/evolucao`).then(x=>x.json()),
        fetch(`/api/alunos/${id}/competencia-fraca`).then(x=>x.json())
    ]);
    document.getElementById("relatorio").innerHTML = `<div class="cards"><div class="card"><h2>${escapeHtml(r.nome||"-")}</h2><p>Redações: ${r.total_redacoes||0}</p></div><div class="card"><h2>${r.media||0}</h2><p>Média</p></div><div class="card"><h2>${r.melhor_nota||0}</h2><p>Melhor nota</p></div><div class="card"><h2>${r.menor_nota||0}</h2><p>Menor nota</p></div></div>`;
    document.getElementById("evolucao").innerHTML = "<h2>Evolução</h2>" + e.map(x=>`<div class="card"><b>${escapeHtml(x.tema)}</b> — ${x.nota_total} — ${escapeHtml(x.data_envio||"")}</div>`).join("");
    document.getElementById("fraca").innerHTML = `<div class="card"><h2>Competências</h2><p>C1: ${c.competencia1||0}</p><p>C2: ${c.competencia2||0}</p><p>C3: ${c.competencia3||0}</p><p>C4: ${c.competencia4||0}</p><p>C5: ${c.competencia5||0}</p></div>`;
}