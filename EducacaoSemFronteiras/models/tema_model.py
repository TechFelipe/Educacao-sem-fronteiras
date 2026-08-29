class Tema:

    def __init__(
        self,
        id=None,
        titulo=None,
        descricao=None,
        dificuldade=None,
        criado_em=None
    ):
        self.id = id
        self.titulo = titulo
        self.descricao = descricao
        self.dificuldade = dificuldade
        self.criado_em = criado_em

    def to_dict(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "descricao": self.descricao,
            "dificuldade": self.dificuldade,
            "criado_em": self.criado_em,
        }
