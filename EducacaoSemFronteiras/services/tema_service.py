"""Regras de negócio para consulta e manutenção dos temas de redação."""
from repositories.tema_repository import TemaRepository


class TemaService:

    def __init__(self):
        self.repository = TemaRepository()

    def buscar(self, termo=None, dificuldade=None):
        if termo == "":
            termo = None

        if dificuldade == "":
            dificuldade = None

        return self.repository.buscar_temas(
            termo,
            dificuldade
        )

    def criar(self, dados):
        if not dados:
            raise ValueError("Nenhum dado foi enviado.")

        titulo = dados.get("titulo")
        descricao = dados.get("descricao")
        dificuldade = dados.get("dificuldade")

        if not titulo or not titulo.strip():
            raise ValueError("O campo 'titulo' é obrigatório.")

        if not dificuldade or not dificuldade.strip():
            raise ValueError("O campo 'dificuldade' é obrigatório.")

        titulo = titulo.strip()
        dificuldade = dificuldade.strip()

        if descricao is not None:
            descricao = descricao.strip()

        return self.repository.criar_tema(
            titulo,
            descricao,
            dificuldade
        )
    def buscar_por_id(self, tema_id):
        """Valida o identificador e consulta um tema específico."""
        try:
            tema_id = int(tema_id)
        except (TypeError, ValueError):
            raise ValueError("ID do tema inválido.")
        if tema_id <= 0:
            raise ValueError("ID do tema deve ser positivo.")
        return self.repository.buscar_por_id(tema_id)

    def atualizar(self, tema_id, dados):
        """Valida campos recebidos antes de atualizar um tema."""
        if not dados:
            raise ValueError("Nenhum dado foi enviado.")
        for campo in ("titulo", "dificuldade"):
            if campo in dados and (not isinstance(dados[campo], str) or not dados[campo].strip()):
                raise ValueError(f"O campo '{campo}' não pode ficar vazio.")
        for campo in ("titulo", "descricao", "dificuldade"):
            if campo in dados and isinstance(dados[campo], str):
                dados[campo] = dados[campo].strip()
        if self.repository.buscar_por_id(tema_id) is None:
            return None
        return self.repository.atualizar_tema(tema_id, dados)

    def deletar(self, tema_id):
        """Exclui um tema sem redações associadas."""
        if self.repository.buscar_por_id(tema_id) is None:
            return None
        if not self.repository.deletar_tema(tema_id):
            raise ValueError("Não é possível excluir um tema vinculado a redações.")
        return True
