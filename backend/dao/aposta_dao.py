from sqlalchemy.orm import Session

from backend.models.aposta import Aposta
from backend.utils.enums import StatusAposta
from backend.utils.enums import StatusAposta, Palpite


class ApostaDAO:

    def __init__(self, session: Session):
        self.session = session

    def salvar(self, aposta: Aposta) -> Aposta:
        self.session.add(aposta)
        self.session.commit()
        self.session.refresh(aposta)
        return aposta

    def buscar_por_id(self, aposta_id: int) -> Aposta | None:
        return (
            self.session.query(Aposta)
            .filter(Aposta.id == aposta_id)
            .first()
        )

    def listar(self) -> list[Aposta]:
        return self.session.query(Aposta).all()

    def listar_por_usuario(self, usuario_id: int) -> list[Aposta]:
        return (
            self.session.query(Aposta)
            .filter(Aposta.usuario_id == usuario_id)
            .all()
        )

    def listar_por_partida(self, partida_id: int) -> list[Aposta]:
        return (
            self.session.query(Aposta)
            .filter(Aposta.partida_id == partida_id)
            .all()
        )

    def listar_ativas(self) -> list[Aposta]:
        return (
            self.session.query(Aposta)
            .filter(Aposta.status == StatusAposta.ATIVA)
            .all()
        )
    
    def contar_apostas_time_a(self, partida_id: int) -> int:
        return (
            self.session.query(Aposta)
            .filter(
                Aposta.partida_id == partida_id,
                Aposta.palpite == Palpite.TIME_A
            )
            .count()
        )


    def contar_apostas_time_b(self, partida_id: int) -> int:
        return (
            self.session.query(Aposta)
            .filter(
                Aposta.partida_id == partida_id,
                Aposta.palpite == Palpite.TIME_B
            )
            .count()
        )

    def atualizar(self, aposta: Aposta) -> Aposta:
        self.session.commit()
        self.session.refresh(aposta)
        return aposta

    def deletar(self, aposta: Aposta) -> None:
        self.session.delete(aposta)
        self.session.commit()