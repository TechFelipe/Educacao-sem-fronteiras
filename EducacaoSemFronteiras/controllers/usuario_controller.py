from flask import Blueprint, jsonify, request, session

from services.auth_service import AuthService


usuario_bp = Blueprint(
    "usuario",
    __name__
)


# ============================================================
# USUÁRIO LOGADO
# ============================================================

@usuario_bp.route("/usuario", methods=["GET"])
def api_usuario():

    usuario = session.get("usuario")

    if not usuario:
        return jsonify({
            "logado": False
        }), 401

    return jsonify({
        "logado": True,
        **usuario
    })


# ============================================================
# LOGIN
# ============================================================

@usuario_bp.route("/auth/login", methods=["POST"])
def api_login():

    dados = request.get_json(silent=True) or {}

    usuario = AuthService.autenticar(
        dados.get("email"),
        dados.get("senha")
    )

    if not usuario:
        return jsonify({
            "sucesso": False,
            "erro": "E-mail ou senha incorretos."
        }), 401

    session["usuario"] = {
        "id": usuario.id,
        "nome": usuario.nome,
        "email": usuario.email,
    }

    return jsonify({
        "sucesso": True,
        "usuario": session["usuario"]
    })


# ============================================================
# CADASTRO
# ============================================================

@usuario_bp.route("/auth/cadastro", methods=["POST"])
def api_cadastro():

    dados = request.get_json(silent=True) or {}

    sucesso, mensagem = AuthService.cadastrar(
        dados.get("email"),
        dados.get("senha"),
        dados.get("confirmar_senha")
    )

    if not sucesso:
        return jsonify({
            "sucesso": False,
            "erro": mensagem
        }), 400

    return jsonify({
        "sucesso": True,
        "mensagem": mensagem
    }), 201
