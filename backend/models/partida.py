from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Enum
)

from sqlalchemy.orm import relationship

from backend.models.base import Base
from backend.utils.enums import StatusPartida


class Partida(Base):

    __tablename__ = "partidas"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    id_api = Column(
        Integer,
        unique=True,
        nullable=False
    )

    time_a = Column(
        String(100),
        nullable=False
    )

    time_b = Column(
        String(100),
        nullable=False
    )

    data_hora = Column(
        DateTime,
        nullable=False
    )

    status = Column(
        Enum(StatusPartida),
        nullable=False
    )

    placar_time_a = Column(
        Integer,
        nullable=True
    )

    placar_time_b = Column(
        Integer,
        nullable=True
    )

    apostas = relationship(
        "Aposta",
        back_populates="partida"
    )