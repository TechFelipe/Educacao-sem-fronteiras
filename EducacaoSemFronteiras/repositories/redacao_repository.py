from config.database import conectar

class RedacaoRepository:

    def criar_redacao(self, usuario_id, tema_id, texto):
        conexao = conectar()
        cursor = conexao.cursor(dictionary=True)
        try:
            cursor.callproc("criar_redacao", (usuario_id, tema_id, texto))
            resultado = {}
            for result in cursor.stored_results():
                linha = result.fetchone()
                if linha:
                    resultado = linha
            conexao.commit()
            return resultado
        finally:
            cursor.close()
            conexao.close()

    def ranking(self):
        conexao = conectar()
        cursor = conexao.cursor(dictionary=True)
        try:
            cursor.callproc("ranking_alunos")
            resultados = []
            for result in cursor.stored_results():
                resultados = result.fetchall()
            return resultados
        finally:
            cursor.close()
            conexao.close()
