"""Casos de uso e regras de validação para envio de redações e ranking."""
from repositories.redacao_repository import RedacaoRepository
from models.redacao_model import Redacao

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

        redacao = Redacao(
            usuario_id=usuario_id,
            tema_id=tema_id,
            texto=texto
        )

        redacao.salvar()

    def ranking(self):
        return self.repository.ranking()
