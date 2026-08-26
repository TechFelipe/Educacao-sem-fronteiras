from config.database import db
from datetime import datetime


class Redacao(db.Model):
    __tablename__ = "redacoes"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey("usuarios.id", ondelete="CASCADE"),
        nullable=False
    )
    tema_id = db.Column(
        db.Integer,
        db.ForeignKey("temas.id"),
        nullable=False
    )
    texto = db.Column(db.Text, nullable=False)
    nota_total = db.Column(db.Integer, default=0, nullable=False)
    data_envio = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    usuario = db.relationship("Usuario", back_populates="redacoes")
    tema = db.relationship("Tema", back_populates="redacoes")
    competencias = db.relationship(
        "NotaCompetencia",
        back_populates="redacao",
        uselist=False,
        cascade="all, delete-orphan"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "usuario_id": self.usuario_id,
            "tema_id": self.tema_id,
            "texto": self.texto,
            "nota_total": self.nota_total,
            "data_envio": self.data_envio.isoformat() if self.data_envio else None,
        }
