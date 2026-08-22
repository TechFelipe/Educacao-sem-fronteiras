from flask import Flask, jsonify, request, render_template
from controllers.tema_controller import tema_bp
from controllers.redacao_controller import redacao_bp
from controllers.relatorio_controller import relatorio_bp

app = Flask(__name__)

app.register_blueprint(tema_bp, url_prefix="/api/temas")
app.register_blueprint(redacao_bp, url_prefix="/api/redacoes")
app.register_blueprint(relatorio_bp, url_prefix="/api/alunos")

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

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/cadastro")
def cadastro():
    return render_template("cadastro.html")

@app.errorhandler(404)
def not_found(error):
    return jsonify({"erro": "Rota não encontrada"}), 404

if __name__ == "__main__":
    app.run(debug=True)
