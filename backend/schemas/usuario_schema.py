from datetime import date
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from backend.utils.enums import TipoUsuario


class UsuarioCadastroSchema(BaseModel):
    """
    Define e valida os dados necessários para cadastrar um novo usuário.
    """

    nome: str = Field(
        min_length=3,
        max_length=100
    )

    email: EmailStr

    cpf: str = Field(
        min_length=11,
        max_length=11
    )

    data_nascimento: date

    login: str = Field(
        min_length=4,
        max_length=50
    )

    senha: str = Field(
        min_length=8
    )


class LoginSchema(BaseModel):
    """
    Define os dados necessários para realizar o login.
    """

    login: str
    senha: str


class UsuarioResponseSchema(BaseModel):
    """
    Define os dados do usuário que podem ser retornados pelo sistema.
    """

    model_config = ConfigDict(
        from_attributes=True
    )

    id: int
    nome: str
    email: EmailStr
    pontos: int
    quantidade_acertos: int
    tipo: TipoUsuario
    ativo: bool


class UsuarioAtualizacaoSchema(BaseModel):
    """
    Define os dados que podem ser alterados pelo usuário.
    """

    nome: str | None = Field(
        default=None,
        min_length=3,
        max_length=100
    )

    email: EmailStr | None = None

    senha: str | None = Field(
        default=None,
        min_length=8
    )