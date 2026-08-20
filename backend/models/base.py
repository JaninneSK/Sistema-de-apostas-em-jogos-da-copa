from sqlalchemy.orm import declarative_base


# Essa Base é usada como classe pai dos Models para que o SQLAlchemy
# reconheça essas classes e consiga mapeá-las para as tabelas do banco
Base = declarative_base()