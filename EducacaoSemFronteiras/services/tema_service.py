from repositories.tema_repository import TemaRepository

class TemaService:
    def __init__(self):
        self.repository = TemaRepository()

    def buscar(self, termo=None, dificuldade=None):
        if termo == "":
            termo = None
        if dificuldade == "":
            dificuldade = None
        return self.repository.buscar_temas(termo, dificuldade)
