from datetime import datetime

from pydantic import ValidationError

from backend.controllers.usuario_controller import UsuarioController
from backend.schemas.usuario_schema import UsuarioCadastroSchema
from backend.utils.enums import TipoUsuario
from backend.exceptions.usuario_exception import UsuarioException
from backend.exceptions.autenticacao_exception import AutenticacaoException

from backend.views.usuario_view import UsuarioView
from backend.views.admin_view import AdminView


class MenuView:
    """
    Exibe o menu inicial do sistema e controla o cadastro e login dos usuários.
    """

    def __init__(self, usuario_controller: UsuarioController, usuario_view: UsuarioView, admin_view: AdminView):
        self.usuario_controller = usuario_controller
        self.usuario_view = usuario_view
        self.admin_view = admin_view

    def executar(self) -> None:
        """
        Mantém o menu principal em execução até que o usuário escolha sair.
        """

        while True:

            print("\n=== SISTEMA DE APOSTAS - COPA DO MUNDO 2026 ===")
            print("1 - Criar conta")
            print("2 - Login")
            print("0 - Sair")

            opcao = input("\nEscolha uma opção: ")

            if opcao == "1":
                self._cadastrar_usuario()

            elif opcao == "2":
                self._realizar_login()

            elif opcao == "0":
                print("\nSistema encerrado.")
                break

            else:
                print("\nOpção inválida.")

    def _cadastrar_usuario(self) -> None:
        """
        Coleta os dados necessários e tenta cadastrar um novo usuário.
        """

        print("\n=== CRIAR CONTA ===")

        try:
            nome = input("Nome: ")
            email = input("E-mail: ")
            cpf = input("CPF (somente números): ")
            data_nascimento = input("Data de nascimento (dd/mm/aaaa): ")
            login = input("Login: ")
            senha = input("Senha: ")

            try:
                data_nascimento = datetime.strptime(data_nascimento, "%d/%m/%Y").date()

            except ValueError:
                print("\nErro: Data de nascimento inválida. Use o formato dd/mm/aaaa.")
                return

            dados = UsuarioCadastroSchema(
                nome=nome,
                email=email,
                cpf=cpf,
                data_nascimento=data_nascimento,
                login=login,
                senha=senha
            )

            usuario = self.usuario_controller.cadastrar(dados)

            print("\nUsuário cadastrado com sucesso!")
            print("ID:", usuario.id)
            print("Nome:", usuario.nome)
            print("Pontos iniciais:", usuario.pontos)

        except UsuarioException as erro:
            print("\nErro:", erro)

        except ValidationError as erro:
            print("\nDados inválidos:")

            for erro_validacao in erro.errors():
                campo = erro_validacao["loc"][0]
                mensagem = erro_validacao["msg"]

                print(f"- {campo}: {mensagem}")

    def _realizar_login(self) -> None:
        """
        Realiza o login e direciona o usuário para o menu correspondente
        ao seu tipo.
        """

        print("\n=== LOGIN ===")

        login = input("Login: ")
        senha = input("Senha: ")

        try:
            usuario = self.usuario_controller.autenticar(login, senha)

            print(f"\nBem-vindo(a), {usuario.nome}!")

            if usuario.tipo == TipoUsuario.ADMIN:
                # Direcionando o administrador ao menu de administrador
                self.admin_view.executar(usuario)

            else:
                # Direcionando o usuario ao menu de usuario
                self.usuario_view.executar(usuario)

        except AutenticacaoException as erro:
            print("\nErro:", erro)

        except ValueError as erro:
            print("\nErro:", erro)