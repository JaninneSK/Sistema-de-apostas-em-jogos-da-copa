from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


DATABASE_URL = "sqlite:///backend/database/copa2026.db"


# A engine é responsável por gerenciar a conexão entre o SQLAlchemy
# e o banco de dados utilizado pelo sistema
engine = create_engine(
    DATABASE_URL
)


# A SessionLocal cria as sessões usadas pelos DAOs para consultar,
# inserir e atualizar os dados no banco
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)