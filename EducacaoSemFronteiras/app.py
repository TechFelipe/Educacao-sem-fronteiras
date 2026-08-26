from flask import Flask, jsonify, request, render_template, redirect, url_for, session, flash
from config.database import init_db, DB_PATH
from controllers.tema_controller import tema_bp
from controllers.redacao_controller import redacao_bp
from controllers.relatorio_controller import relatorio_bp
from services.auth_service import AuthService

app = Flask(__name__)
app.config["SECRET_KEY"] = "enem-plus-chave-local-2026"
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_PATH.as_posix()}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

init_db(app)

app.register_blueprint(tema_bp, url_prefix="/api/temas")
app.register_blueprint(redacao_bp, url_prefix="/api/redacoes")
app.register_blueprint(relatorio_bp, url_prefix="/api/alunos")


@app.context_processor
def inject_usuario():
    return {"usuario_logado": session.get("usuario")}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/temas")
def temas():
    return render_template("temas.html")


@app.route("/redacao")
def redacao():
    return render_template("redacao.html")


@app.route("/desempenho")
def desempenho():
    return render_template("desempenho.html")


@app.route("/ranking")
def ranking():
    return render_template("ranking.html")


@app.route("/assistente")
def assistente():
    return render_template("assistente.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = AuthService.autenticar(
            request.form.get("email"),
            request.form.get("senha"),
        )
        if usuario:
            session["usuario"] = {
                "id": usuario.id,
                "nome": usuario.nome,
                "email": usuario.email,
            }
            flash("Login realizado com sucesso!", "success")
            return redirect(url_for("dashboard"))

        flash("E-mail ou senha incorretos.", "error")
        return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        sucesso, mensagem = AuthService.cadastrar(
            request.form.get("email"),
            request.form.get("senha"),
            request.form.get("confirmar_senha"),
        )
        flash(mensagem, "success" if sucesso else "error")

        if sucesso:
            return redirect(url_for("login"))
        return render_template("cadastro.html")

    return render_template("cadastro.html")


@app.route("/logout")
def logout():
    session.pop("usuario", None)
    flash("Você saiu da conta.", "success")
    return redirect(url_for("dashboard"))


@app.errorhandler(404)
def not_found(error):
    return jsonify({"erro": "Rota não encontrada"}), 404


if __name__ == "__main__":
    app.run(debug=True)
