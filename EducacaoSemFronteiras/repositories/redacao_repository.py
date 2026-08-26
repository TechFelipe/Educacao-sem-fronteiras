from sqlalchemy import func
from config.database import db
from models.usuario_model import Usuario
from models.redacao_model import Redacao


class RedacaoRepository:
    def criar_redacao(self, usuario_id, tema_id, texto):
        redacao = Redacao(
            usuario_id=usuario_id,
            tema_id=tema_id,
            texto=texto,
            nota_total=0
        )
        db.session.add(redacao)
        db.session.commit()
        return redacao.to_dict()

    def ranking(self):
        resultados = (
            db.session.query(
                Usuario.id,
                Usuario.nome,
                func.count(Redacao.id).label("quantidade_redacoes"),
                func.round(func.avg(Redacao.nota_total), 2).label("media")
            )
            .join(Redacao, Usuario.id == Redacao.usuario_id)
            .group_by(Usuario.id, Usuario.nome)
            .having(func.count(Redacao.id) > 0)
            .order_by(func.avg(Redacao.nota_total).desc())
            .all()
        )

        return [
            {
                "id": r.id,
                "nome": r.nome,
                "quantidade_redacoes": r.quantidade_redacoes,
                "media": float(r.media) if r.media is not None else 0,
            }
            for r in resultados
        ]
