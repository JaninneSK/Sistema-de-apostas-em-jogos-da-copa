from sqlalchemy.orm import Session

from backend.models.aposta import Aposta
from backend.utils.enums import StatusAposta, Palpite


class ApostaDAO:
    """
    Responsável pelo acesso e pelas operações realizadas com apostas no banco de dados.
    """

    def __init__(self, session: Session):
        self.session = session

    def salvar(self, aposta: Aposta) -> Aposta:
        """
        Salva uma nova aposta no banco de dados.
        """
        self.session.add(aposta)
        self.session.commit()
        self.session.refresh(aposta)
        return aposta

    def buscar_por_id(self, aposta_id: int) -> Aposta | None:
        """
        Busca uma aposta pelo seu ID.
        """
        return (
            self.session.query(Aposta)
            .filter(Aposta.id == aposta_id)
            .first()
        )

    def listar(self) -> list[Aposta]:
        """
        Retorna todas as apostas cadastradas no sistema.
        """
        return self.session.query(Aposta).all()

    def listar_por_usuario(self, usuario_id: int) -> list[Aposta]:
        """
        Retorna todas as apostas realizadas por um usuário.
        """
        return (
            self.session.query(Aposta)
            .filter(Aposta.usuario_id == usuario_id)
            .all()
        )

    def listar_por_partida(self, partida_id: int) -> list[Aposta]:
        """
        Retorna todas as apostas realizadas em uma partida.
        """
        return (
            self.session.query(Aposta)
            .filter(Aposta.partida_id == partida_id)
            .all()
        )

    def listar_ativas(self) -> list[Aposta]:
        """
        Retorna todas as apostas que ainda estão ativas.
        """
        return (
            self.session.query(Aposta)
            .filter(Aposta.status == StatusAposta.ATIVA)
            .all()
        )

    def contar_apostas_time_a(self, partida_id: int) -> int:
        """
        Conta quantas apostas foram realizadas no time A de uma partida.
        """
        return (
            self.session.query(Aposta)
            .filter(
                Aposta.partida_id == partida_id,
                Aposta.palpite == Palpite.TIME_A
            )
            .count()
        )

    def contar_apostas_time_b(self, partida_id: int) -> int:
        """
        Conta quantas apostas foram realizadas no time B de uma partida.
        """
        return (
            self.session.query(Aposta)
            .filter(
                Aposta.partida_id == partida_id,
                Aposta.palpite == Palpite.TIME_B
            )
            .count()
        )
    
    def buscar_por_usuario_e_partida(self, usuario_id: int, partida_id: int) -> Aposta | None:
        """
        Busca a aposta de um usuário em uma determinada partida.
        """
        return (
            self.session.query(Aposta)
            .filter(
                Aposta.usuario_id == usuario_id,
                Aposta.partida_id == partida_id
            )
            .first()
        )

    def atualizar(self, aposta: Aposta) -> Aposta:
        """
        Salva no banco as alterações feitas em uma aposta.
        """
        self.session.commit()
        self.session.refresh(aposta)
        return aposta

    def deletar(self, aposta: Aposta) -> None:
        """
        Remove uma aposta do banco de dados.
        """
        self.session.delete(aposta)
        self.session.commit()

    def possui_aposta_ativa(self, usuario_id: int) -> bool:
        """
        Verifica se o usuário ainda possui alguma aposta ativa.
        """
        return (
            self.session.query(Aposta)
            .filter(
                Aposta.usuario_id == usuario_id,
                Aposta.status == StatusAposta.ATIVA
            )
            .first()
            is not None
        )