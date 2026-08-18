from backend.models.usuario import Usuario
from backend.schemas.usuario_schema import UsuarioCadastroSchema, UsuarioAtualizacaoSchema
from backend.services.usuario_service import UsuarioService


class UsuarioController:

    def __init__(self, usuario_service: UsuarioService):
        self.usuario_service = usuario_service

    def cadastrar(self, dados: UsuarioCadastroSchema) -> Usuario:
        return self.usuario_service.cadastrar_usuario(dados)

    def autenticar(self, login: str, senha: str) -> Usuario | None:
        return self.usuario_service.autenticar_usuario(login, senha)

    def consultar_perfil(self, usuario_id: int) -> Usuario | None:
        return self.usuario_service.buscar_usuario_por_id(usuario_id)

    def consultar_saldo(self, usuario_id: int) -> int:

        usuario = self.usuario_service.buscar_usuario_por_id(usuario_id)

        if not usuario:
            raise ValueError("Usuário não encontrado.")

        return usuario.pontos

    def atualizar_perfil(self, usuario_id: int, dados: UsuarioAtualizacaoSchema) -> Usuario:
        return self.usuario_service.atualizar_usuario(usuario_id, dados)

    def desativar_conta(self, usuario_id: int) -> Usuario:
        return self.usuario_service.desativar_usuario(usuario_id)

    def consultar_ranking(self) -> list[Usuario]:
        return self.usuario_service.listar_ranking()