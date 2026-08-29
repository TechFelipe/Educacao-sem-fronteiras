from flask import Blueprint, request, jsonify
from services.redacao_service import RedacaoService


redacao_bp = Blueprint(
    "redacao",
    __name__
)

service = RedacaoService()

@redacao_bp.route("", methods=["POST"])
def criar():

    try:
        dados = request.get_json(silent=True)

        if not dados:
            return jsonify({
                "sucesso": False,
                "erro": "Nenhum dado foi enviado."
            }), 400

        resultado = service.criar(
            dados.get("usuario_id"),
            dados.get("tema_id"),
            dados.get("texto")
        )

        return jsonify({
            "sucesso": True,
            "mensagem": "Redação criada com sucesso.",
            "redacao": resultado
        }), 201

    except ValueError as e:

        return jsonify({
            "sucesso": False,
            "erro": str(e)
        }), 400

    except Exception as e:

        return jsonify({
            "sucesso": False,
            "erro": "Erro ao criar redação.",
            "detalhes": str(e)
        }), 500

@redacao_bp.route("/ranking", methods=["GET"])
def ranking():

    try:
        resultado = service.ranking()

        return jsonify(resultado), 200

    except Exception as e:

        return jsonify({
            "erro": "Erro ao buscar ranking.",
            "detalhes": str(e)
        }), 500
