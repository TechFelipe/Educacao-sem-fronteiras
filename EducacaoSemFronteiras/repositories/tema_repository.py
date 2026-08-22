from config.database import conectar

class TemaRepository:

    def buscar_temas(self, termo=None, dificuldade=None):
        conexao = conectar()
        cursor = conexao.cursor(dictionary=True)
        try:
            cursor.callproc("buscar_temas", (termo, dificuldade))
            resultados = []
            for result in cursor.stored_results():
                resultados = result.fetchall()
            return resultados
        finally:
            cursor.close()
            conexao.close()
