"""Consultas especiais de redações e ranking; SQL fica isolado nesta camada."""
from config.database import get_connection


class RedacaoRepository:

    def criar_redacao(
        self,
        usuario_id,
        tema_id,
        texto
    ):

        conn = get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO redacoes (
                    usuario_id,
                    tema_id,
                    texto,
                    nota_total
                )
                VALUES (?, ?, ?, ?)
                """,
                (
                    usuario_id,
                    tema_id,
                    texto,
                    0
                )
            )

            redacao_id = cursor.lastrowid

            conn.commit()

            cursor.execute(
                """
                SELECT
                    id,
                    usuario_id,
                    tema_id,
                    texto,
                    nota_total,
                    data_envio
                FROM redacoes
                WHERE id = ?
                """,
                (redacao_id,)
            )

            redacao = cursor.fetchone()

            return {
                "id": redacao["id"],
                "usuario_id": redacao["usuario_id"],
                "tema_id": redacao["tema_id"],
                "texto": redacao["texto"],
                "nota_total": redacao["nota_total"],
                "data_envio": redacao["data_envio"],
            }

        except Exception:
            conn.rollback()
            raise

        finally:
            conn.close()

    def ranking(self):

        conn = get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT
                    u.id,
                    u.nome,
                    COUNT(r.id) AS quantidade_redacoes,
                    ROUND(AVG(r.nota_total), 2) AS media,
                    MAX(r.nota_total) AS melhor_nota
                FROM usuarios u
                INNER JOIN redacoes r
                    ON u.id = r.usuario_id
                GROUP BY
                    u.id,
                    u.nome
                HAVING COUNT(r.id) > 0
                -- Primeiro: maior média das notas. Em caso de empate,
                -- vence quem enviou mais redações. O nome/ID estabiliza a ordem.
                ORDER BY
                    AVG(r.nota_total) DESC,
                    COUNT(r.id) DESC,
                    u.nome COLLATE NOCASE ASC,
                    u.id ASC
                """
            )

            resultados = cursor.fetchall()

            return [
                {
                    "id": resultado["id"],
                    "nome": resultado["nome"],
                    "quantidade_redacoes": resultado["quantidade_redacoes"],
                    "melhor_nota": (
                        int(resultado["melhor_nota"])
                        if resultado["melhor_nota"] is not None
                        else 0
                    ),
                    "media": (
                        float(resultado["media"])
                        if resultado["media"] is not None
                        else 0
                    ),
                }
                for resultado in resultados
            ]

        finally:
            conn.close()
