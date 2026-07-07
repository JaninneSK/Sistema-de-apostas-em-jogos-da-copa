from datetime import date
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from backend.utils.enums import TipoUsuario


class UsuarioCadastroSchema(BaseModel):
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
    login: str
    senha: str


class UsuarioResponseSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

    id: int
    nome: str
    email: str
    pontos: int
    quantidade_acertos: int
    tipo: TipoUsuario
    ativo: bool

class UsuarioAtualizacaoSchema(BaseModel):
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