from backend.models.usuario import Usuario
from backend.schemas.usuario_schema import UsuarioCadastroSchema, UsuarioAtualizacaoSchema
from backend.services.usuario_service import UsuarioService
from backend.exceptions.usuario_exception import UsuarioException


class UsuarioController:
    """
    Faz a comunicação entre as Views e as funcionalidades relacionadas
    aos usuários.
    """

    def __init__(self, usuario_service: UsuarioService):
        self.usuario_service = usuario_service

    def cadastrar(self, dados: UsuarioCadastroSchema) -> Usuario:
        """
        Envia os dados para o cadastro de um novo usuário.
        """
        return self.usuario_service.cadastrar_usuario(dados)

    def autenticar(self, login: str, senha: str) -> Usuario | None:
        """
        Envia os dados informados para autenticar o usuário.
        """
        return self.usuario_service.autenticar_usuario(login, senha)

    def consultar_perfil(self, usuario_id: int) -> Usuario | None:
        """
        Busca os dados do perfil do usuário.
        """
        return self.usuario_service.buscar_usuario_por_id(usuario_id)

    def consultar_saldo(self, usuario_id: int) -> int:
        """
        Retorna a quantidade de pontos disponíveis do usuário.
        """

        usuario = self.usuario_service.buscar_usuario_por_id(usuario_id)

        if not usuario:
            raise UsuarioException("Usuário não encontrado.")

        return usuario.pontos

    def atualizar_perfil(self, usuario_id: int, dados: UsuarioAtualizacaoSchema) -> Usuario:
        """
        Envia os novos dados para atualização do perfil do usuário.
        """
        return self.usuario_service.atualizar_usuario(usuario_id, dados)

    def desativar_conta(self, usuario_id: int) -> Usuario:
        """
        Solicita a desativação da conta do usuário.
        """
        return self.usuario_service.desativar_usuario(usuario_id)

    def consultar_ranking(self) -> list[Usuario]:
        """
        Retorna o ranking dos usuários.
        """
        return self.usuario_service.listar_ranking()