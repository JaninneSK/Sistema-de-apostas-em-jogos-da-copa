from datetime import datetime
from pydantic import BaseModel, ConfigDict
from backend.utils.enums import StatusPartida

class PartidaImportacaoSchema(BaseModel):

    id_api: int

    time_a: str

    time_b: str

    data_hora: datetime

    status: StatusPartida

    placar_time_a: int | None = None

    placar_time_b: int | None = None

class PartidaResponseSchema(BaseModel):

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