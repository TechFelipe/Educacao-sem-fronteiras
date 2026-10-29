"""Consultas específicas de temas; SQL fica encapsulado nesta camada."""
from config.database import get_connection

class TemaRepository:
    def buscar_todos(self, termo=None, dificuldade=None):
        """Busca temas com filtros opcionais por título/descrição e dificuldade."""
        conn = get_connection()
        try:
            sql = "SELECT id,titulo,descricao,dificuldade,criado_em FROM temas WHERE 1=1"
            params = []
            if termo:
                sql += " AND (titulo LIKE ? OR descricao LIKE ?)"
                params.extend([f"%{termo}%", f"%{termo}%"])
            if dificuldade:
                sql += " AND LOWER(dificuldade) = LOWER(?)"
                params.append(dificuldade)
            sql += " ORDER BY titulo COLLATE NOCASE"
            return [dict(row) for row in conn.execute(sql, params).fetchall()]
        finally:
            conn.close()

    # Nome legado mantido para compatibilidade com chamadas anteriores.
    def buscar_temas(self, termo=None, dificuldade=None):
        """Compatibilidade com o nome usado pelo Service existente."""
        return self.buscar_todos(termo, dificuldade)

    def buscar_por_id(self, tema_id):
        """Retorna um tema pelo ID ou None quando não existe."""
        conn = get_connection()
        try:
            row = conn.execute("SELECT id,titulo,descricao,dificuldade,criado_em FROM temas WHERE id=?", (tema_id,)).fetchone()
            return dict(row) if row else None
        finally:
            conn.close()

    def criar_tema(self, titulo, descricao, dificuldade):
        """Insere um tema e retorna os dados persistidos."""
        conn = get_connection()
        try:
            cur = conn.execute("INSERT INTO temas (titulo,descricao,dificuldade) VALUES (?,?,?)", (titulo, descricao, dificuldade))
            conn.commit()
            return self.buscar_por_id(cur.lastrowid)
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def atualizar_tema(self, tema_id, dados):
        """Atualiza campos permitidos de um tema existente."""
        permitidos = {k: dados[k] for k in ("titulo", "descricao", "dificuldade") if k in dados}
        if not permitidos:
            raise ValueError("Informe ao menos um campo para atualizar.")
        conn = get_connection()
        try:
            conn.execute("UPDATE temas SET " + ",".join(f"{k}=?" for k in permitidos) + " WHERE id=?", [*permitidos.values(), tema_id])
            conn.commit()
            return self.buscar_por_id(tema_id)
        except Exception:
            conn.rollback(); raise
        finally:
            conn.close()

    def deletar_tema(self, tema_id):
        """Exclui tema somente se não estiver vinculado a redações."""
        conn = get_connection()
        try:
            cur = conn.execute("DELETE FROM temas WHERE id=? AND NOT EXISTS (SELECT 1 FROM redacoes WHERE tema_id=?)", (tema_id, tema_id))
            conn.commit()
            return cur.rowcount > 0
        except Exception:
            conn.rollback(); raise
        finally:
            conn.close()
