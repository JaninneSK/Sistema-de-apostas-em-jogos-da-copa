from pydantic import BaseModel, ConfigDict, Field
from backend.utils.enums import Multiplicador, Palpite, StatusAposta


class ApostaCadastroSchema(BaseModel):
    """
    Define e valida os dados necessários para registrar uma nova aposta.
    """

    partida_id: int
    valor_apostado: int = Field(gt=0)
    multiplicador: Multiplicador = Multiplicador.X1
    palpite: Palpite


class ApostaResponseSchema(BaseModel):
    """
    Define os dados de uma aposta que podem ser retornados pelo sistema.
    """

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