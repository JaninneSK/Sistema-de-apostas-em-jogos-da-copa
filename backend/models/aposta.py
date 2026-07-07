from sqlalchemy import (
    Column,
    Integer,
    Float,
    Boolean,
    Enum,
    ForeignKey
)

from sqlalchemy.orm import relationship

from backend.models.base import Base
from backend.utils.enums import (
    Palpite,
    StatusAposta
)


class Aposta(Base):

    __tablename__ = "apostas"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    usuario_id = Column(
        Integer,
        ForeignKey("usuarios.id"),
        nullable=False
    )

    partida_id = Column(
        Integer,
        ForeignKey("partidas.id"),
        nullable=False
    )

    valor_apostado = Column(
        Integer,
        nullable=False
    )

    odd_aplicada = Column(
        Float,
        nullable=False
    )

    multiplicador = Column(
        Integer,
        default=1,
        nullable=False
    )

    palpite = Column(
        Enum(Palpite),
        nullable=False
    )

    status = Column(
        Enum(StatusAposta),
        nullable=False
    )

    acertou = Column(
        Boolean,
        nullable=True
    )

    pontos_ganhos = Column(
        Integer,
        default=0,
        nullable=False
    )

    usuario = relationship(
        "Usuario",
        back_populates="apostas"
    )

    partida = relationship(
        "Partida",
        back_populates="apostas"
    )