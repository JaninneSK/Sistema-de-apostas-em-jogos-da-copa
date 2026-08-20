from sqlalchemy.orm import DeclarativeBase


# Essa classe é usada como base dos Models para que o SQLAlchemy
# reconheça essas classes e consiga mapeá-las para as tabelas do banco
class Base(DeclarativeBase):
    pass