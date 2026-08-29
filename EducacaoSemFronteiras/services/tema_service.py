from repositories.tema_repository import TemaRepository


class TemaService:

    def __init__(self):
        self.repository = TemaRepository()

    def buscar(self, termo=None, dificuldade=None):
        if termo == "":
            termo = None

        if dificuldade == "":
            dificuldade = None

        return self.repository.buscar_temas(
            termo,
            dificuldade
        )

    def criar(self, dados):
        if not dados:
            raise ValueError("Nenhum dado foi enviado.")

        titulo = dados.get("titulo")
        descricao = dados.get("descricao")
        dificuldade = dados.get("dificuldade")

        if not titulo or not titulo.strip():
            raise ValueError("O campo 'titulo' é obrigatório.")

        if not dificuldade or not dificuldade.strip():
            raise ValueError("O campo 'dificuldade' é obrigatório.")

        titulo = titulo.strip()
        dificuldade = dificuldade.strip()

        if descricao is not None:
            descricao = descricao.strip()

        return self.repository.criar_tema(
            titulo,
            descricao,
            dificuldade
        )
    def buscar_por_id(self, tema_id):
        return self.repository.buscar_por_id(tema_id)
