from repositories.redacao_repository import RedacaoRepository

class RedacaoService:
    def __init__(self):
        self.repository = RedacaoRepository()

    def criar(self, usuario_id, tema_id, texto):
        if not usuario_id or not tema_id or not texto:
            raise ValueError("usuario_id, tema_id e texto são obrigatórios")
        if len(texto.strip()) < 20:
            raise ValueError("A redação deve possuir pelo menos 20 caracteres")
        return self.repository.criar_redacao(usuario_id, tema_id, texto)

    def ranking(self):
        return self.repository.ranking()
