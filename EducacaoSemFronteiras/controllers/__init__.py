"""Compatibilidade: as rotas de PDFs foram separadas em pdf_controller.py."""
from controllers.pdf_controller import (
    pdf_bp as materias_bp,
    MateriasCategoriasController,
    MateriaisController,
    MaterialDetalheController,
    MaterialArquivoController,
)

__all__ = ["materias_bp", "MateriasCategoriasController", "MateriaisController", "MaterialDetalheController", "MaterialArquivoController"]
