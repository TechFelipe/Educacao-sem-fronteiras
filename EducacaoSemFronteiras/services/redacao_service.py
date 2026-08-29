from repositories.redacao_repository import RedacaoRepository


class RedacaoService:

    def __init__(self):
        self.repository = RedacaoRepository()

    def criar(self, usuario_id, tema_id, texto):

        if not usuario_id:
            raise ValueError(
                "usuario_id é obrigatório"
            )

        if not tema_id:
            raise ValueError(
                "tema_id é obrigatório"
            )

        if not texto:
            raise ValueError(
                "texto é obrigatório"
            )

        texto = texto.strip()

        if len(texto) < 20:
            raise ValueError(
                "A redação deve possuir pelo menos 20 caracteres"
            )

        return self.repository.criar_redacao(
            usuario_id,
            tema_id,
            texto
        )

    def ranking(self):
        return self.repository.ranking()
