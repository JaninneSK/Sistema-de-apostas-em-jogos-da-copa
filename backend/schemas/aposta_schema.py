from pydantic import BaseModel, ConfigDict, Field
from backend.utils.enums import Palpite, StatusAposta

class ApostaCadastroSchema(BaseModel):

    partida_id: int

    valor_apostado: int = Field(
        gt=0
    )

    multiplicador: int = Field(
        ge=1
    )

    palpite: Palpite

class ApostaResponseSchema(BaseModel):

    model_config = ConfigDict(
        from_attributes=True
    )

    id: int

    usuario_id: int

    partida_id: int

    valor_apostado: int

    odd_aplicada: float

    multiplicador: int

    palpite: Palpite

    status: StatusAposta

    acertou: bool | None

    pontos_ganhos: int