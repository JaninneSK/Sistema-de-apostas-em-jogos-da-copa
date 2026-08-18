from sqlalchemy.orm import Session

from backend.models.usuario import Usuario


class UsuarioDAO:

    def __init__(self, session: Session):
        self.session = session

    def salvar(self, usuario: Usuario) -> Usuario:
        self.session.add(usuario)
        self.session.commit()
        self.session.refresh(usuario)
        return usuario

    def buscar_por_id(self, usuario_id: int) -> Usuario | None:
        return (
            self.session.query(Usuario)
            .filter(Usuario.id == usuario_id)
            .first()
        )

    def buscar_por_login(self, login: str) -> Usuario | None:
        return (
            self.session.query(Usuario)
            .filter(Usuario.login == login)
            .first()
        )

    def buscar_por_email(self, email: str) -> Usuario | None:
        return (
            self.session.query(Usuario)
            .filter(Usuario.email == email)
            .first()
        )

    def buscar_por_cpf(self, cpf: str) -> Usuario | None:
        return (
            self.session.query(Usuario)
            .filter(Usuario.cpf == cpf)
            .first()
        )

    def listar(self) -> list[Usuario]:
        return self.session.query(Usuario).all()
    
    def listar_ativos(self) -> list[Usuario]:
        return (
            self.session.query(Usuario)
            .filter(Usuario.ativo.is_(True))
            .all()
        )
    
    def listar_inativos(self) -> list[Usuario]:
        return (
            self.session.query(Usuario)
            .filter(Usuario.ativo.is_(False))
            .all()
        )

    def listar_ranking(self) -> list[Usuario]:
        return (
            self.session.query(Usuario)
            .order_by(Usuario.quantidade_acertos.desc())
            .all()
        )

    def atualizar(self, usuario: Usuario) -> Usuario:
        self.session.commit()
        self.session.refresh(usuario)
        return usuario

    def remover(self, usuario: Usuario) -> None:
        self.session.delete(usuario)
        self.session.commit()