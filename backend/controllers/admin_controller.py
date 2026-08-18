from backend.models.aposta import Aposta
from backend.models.partida import Partida
from backend.models.usuario import Usuario
from backend.services.aposta_service import ApostaService
from backend.services.partida_service import PartidaService
from backend.services.usuario_service import UsuarioService


class AdminController:

    def __init__(self, usuario_service: UsuarioService, partida_service: PartidaService, aposta_service: ApostaService):
        self.usuario_service = usuario_service
        self.partida_service = partida_service
        self.aposta_service = aposta_service

    def listar_usuarios(self, admin_id: int) -> list[Usuario]:

        self.usuario_service.validar_admin(admin_id)

        return self.usuario_service.listar_usuarios()

    def listar_usuarios_ativos(self, admin_id: int) -> list[Usuario]:

        self.usuario_service.validar_admin(admin_id)

        return self.usuario_service.listar_usuarios_ativos()

    def listar_usuarios_inativos(self, admin_id: int) -> list[Usuario]:

        self.usuario_service.validar_admin(admin_id)

        return self.usuario_service.listar_usuarios_inativos()

    def buscar_usuario_por_id(self, admin_id: int, usuario_id: int) -> Usuario | None:

        self.usuario_service.validar_admin(admin_id)

        return self.usuario_service.buscar_usuario_por_id(usuario_id)

    def buscar_usuario_por_login(self, admin_id: int, login: str) -> Usuario | None:

        self.usuario_service.validar_admin(admin_id)

        return self.usuario_service.buscar_usuario_por_login(login)

    def buscar_usuario_por_email(self, admin_id: int, email: str) -> Usuario | None:

        self.usuario_service.validar_admin(admin_id)

        return self.usuario_service.buscar_usuario_por_email(email)

    def buscar_usuario_por_cpf(self, admin_id: int, cpf: str) -> Usuario | None:

        self.usuario_service.validar_admin(admin_id)

        return self.usuario_service.buscar_usuario_por_cpf(cpf)

    def desativar_usuario(self, admin_id: int, usuario_id: int) -> Usuario:

        self.usuario_service.validar_admin(admin_id)

        return self.usuario_service.desativar_usuario(usuario_id)

    def importar_partidas(self, admin_id: int) -> list[Partida]:

        self.usuario_service.validar_admin(admin_id)

        return self.partida_service.importar_partidas()

    def listar_partidas(self, admin_id: int) -> list[Partida]:

        self.usuario_service.validar_admin(admin_id)

        return self.partida_service.listar_partidas()

    def iniciar_partida(self, admin_id: int, partida_id: int) -> Partida:

        self.usuario_service.validar_admin(admin_id)

        return self.partida_service.iniciar_partida(partida_id)

    def finalizar_partida(self, admin_id: int, partida_id: int) -> tuple[Partida, list[Aposta]]:

        self.usuario_service.validar_admin(admin_id)

        partida = self.partida_service.finalizar_partida(partida_id)

        apostas = self.aposta_service.encerrar_apostas_da_partida(partida.id)

        return partida, apostas

    def listar_apostas_por_partida(self, admin_id: int, partida_id: int) -> list[Aposta]:

        self.usuario_service.validar_admin(admin_id)

        return self.aposta_service.listar_apostas_por_partida(partida_id)

    def consultar_detalhes_partida(self, admin_id: int, partida_id: int) -> dict:

        self.usuario_service.validar_admin(admin_id)

        return self.aposta_service.consultar_detalhes_partida(partida_id)

    def consultar_ranking(self, admin_id: int) -> list[Usuario]:

        self.usuario_service.validar_admin(admin_id)

        return self.usuario_service.listar_ranking()