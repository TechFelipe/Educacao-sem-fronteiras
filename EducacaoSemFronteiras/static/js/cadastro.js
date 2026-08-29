document.getElementById("cadastroForm").addEventListener("submit", async e => {
    e.preventDefault();
    const msg = document.getElementById("msg");
    const dados = Object.fromEntries(new FormData(e.currentTarget));
    const res = await fetch("/api/auth/cadastro", {method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify(dados)});
    const json = await res.json();
    if (res.ok) {
        msg.textContent = json.mensagem;
        msg.className = "auth-message success";
        setTimeout(() => location.href = "/login", 1000);
    } else {
        msg.textContent = json.erro || "Não foi possível cadastrar.";
        msg.className = "auth-message error";
    }
});