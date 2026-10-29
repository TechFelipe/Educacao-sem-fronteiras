"""Endpoints HTTP de temas. A Controller apenas interpreta HTTP e chama o Service."""
from flask import Blueprint, request, jsonify
from flask.views import MethodView
from services.tema_service import TemaService

tema_bp = Blueprint("tema", __name__)

class TemaBuscarController(MethodView):
    """Consulta temas usando filtros opcionais."""
    def get(self):
        try:
            dados = TemaService().buscar(request.args.get("termo"), request.args.get("dificuldade"))
            return jsonify(dados), 200
        except Exception:
            return jsonify({"erro": "Erro ao buscar temas."}), 500

class TemaController(MethodView):
    """Cria um tema e valida o retorno HTTP."""
    def post(self):
        try:
            tema = TemaService().criar(request.get_json(silent=True) or {})
            return jsonify({"sucesso": True, "mensagem": "Tema criado com sucesso.", "tema": tema}), 201
        except ValueError as erro:
            return jsonify({"sucesso": False, "erro": str(erro)}), 400
        except Exception:
            return jsonify({"sucesso": False, "erro": "Erro ao criar tema."}), 500

class TemaDetalheController(MethodView):
    """Consulta, atualiza ou exclui um tema pelo identificador."""
    def get(self, tema_id):
        try:
            tema = TemaService().buscar_por_id(tema_id)
            return (jsonify(tema), 200) if tema else (jsonify({"erro": "Tema não encontrado."}), 404)
        except ValueError as erro:
            return jsonify({"erro": str(erro)}), 400
        except Exception:
            return jsonify({"erro": "Erro ao buscar tema."}), 500
    def put(self, tema_id):
        try:
            tema = TemaService().atualizar(tema_id, request.get_json(silent=True) or {})
            return (jsonify({"sucesso": True, "tema": tema}), 200) if tema else (jsonify({"erro": "Tema não encontrado."}), 404)
        except ValueError as erro:
            return jsonify({"erro": str(erro)}), 400
        except Exception:
            return jsonify({"erro": "Erro ao atualizar tema."}), 500
    def delete(self, tema_id):
        try:
            resultado = TemaService().deletar(tema_id)
            return (jsonify({"sucesso": True, "mensagem": "Tema excluído."}), 200) if resultado else (jsonify({"erro": "Tema não encontrado."}), 404)
        except ValueError as erro:
            return jsonify({"erro": str(erro)}), 409
        except Exception:
            return jsonify({"erro": "Erro ao excluir tema."}), 500

tema_bp.add_url_rule("/buscar", view_func=TemaBuscarController.as_view("buscar"), methods=["GET"])
tema_bp.add_url_rule("", view_func=TemaController.as_view("criar"), methods=["POST"])
tema_bp.add_url_rule("/<int:tema_id>", view_func=TemaDetalheController.as_view("detalhe"), methods=["GET", "PUT", "DELETE"])
