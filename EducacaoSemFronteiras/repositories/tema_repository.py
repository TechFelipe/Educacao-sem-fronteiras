from config.database import get_connection

class TemaRepository:
    # ... seus outros métodos ...

    def buscar_por_id(self, tema_id):

        conn = get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT
                    id,
                    titulo,
                    descricao,
                    dificuldade,
                    criado_em
                FROM temas
                WHERE id = ?
                """,
                (tema_id,)
            )

            tema = cursor.fetchone()

            if tema is None:
                return None

            return {
                "id": tema["id"],
                "titulo": tema["titulo"],
                "descricao": tema["descricao"],
                "dificuldade": tema["dificuldade"],
                "criado_em": tema["criado_em"]
            }

        finally:
            conn.close()