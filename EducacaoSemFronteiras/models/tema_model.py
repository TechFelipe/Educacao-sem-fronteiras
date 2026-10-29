"""Entidade ORM que representa um tema de redação."""
from config.database import db
class Tema(db.Model):
    __tablename__ = "temas"
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(255), nullable=False)
    descricao = db.Column(db.Text)
    dificuldade = db.Column(db.String(30), nullable=False)
    criado_em = db.Column(db.DateTime, server_default=db.func.current_timestamp(), nullable=False)
    redacoes = db.relationship("Redacao", back_populates="tema", lazy=True)
    def salvar(self):
        """Salva um tema novo no banco."""
        db.session.add(self); db.session.commit(); return self
    def atualizar(self, **dados):
        """Atualiza título, descrição ou dificuldade do tema."""
        for chave in ("titulo", "descricao", "dificuldade"):
            if chave in dados: setattr(self, chave, dados[chave])
        db.session.commit(); return self
    def deletar(self):
        """Exclui o tema após validar dependências no serviço."""
        db.session.delete(self); db.session.commit()
    @classmethod
    def listar_todos(cls):
        """Lista temas em ordem alfabética."""
        return cls.query.order_by(cls.titulo.asc()).all()
    @classmethod
    def buscar_por_id(cls, identificador):
        """Busca um tema pelo ID."""
        return cls.query.get(identificador)
    def to_dict(self):
        """Converte o tema em objeto seguro para a API."""
        return {"id": self.id, "titulo": self.titulo, "descricao": self.descricao, "dificuldade": self.dificuldade, "criado_em": self.criado_em.isoformat() if self.criado_em else None}
