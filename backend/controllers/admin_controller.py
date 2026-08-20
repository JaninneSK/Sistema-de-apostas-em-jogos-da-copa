from backend.models.aposta import Aposta
from backend.models.partida import Partida
from backend.models.usuario import Usuario
from backend.services.aposta_service import ApostaService
from backend.services.partida_service import PartidaService
from backend.services.usuario_service import UsuarioService
from backend.schemas.partida_schema import PartidaImportacaoSchema
from backend.exceptions.partida_exception import PartidaException


class AdminController:
    """
    Reúne as ações administrativas e faz a comunicação entre a View do
    administrador e os Services do sistema.
    """

    def __init__(self, usuario_service: UsuarioService, partida_service: PartidaService, aposta_service: ApostaService):
        self.usuario_service = usuario_service
        self.partida_service = partida_service
        self.aposta_service = aposta_service

    def listar_usuarios(self, admin_id: int) -> list[Usuario]:
        """
        Retorna todos os usuários comuns cadastrados no sistema.
        """

        self.usuario_service.validar_admin(admin_id)

        return self.usuario_service.listar_usuarios()

    def listar_usuarios_ativos(self, admin_id: int) -> list[Usuario]:
        """
        Retorna os usuários que estão ativos.
        """

        self.usuario_service.validar_admin(admin_id)

        return self.usuario_service.listar_usuarios_ativos()

    def listar_usuarios_inativos(self, admin_id: int) -> list[Usuario]:
        """
        Retorna os usuários que estão inativos.
        """

        self.usuario_service.validar_admin(admin_id)

        return self.usuario_service.listar_usuarios_inativos()

    def buscar_usuario_por_id(self, admin_id: int, usuario_id: int) -> Usuario | None:
        """
        Busca um usuário pelo seu ID.
        """

        self.usuario_service.validar_admin(admin_id)

        return self.usuario_service.buscar_usuario_por_id(usuario_id)

    def buscar_usuario_por_login(self, admin_id: int, login: str) -> Usuario | None:
        """
        Busca um usuário pelo login.
        """

        self.usuario_service.validar_admin(admin_id)

        return self.usuario_service.buscar_usuario_por_login(login)

    def buscar_usuario_por_email(self, admin_id: int, email: str) -> Usuario | None:
        """
        Busca um usuário pelo e-mail.
        """

        self.usuario_service.validar_admin(admin_id)

        return self.usuario_service.buscar_usuario_por_email(email)

    def buscar_usuario_por_cpf(self, admin_id: int, cpf: str) -> Usuario | None:
        """
        Busca um usuário pelo CPF.
        """

        self.usuario_service.validar_admin(admin_id)

        return self.usuario_service.buscar_usuario_por_cpf(cpf)

    def desativar_usuario(self, admin_id: int, usuario_id: int) -> Usuario:
        """
        Solicita a desativação de um usuário.
        """

        self.usuario_service.validar_admin(admin_id)

        return self.usuario_service.desativar_usuario(usuario_id)

    def listar_partidas_api(self, admin_id: int) -> list[PartidaImportacaoSchema]:
        """
        Retorna as partidas da Copa de 2026 disponíveis na API.
        """

        self.usuario_service.validar_admin(admin_id)

        return self.partida_service.listar_partidas_api()

    def criar_partida(self, admin_id: int, id_api: int) -> Partida:
        """
        Cria uma partida no sistema a partir de uma partida escolhida na API.
        """

        self.usuario_service.validar_admin(admin_id)

        return self.partida_service.criar_partida(id_api)

    def buscar_partida(self, admin_id: int, partida_id: int) -> Partida:
        """
        Busca uma partida cadastrada no sistema.
        """

        self.usuario_service.validar_admin(admin_id)

        partida = self.partida_service.buscar_partida(partida_id)

        if not partida:
            raise PartidaException("Partida não encontrada.")

        return partida

    def listar_partidas(self, admin_id: int) -> list[Partida]:
        """
        Retorna todas as partidas cadastradas no sistema.
        """

        self.usuario_service.validar_admin(admin_id)

        return self.partida_service.listar_partidas()

    def iniciar_partida(self, admin_id: int, partida_id: int) -> Partida:
        """
        Solicita o início de uma partida.
        """

        self.usuario_service.validar_admin(admin_id)

        return self.partida_service.iniciar_partida(partida_id)

    def finalizar_partida(self, admin_id: int, partida_id: int) -> tuple[Partida, list[Aposta]]:
        """
        Finaliza a partida e, em seguida, processa todas as apostas feitas nela.
        """

        self.usuario_service.validar_admin(admin_id)

        # A finalização da partida e o encerramento das apostas ficam separados
        # nos Services, então o Controller junta as duas ações em um único fluxo
        partida = self.partida_service.finalizar_partida(partida_id)

        apostas = self.aposta_service.encerrar_apostas_da_partida(partida.id)

        return partida, apostas

    def listar_apostas_por_partida(self, admin_id: int, partida_id: int) -> list[Aposta]:
        """
        Retorna todas as apostas feitas em uma determinada partida.
        """

        self.usuario_service.validar_admin(admin_id)

        return self.aposta_service.listar_apostas_por_partida(partida_id)

    def consultar_detalhes_partida(self, admin_id: int, partida_id: int) -> dict:
        """
        Retorna os times, a quantidade de apostadores e as odds de uma partida.
        """

        self.usuario_service.validar_admin(admin_id)

        return self.aposta_service.consultar_detalhes_partida(partida_id)

    def consultar_ranking(self, admin_id: int) -> list[Usuario]:
        """
        Retorna o ranking dos usuários.
        """

        self.usuario_service.validar_admin(admin_id)

        return self.usuario_service.listar_ranking()