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


class UsuarioService:

    def __init__(self, usuario_dao: UsuarioDAO):
        self.usuario_dao = usuario_dao

    def cadastrar_usuario(self, dados: UsuarioCadastroSchema) -> Usuario:

        if self.usuario_dao.buscar_por_login(dados.login):
            raise ValueError("Login já cadastrado.")

        if self.usuario_dao.buscar_por_email(dados.email):
            raise ValueError("E-mail já cadastrado.")

        if self.usuario_dao.buscar_por_cpf(dados.cpf):
            raise ValueError("CPF já cadastrado.")

        if not validar_cpf(dados.cpf):
            raise ValueError("CPF inválido.")

        if not validar_idade(dados.data_nascimento):
            raise ValueError("Usuário deve possuir idade mínima permitida.")

        if not validar_senha(dados.senha):
            raise ValueError(
                "Senha deve possuir no mínimo 8 caracteres, uma letra maiúscula, uma letra minúscula, um número e um caractere especial."
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

    def autenticar_usuario(self, login: str, senha: str) -> Usuario | None:

        usuario = self.usuario_dao.buscar_por_login(login)

        if not usuario:
            return None

        senha_hash = gerar_hash_senha(senha)

        if usuario.senha_hash != senha_hash:
            return None

        return usuario

    def buscar_usuario_por_id(self, usuario_id: int) -> Usuario | None:

        return self.usuario_dao.buscar_por_id(usuario_id)
    
    def buscar_usuario_por_login(self, login: str) -> Usuario | None:
        return self.usuario_dao.buscar_por_login(login)


    def buscar_usuario_por_email(self, email: str) -> Usuario | None:
        return self.usuario_dao.buscar_por_email(email)


    def buscar_usuario_por_cpf(self, cpf: str) -> Usuario | None:
        return self.usuario_dao.buscar_por_cpf(cpf)

    def listar_usuarios(self) -> list[Usuario]:
        return self.usuario_dao.listar()
    
    def listar_usuarios_ativos(self) -> list[Usuario]:
        return self.usuario_dao.listar_ativos()
    
    def listar_usuarios_inativos(self) -> list[Usuario]:
        return self.usuario_dao.listar_inativos()

    def atualizar_usuario(self, usuario_id: int, dados: UsuarioAtualizacaoSchema) -> Usuario:

        usuario = self.usuario_dao.buscar_por_id(usuario_id)

        if not usuario:
            raise ValueError("Usuário não encontrado.")

        if dados.nome is not None:
            usuario.nome = dados.nome

        if dados.email is not None:
            usuario.email = dados.email

        if dados.senha is not None:

            if not validar_senha(dados.senha):
                raise ValueError(
                    "Senha deve possuir no mínimo 8 caracteres, uma letra maiúscula, uma letra minúscula, um número e um caractere especial."
                )

            usuario.senha_hash = gerar_hash_senha(dados.senha)

        return self.usuario_dao.atualizar(usuario)

    def desativar_usuario(self, usuario_id: int) -> Usuario:

        usuario = self.usuario_dao.buscar_por_id(usuario_id)

        if not usuario:
            raise ValueError("Usuário não encontrado.")

        usuario.ativo = False

        return self.usuario_dao.atualizar(usuario)