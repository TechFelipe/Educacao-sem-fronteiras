"""Persistência de materiais no SQLite sem alterar a estrutura antiga dos PDFs."""
from __future__ import annotations

import base64
import hashlib
import sqlite3
import unicodedata
from contextlib import contextmanager
from pathlib import Path
from typing import Any



DB_PATH = Path(__file__).resolve().parent.parent / "database" / "materias.sqlite"
TABELA_GERENCIADOS = "_materiais_gerenciados"
TABELA_METADADOS = "_materiais_metadados"


def _quote_identifier(nome: str) -> str:
    """Protege nomes de tabelas/colunas vindos do próprio esquema SQLite."""
    return '"' + str(nome).replace('"', '""') + '"'


class PdfRepository:
    def __init__(self, caminho: Path | str = DB_PATH):
        self.caminho = Path(caminho)
        self.caminho.parent.mkdir(parents=True, exist_ok=True)
        self._garantir_estrutura()

    def _conectar(self) -> sqlite3.Connection:
        conexao = sqlite3.connect(str(self.caminho))
        conexao.row_factory = sqlite3.Row
        return conexao

    @contextmanager
    def _conexao(self):
        """Fecha a conexão ao final de cada consulta, mesmo quando ocorre um erro."""
        conexao = self._conectar()
        try:
            yield conexao
        finally:
            conexao.close()

    def _garantir_estrutura(self) -> None:
        """Cria as tabelas administrativas sem mexer nas tabelas antigas."""
        with self._conexao() as conexao:
            conexao.execute(f"""
                CREATE TABLE IF NOT EXISTS {TABELA_GERENCIADOS} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    materia TEXT NOT NULL,
                    titulo TEXT NOT NULL,
                    nivel TEXT NOT NULL,
                    nome_arquivo TEXT NOT NULL,
                    tipo_arquivo TEXT NOT NULL DEFAULT 'application/pdf',
                    arquivo BLOB NOT NULL,
                    criado_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    atualizado_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conexao.execute(f"""
                CREATE TABLE IF NOT EXISTS {TABELA_METADADOS} (
                    material_id TEXT PRIMARY KEY,
                    titulo TEXT,
                    nivel TEXT,
                    atualizado_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conexao.commit()

    def _nomes_tabelas_legacy(self, conexao: sqlite3.Connection) -> list[str]:
        linhas = conexao.execute(
            "SELECT name FROM sqlite_master WHERE type='table' "
            "AND name NOT LIKE 'sqlite_%' ORDER BY name COLLATE NOCASE"
        ).fetchall()
        internas = {TABELA_GERENCIADOS.casefold(), TABELA_METADADOS.casefold()}
        return [linha[0] for linha in linhas if linha[0].casefold() not in internas]

    @staticmethod
    def _id_legacy(tabela: str, rowid: int, coluna: str) -> str:
        chave = f"{tabela}|{rowid}|{coluna}"
        return "leg_" + hashlib.sha256(chave.encode("utf-8")).hexdigest()[:24]

    @staticmethod
    def _nivel_da_coluna(nome_coluna: str) -> str:
        """Converte o nome da coluna do banco para o nível exibido na interface."""
        normalizado = "".join(
            char for char in unicodedata.normalize("NFKD", str(nome_coluna or ""))
            if not unicodedata.combining(char)
        ).casefold().replace(" ", "")
        niveis = {
            "ensinofundamental": "Ensino Fundamental",
            "ensinomedio": "Ensino Médio",
            "faculdade": "Faculdade",
            "fundamental": "Ensino Fundamental",
        }
        return niveis.get(normalizado, "")

    @staticmethod
    def _coluna_do_nivel(colunas: list[str], nivel: str) -> str | None:
        """Encontra a coluna de destino sem depender de acentos no esquema SQLite."""
        for coluna in colunas:
            if PdfRepository._nivel_da_coluna(coluna) == nivel:
                return coluna
        return None

    @staticmethod
    def _decodificar_pdf(valor: Any) -> bytes | None:
        """Lê PDFs BLOB e PDFs codificados em texto em colunas SQLite STRICT TEXT."""
        if isinstance(valor, bytes) and valor.startswith(b"%PDF-"):
            return valor
        if isinstance(valor, str) and valor.startswith("PDFBASE64:"):
            try:
                conteudo = base64.b64decode(valor[len("PDFBASE64:"):], validate=True)
                return conteudo if conteudo.startswith(b"%PDF-") else None
            except (ValueError, base64.binascii.Error):
                return None
        return None

    @staticmethod
    def _valor_para_coluna(conteudo: bytes, tipo_coluna: str) -> Any:
        """Converte o PDF para o tipo permitido pela coluna SQLite."""
        if str(tipo_coluna or "").upper() == "TEXT":
            return "PDFBASE64:" + base64.b64encode(conteudo).decode("ascii")
        return sqlite3.Binary(conteudo)

    @staticmethod
    def _tipo_coluna(conexao: sqlite3.Connection, tabela: str, coluna: str) -> str:
        for info in conexao.execute(f"PRAGMA table_info({_quote_identifier(tabela)})").fetchall():
            if str(info["name"]) == coluna:
                return str(info["type"] or "")
        return ""

    def _carregar_metadados(self, conexao: sqlite3.Connection) -> dict[str, dict[str, str]]:
        linhas = conexao.execute(
            f"SELECT material_id, titulo, nivel FROM {TABELA_METADADOS}"
        ).fetchall()
        return {
            linha["material_id"]: {
                "titulo": linha["titulo"] or "",
                "nivel": linha["nivel"] or "",
            }
            for linha in linhas
        }

    def listar_categorias(self) -> list[str]:
        with self._conexao() as conexao:
            categorias = set(self._nomes_tabelas_legacy(conexao))
            linhas = conexao.execute(
                f"SELECT DISTINCT materia FROM {TABELA_GERENCIADOS} "
                "WHERE TRIM(materia) <> ''"
            ).fetchall()
            categorias.update(linha[0] for linha in linhas)
        return sorted(categorias, key=str.casefold)

    def listar(self) -> list[dict[str, Any]]:
        materiais: list[dict[str, Any]] = []
        with self._conexao() as conexao:
            metadados = self._carregar_metadados(conexao)
            for tabela in self._nomes_tabelas_legacy(conexao):
                tabela_sql = _quote_identifier(tabela)
                try:
                    colunas = conexao.execute(f"PRAGMA table_info({tabela_sql})").fetchall()
                    if not colunas:
                        continue
                    # rowid é usado para conservar um identificador estável da linha.
                    registros = conexao.execute(f"SELECT rowid, * FROM {tabela_sql}").fetchall()
                except sqlite3.Error:
                    # Tabelas WITHOUT ROWID ou não convencionais permanecem preservadas.
                    continue

                for registro in registros:
                    rowid = int(registro[0])
                    for indice, coluna_info in enumerate(colunas, start=1):
                        conteudo = registro[indice]
                        if self._decodificar_pdf(conteudo) is None:
                            continue
                        nome_coluna = str(coluna_info["name"])
                        material_id = self._id_legacy(tabela, rowid, nome_coluna)
                        meta = metadados.get(material_id, {})
                        materiais.append({
                            "id": material_id,
                            "materia": tabela,
                            "titulo": meta.get("titulo") or f"{tabela} — {nome_coluna}",
                            "nivel": self._nivel_da_coluna(nome_coluna) or meta.get("nivel", ""),
                            "nome_arquivo": f"{tabela}_{nome_coluna}.pdf",
                            "coluna": nome_coluna,
                            "registro": rowid,
                            "origem": "legado",
                            "pode_editar_materia": False,
                        })

            linhas = conexao.execute(f"""
                SELECT id, materia, titulo, nivel, nome_arquivo
                FROM {TABELA_GERENCIADOS}
                ORDER BY materia COLLATE NOCASE, titulo COLLATE NOCASE
            """).fetchall()
            for linha in linhas:
                materiais.append({
                    "id": f"novo_{linha['id']}",
                    "materia": linha["materia"],
                    "titulo": linha["titulo"],
                    "nivel": linha["nivel"],
                    "nome_arquivo": linha["nome_arquivo"],
                    "origem": "gerenciado",
                    "pode_editar_materia": True,
                })

        return materiais

    def adicionar(self, materia: str, titulo: str, nivel: str, nome_arquivo: str, arquivo: bytes) -> dict[str, Any]:
        """Armazena o PDF na coluna do nível correspondente da tabela da matéria."""
        with self._conexao() as conexao:
            # A tabela da matéria deve existir; a tabela define quais níveis ela suporta.
            tabelas = self._nomes_tabelas_legacy(conexao)
            tabela_real = next((t for t in tabelas if t.casefold() == materia.casefold()), None)
            if not tabela_real:
                raise ValueError("A matéria selecionada não possui uma tabela no banco de dados.")

            tabela_sql = _quote_identifier(tabela_real)
            colunas_info = conexao.execute(f"PRAGMA table_info({tabela_sql})").fetchall()
            nomes_colunas = [str(coluna["name"]) for coluna in colunas_info]
            coluna_destino = self._coluna_do_nivel(nomes_colunas, nivel)
            if not coluna_destino:
                raise ValueError(f"A matéria {materia} não possui uma coluna para o nível {nivel}.")

            # Cada PDF ganha sua própria linha para não sobrescrever PDFs existentes.
            valores = {coluna: None for coluna in nomes_colunas}
            tipo_destino = self._tipo_coluna(conexao, tabela_real, coluna_destino)
            valores[coluna_destino] = self._valor_para_coluna(arquivo, tipo_destino)
            colunas_sql = ", ".join(_quote_identifier(coluna) for coluna in valores)
            placeholders = ", ".join("?" for _ in valores)
            cursor = conexao.execute(
                f"INSERT INTO {tabela_sql} ({colunas_sql}) VALUES ({placeholders})",
                list(valores.values()),
            )
            rowid = int(cursor.lastrowid)
            material_id = self._id_legacy(tabela_real, rowid, coluna_destino)
            conexao.execute(
                f"INSERT OR REPLACE INTO {TABELA_METADADOS} (material_id, titulo, nivel) VALUES (?, ?, ?)",
                (material_id, titulo, self._nivel_da_coluna(coluna_destino)),
            )
            conexao.commit()
        return self.buscar_por_id(material_id)

    def _encontrar_legacy(self, conexao: sqlite3.Connection, material_id: str) -> dict[str, Any] | None:
        if not material_id.startswith("leg_"):
            return None
        for tabela in self._nomes_tabelas_legacy(conexao):
            tabela_sql = _quote_identifier(tabela)
            try:
                colunas = conexao.execute(f"PRAGMA table_info({tabela_sql})").fetchall()
                registros = conexao.execute(f"SELECT rowid, * FROM {tabela_sql}").fetchall()
            except sqlite3.Error:
                continue
            for registro in registros:
                rowid = int(registro[0])
                for indice, info_coluna in enumerate(colunas, start=1):
                    valor = registro[indice]
                    coluna = str(info_coluna["name"])
                    if self._decodificar_pdf(valor) is not None:
                        if self._id_legacy(tabela, rowid, coluna) == material_id:
                            return {"tabela": tabela, "rowid": rowid, "coluna": coluna}
        return None

    def buscar_por_id(self, material_id: str) -> dict[str, Any] | None:
        for material in self.listar():
            if material["id"] == material_id:
                return material
        return None

    def obter_arquivo(self, material_id: str) -> dict[str, Any] | None:
        with self._conexao() as conexao:
            if material_id.startswith("novo_"):
                try:
                    novo_id = int(material_id[5:])
                except ValueError:
                    return None
                linha = conexao.execute(
                    f"SELECT materia, titulo, nome_arquivo, arquivo FROM {TABELA_GERENCIADOS} WHERE id = ?",
                    (novo_id,),
                ).fetchone()
                if not linha:
                    return None
                return {"materia": linha["materia"], "titulo": linha["titulo"], "nome_arquivo": linha["nome_arquivo"], "arquivo": bytes(linha["arquivo"])}

            localizado = self._encontrar_legacy(conexao, material_id)
            if not localizado:
                return None
            linha = conexao.execute(
                f"SELECT {_quote_identifier(localizado['coluna'])} FROM {_quote_identifier(localizado['tabela'])} WHERE rowid = ?",
                (localizado["rowid"],),
            ).fetchone()
            if not linha:
                return None
            conteudo_pdf = self._decodificar_pdf(linha[0])
            if conteudo_pdf is None:
                return None
            metadados = self._carregar_metadados(conexao).get(material_id, {})
            return {
                "materia": localizado["tabela"],
                "titulo": metadados.get("titulo") or f"{localizado['tabela']} — {localizado['coluna']}",
                "nome_arquivo": f"{localizado['tabela']}_{localizado['coluna']}.pdf",
                "arquivo": conteudo_pdf,
            }

    def editar(self, material_id: str, dados: dict[str, str]) -> dict[str, Any] | None:
        with self._conexao() as conexao:
            if material_id.startswith("novo_"):
                try:
                    novo_id = int(material_id[5:])
                except ValueError:
                    return None
                atual = conexao.execute(
                    f"SELECT id FROM {TABELA_GERENCIADOS} WHERE id = ?", (novo_id,)
                ).fetchone()
                if not atual:
                    return None
                campos_permitidos = {"materia", "titulo", "nivel"}
                alteracoes = {chave: valor for chave, valor in dados.items() if chave in campos_permitidos}
                if not alteracoes:
                    return self.buscar_por_id(material_id)
                alteracoes["atualizado_em"] = "CURRENT_TIMESTAMP"
                atribuicoes = []
                valores = []
                for campo, valor in alteracoes.items():
                    if campo == "atualizado_em":
                        atribuicoes.append("atualizado_em = CURRENT_TIMESTAMP")
                    else:
                        atribuicoes.append(f"{campo} = ?")
                        valores.append(valor)
                valores.append(novo_id)
                conexao.execute(
                    f"UPDATE {TABELA_GERENCIADOS} SET {', '.join(atribuicoes)} WHERE id = ?", valores
                )
            else:
                localizado = self._encontrar_legacy(conexao, material_id)
                if not localizado:
                    return None
                atual = conexao.execute(
                    f"SELECT material_id FROM {TABELA_METADADOS} WHERE material_id = ?", (material_id,)
                ).fetchone()
                titulo = dados.get("titulo")
                nivel = self._nivel_da_coluna(localizado["coluna"])
                if atual:
                    conexao.execute(
                        f"UPDATE {TABELA_METADADOS} SET titulo = ?, nivel = ?, atualizado_em = CURRENT_TIMESTAMP WHERE material_id = ?",
                        (titulo, nivel, material_id),
                    )
                else:
                    conexao.execute(
                        f"INSERT INTO {TABELA_METADADOS} (material_id, titulo, nivel) VALUES (?, ?, ?)",
                        (material_id, titulo, nivel),
                    )
            conexao.commit()
        return self.buscar_por_id(material_id)

    def substituir_arquivo(self, material_id: str, arquivo: bytes, nome_arquivo: str) -> bool:
        with self._conexao() as conexao:
            if material_id.startswith("novo_"):
                try:
                    novo_id = int(material_id[5:])
                except ValueError:
                    return False
                cursor = conexao.execute(
                    f"UPDATE {TABELA_GERENCIADOS} SET arquivo = ?, nome_arquivo = ?, atualizado_em = CURRENT_TIMESTAMP WHERE id = ?",
                    (sqlite3.Binary(arquivo), nome_arquivo, novo_id),
                )
            else:
                localizado = self._encontrar_legacy(conexao, material_id)
                if not localizado:
                    return False
                tipo_coluna = self._tipo_coluna(conexao, localizado["tabela"], localizado["coluna"])
                valor_arquivo = self._valor_para_coluna(arquivo, tipo_coluna)
                cursor = conexao.execute(
                    f"UPDATE {_quote_identifier(localizado['tabela'])} SET {_quote_identifier(localizado['coluna'])} = ? WHERE rowid = ?",
                    (valor_arquivo, localizado["rowid"]),
                )
            conexao.commit()
            return cursor.rowcount > 0

    def excluir(self, material_id: str) -> bool:
        with self._conexao() as conexao:
            if material_id.startswith("novo_"):
                try:
                    novo_id = int(material_id[5:])
                except ValueError:
                    return False
                cursor = conexao.execute(f"DELETE FROM {TABELA_GERENCIADOS} WHERE id = ?", (novo_id,))
                conexao.commit()
                return cursor.rowcount > 0

            localizado = self._encontrar_legacy(conexao, material_id)
            if not localizado:
                return False
            try:
                # Esvazia somente a coluna do PDF; os demais campos da linha são preservados.
                tipo_coluna = self._tipo_coluna(conexao, localizado["tabela"], localizado["coluna"])
                valor_vazio = "" if tipo_coluna.upper() == "TEXT" else sqlite3.Binary(b"")
                cursor = conexao.execute(
                    f"UPDATE {_quote_identifier(localizado['tabela'])} SET {_quote_identifier(localizado['coluna'])} = ? WHERE rowid = ?",
                    (valor_vazio, localizado["rowid"]),
                )
                conexao.execute(f"DELETE FROM {TABELA_METADADOS} WHERE material_id = ?", (material_id,))
                conexao.commit()
                return cursor.rowcount > 0
            except sqlite3.Error:
                conexao.rollback()
                raise ValueError(
                    "O banco não permitiu remover o PDF sem violar uma regra da tabela original. "
                    "Nenhuma alteração foi confirmada."
                )
