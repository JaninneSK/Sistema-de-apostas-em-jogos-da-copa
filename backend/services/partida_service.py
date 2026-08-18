from backend.api.football_data_api import FootballDataAPI
from backend.dao.partida_dao import PartidaDAO
from backend.models.partida import Partida
from backend.utils.enums import StatusPartida
from backend.schemas.partida_schema import PartidaImportacaoSchema


class PartidaService:

    def __init__(self, partida_dao: PartidaDAO, football_api: FootballDataAPI):
        self.partida_dao = partida_dao
        self.football_api = football_api

    def buscar_partida(self, partida_id: int) -> Partida | None:
        return self.partida_dao.buscar_por_id(partida_id)

    def listar_partidas(self) -> list[Partida]:
        return self.partida_dao.listar()

    def listar_agendadas(self) -> list[Partida]:
        return self.partida_dao.listar_agendadas()

    def listar_em_andamento(self) -> list[Partida]:
        return self.partida_dao.listar_em_andamento()

    def listar_finalizadas(self) -> list[Partida]:
        return self.partida_dao.listar_finalizadas()

    def importar_partidas(self) -> list[Partida]:

        dados_partidas = self.football_api.buscar_partidas_copa_2026()

        partidas_importadas = []

        for dados in dados_partidas:

            partida_existente = self.partida_dao.buscar_por_id_api(dados.id_api)

            if partida_existente:
                continue

            partida = Partida(
                id_api=dados.id_api,
                time_a=dados.time_a,
                time_b=dados.time_b,
                data_hora=dados.data_hora,
                status=StatusPartida.AGENDADA,
                placar_time_a=None,
                placar_time_b=None
            )

            partida = self.partida_dao.salvar(partida)
            partidas_importadas.append(partida)

        return partidas_importadas

    def iniciar_partida(self, partida_id: int) -> Partida:

        partida = self.partida_dao.buscar_por_id(partida_id)

        if not partida:
            raise ValueError("Partida não encontrada.")

        if partida.status != StatusPartida.AGENDADA:
            raise ValueError("Apenas partidas agendadas podem ser iniciadas.")

        partida.status = StatusPartida.EM_ANDAMENTO

        return self.partida_dao.atualizar(partida)


    def finalizar_partida(self, partida_id: int) -> Partida:

        partida = self.partida_dao.buscar_por_id(partida_id)

        if not partida:
            raise ValueError("Partida não encontrada.")

        if partida.status != StatusPartida.EM_ANDAMENTO:
            raise ValueError("Apenas partidas em andamento podem ser finalizadas.")

        dados_api = self.football_api.buscar_partida_por_id(partida.id_api)

        partida.placar_time_a = dados_api.placar_time_a
        partida.placar_time_b = dados_api.placar_time_b
        partida.status = StatusPartida.FINALIZADA

        return self.partida_dao.atualizar(partida)

    def buscar_resultados_por_selecao(self, selecao: str) -> list[PartidaImportacaoSchema]:

        partidas = self.football_api.buscar_partidas_copa_2026()

        resultados = []

        for partida in partidas:

            if partida.status != StatusPartida.FINALIZADA:
                continue

            if partida.time_a.lower() == selecao.lower() or partida.time_b.lower() == selecao.lower():
                resultados.append(partida)

        return resultados