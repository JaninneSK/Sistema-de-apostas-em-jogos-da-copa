from datetime import date

import backend.models

from backend.config.database import SessionLocal
from backend.dao.usuario_dao import UsuarioDAO
from backend.models.usuario import Usuario
from backend.utils.enums import TipoUsuario
from backend.utils.seguranca import gerar_hash_senha


def criar_admin():
    session = SessionLocal()

    try:
        usuario_dao = UsuarioDAO(session)

        admin_existente = usuario_dao.buscar_por_login("admin")

        if admin_existente:
            print("Administrador já cadastrado.")
            return

        admin = Usuario(
            nome="Administrador",
            email="admin@email.com",
            cpf="00000000000",
            data_nascimento=date(1990, 1, 1),
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