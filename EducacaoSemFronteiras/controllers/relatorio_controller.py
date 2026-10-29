"""Endpoints para indicadores, evolução e notas de competências."""
from flask import Blueprint, jsonify, session
from flask.views import MethodView
from services.relatorio_service import RelatorioService

relatorio_bp = Blueprint("relatorio", __name__)

class RelatorioController(MethodView):
    """Entrega um relatório consolidado de um aluno."""
    def get(self, usuario_id):
        try:
            dados = RelatorioService().relatorio(usuario_id)
            return (jsonify(dados), 200) if dados else (jsonify({"erro": "Usuário não encontrado."}), 404)
        except ValueError as erro:
            return jsonify({"erro": str(erro)}), 400

class EvolucaoController(MethodView):
    """Entrega a sequência histórica das notas de redação."""
    def get(self, usuario_id):
        try: return jsonify(RelatorioService().evolucao(usuario_id)), 200
        except ValueError as erro: return jsonify({"erro": str(erro)}), 400

class CompetenciaFracaController(MethodView):
    """Entrega médias das cinco competências do aluno."""
    def get(self, usuario_id):
        try: return jsonify(RelatorioService().competencia_fraca(usuario_id)), 200
        except ValueError as erro: return jsonify({"erro": str(erro)}), 400


class MeuDesempenhoController(MethodView):
    """Retorna o desempenho do usuário autenticado sem exigir que ele informe o ID."""
    def get(self):
        # A sessão é preenchida pelo LoginController após autenticação.
        usuario = session.get("usuario")

        # O mesmo objeto de sessão é preenchido pelo LoginController.
        # Sem um ID válido, não há como associar o relatório a uma conta autenticada.
        if not isinstance(usuario, dict) or not usuario.get("id"):
            return jsonify({"erro": "Entre na sua conta para consultar seu desempenho."}), 401

        try:
            usuario_id = int(usuario["id"])
            if usuario_id <= 0:
                return jsonify({"erro": "Sessão de usuário inválida. Entre novamente."}), 401

            # O ID vem exclusivamente da sessão assinada pelo Flask, nunca da tela.
            dados = RelatorioService().meu_desempenho(usuario_id)
            relatorio = dados.get("relatorio") or {}
            if not relatorio:
                return jsonify({"erro": "Não foi possível encontrar os dados deste usuário."}), 404

            # Devolve dados públicos da conta autenticada para a interface confirmar
            # qual usuário está vendo o relatório. Não retorna senha ou outros segredos.
            dados["usuario"] = {
                "nome": relatorio.get("nome") or usuario.get("nome") or "Estudante",
                "email": usuario.get("email"),
            }
            return jsonify(dados), 200
        except (ValueError, TypeError):
            return jsonify({"erro": "Sessão de usuário inválida. Entre novamente."}), 401


relatorio_bp.add_url_rule("/<int:usuario_id>/relatorio", view_func=RelatorioController.as_view("relatorio"), methods=["GET"])
relatorio_bp.add_url_rule("/<int:usuario_id>/evolucao", view_func=EvolucaoController.as_view("evolucao"), methods=["GET"])
relatorio_bp.add_url_rule("/<int:usuario_id>/competencia-fraca", view_func=CompetenciaFracaController.as_view("competencia_fraca"), methods=["GET"])

# A rota usa a sessão e não recebe usuario_id pela URL.
relatorio_bp.add_url_rule("/meu-desempenho", view_func=MeuDesempenhoController.as_view("meu_desempenho"), methods=["GET"])
