"""Validação dos identificadores e coordenação dos relatórios do aluno."""
from repositories.relatorio_repository import RelatorioRepository
from repositories.redacao_repository import RedacaoRepository

class RelatorioService:
    def __init__(self):
        self.repository = RelatorioRepository()

    def validar_id(self, usuario_id):
        try:
            return int(usuario_id)
        except (ValueError, TypeError):
            raise ValueError("ID de usuário inválido")

    def relatorio(self, usuario_id):
        return self.repository.relatorio_aluno(self.validar_id(usuario_id))

    def evolucao(self, usuario_id):
        return self.repository.evolucao(self.validar_id(usuario_id))

    def competencia_fraca(self, usuario_id):
        return self.repository.competencia_fraca(self.validar_id(usuario_id))


    def meu_desempenho(self, usuario_id):
        """
        Monta todos os indicadores individuais em uma única resposta para a tela.

        O ID é fornecido pelo backend a partir da sessão autenticada, não pelo
        navegador. Os métodos chamados continuam delegando a persistência ao Repository.
        """
        usuario_id = self.validar_id(usuario_id)
        relatorio = self.relatorio(usuario_id)

        # Usa exatamente a mesma ordenação da página de ranking global.
        classificacao = RedacaoRepository().ranking()
        posicao = next(
            (indice + 1 for indice, estudante in enumerate(classificacao)
             if int(estudante["id"]) == usuario_id),
            None
        )

        return {
            "relatorio": relatorio,
            "evolucao": self.evolucao(usuario_id),
            "competencias": self.competencia_fraca(usuario_id),
            "ranking": {
                "posicao": posicao,
                "total_estudantes": len(classificacao),
            },
        }
