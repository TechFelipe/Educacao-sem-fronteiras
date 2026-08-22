from config.database import conectar

class RelatorioRepository:

    def relatorio_aluno(self, usuario_id):
        conexao = conectar()
        cursor = conexao.cursor(dictionary=True)
        try:
            cursor.callproc("relatorio_aluno", (usuario_id,))
            resultado = {}
            for result in cursor.stored_results():
                linha = result.fetchone()
                if linha:
                    resultado = linha
            return resultado
        finally:
            cursor.close()
            conexao.close()

    def evolucao(self, usuario_id):
        conexao = conectar()
        cursor = conexao.cursor(dictionary=True)
        try:
            cursor.callproc("evolucao_aluno", (usuario_id,))
            resultados = []
            for result in cursor.stored_results():
                resultados = result.fetchall()
            return resultados
        finally:
            cursor.close()
            conexao.close()

    def competencia_fraca(self, usuario_id):
        conexao = conectar()
        cursor = conexao.cursor(dictionary=True)
        try:
            cursor.callproc("competencia_fraca", (usuario_id,))
            resultado = {}
            for result in cursor.stored_results():
                linha = result.fetchone()
                if linha:
                    resultado = linha
            return resultado
        finally:
            cursor.close()
            conexao.close()
