"""Entidade ORM que representa uma redação enviada por um aluno."""
from config.database import db
class Redacao(db.Model):
    __tablename__ = "redacoes"
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False)
    tema_id = db.Column(db.Integer, db.ForeignKey("temas.id"), nullable=False)
    texto = db.Column(db.Text, nullable=False)
    nota_total = db.Column(db.Integer, nullable=False, default=0)
    data_envio = db.Column(db.DateTime, server_default=db.func.current_timestamp(), nullable=False)
    tema = db.relationship("Tema", back_populates="redacoes")
    notas_competencias = db.relationship("NotaCompetencia", back_populates="redacao", cascade="all, delete-orphan")
    def salvar(self):
        """Persiste a redação."""
        db.session.add(self); db.session.commit(); return self
    def atualizar(self, **dados):
        """Atualiza texto ou nota total da redação."""
        for chave in ("texto", "nota_total"):
            if chave in dados: setattr(self, chave, dados[chave])
        db.session.commit(); return self
    def deletar(self):
        """Remove a redação e suas notas relacionadas."""
        db.session.delete(self); db.session.commit()
    @classmethod
    def listar_todos(cls):
        """Lista redações mais recentes primeiro."""
        return cls.query.order_by(cls.data_envio.desc()).all()
    @classmethod
    def buscar_por_id(cls, identificador):
        """Busca uma redação pelo ID."""
        return cls.query.get(identificador)
    def to_dict(self):
        """Serializa os campos principais da redação."""
        return {"id": self.id, "usuario_id": self.usuario_id, "tema_id": self.tema_id, "texto": self.texto, "nota_total": self.nota_total, "data_envio": self.data_envio.isoformat() if self.data_envio else None}
