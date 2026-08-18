from backend.config.database import engine
from backend.models.base import Base

from backend.models.usuario import Usuario
from backend.models.partida import Partida
from backend.models.aposta import Aposta


def criar_tabelas():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    criar_tabelas()