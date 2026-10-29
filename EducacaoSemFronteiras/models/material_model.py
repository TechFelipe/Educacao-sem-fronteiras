"""Entidade e regras simples de domínio dos materiais didáticos em PDF."""
from dataclasses import dataclass
from typing import ClassVar


@dataclass
class MaterialModel:
    id: str | int
    materia: str
    titulo: str
    nivel: str
    nome_arquivo: str = ""
    origem: str = "gerenciado"

    NIVEIS_VALIDOS: ClassVar[tuple[str, ...]] = (
        "Ensino Fundamental",
        "Ensino Médio",
        "Faculdade",
    )

    @classmethod
    def nivel_valido(cls, nivel: str) -> bool:
        return nivel in cls.NIVEIS_VALIDOS
