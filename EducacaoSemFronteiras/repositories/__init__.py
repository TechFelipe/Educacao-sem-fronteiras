"""Compatibilidade com imports antigos; persistência de PDF fica em pdf_repository.py."""
from repositories.pdf_repository import PdfRepository

MaterialRepository = PdfRepository
__all__ = ["MaterialRepository", "PdfRepository"]
