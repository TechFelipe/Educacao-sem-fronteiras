function searchHome() {
    location.href = "/temas?termo=" + encodeURIComponent(document.getElementById("homeSearch").value);
}