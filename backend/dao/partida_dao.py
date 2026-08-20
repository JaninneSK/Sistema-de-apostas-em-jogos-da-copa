from sqlalchemy.orm import Session

from backend.models.partida import Partida
from backend.utils.enums import StatusPartida


class PartidaDAO:
    """
    Responsável pelo acesso e pelas operações realizadas com partidas no banco de dados.
    """

    def __init__(self, session: Session):
        self.session = session

    def salvar(self, partida: Partida) -> Partida:
        """
        Salva uma nova partida no banco de dados.
        """
        self.session.add(partida)
        self.session.commit()
        self.session.refresh(partida)
        return partida

    def buscar_por_id(self, partida_id: int) -> Partida | None:
        """
        Busca uma partida pelo seu ID.
        """
        return (
            self.session.query(Partida)
            .filter(Partida.id == partida_id)
            .first()
        )

    def buscar_por_id_api(self, id_api: int) -> Partida | None:
        """
        Busca uma partida pelo ID fornecido pela API.
        """
        return (
            self.session.query(Partida)
            .filter(Partida.id_api == id_api)
            .first()
        )

    def listar(self) -> list[Partida]:
        """
        Retorna todas as partidas cadastradas no sistema.
        """
        return self.session.query(Partida).all()

    def listar_agendadas(self) -> list[Partida]:
        """
        Retorna as partidas que estão agendadas.
        """
        return (
            self.session.query(Partida)
            .filter(Partida.status == StatusPartida.AGENDADA)
            .all()
        )
    
    def listar_em_andamento(self) -> list[Partida]:
        """
        Retorna as partidas que estão em andamento.
        """
        return (
            self.session.query(Partida)
            .filter(Partida.status == StatusPartida.EM_ANDAMENTO)
            .all()
        )

    def listar_finalizadas(self) -> list[Partida]:
        """
        Retorna as partidas que já foram finalizadas.
        """
        return (
            self.session.query(Partida)
            .filter(Partida.status == StatusPartida.FINALIZADA)
            .all()
        )

    def atualizar(self, partida: Partida) -> Partida:
        """
        Salva no banco as alterações feitas em uma partida.
        """
        self.session.commit()
        self.session.refresh(partida)
        return partida

    def deletar(self, partida: Partida) -> None:
        """
        Remove uma partida do banco de dados.
        """
        self.session.delete(partida)
        self.session.commit()