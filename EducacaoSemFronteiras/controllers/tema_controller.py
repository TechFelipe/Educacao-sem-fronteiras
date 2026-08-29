from flask import Blueprint, request, jsonify
from services.tema_service import TemaService


tema_bp = Blueprint("tema", __name__)

service = TemaService()

@tema_bp.route("/buscar", methods=["GET"])
def buscar():
    termo = request.args.get("termo")
    dificuldade = request.args.get("dificuldade")

    try:
        temas = service.buscar(
            termo,
            dificuldade
        )

        return jsonify(temas), 200

    except Exception as e:
        return jsonify({
            "erro": "Erro ao buscar temas.",
            "detalhes": str(e)
        }), 500

@tema_bp.route("", methods=["POST"])
def criar():
    dados = request.get_json(silent=True)

    if not dados:
        return jsonify({
            "sucesso": False,
            "erro": "Nenhum dado foi enviado."
        }), 400

    try:
        tema = service.criar(dados)

        return jsonify({
            "sucesso": True,
            "mensagem": "Tema criado com sucesso.",
            "tema": tema
        }), 201

    except ValueError as e:
        return jsonify({
            "sucesso": False,
            "erro": str(e)
        }), 400

    except Exception as e:
        return jsonify({
            "sucesso": False,
            "erro": "Erro ao criar tema.",
            "detalhes": str(e)
        }), 500

@tema_bp.route("/<int:tema_id>", methods=["GET"])
def buscar_por_id(tema_id):

    try:
        tema = service.buscar_por_id(tema_id)

        if tema is None:
            return jsonify({
                "erro": "Tema não encontrado."
            }), 404

        return jsonify(tema), 200

    except Exception as e:
        return jsonify({
            "erro": "Erro ao buscar tema.",
            "detalhes": str(e)
        }), 500