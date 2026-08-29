from config.database import get_connection
from models.usuario_model import Usuario


class UsuarioRepository:

    @staticmethod
    def buscar_por_email(email):

        conn = get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT
                    id,
                    nome,
                    email,
                    senha
                FROM usuarios
                WHERE email = ?
                LIMIT 1
                """,
                (email.strip().lower(),)
            )

            resultado = cursor.fetchone()

            if resultado is None:
                return None

            return Usuario(
                id=resultado["id"],
                nome=resultado["nome"],
                email=resultado["email"],
                senha=resultado["senha"]
            )

        finally:
            conn.close()

    @staticmethod
    def criar(nome, email, senha_hash):

        conn = get_connection()

        try:
            cursor = conn.cursor()

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
                    nome,
                    email.strip().lower(),
                    senha_hash
                )
            )

            usuario_id = cursor.lastrowid

            conn.commit()

            cursor.execute(
                """
                SELECT
                    id,
                    nome,
                    email,
                    senha
                FROM usuarios
                WHERE id = ?
                """,
                (usuario_id,)
            )

            resultado = cursor.fetchone()

            return Usuario(
                id=resultado["id"],
                nome=resultado["nome"],
                email=resultado["email"],
                senha=resultado["senha"]
            )

        except Exception:
            conn.rollback()
            raise

        finally:
            conn.close()
