from backend.models.partida import Partida
from backend.schemas.partida_schema import PartidaImportacaoSchema
from backend.services.partida_service import PartidaService


class PartidaController:

    def __init__(self, partida_service: PartidaService):
        self.partida_service = partida_service

    def buscar(self, partida_id: int) -> Partida | None:
        return self.partida_service.buscar_partida(partida_id)

    def listar(self) -> list[Partida]:
        return self.partida_service.listar_partidas()

    def listar_agendadas(self) -> list[Partida]:
        return self.partida_service.listar_agendadas()

    def listar_em_andamento(self) -> list[Partida]:
        return self.partida_service.listar_em_andamento()

    def listar_finalizadas(self) -> list[Partida]:
        return self.partida_service.listar_finalizadas()

    def buscar_resultados_por_selecao(self, selecao: str) -> list[PartidaImportacaoSchema]:
        return self.partida_service.buscar_resultados_por_selecao(selecao)