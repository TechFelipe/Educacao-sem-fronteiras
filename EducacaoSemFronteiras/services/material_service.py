"""Compatibilidade com imports antigos; regras de PDF ficam em pdf_service.py."""
from services.pdf_service import PdfService

MaterialService = PdfService
__all__ = ["MaterialService", "PdfService"]
