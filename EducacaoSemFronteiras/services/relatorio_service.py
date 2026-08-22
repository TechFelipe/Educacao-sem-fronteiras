from repositories.relatorio_repository import RelatorioRepository

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
