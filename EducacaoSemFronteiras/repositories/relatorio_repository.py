from sqlalchemy import func
from config.database import db
from models.usuario_model import Usuario
from models.redacao_model import Redacao
from models.tema_model import Tema
from models.nota_competencia_model import NotaCompetencia


class RelatorioRepository:
    def relatorio_aluno(self, usuario_id):
        usuario = db.session.get(Usuario, usuario_id)
        if usuario is None:
            return {}

        total = Redacao.query.filter_by(usuario_id=usuario_id).count()
        media = db.session.query(func.avg(Redacao.nota_total)).filter_by(usuario_id=usuario_id).scalar()
        melhor = db.session.query(func.max(Redacao.nota_total)).filter_by(usuario_id=usuario_id).scalar()
        menor = db.session.query(func.min(Redacao.nota_total)).filter_by(usuario_id=usuario_id).scalar()

        return {
            "nome": usuario.nome,
            "total_redacoes": total,
            "media": round(float(media), 2) if media is not None else 0,
            "melhor_nota": int(melhor) if melhor is not None else 0,
            "menor_nota": int(menor) if menor is not None else 0,
        }

    def evolucao(self, usuario_id):
        redacoes = (
            db.session.query(Redacao, Tema)
            .join(Tema, Redacao.tema_id == Tema.id)
            .filter(Redacao.usuario_id == usuario_id)
            .order_by(Redacao.data_envio.asc())
            .all()
        )

        return [
            {
                "id": redacao.id,
                "tema": tema.titulo,
                "nota_total": redacao.nota_total,
                "data_envio": redacao.data_envio.isoformat() if redacao.data_envio else None,
            }
            for redacao, tema in redacoes
        ]

    def competencia_fraca(self, usuario_id):
        valores = (
            db.session.query(
                func.avg(NotaCompetencia.competencia1),
                func.avg(NotaCompetencia.competencia2),
                func.avg(NotaCompetencia.competencia3),
                func.avg(NotaCompetencia.competencia4),
                func.avg(NotaCompetencia.competencia5),
            )
            .join(Redacao, NotaCompetencia.redacao_id == Redacao.id)
            .filter(Redacao.usuario_id == usuario_id)
            .one()
        )

        return {
            f"competencia{i}": round(float(valor), 2) if valor is not None else 0
            for i, valor in enumerate(valores, start=1)
        }
