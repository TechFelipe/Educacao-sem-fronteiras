from config.database import db
from models.usuario_model import Usuario


class UsuarioRepository:
    @staticmethod
    def buscar_por_email(email):
        return Usuario.query.filter_by(email=email.strip().lower()).first()

    @staticmethod
    def criar(nome, email, senha_hash):
        usuario = Usuario(
            nome=nome,
            email=email.strip().lower(),
            senha=senha_hash,
        )
        db.session.add(usuario)
        db.session.commit()
        return usuario
