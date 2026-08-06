from backend.dao.partida_dao import PartidaDAO
from backend.models.partida import Partida


class PartidaService:

    def __init__(self, partida_dao: PartidaDAO):
        self.partida_dao = partida_dao

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