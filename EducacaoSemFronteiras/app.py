from controllers.usuario_controller import usuario_bp

from flask import (
    Flask,
    jsonify,
    send_from_directory,
    redirect,
)

from pathlib import Path

from config.database import init_db

from controllers.tema_controller import tema_bp
from controllers.redacao_controller import redacao_bp
from controllers.relatorio_controller import relatorio_bp
from controllers.usuario_controller import usuario_bp


app = Flask(__name__)

app.config["SECRET_KEY"] = "enem-plus-chave-local-2026"


# ============================================================
# FRONTEND
# ============================================================

FRONTEND_DIR = Path(app.root_path) / "frontend"


# ============================================================
# BANCO DE DADOS
# ============================================================

init_db(app)


# ============================================================
# BLUEPRINTS / APIs
# ============================================================

app.register_blueprint(
    tema_bp,
    url_prefix="/api/temas"
)

app.register_blueprint(
    redacao_bp,
    url_prefix="/api/redacoes"
)

app.register_blueprint(
    relatorio_bp,
    url_prefix="/api/alunos"
)

app.register_blueprint(
    usuario_bp,
    url_prefix="/api"
)


# ============================================================
# FRONTEND / PÁGINAS
# ============================================================

@app.route("/")
def index():
    return send_from_directory(
        str(FRONTEND_DIR),
        "index.html"
    )


@app.route("/dashboard")
def dashboard():
    return send_from_directory(
        str(FRONTEND_DIR),
        "dashboard.html"
    )


@app.route("/temas")
def temas():
    return send_from_directory(
        str(FRONTEND_DIR),
        "temas.html"
    )


@app.route("/redacao")
def redacao():
    return send_from_directory(
        str(FRONTEND_DIR),
        "redacao.html"
    )


@app.route("/desempenho")
def desempenho():
    return send_from_directory(
        str(FRONTEND_DIR),
        "desempenho.html"
    )


@app.route("/ranking")
def ranking():
    return send_from_directory(
        str(FRONTEND_DIR),
        "ranking.html"
    )


@app.route("/assistente")
def assistente():
    return send_from_directory(
        str(FRONTEND_DIR),
        "assistente.html"
    )


@app.route("/login")
def login():
    return send_from_directory(
        str(FRONTEND_DIR),
        "login.html"
    )


@app.route("/cadastro")
def cadastro():
    return send_from_directory(
        str(FRONTEND_DIR),
        "cadastro.html"
    )


# ============================================================
# LOGOUT
# ============================================================

@app.route("/logout")
def logout():

    from flask import session

    session.pop("usuario", None)

    return redirect("/dashboard")


# ============================================================
# ERRO 404
# ============================================================

@app.errorhandler(404)
def not_found(error):

    return jsonify({
        "erro": "Rota não encontrada"
    }), 404


# ============================================================
# EXECUÇÃO
# ============================================================

if __name__ == "__main__":
    app.run(
        debug=True
    )
