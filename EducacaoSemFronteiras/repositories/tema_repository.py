from sqlalchemy import or_
from config.database import db
from models.tema_model import Tema


class TemaRepository:
    def buscar_temas(self, termo=None, dificuldade=None):
        query = Tema.query

        if termo:
            termo_like = f"%{termo}%"
            query = query.filter(
                or_(
                    Tema.titulo.ilike(termo_like),
                    Tema.descricao.ilike(termo_like)
                )
            )

        if dificuldade:
            query = query.filter(Tema.dificuldade == dificuldade)

        return [tema.to_dict() for tema in query.order_by(Tema.criado_em.desc()).all()]
