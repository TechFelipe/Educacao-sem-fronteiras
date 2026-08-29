document.getElementById("loginForm").addEventListener("submit", async e => {
    e.preventDefault();
    const msg = document.getElementById("msg");
    const dados = Object.fromEntries(new FormData(e.currentTarget));
    const res = await fetch("/api/auth/login", {method:"POST", headers:{"Content-Type":"application/json"}, credentials:"same-origin", body:JSON.stringify(dados)});
    const json = await res.json();
    if (res.ok) location.href = "/dashboard";
    else { msg.textContent = json.erro || "Erro ao fazer login."; msg.className = "auth-message error"; }
});