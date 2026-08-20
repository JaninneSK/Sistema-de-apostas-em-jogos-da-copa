from sqlalchemy.orm import Session

from backend.models.usuario import Usuario
from backend.utils.enums import TipoUsuario


class UsuarioDAO:
    """
    Responsável pelo acesso e pelas operações realizadas com usuários no banco de dados.
    """

    def __init__(self, session: Session):
        self.session = session

    def salvar(self, usuario: Usuario) -> Usuario:
        """
        Salva um novo usuário no banco de dados.
        """
        self.session.add(usuario)
        self.session.commit()
        self.session.refresh(usuario)
        return usuario

    def buscar_por_id(self, usuario_id: int) -> Usuario | None:
        """
        Busca um usuário pelo seu ID.
        """
        return (
            self.session.query(Usuario)
            .filter(Usuario.id == usuario_id)
            .first()
        )

    def buscar_por_login(self, login: str) -> Usuario | None:
        """
        Busca um usuário pelo login.
        """
        return (
            self.session.query(Usuario)
            .filter(Usuario.login == login)
            .first()
        )

    def buscar_por_email(self, email: str) -> Usuario | None:
        """
        Busca um usuário pelo e-mail.
        """
        return (
            self.session.query(Usuario)
            .filter(Usuario.email == email)
            .first()
        )

    def buscar_por_cpf(self, cpf: str) -> Usuario | None:
        """
        Busca um usuário pelo CPF.
        """
        return (
            self.session.query(Usuario)
            .filter(Usuario.cpf == cpf)
            .first()
        )

    def listar(self) -> list[Usuario]:
        """
        Retorna todos os usuários comuns cadastrados no sistema.
        """
        return (
            self.session.query(Usuario)
            .filter(Usuario.tipo == TipoUsuario.USUARIO)
            .all()
        )
    
    def listar_ativos(self) -> list[Usuario]:
        """
        Retorna todos os usuários comuns que estão ativos.
        """
        return (
            self.session.query(Usuario)
            .filter(
                Usuario.tipo == TipoUsuario.USUARIO,
                Usuario.ativo == True
            )
            .all()
        )
    
    def listar_inativos(self) -> list[Usuario]:
        """
        Retorna todos os usuários comuns que estão inativos.
        """
        return (
            self.session.query(Usuario)
            .filter(
                Usuario.tipo == TipoUsuario.USUARIO,
                Usuario.ativo == False
            )
            .all()
        )
    
    def listar_ranking(self) -> list[Usuario]:
        """
        Retorna os usuários ordenados pela quantidade de acertos e, em caso
        de empate, pela quantidade de pontos.
        """
        return (
            self.session.query(Usuario)
            .filter(Usuario.tipo == TipoUsuario.USUARIO)
            .order_by(
                Usuario.quantidade_acertos.desc(),
                Usuario.pontos.desc()
            )
            .all()
        )

    def atualizar(self, usuario: Usuario) -> Usuario:
        """
        Salva no banco as alterações feitas em um usuário.
        """
        self.session.commit()
        self.session.refresh(usuario)
        return usuario

    def remover(self, usuario: Usuario) -> None:
        """
        Remove um usuário do banco de dados.
        """
        self.session.delete(usuario)
        self.session.commit()