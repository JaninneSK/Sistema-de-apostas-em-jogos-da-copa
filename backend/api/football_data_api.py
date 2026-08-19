from datetime import datetime

from backend.api.api_client import APIClient
from backend.schemas.partida_schema import PartidaImportacaoSchema
from backend.utils.enums import StatusPartida


class FootballDataAPI:

    def __init__(self, api_client: APIClient):
        self.api_client = api_client

    def buscar_partidas_copa_2026(self) -> list[PartidaImportacaoSchema]:

        dados = self.api_client.get(
            "competitions/WC/matches",
            {"season": 2026}
        )

        partidas = []

        for dados_partida in dados["matches"]:
            partida = self._converter_partida(dados_partida)
            partidas.append(partida)

        return partidas

    def _converter_status(self, status_api: str) -> StatusPartida:

        if status_api in ["SCHEDULED", "TIMED"]:
            return StatusPartida.AGENDADA

        if status_api in ["LIVE", "IN_PLAY", "PAUSED"]:
            return StatusPartida.EM_ANDAMENTO

        if status_api == "FINISHED":
            return StatusPartida.FINALIZADA

        raise ValueError(f"Status da API não reconhecido: {status_api}")

    def _converter_partida(self, dados: dict) -> PartidaImportacaoSchema:

        placar = dados["score"]["fullTime"]

        return PartidaImportacaoSchema(
            id_api=dados["id"],
            time_a=dados["homeTeam"]["name"],
            time_b=dados["awayTeam"]["name"],
            data_hora=datetime.fromisoformat(
                dados["utcDate"].replace("Z", "+00:00")
            ),
            status=self._converter_status(dados["status"]),
            placar_time_a=placar["home"],
            placar_time_b=placar["away"]
        )

    def buscar_partida_por_id(self, id_api: int) -> PartidaImportacaoSchema:

        dados = self.api_client.get(f"matches/{id_api}")
        
        return self._converter_partida(dados)

    def listar_partidas_copa_2026(self) -> list[PartidaImportacaoSchema]:
        return self.buscar_partidas_copa_2026()