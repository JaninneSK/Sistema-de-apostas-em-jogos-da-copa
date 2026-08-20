from backend.config.database import engine
from backend.models.base import Base

# Os Models precisam ser importados para que o SQLAlchemy reconheça
# todas as tabelas antes de executar o create_all
from backend.models.usuario import Usuario
from backend.models.partida import Partida
from backend.models.aposta import Aposta


def criar_tabelas():
    """
    Cria no banco todas as tabelas definidas pelos Models do sistema.
    """

    # Os Models são importados neste arquivo para que o SQLAlchemy conheça
    # todas as tabelas antes de executar o create_all
    print("URL do banco:", engine.url)

    Base.metadata.create_all(bind=engine)

    print("Tabelas criadas com sucesso!")


if __name__ == "__main__":
    criar_tabelas()