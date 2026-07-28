from sqlalchemy.orm import Session

from backend.models.partida import Partida
from backend.utils.enums import StatusPartida


class PartidaDAO:

    def __init__(self, session: Session):
        self.session = session

    def salvar(self, partida: Partida) -> Partida:
        self.session.add(partida)
        self.session.commit()
        self.session.refresh(partida)
        return partida

    def buscar_por_id(self, partida_id: int) -> Partida | None:
        return (
            self.session.query(Partida)
            .filter(Partida.id == partida_id)
            .first()
        )

    def buscar_por_id_api(self, id_api: int) -> Partida | None:
        return (
            self.session.query(Partida)
            .filter(Partida.id_api == id_api)
            .first()
        )

    def listar(self) -> list[Partida]:
        return self.session.query(Partida).all()

    def listar_agendadas(self) -> list[Partida]:
        return (
            self.session.query(Partida)
            .filter(Partida.status == StatusPartida.AGENDADA)
            .all()
        )
    
    def listar_em_andamento(self) -> list[Partida]:
        return (
            self.session.query(Partida)
            .filter(Partida.status == StatusPartida.EM_ANDAMENTO)
            .all()
        )

    def listar_finalizadas(self) -> list[Partida]:
        return (
            self.session.query(Partida)
            .filter(Partida.status == StatusPartida.FINALIZADA)
            .all()
        )

    def atualizar(self, partida: Partida) -> Partida:
        self.session.commit()
        self.session.refresh(partida)
        return partida

    def deletar(self, partida: Partida) -> None:
        self.session.delete(partida)
        self.session.commit()