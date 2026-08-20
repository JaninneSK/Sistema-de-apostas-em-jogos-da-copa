from backend.models.aposta import Aposta
from backend.schemas.aposta_schema import ApostaCadastroSchema
from backend.services.aposta_service import ApostaService
from backend.utils.enums import Palpite, StatusAposta, Multiplicador


class ApostaController:
    """
    Faz a comunicação entre as Views e as funcionalidades relacionadas
    às apostas.
    """

    def __init__(self, aposta_service: ApostaService):
        self.aposta_service = aposta_service

    def registrar(self, usuario_id: int, dados: ApostaCadastroSchema) -> Aposta:
        """
        Envia os dados para registrar uma nova aposta.
        """
        return self.aposta_service.registrar_aposta(usuario_id, dados)

    def multiplicar(self, usuario_id: int, aposta_id: int, multiplicador: Multiplicador) -> Aposta:
        """
        Solicita o aumento do multiplicador de uma aposta.
        """
        return self.aposta_service.multiplicar_aposta(usuario_id, aposta_id, multiplicador)

    def consultar_odds(self, partida_id: int) -> dict[Palpite, float]:
        """
        Retorna as odds atuais de uma partida.
        """
        return self.aposta_service.consultar_odds(partida_id)

    def consultar_status(self, aposta_id: int) -> StatusAposta:
        """
        Retorna o status de uma aposta.
        """
        return self.aposta_service.consultar_status_aposta(aposta_id)

    def consultar_aposta(self, usuario_id: int, partida_id: int) -> Aposta | None:
        """
        Busca a aposta de um usuário em uma determinada partida.
        """
        return self.aposta_service.buscar_aposta_por_usuario_e_partida(usuario_id, partida_id)

    def consultar_aposta_por_id(self, aposta_id: int) -> Aposta | None:
        """
        Busca uma aposta pelo seu ID.
        """
        return self.aposta_service.buscar_aposta(aposta_id)

    def listar_apostas_do_usuario(self, usuario_id: int) -> list[Aposta]:
        """
        Retorna todas as apostas realizadas pelo usuário.
        """
        return self.aposta_service.listar_apostas_por_usuario(usuario_id)

    def listar_disponiveis(self) -> list[dict]:
        """
        Retorna as partidas que estão disponíveis para apostas junto com
        suas odds atuais.
        """
        return self.aposta_service.listar_apostas_disponiveis()