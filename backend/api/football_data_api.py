from datetime import datetime

from backend.api.api_client import APIClient
from backend.schemas.partida_schema import PartidaImportacaoSchema
from backend.utils.enums import StatusPartida


class FootballDataAPI:
    """
    Busca os dados da Copa do Mundo de 2026 e converte as informações da
    football-data.org para o formato utilizado pelo sistema.
    """

    def __init__(self, api_client: APIClient):
        self.api_client = api_client

    def buscar_partidas_copa_2026(self) -> list[PartidaImportacaoSchema]:
        """
        Busca todas as partidas da Copa do Mundo de 2026 na API.
        """

        dados = self.api_client.get(
            "competitions/WC/matches",
            {"season": 2026}
        )

        partidas = []

        for dados_partida in dados["matches"]:
            partida = self._converter_partida(dados_partida)
            partidas.append(partida)

        return partidas

    def buscar_partida_por_id(self, id_api: int) -> PartidaImportacaoSchema:
        """
        Busca uma partida específica utilizando o ID fornecido pela API.
        """

        dados = self.api_client.get(
            f"matches/{id_api}"
        )

        return self._converter_partida(dados)

    def _converter_status(self, status_api: str) -> StatusPartida:
        """
        Converte os status utilizados pela API para os status definidos
        pelo sistema.
        """

        if status_api in ["SCHEDULED", "TIMED"]:
            return StatusPartida.AGENDADA

        if status_api in ["LIVE", "IN_PLAY", "PAUSED"]:
            return StatusPartida.EM_ANDAMENTO

        if status_api == "FINISHED":
            return StatusPartida.FINALIZADA

        raise ValueError(
            f"Status da API não reconhecido: {status_api}"
        )

    def _converter_partida(self, dados: dict) -> PartidaImportacaoSchema:
        """
        Converte os dados de uma partida recebidos da API para o schema
        utilizado pelo sistema.
        """

        placar = dados["score"]["fullTime"]

        # A API retorna a data em UTC e com o caractere Z no final. Essa
        # conversão permite transformar esse valor em um datetime do Python
        data_hora = datetime.fromisoformat(
            dados["utcDate"].replace("Z", "+00:00")
        )

        return PartidaImportacaoSchema(
            id_api=dados["id"],
            time_a=dados["homeTeam"]["name"],
            time_b=dados["awayTeam"]["name"],
            data_hora=data_hora,
            status=self._converter_status(dados["status"]),
            placar_time_a=placar["home"],
            placar_time_b=placar["away"]
        )

    def listar_partidas_copa_2026(self) -> list[PartidaImportacaoSchema]:
        return self.buscar_partidas_copa_2026()