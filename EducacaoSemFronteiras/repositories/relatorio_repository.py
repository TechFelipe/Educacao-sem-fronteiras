from config.database import get_connection


class RelatorioRepository:

    def relatorio_aluno(self, usuario_id):

        conn = get_connection()

        try:
            cursor = conn.cursor()

            # =================================================
            # USUARIO
            # =================================================

            cursor.execute(
                """
                SELECT
                    id,
                    nome
                FROM usuarios
                WHERE id = ?
                LIMIT 1
                """,
                (usuario_id,)
            )

            usuario = cursor.fetchone()

            if usuario is None:
                return {}

            # =================================================
            # TOTAL DE REDAÇÕES
            # =================================================

            cursor.execute(
                """
                SELECT COUNT(*) AS total
                FROM redacoes
                WHERE usuario_id = ?
                """,
                (usuario_id,)
            )

            total = cursor.fetchone()["total"]

            # =================================================
            # MÉDIA
            # =================================================

            cursor.execute(
                """
                SELECT AVG(nota_total) AS media
                FROM redacoes
                WHERE usuario_id = ?
                """,
                (usuario_id,)
            )

            media = cursor.fetchone()["media"]

            # =================================================
            # MELHOR NOTA
            # =================================================

            cursor.execute(
                """
                SELECT MAX(nota_total) AS melhor
                FROM redacoes
                WHERE usuario_id = ?
                """,
                (usuario_id,)
            )

            melhor = cursor.fetchone()["melhor"]

            # =================================================
            # MENOR NOTA
            # =================================================

            cursor.execute(
                """
                SELECT MIN(nota_total) AS menor
                FROM redacoes
                WHERE usuario_id = ?
                """,
                (usuario_id,)
            )

            menor = cursor.fetchone()["menor"]

            return {
                "nome": usuario["nome"],
                "total_redacoes": total,
                "media": (
                    round(float(media), 2)
                    if media is not None
                    else 0
                ),
                "melhor_nota": (
                    int(melhor)
                    if melhor is not None
                    else 0
                ),
                "menor_nota": (
                    int(menor)
                    if menor is not None
                    else 0
                ),
            }

        finally:
            conn.close()

    def evolucao(self, usuario_id):

        conn = get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT
                    r.id,
                    t.titulo AS tema,
                    r.nota_total,
                    r.data_envio
                FROM redacoes r
                INNER JOIN temas t
                    ON r.tema_id = t.id
                WHERE r.usuario_id = ?
                ORDER BY r.data_envio ASC
                """,
                (usuario_id,)
            )

            redacoes = cursor.fetchall()

            return [
                {
                    "id": redacao["id"],
                    "tema": redacao["tema"],
                    "nota_total": redacao["nota_total"],
                    "data_envio": redacao["data_envio"],
                }
                for redacao in redacoes
            ]

        finally:
            conn.close()

    def competencia_fraca(self, usuario_id):

        conn = get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT
                    AVG(nc.competencia1) AS competencia1,
                    AVG(nc.competencia2) AS competencia2,
                    AVG(nc.competencia3) AS competencia3,
                    AVG(nc.competencia4) AS competencia4,
                    AVG(nc.competencia5) AS competencia5
                FROM notas_competencias nc
                INNER JOIN redacoes r
                    ON nc.redacao_id = r.id
                WHERE r.usuario_id = ?
                """,
                (usuario_id,)
            )

            valores = cursor.fetchone()

            return {
                "competencia1": (
                    round(float(valores["competencia1"]), 2)
                    if valores["competencia1"] is not None
                    else 0
                ),
                "competencia2": (
                    round(float(valores["competencia2"]), 2)
                    if valores["competencia2"] is not None
                    else 0
                ),
                "competencia3": (
                    round(float(valores["competencia3"]), 2)
                    if valores["competencia3"] is not None
                    else 0
                ),
                "competencia4": (
                    round(float(valores["competencia4"]), 2)
                    if valores["competencia4"] is not None
                    else 0
                ),
                "competencia5": (
                    round(float(valores["competencia5"]), 2)
                    if valores["competencia5"] is not None
                    else 0
                ),
            }

        finally:
            conn.close()
