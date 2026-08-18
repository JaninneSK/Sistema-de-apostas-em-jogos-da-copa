from backend.models.aposta import Aposta
from backend.schemas.aposta_schema import ApostaCadastroSchema
from backend.services.aposta_service import ApostaService
from backend.utils.enums import Palpite, StatusAposta, Multiplicador


class ApostaController:

    def __init__(self, aposta_service: ApostaService):
        self.aposta_service = aposta_service

    def registrar(self, usuario_id: int, dados: ApostaCadastroSchema) -> Aposta:
        return self.aposta_service.registrar_aposta(usuario_id, dados)

    def multiplicar(self, usuario_id: int, aposta_id: int, multiplicador: Multiplicador) -> Aposta:
        return self.aposta_service.multiplicar_aposta(usuario_id, aposta_id, multiplicador)

    def consultar_odds(self, partida_id: int) -> dict[Palpite, float]:
        return self.aposta_service.consultar_odds(partida_id)

    def consultar_status(self, aposta_id: int) -> StatusAposta:
        return self.aposta_service.consultar_status_aposta(aposta_id)

    def consultar_aposta(self, usuario_id: int, partida_id: int) -> Aposta | None:
        return self.aposta_service.buscar_aposta_por_usuario_e_partida(usuario_id, partida_id)

    def listar_apostas_do_usuario(self, usuario_id: int) -> list[Aposta]:
        return self.aposta_service.listar_apostas_por_usuario(usuario_id)

    def listar_disponiveis(self) -> list[dict]:
        return self.aposta_service.listar_apostas_disponiveis()