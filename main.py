import backend.models

from backend.api.api_client import APIClient
from backend.api.football_data_api import FootballDataAPI

from backend.config.database import SessionLocal

from backend.dao.usuario_dao import UsuarioDAO
from backend.dao.partida_dao import PartidaDAO
from backend.dao.aposta_dao import ApostaDAO

from backend.services.usuario_service import UsuarioService
from backend.services.partida_service import PartidaService
from backend.services.aposta_service import ApostaService

from backend.controllers.usuario_controller import UsuarioController
from backend.controllers.partida_controller import PartidaController
from backend.controllers.aposta_controller import ApostaController
from backend.controllers.admin_controller import AdminController

from backend.views.usuario_view import UsuarioView
from backend.views.admin_view import AdminView
from backend.views.menu_view import MenuView


def main():
    session = SessionLocal()

    try:
        # DAOs
        usuario_dao = UsuarioDAO(session)
        partida_dao = PartidaDAO(session)
        aposta_dao = ApostaDAO(session)

        # API
        api_client = APIClient()
        football_api = FootballDataAPI(api_client)

        # Services
        usuario_service = UsuarioService(usuario_dao)
        partida_service = PartidaService(partida_dao, football_api)
        aposta_service = ApostaService(aposta_dao, usuario_dao, partida_dao)

        # Controllers
        usuario_controller = UsuarioController(usuario_service)
        partida_controller = PartidaController(partida_service)
        aposta_controller = ApostaController(aposta_service)

        admin_controller = AdminController(
            usuario_service,
            partida_service,
            aposta_service
        )

        # Views
        usuario_view = UsuarioView(
            usuario_controller,
            aposta_controller,
            partida_controller
        )

        admin_view = AdminView(
            admin_controller
        )

        menu_view = MenuView(
            usuario_controller,
            usuario_view,
            admin_view
        )

        # Início da aplicação
        menu_view.executar()

    finally:
        session.close()


if __name__ == "__main__":
    main()