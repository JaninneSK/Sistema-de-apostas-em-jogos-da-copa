from backend.models.partida import Partida
from backend.schemas.partida_schema import PartidaImportacaoSchema
from backend.services.partida_service import PartidaService


class PartidaController:
    """
    Faz a comunicação entre as Views e as funcionalidades relacionadas
    às partidas.
    """

    def __init__(self, partida_service: PartidaService):
        self.partida_service = partida_service

    def buscar(self, partida_id: int) -> Partida | None:
        """
        Busca uma partida pelo seu ID.
        """
        return self.partida_service.buscar_partida(partida_id)

    def listar(self) -> list[Partida]:
        """
        Retorna todas as partidas cadastradas no sistema.
        """
        return self.partida_service.listar_partidas()

    def listar_agendadas(self) -> list[Partida]:
        """
        Retorna as partidas que ainda estão agendadas.
        """
        return self.partida_service.listar_agendadas()

    def listar_em_andamento(self) -> list[Partida]:
        """
        Retorna as partidas que estão em andamento.
        """
        return self.partida_service.listar_em_andamento()

    def listar_finalizadas(self) -> list[Partida]:
        """
        Retorna as partidas que já foram finalizadas.
        """
        return self.partida_service.listar_finalizadas()

    def buscar_resultados_por_selecao(self, selecao: str) -> list[PartidaImportacaoSchema]:
        """
        Busca os resultados anteriores de uma seleção na Copa de 2026.
        """
        return self.partida_service.buscar_resultados_por_selecao(selecao)