from backend.dao.usuario_dao import UsuarioDAO
from backend.models.usuario import Usuario
from backend.utils.enums import TipoUsuario
from backend.schemas.usuario_schema import (
    UsuarioCadastroSchema,
    UsuarioAtualizacaoSchema
)
from backend.utils.validadores import (
    validar_senha,
    validar_cpf,
    validar_idade
)
from backend.utils.seguranca import gerar_hash_senha
from backend.exceptions.usuario_exception import UsuarioException
from backend.exceptions.autenticacao_exception import AutenticacaoException
from backend.exceptions.permissao_exception import PermissaoException


class UsuarioService:
    """
    Reúne as regras de negócio relacionadas aos usuários do sistema.
    """

    def __init__(self, usuario_dao: UsuarioDAO):
        self.usuario_dao = usuario_dao

    def cadastrar_usuario(self, dados: UsuarioCadastroSchema) -> Usuario:
        """
        Cadastra um novo usuário depois de validar seus dados e verificar
        se login, e-mail e CPF já estão sendo utilizados.
        """

        if self.usuario_dao.buscar_por_login(dados.login):
            raise UsuarioException("Login já cadastrado.")

        if self.usuario_dao.buscar_por_email(dados.email):
            raise UsuarioException("E-mail já cadastrado.")

        if self.usuario_dao.buscar_por_cpf(dados.cpf):
            raise UsuarioException("CPF já cadastrado.")

        if not validar_cpf(dados.cpf):
            raise UsuarioException("CPF inválido.")

        if not validar_idade(dados.data_nascimento):
            raise UsuarioException("Usuário deve possuir idade mínima permitida.")

        if not validar_senha(dados.senha):
            raise UsuarioException(
                "Senha deve possuir no mínimo 8 caracteres, uma letra maiúscula, " \
                "uma letra minúscula, um número e um caractere especial."
            )

        usuario = Usuario(
            nome=dados.nome,
            email=dados.email,
            cpf=dados.cpf,
            data_nascimento=dados.data_nascimento,
            login=dados.login,
            senha_hash=gerar_hash_senha(dados.senha),
            tipo=TipoUsuario.USUARIO
        )

        return self.usuario_dao.salvar(usuario)

    def autenticar_usuario(self, login: str, senha: str) -> Usuario:
        """
        Autentica o usuário a partir do login e da senha informados.
        """

        usuario = self.usuario_dao.buscar_por_login(login)

        if not usuario:
            raise AutenticacaoException("Login ou senha inválidos.")

        senha_hash = gerar_hash_senha(senha)

        if usuario.senha_hash != senha_hash:
            raise AutenticacaoException("Login ou senha inválidos.")

        if not usuario.ativo:
            raise AutenticacaoException("Usuário inativo. Acesso ao sistema não permitido.")

        return usuario

    def buscar_usuario_por_id(self, usuario_id: int) -> Usuario | None:
        """
        Busca um usuário pelo seu ID.
        """
        return self.usuario_dao.buscar_por_id(usuario_id)
    
    def buscar_usuario_por_login(self, login: str) -> Usuario | None:
        """
        Busca um usuário pelo login.
        """
        return self.usuario_dao.buscar_por_login(login)

    def buscar_usuario_por_email(self, email: str) -> Usuario | None:
        """
        Busca um usuário pelo e-mail.
        """
        return self.usuario_dao.buscar_por_email(email)

    def buscar_usuario_por_cpf(self, cpf: str) -> Usuario:
        """
        Busca um usuário pelo CPF informado.
        """

        usuario = self.usuario_dao.buscar_por_cpf(cpf)

        if not usuario:
            raise UsuarioException("Usuário não encontrado.")

        return usuario

    def listar_usuarios(self) -> list[Usuario]:
        """
        Retorna todos os usuários comuns cadastrados no sistema.
        """
        return self.usuario_dao.listar()
    
    def listar_usuarios_ativos(self) -> list[Usuario]:
        """
        Retorna os usuários que ainda estão ativos no sistema.
        """
        return self.usuario_dao.listar_ativos()
    
    def listar_usuarios_inativos(self) -> list[Usuario]:
        """
        Retorna os usuários que estão inativos no sistema.
        """
        return self.usuario_dao.listar_inativos()

    def listar_ranking(self) -> list[Usuario]:
        """
        Retorna o ranking dos usuários de acordo com seus acertos e pontos.
        """
        return self.usuario_dao.listar_ranking()

    def atualizar_usuario(self, usuario_id: int, dados: UsuarioAtualizacaoSchema) -> Usuario:
        """
        Atualiza os dados informados pelo usuário e valida novamente a senha
        caso ela também esteja sendo alterada.
        """

        usuario = self.usuario_dao.buscar_por_id(usuario_id)

        if not usuario:
            raise UsuarioException("Usuário não encontrado.")

        if dados.nome is not None:
            usuario.nome = dados.nome

        if dados.email is not None:
            usuario.email = dados.email

        if dados.senha is not None:

            if not validar_senha(dados.senha):
                raise UsuarioException(
                    "Senha deve possuir no mínimo 8 caracteres, uma letra maiúscula, " \
                    "uma letra minúscula, um número e um caractere especial."
                )

            usuario.senha_hash = gerar_hash_senha(dados.senha)

        return self.usuario_dao.atualizar(usuario)

    def desativar_usuario(self, usuario_id: int) -> Usuario:
        """
        Desativa a participação do usuário sem remover seus dados do sistema.
        """

        usuario = self.usuario_dao.buscar_por_id(usuario_id)

        if not usuario:
            raise UsuarioException("Usuário não encontrado.")

        # O usuário não é excluído para que seus dados e sua posição no ranking
        # continuem disponíveis mesmo depois do cancelamento da participação
        usuario.ativo = False

        return self.usuario_dao.atualizar(usuario)

    def validar_admin(self, usuario_id: int) -> Usuario:
        """
        Confirma se o usuário informado existe, está ativo e possui permissão
        de administrador.
        """

        usuario = self.usuario_dao.buscar_por_id(usuario_id)

        if not usuario:
            raise UsuarioException("Usuário não encontrado.")

        if usuario.tipo != TipoUsuario.ADMIN:
            raise PermissaoException("Acesso permitido apenas para administradores.")

        if not usuario.ativo:
            raise AutenticacaoException("Administrador inativo.")

        return usuario