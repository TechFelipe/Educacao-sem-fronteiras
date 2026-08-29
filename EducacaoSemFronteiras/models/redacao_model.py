class Redacao:

    def __init__(
        self,
        id=None,
        usuario_id=None,
        tema_id=None,
        texto=None,
        nota_total=0,
        data_envio=None
    ):
        self.id = id
        self.usuario_id = usuario_id
        self.tema_id = tema_id
        self.texto = texto
        self.nota_total = nota_total
        self.data_envio = data_envio

    def to_dict(self):
        return {
            "id": self.id,
            "usuario_id": self.usuario_id,
            "tema_id": self.tema_id,
            "texto": self.texto,
            "nota_total": self.nota_total,
            "data_envio": self.data_envio,
        }
