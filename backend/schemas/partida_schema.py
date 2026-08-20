from datetime import datetime
from pydantic import BaseModel, ConfigDict
from backend.utils.enums import StatusPartida


class PartidaImportacaoSchema(BaseModel):
    """
    Define os dados de uma partida recebidos e convertidos a partir da API.
    """

    id_api: int
    time_a: str
    time_b: str
    data_hora: datetime
    status: StatusPartida
    placar_time_a: int | None = None
    placar_time_b: int | None = None


class PartidaResponseSchema(BaseModel):
    """
    Define os dados de uma partida que podem ser retornados pelo sistema.
    """

    model_config = ConfigDict(
        from_attributes=True
    )

    id: int
    id_api: int
    time_a: str
    time_b: str
    data_hora: datetime
    status: StatusPartida
    placar_time_a: int | None
    placar_time_b: int | None