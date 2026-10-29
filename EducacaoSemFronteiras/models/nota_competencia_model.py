"""Notas das cinco competências associadas a uma redação."""
from config.database import db
class NotaCompetencia(db.Model):
    __tablename__ = "notas_competencias"
    id = db.Column(db.Integer, primary_key=True)
    redacao_id = db.Column(db.Integer, db.ForeignKey("redacoes.id", ondelete="CASCADE"), nullable=False)
    competencia1 = db.Column(db.Integer, nullable=False, default=0)
    competencia2 = db.Column(db.Integer, nullable=False, default=0)
    competencia3 = db.Column(db.Integer, nullable=False, default=0)
    competencia4 = db.Column(db.Integer, nullable=False, default=0)
    competencia5 = db.Column(db.Integer, nullable=False, default=0)
    redacao = db.relationship("Redacao", back_populates="notas_competencias")
    def salvar(self):
        """Salva as notas das competências."""
        db.session.add(self); db.session.commit(); return self
    def atualizar(self, **dados):
        """Atualiza valores das competências informadas."""
        for chave in ("competencia1", "competencia2", "competencia3", "competencia4", "competencia5"):
            if chave in dados: setattr(self, chave, dados[chave])
        db.session.commit(); return self
    def deletar(self):
        """Remove o registro de notas."""
        db.session.delete(self); db.session.commit()
    @classmethod
    def listar_todos(cls):
        """Lista todas as notas registradas."""
        return cls.query.all()
    @classmethod
    def buscar_por_id(cls, identificador):
        """Busca um conjunto de notas pelo ID."""
        return cls.query.get(identificador)
    def to_dict(self):
        """Converte notas em dicionário para respostas da API."""
        return {"id": self.id, "redacao_id": self.redacao_id, **{f"competencia{i}": getattr(self, f"competencia{i}") for i in range(1, 6)}}
