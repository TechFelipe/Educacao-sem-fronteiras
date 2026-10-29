"""Entidade ORM que representa uma conta de usuário."""
from config.database import db

class Usuario(db.Model):
    __tablename__ = "usuarios"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    senha = db.Column(db.String(255), nullable=False)

    def salvar(self):
        """Persiste um novo usuário e confirma a transação."""
        db.session.add(self); db.session.commit(); return self
    def atualizar(self, **dados):
        """Atualiza somente atributos existentes e confirma a transação."""
        for chave, valor in dados.items():
            if chave in {"nome", "email", "senha"}: setattr(self, chave, valor)
        db.session.commit(); return self
    def deletar(self):
        """Remove o usuário e confirma a transação."""
        db.session.delete(self); db.session.commit()
    @classmethod
    def listar_todos(cls):
        """Retorna todos os usuários cadastrados."""
        return cls.query.order_by(cls.nome.asc()).all()
    @classmethod
    def buscar_por_id(cls, identificador):
        """Busca um usuário pela chave primária."""
        return cls.query.get(identificador)
    def to_dict(self):
        """Serializa dados públicos, sem expor o hash da senha."""
        return {"id": self.id, "nome": self.nome, "email": self.email}
