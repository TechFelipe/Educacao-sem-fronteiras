"""Configuração central do banco SQLite e do Flask-SQLAlchemy."""
from pathlib import Path
import sqlite3
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash

# Instância compartilhada usada pelas Models ORM.
db = SQLAlchemy()
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database" / "enem_plus.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)


def get_connection():
    """Abre conexão SQLite para consultas especiais encapsuladas nos Repositories."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db(app=None):
    """Configura SQLAlchemy, cria tabelas ausentes e mantém dados iniciais de teste."""
    if app is not None:
        app.config.setdefault("SQLALCHEMY_DATABASE_URI", f"sqlite:///{DB_PATH.as_posix()}")
        app.config.setdefault("SQLALCHEMY_TRACK_MODIFICATIONS", False)
        db.init_app(app)
        with app.app_context():
            # Importar aqui garante que todas as entidades estejam registradas no ORM.
            from models import Usuario, Tema, Redacao, NotaCompetencia  # noqa: F401
            db.create_all()
            _seed_database()


def _seed_database():
    """Cria usuário e temas de demonstração apenas quando o banco está vazio deles."""
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("SELECT id, senha FROM usuarios WHERE email = ? LIMIT 1", ("aluno@teste.com",))
        usuario = cur.fetchone()
        if usuario is None:
            cur.execute("INSERT INTO usuarios (nome,email,senha) VALUES (?,?,?)", (
                "Aluno Teste", "aluno@teste.com", generate_password_hash("123456")))
        elif not usuario["senha"].startswith(("scrypt:", "pbkdf2:")):
            cur.execute("UPDATE usuarios SET senha=? WHERE id=?", (
                generate_password_hash("123456"), usuario["id"]))
        cur.execute("SELECT COUNT(*) AS total FROM temas")
        if cur.fetchone()["total"] == 0:
            temas = [
                ("Desafios da educação digital no Brasil", "Impactos da tecnologia no processo educacional.", "Media"),
                ("Combate à desinformação no Brasil", "Efeitos das notícias falsas na sociedade.", "Dificil"),
                ("A importância da leitura na formação cidadã", "Leitura, educação e cidadania.", "Facil"),
                ("Inclusão de pessoas com deficiência nas escolas", "Acessibilidade e inclusão educacional.", "Media"),
                ("Sustentabilidade e consumo consciente", "Responsabilidade ambiental no cotidiano.", "Media"),
            ]
            cur.executemany("INSERT INTO temas (titulo,descricao,dificuldade) VALUES (?,?,?)", temas)
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
