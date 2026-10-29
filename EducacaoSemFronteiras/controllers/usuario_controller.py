"""Endpoints de sessão, login, cadastro e consulta do usuário autenticado."""
from flask import Blueprint, jsonify, request, session
from flask.views import MethodView
from services.auth_service import AuthService

usuario_bp = Blueprint("usuario", __name__)

class UsuarioAtualController(MethodView):
    """Retorna o estado da sessão sem revelar informações sensíveis."""
    def get(self):
        usuario = session.get("usuario")
        if not usuario: return jsonify({"logado": False}), 401
        return jsonify({"logado": True, **usuario}), 200

class LoginController(MethodView):
    """Autentica credenciais e grava os dados públicos na sessão."""
    def post(self):
        dados = request.get_json(silent=True) or {}
        usuario = AuthService.autenticar(dados.get("email"), dados.get("senha"))
        if not usuario: return jsonify({"sucesso": False, "erro": "E-mail ou senha incorretos."}), 401
        session["usuario"] = {"id": usuario.id, "nome": usuario.nome, "email": usuario.email}
        return jsonify({"sucesso": True, "usuario": session["usuario"]}), 200

class CadastroController(MethodView):
    """Valida os campos de cadastro e responde com o status apropriado."""
    def post(self):
        dados = request.get_json(silent=True) or {}
        sucesso, mensagem = AuthService.cadastrar(dados.get("email"), dados.get("senha"), dados.get("confirmar_senha"))
        if not sucesso: return jsonify({"sucesso": False, "erro": mensagem}), 400
        return jsonify({"sucesso": True, "mensagem": mensagem}), 201

usuario_bp.add_url_rule("/usuario", view_func=UsuarioAtualController.as_view("atual"), methods=["GET"])
usuario_bp.add_url_rule("/auth/login", view_func=LoginController.as_view("login"), methods=["POST"])
usuario_bp.add_url_rule("/auth/cadastro", view_func=CadastroController.as_view("cadastro"), methods=["POST"])
