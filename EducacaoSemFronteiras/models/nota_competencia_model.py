from config.database import db


class NotaCompetencia(db.Model):
    __tablename__ = "notas_competencias"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    redacao_id = db.Column(
        db.Integer,
        db.ForeignKey("redacoes.id", ondelete="CASCADE"),
        nullable=False
    )
    competencia1 = db.Column(db.Integer, default=0, nullable=False)
    competencia2 = db.Column(db.Integer, default=0, nullable=False)
    competencia3 = db.Column(db.Integer, default=0, nullable=False)
    competencia4 = db.Column(db.Integer, default=0, nullable=False)
    competencia5 = db.Column(db.Integer, default=0, nullable=False)

    redacao = db.relationship("Redacao", back_populates="competencias")
