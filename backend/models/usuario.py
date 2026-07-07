from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    Boolean,
    Enum
)

from sqlalchemy.orm import relationship

from backend.models.base import Base
from backend.utils.enums import TipoUsuario


class Usuario(Base):

    __tablename__ = "usuarios"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    nome = Column(
        String(200),
        nullable=False
    )

    email = Column(
        String(100),
        unique=True,
        nullable=False
    )

    cpf = Column(
        String(11),
        unique=True,
        nullable=False
    )

    data_nascimento = Column(
        Date,
        nullable=False
    )

    login = Column(
        String(50),
        unique=True,
        nullable=False
    )

    senha_hash = Column(
        String(255),
        nullable=False
    )

    pontos = Column(
        Integer,
        default=100,
        nullable=False
    )

    quantidade_acertos = Column(
        Integer,
        default=0,
        nullable=False
    )

    tipo = Column(
        Enum(TipoUsuario),
        nullable=False
    )

    ativo = Column(
        Boolean,
        default=True,
        nullable=False
    )

    apostas = relationship(
        "Aposta",
        back_populates="usuario"
    )