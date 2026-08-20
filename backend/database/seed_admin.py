from datetime import date

from backend.config.database import SessionLocal
from backend.dao.usuario_dao import UsuarioDAO
from backend.models.usuario import Usuario
from backend.utils.enums import TipoUsuario
from backend.utils.seguranca import gerar_hash_senha
from backend.models.usuario import Usuario
from backend.models.partida import Partida
from backend.models.aposta import Aposta


def criar_admin():
    """
    Cria o administrador inicial do sistema caso ele ainda não esteja
    cadastrado no banco.
    """

    session = SessionLocal()

    try:
        usuario_dao = UsuarioDAO(session)

        admin_existente = usuario_dao.buscar_por_login("admin")

        # O administrador não pode ser cadastrado pela tela de criação de conta,
        # então ele é criado diretamente no banco na primeira execução deste arquivo
        if admin_existente:
            print("Administrador já cadastrado.")
            return

        admin = Usuario(
            nome="Administrador",
            email="admin@gmail.com",
            cpf="00000000000",
            data_nascimento=date(1986, 7, 12),
            login="admin",
            senha_hash=gerar_hash_senha("Admin@123"),
            tipo=TipoUsuario.ADMIN,
            ativo=True
        )

        usuario_dao.salvar(admin)

        print("Administrador criado com sucesso!")

    finally:
        session.close()


if __name__ == "__main__":
    criar_admin()