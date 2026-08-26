from config.database import db
from datetime import datetime


class Tema(db.Model):
    __tablename__ = "temas"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    titulo = db.Column(db.String(255), nullable=False)
    descricao = db.Column(db.Text)
    dificuldade = db.Column(db.String(30), nullable=False)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    redacoes = db.relationship("Redacao", back_populates="tema")

    def to_dict(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "descricao": self.descricao,
            "dificuldade": self.dificuldade,
            "criado_em": self.criado_em.isoformat() if self.criado_em else None,
        }
