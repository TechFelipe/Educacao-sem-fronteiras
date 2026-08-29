from pathlib import Path
import sqlite3

from werkzeug.security import generate_password_hash


BASE_DIR = Path(__file__).resolve().parent.parent

DB_PATH = BASE_DIR / "database" / "enem_plus.db"

DB_PATH.parent.mkdir(
    parents=True,
    exist_ok=True
)


def get_connection():
    """
    Cria uma conexão com o banco SQLite.

    Todas as operações do projeto devem usar esta função
    para acessar o banco.
    """

    conn = sqlite3.connect(DB_PATH)

    conn.row_factory = sqlite3.Row

    # Ativa as chaves estrangeiras do SQLite
    conn.execute("PRAGMA foreign_keys = ON")

    return conn


def init_db(app=None):
    """
    Cria as tabelas do banco caso elas ainda não existam
    e insere os dados iniciais.
    """

    conn = get_connection()

    try:
        cursor = conn.cursor()

        # =====================================================
        # TABELA USUARIOS
        # =====================================================

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome VARCHAR(100) NOT NULL,
                email VARCHAR(150) NOT NULL UNIQUE,
                senha VARCHAR(255) NOT NULL
            )
            """
        )

        # =====================================================
        # TABELA TEMAS
        # =====================================================

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS temas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo VARCHAR(255) NOT NULL,
                descricao TEXT,
                dificuldade VARCHAR(30) NOT NULL,
                criado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        # =====================================================
        # TABELA REDACOES
        # =====================================================

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS redacoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER NOT NULL,
                tema_id INTEGER NOT NULL,
                texto TEXT NOT NULL,
                nota_total INTEGER NOT NULL DEFAULT 0,
                data_envio DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY (usuario_id)
                    REFERENCES usuarios(id)
                    ON DELETE CASCADE,

                FOREIGN KEY (tema_id)
                    REFERENCES temas(id)
            )
            """
        )

        # =====================================================
        # TABELA NOTAS_COMPETENCIAS
        # =====================================================

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS notas_competencias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                redacao_id INTEGER NOT NULL,

                competencia1 INTEGER NOT NULL DEFAULT 0,
                competencia2 INTEGER NOT NULL DEFAULT 0,
                competencia3 INTEGER NOT NULL DEFAULT 0,
                competencia4 INTEGER NOT NULL DEFAULT 0,
                competencia5 INTEGER NOT NULL DEFAULT 0,

                FOREIGN KEY (redacao_id)
                    REFERENCES redacoes(id)
                    ON DELETE CASCADE
            )
            """
        )

        conn.commit()

        seed_database(conn)

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()


def seed_database(conn):
    """
    Insere dados iniciais somente se ainda não existirem.
    """

    cursor = conn.cursor()

    # =====================================================
    # USUARIO DE TESTE
    # =====================================================

    cursor.execute(
        """
        SELECT id, senha
        FROM usuarios
        WHERE email = ?
        LIMIT 1
        """,
        ("aluno@teste.com",)
    )

    usuario_teste = cursor.fetchone()

    if usuario_teste is None:

        senha_hash = generate_password_hash("123456")

        cursor.execute(
            """
            INSERT INTO usuarios (
                nome,
                email,
                senha
            )
            VALUES (?, ?, ?)
            """,
            (
                "Aluno Teste",
                "aluno@teste.com",
                senha_hash
            )
        )

    else:
        senha_atual = usuario_teste["senha"]

        # Atualiza senhas antigas que não estejam usando
        # os formatos atuais do Werkzeug.
        if not senha_atual.startswith(
            ("scrypt:", "pbkdf2:")
        ):
            cursor.execute(
                """
                UPDATE usuarios
                SET senha = ?
                WHERE id = ?
                """,
                (
                    generate_password_hash("123456"),
                    usuario_teste["id"]
                )
            )

    # =====================================================
    # TEMAS INICIAIS
    # =====================================================

    cursor.execute(
        """
        SELECT COUNT(*) AS quantidade
        FROM temas
        """
    )

    quantidade_temas = cursor.fetchone()["quantidade"]

    if quantidade_temas == 0:

        temas = [
            (
                "Desafios da educação digital no Brasil",
                "Os impactos da tecnologia no processo educacional brasileiro.",
                "Media"
            ),
            (
                "Desafios para combater a desinformação no Brasil",
                "Os efeitos das notícias falsas na sociedade brasileira.",
                "Dificil"
            ),
            (
                "A importância da educação financeira para os jovens",
                "A necessidade de preparar jovens para decisões financeiras.",
                "Facil"
            ),
        ]

        cursor.executemany(
            """
            INSERT INTO temas (
                titulo,
                descricao,
                dificuldade
            )
            VALUES (?, ?, ?)
            """,
            temas
        )

    conn.commit()
