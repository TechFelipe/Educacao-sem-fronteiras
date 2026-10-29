"""Casos de uso para adicionar, listar, editar, substituir e excluir PDFs."""
import unicodedata
from werkzeug.utils import secure_filename

from models.material_model import MaterialModel
from repositories.pdf_repository import PdfRepository


TAMANHO_MAXIMO_PDF = 50 * 1024 * 1024  # 50 MB por arquivo enviado.


def _normalizar_texto(valor: str) -> str:
    texto = unicodedata.normalize("NFKD", str(valor or ""))
    return "".join(char for char in texto if not unicodedata.combining(char)).casefold()


class PdfService:
    def __init__(self, repository: PdfRepository | None = None):
        self.repository = repository or PdfRepository()

    def listar_categorias(self):
        return [{"nome": nome} for nome in self.repository.listar_categorias()]

    def listar(self, termo: str = "", materia: str = "", todos: bool = False):
        termo_normalizado = _normalizar_texto(termo.strip())
        materia_normalizada = _normalizar_texto(materia.strip())
        if not todos and not termo_normalizado and not materia_normalizada:
            return []
        materiais = self.repository.listar()
        if termo_normalizado:
            materiais = [item for item in materiais if (
                termo_normalizado in _normalizar_texto(item["materia"])
                or termo_normalizado in _normalizar_texto(item["titulo"])
                or termo_normalizado in _normalizar_texto(item.get("nome_arquivo", ""))
            )]
        if materia_normalizada:
            materiais = [item for item in materiais if _normalizar_texto(item["materia"]) == materia_normalizada]
        return materiais

    @staticmethod
    def _validar_nivel(nivel: str) -> str:
        if not isinstance(nivel, str):
            raise ValueError("Selecione um nível de ensino válido.")
        nivel = nivel.strip()
        if nivel not in MaterialModel.NIVEIS_VALIDOS:
            raise ValueError("Selecione um nível válido: Ensino Fundamental, Ensino Médio ou Faculdade.")
        return nivel

    @staticmethod
    def _validar_pdf(arquivo):
        if arquivo is None or not getattr(arquivo, "filename", ""):
            raise ValueError("Selecione um arquivo PDF.")
        nome = secure_filename(arquivo.filename)
        if not nome or not nome.lower().endswith(".pdf"):
            raise ValueError("O arquivo precisa ter a extensão .pdf.")
        conteudo = arquivo.read(TAMANHO_MAXIMO_PDF + 1)
        if len(conteudo) > TAMANHO_MAXIMO_PDF:
            raise ValueError("O PDF excede o limite de 50 MB.")
        if not conteudo.startswith(b"%PDF-"):
            raise ValueError("O arquivo enviado não parece ser um PDF válido.")
        return nome, conteudo

    def adicionar(self, formulario, arquivo):
        materia = (formulario.get("materia") or "").strip()
        titulo = (formulario.get("titulo") or "").strip()
        if not materia:
            raise ValueError("Informe a matéria do PDF.")
        if len(materia) > 100:
            raise ValueError("O nome da matéria deve ter até 100 caracteres.")
        if not titulo:
            raise ValueError("Informe o título do PDF.")
        if len(titulo) > 200:
            raise ValueError("O título deve ter até 200 caracteres.")
        # Reutiliza a grafia de uma matéria existente para evitar botões duplicados
        # quando a pessoa digita, por exemplo, "Matemática" em um banco chamado "Matematica".
        for categoria_existente in self.repository.listar_categorias():
            if _normalizar_texto(categoria_existente) == _normalizar_texto(materia):
                materia = categoria_existente
                break
        nivel = self._validar_nivel(formulario.get("nivel"))
        nome, conteudo = self._validar_pdf(arquivo)
        return self.repository.adicionar(materia, titulo, nivel, nome, conteudo)

    def editar(self, material_id: str, dados: dict):
        if not isinstance(dados, dict) or not dados:
            raise ValueError("Informe os campos que deseja editar.")
        material_atual = self.repository.buscar_por_id(material_id)
        if not material_atual:
            return None
        alteracoes = {}
        if "titulo" in dados:
            titulo = dados.get("titulo")
            if not isinstance(titulo, str) or not titulo.strip():
                raise ValueError("O título não pode ficar vazio.")
            if len(titulo.strip()) > 200:
                raise ValueError("O título deve ter até 200 caracteres.")
            alteracoes["titulo"] = titulo.strip()
        # O nível dos PDFs guardados nas colunas antigas é determinado pela coluna.
        # Não aceitamos alteração manual do nível nesse caso.
        if "nivel" in dados and material_atual.get("origem") != "legado":
            alteracoes["nivel"] = self._validar_nivel(dados.get("nivel"))
        if "materia" in dados:
            materia_recebida = dados.get("materia")
            if not isinstance(materia_recebida, str):
                raise ValueError("Informe uma matéria válida.")
            if material_atual["origem"] == "legado":
                if materia_recebida.strip() != material_atual["materia"]:
                    raise ValueError("A matéria de um PDF antigo é definida pelo nome da tabela original.")
            else:
                materia = materia_recebida.strip()
                if not materia:
                    raise ValueError("O nome da matéria não pode ficar vazio.")
                if len(materia) > 100:
                    raise ValueError("O nome da matéria deve ter até 100 caracteres.")
                for categoria_existente in self.repository.listar_categorias():
                    if _normalizar_texto(categoria_existente) == _normalizar_texto(materia):
                        materia = categoria_existente
                        break
                alteracoes["materia"] = materia
        if not alteracoes:
            raise ValueError("Nenhum campo válido foi informado para edição.")
        # Para metadados antigos, preserva o título/nível existente quando o usuário altera apenas um campo.
        if material_atual["origem"] == "legado":
            alteracoes = {
                "titulo": alteracoes.get("titulo", material_atual["titulo"]),
                "nivel": alteracoes.get("nivel", material_atual.get("nivel", "")),
            }
        return self.repository.editar(material_id, alteracoes)

    def substituir_pdf(self, material_id: str, arquivo):
        if not self.repository.buscar_por_id(material_id):
            return None
        nome, conteudo = self._validar_pdf(arquivo)
        if not self.repository.substituir_arquivo(material_id, conteudo, nome):
            return None
        return self.repository.buscar_por_id(material_id)

    def excluir(self, material_id: str):
        if not self.repository.buscar_por_id(material_id):
            return False
        return self.repository.excluir(material_id)
