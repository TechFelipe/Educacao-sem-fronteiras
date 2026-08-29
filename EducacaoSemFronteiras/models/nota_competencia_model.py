class NotaCompetencia:

    def __init__(
        self,
        id=None,
        redacao_id=None,
        competencia1=0,
        competencia2=0,
        competencia3=0,
        competencia4=0,
        competencia5=0
    ):
        self.id = id
        self.redacao_id = redacao_id
        self.competencia1 = competencia1
        self.competencia2 = competencia2
        self.competencia3 = competencia3
        self.competencia4 = competencia4
        self.competencia5 = competencia5

    def to_dict(self):
        return {
            "id": self.id,
            "redacao_id": self.redacao_id,
            "competencia1": self.competencia1,
            "competencia2": self.competencia2,
            "competencia3": self.competencia3,
            "competencia4": self.competencia4,
            "competencia5": self.competencia5,
        }
