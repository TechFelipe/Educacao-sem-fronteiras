"""Endpoints HTTP das operações CRUD de materiais em PDF."""
from flask import Blueprint, jsonify, request, session, make_response
from flask.views import MethodView
from werkzeug.utils import secure_filename

from services.pdf_service import PdfService

pdf_bp = Blueprint("materiais", __name__)


def _exigir_login():
    """Bloqueia alterações por visitantes que ainda não entraram na conta."""
    if not session.get("usuario"):
        return jsonify({"sucesso": False, "erro": "Entre na sua conta para gerenciar os PDFs."}), 401
    return None


class MateriasCategoriasController(MethodView):
    def get(self):
        try:
            return jsonify(PdfService().listar_categorias()), 200
        except Exception:
            return jsonify({"erro": "Não foi possível listar as matérias."}), 500


class MateriaisController(MethodView):
    def get(self):
        try:
            materiais = PdfService().listar(
                termo=request.args.get("termo", ""),
                materia=request.args.get("materia", ""),
                todos=request.args.get("administracao") == "1",
            )
            return jsonify(materiais), 200
        except Exception:
            return jsonify({"erro": "Não foi possível listar os PDFs."}), 500

    def post(self):
        bloqueio = _exigir_login()
        if bloqueio:
            return bloqueio
        try:
            material = PdfService().adicionar(request.form, request.files.get("arquivo"))
            return jsonify({"sucesso": True, "mensagem": "PDF adicionado com sucesso.", "material": material}), 201
        except ValueError as erro:
            return jsonify({"sucesso": False, "erro": str(erro)}), 400
        except Exception:
            return jsonify({"sucesso": False, "erro": "Erro ao salvar o PDF no banco de dados."}), 500


class MaterialDetalheController(MethodView):
    def patch(self, material_id):
        bloqueio = _exigir_login()
        if bloqueio:
            return bloqueio
        try:
            material = PdfService().editar(material_id, request.get_json(silent=True) or {})
            if not material:
                return jsonify({"sucesso": False, "erro": "PDF não encontrado."}), 404
            return jsonify({"sucesso": True, "mensagem": "Dados do PDF atualizados.", "material": material}), 200
        except ValueError as erro:
            return jsonify({"sucesso": False, "erro": str(erro)}), 400
        except Exception:
            return jsonify({"sucesso": False, "erro": "Erro ao editar o PDF."}), 500

    def delete(self, material_id):
        bloqueio = _exigir_login()
        if bloqueio:
            return bloqueio
        try:
            excluido = PdfService().excluir(material_id)
            if not excluido:
                return jsonify({"sucesso": False, "erro": "PDF não encontrado."}), 404
            return jsonify({"sucesso": True, "mensagem": "PDF excluído com sucesso."}), 200
        except ValueError as erro:
            return jsonify({"sucesso": False, "erro": str(erro)}), 409
        except Exception:
            return jsonify({"sucesso": False, "erro": "Erro ao excluir o PDF."}), 500


class MaterialArquivoController(MethodView):
    def get(self, material_id):
        try:
            material = PdfService().repository.obter_arquivo(material_id)
            if not material:
                return jsonify({"erro": "PDF não encontrado."}), 404
            resposta = make_response(material["arquivo"])
            resposta.headers["Content-Type"] = "application/pdf"
            nome_seguro = secure_filename(material["nome_arquivo"]) or "material.pdf"
            resposta.headers["Content-Disposition"] = f'inline; filename="{nome_seguro}"'
            resposta.headers["X-Content-Type-Options"] = "nosniff"
            return resposta
        except Exception:
            return jsonify({"erro": "Não foi possível abrir o PDF."}), 500

    def put(self, material_id):
        bloqueio = _exigir_login()
        if bloqueio:
            return bloqueio
        try:
            material = PdfService().substituir_pdf(material_id, request.files.get("arquivo"))
            if not material:
                return jsonify({"sucesso": False, "erro": "PDF não encontrado."}), 404
            return jsonify({"sucesso": True, "mensagem": "Arquivo PDF substituído com sucesso.", "material": material}), 200
        except ValueError as erro:
            return jsonify({"sucesso": False, "erro": str(erro)}), 400
        except Exception:
            return jsonify({"sucesso": False, "erro": "Erro ao substituir o arquivo PDF."}), 500


pdf_bp.add_url_rule("/categorias", view_func=MateriasCategoriasController.as_view("categorias"), methods=["GET"])
pdf_bp.add_url_rule("", view_func=MateriaisController.as_view("colecao"), methods=["GET", "POST"])
pdf_bp.add_url_rule("/<material_id>", view_func=MaterialDetalheController.as_view("detalhe"), methods=["PATCH", "DELETE"])
pdf_bp.add_url_rule("/<material_id>/pdf", view_func=MaterialArquivoController.as_view("arquivo"), methods=["GET", "PUT"])
