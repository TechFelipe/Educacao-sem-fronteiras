from pathlib import Path
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
from werkzeug.security import generate_password_hash

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database" / "enem_plus.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

# Instância única do SQLAlchemy usada por toda a aplicação.
db = SQLAlchemy()


def init_db(app):
    """Configura o SQLite e cria/popula as tabelas na primeira execução."""
    app.config.setdefault(
        "SQLALCHEMY_DATABASE_URI",
        f"sqlite:///{DB_PATH.as_posix()}"
    )
    app.config.setdefault("SQLALCHEMY_TRACK_MODIFICATIONS", False)

    db.init_app(app)

    with app.app_context():
        # Importar os modelos antes do create_all registra todas as tabelas.
        import models  # noqa: F401

        # Ativa foreign keys no SQLite para a conexão da aplicação.
        engine = db.engine

        @event.listens_for(engine, "connect")
        def _set_sqlite_pragma(dbapi_connection, connection_record):
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()

        db.create_all()
        seed_database()


def seed_database():
    """Insere os dados iniciais somente se ainda não existirem."""
    from models.usuario_model import Usuario
    from models.tema_model import Tema

    usuario_teste = Usuario.query.filter_by(email="aluno@teste.com").first()
    if usuario_teste is None:
        db.session.add(
            Usuario(
                nome="Aluno Teste",
                email="aluno@teste.com",
                senha=generate_password_hash("123456")
            )
        )
    elif not usuario_teste.senha.startswith(("scrypt:", "pbkdf2:")):
        # Migra automaticamente o usuário de teste criado em versões anteriores.
        usuario_teste.senha = generate_password_hash("123456")

    if Tema.query.count() == 0:
        db.session.add_all([
            Tema(
                titulo="Desafios da educação digital no Brasil",
                descricao="Os impactos da tecnologia no processo educacional brasileiro.",
                dificuldade="Media"
            ),
            Tema(
                titulo="Desafios para combater a desinformação no Brasil",
                descricao="Os efeitos das notícias falsas na sociedade brasileira.",
                dificuldade="Dificil"
            ),
            Tema(
                titulo="A importância da educação financeira para os jovens",
                descricao="A necessidade de preparar jovens para decisões financeiras.",
                dificuldade="Facil"
            ),
        ])

    db.session.commit()
