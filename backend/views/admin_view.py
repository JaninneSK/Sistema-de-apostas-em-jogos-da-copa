from backend.controllers.admin_controller import AdminController
from backend.models.usuario import Usuario


class AdminView:

    def __init__(self, admin_controller: AdminController):
        self.admin_controller = admin_controller

    def executar(self, admin: Usuario) -> None:

        while True:

            print(f"\n=== MENU DO ADMINISTRADOR - {admin.nome} ===")
            print("1 - Importar/Criar partidas da Copa")
            print("2 - Listar partidas")
            print("3 - Consultar detalhes de uma partida")
            print("4 - Iniciar partida")
            print("5 - Finalizar partida")
            print("6 - Listar todos os usuários")
            print("7 - Listar usuários ativos")
            print("8 - Listar usuários inativos")
            print("9 - Pesquisar usuário")
            print("10 - Consultar apostas de uma partida")
            print("11 - Ver ranking")
            print("0 - Logout")

            opcao = input("\nEscolha uma opção: ")

            try:

                if opcao == "1":
                    self._importar_partidas(admin.id)

                elif opcao == "2":
                    self._listar_partidas(admin.id)

                elif opcao == "3":
                    self._consultar_detalhes_partida(admin.id)

                elif opcao == "4":
                    self._iniciar_partida(admin.id)

                elif opcao == "5":
                    self._finalizar_partida(admin.id)

                elif opcao == "6":
                    self._listar_usuarios(admin.id)

                elif opcao == "7":
                    self._listar_usuarios_ativos(admin.id)

                elif opcao == "8":
                    self._listar_usuarios_inativos(admin.id)

                elif opcao == "9":
                    self._pesquisar_usuario(admin.id)

                elif opcao == "10":
                    self._consultar_apostas_partida(admin.id)

                elif opcao == "11":
                    self._mostrar_ranking(admin.id)

                elif opcao == "0":
                    print("\nLogout realizado.")
                    return

                else:
                    print("\nOpção inválida.")

            except ValueError as erro:
                print("\nErro:", erro)

            except RuntimeError as erro:
                print("\nErro ao acessar a API:", erro)

    def _importar_partidas(self, admin_id: int) -> None:

        print("\n=== IMPORTAR PARTIDAS ===")

        partidas = self.admin_controller.importar_partidas(admin_id)

        if not partidas:
            print("Nenhuma nova partida foi importada.")
            return

        print(f"{len(partidas)} partidas importadas com sucesso.")

    def _listar_partidas(self, admin_id: int) -> None:

        partidas = self.admin_controller.listar_partidas(admin_id)

        print("\n=== PARTIDAS ===")

        if not partidas:
            print("Nenhuma partida encontrada.")
            return

        for partida in partidas:

            print(f"\nID: {partida.id}")
            print(partida.time_a, "x", partida.time_b)
            print("Status:", partida.status.value)

            if partida.placar_time_a is not None and partida.placar_time_b is not None:
                print(
                    "Placar:",
                    partida.placar_time_a,
                    "x",
                    partida.placar_time_b
                )

    def _consultar_detalhes_partida(self, admin_id: int) -> None:

        print("\n=== DETALHES DA PARTIDA ===")

        partida_id = int(input("ID da partida: "))

        dados = self.admin_controller.consultar_detalhes_partida(
            admin_id,
            partida_id
        )

        partida = dados["partida"]

        print("\nPartida:", partida.time_a, "x", partida.time_b)

        print(
            partida.time_a,
            "- Apostadores:",
            dados["quantidade_time_a"],
            "- Odd:",
            dados["odd_time_a"]
        )

        print(
            partida.time_b,
            "- Apostadores:",
            dados["quantidade_time_b"],
            "- Odd:",
            dados["odd_time_b"]
        )

    def _iniciar_partida(self, admin_id: int) -> None:

        print("\n=== INICIAR PARTIDA ===")

        partida_id = int(input("ID da partida: "))

        partida = self.admin_controller.iniciar_partida(
            admin_id,
            partida_id
        )

        print("\nPartida iniciada com sucesso.")
        print(partida.time_a, "x", partida.time_b)
        print("Status:", partida.status.value)

    def _finalizar_partida(self, admin_id: int) -> None:

        print("\n=== FINALIZAR PARTIDA ===")

        partida_id = int(input("ID da partida: "))

        partida, apostas = self.admin_controller.finalizar_partida(
            admin_id,
            partida_id
        )

        print("\nPartida finalizada com sucesso.")
        print(
            partida.time_a,
            partida.placar_time_a,
            "x",
            partida.placar_time_b,
            partida.time_b
        )

        print("\nApostas processadas:", len(apostas))

        for aposta in apostas:

            print(f"\nAposta ID: {aposta.id}")
            print("Usuário ID:", aposta.usuario_id)
            print("Palpite:", aposta.palpite.value)
            print("Status:", aposta.status.value)
            print("Pontos ganhos:", aposta.pontos_ganhos)

    def _exibir_usuario(self, usuario: Usuario) -> None:

        print("\n=== DADOS DO USUÁRIO ===")
        print("ID:", usuario.id)
        print("Nome:", usuario.nome)
        print("E-mail:", usuario.email)
        print("CPF:", usuario.cpf)
        print("Login:", usuario.login)
        print("Pontos:", usuario.pontos)
        print("Acertos:", usuario.quantidade_acertos)
        print("Tipo:", usuario.tipo.value)
        print("Ativo:", usuario.ativo)

    def _exibir_usuarios(self, usuarios: list[Usuario]) -> None:

        if not usuarios:
            print("Nenhum usuário encontrado.")
            return

        for usuario in usuarios:
            self._exibir_usuario(usuario)

    def _listar_usuarios(self, admin_id: int) -> None:

        usuarios = self.admin_controller.listar_usuarios(admin_id)

        print("\n=== TODOS OS USUÁRIOS ===")

        self._exibir_usuarios(usuarios)

    def _listar_usuarios_ativos(self, admin_id: int) -> None:

        usuarios = self.admin_controller.listar_usuarios_ativos(admin_id)

        print("\n=== USUÁRIOS ATIVOS ===")

        self._exibir_usuarios(usuarios)

    def _listar_usuarios_inativos(self, admin_id: int) -> None:

        usuarios = self.admin_controller.listar_usuarios_inativos(admin_id)

        print("\n=== USUÁRIOS INATIVOS ===")

        self._exibir_usuarios(usuarios)

    def _pesquisar_usuario(self, admin_id: int) -> None:

        while True:

            print("\n=== PESQUISAR USUÁRIO ===")
            print("1 - Buscar por ID")
            print("2 - Buscar por CPF")
            print("3 - Buscar por login")
            print("4 - Buscar por e-mail")
            print("0 - Voltar")

            opcao = input("\nEscolha uma opção: ")

            if opcao == "1":

                usuario_id = int(input("ID do usuário: "))

                usuario = self.admin_controller.buscar_usuario_por_id(
                    admin_id,
                    usuario_id
                )

            elif opcao == "2":

                cpf = input("CPF: ")

                usuario = self.admin_controller.buscar_usuario_por_cpf(
                    admin_id,
                    cpf
                )

            elif opcao == "3":

                login = input("Login: ")

                usuario = self.admin_controller.buscar_usuario_por_login(
                    admin_id,
                    login
                )

            elif opcao == "4":

                email = input("E-mail: ")

                usuario = self.admin_controller.buscar_usuario_por_email(
                    admin_id,
                    email
                )

            elif opcao == "0":
                return

            else:
                print("\nOpção inválida.")
                continue

            if not usuario:
                print("\nUsuário não encontrado.")
                continue

            self._exibir_usuario(usuario)

    def _consultar_apostas_partida(self, admin_id: int) -> None:

        print("\n=== APOSTAS DA PARTIDA ===")

        partida_id = int(input("ID da partida: "))

        apostas = self.admin_controller.listar_apostas_por_partida(
            admin_id,
            partida_id
        )

        if not apostas:
            print("\nNenhuma aposta encontrada para essa partida.")
            return

        for aposta in apostas:

            print(f"\nAposta ID: {aposta.id}")
            print("Usuário ID:", aposta.usuario_id)
            print("Palpite:", aposta.palpite.value)
            print("Valor:", aposta.valor_apostado)
            print("Multiplicador:", aposta.multiplicador)
            print("Odd:", aposta.odd_aplicada)
            print("Status:", aposta.status.value)

    def _mostrar_ranking(self, admin_id: int) -> None:

        ranking = self.admin_controller.consultar_ranking(admin_id)

        print("\n=== RANKING ===")

        if not ranking:
            print("Nenhum usuário encontrado.")
            return

        posicao = 1

        for usuario in ranking:

            print(
                f"{posicao}º - {usuario.nome} | "
                f"Acertos: {usuario.quantidade_acertos} | "
                f"Pontos: {usuario.pontos}"
            )

            posicao += 1

    def _exibir_usuarios(self, usuarios: list[Usuario]) -> None:

        if not usuarios:
            print("Nenhum usuário encontrado.")
            return

        for usuario in usuarios:

            print(f"\nID: {usuario.id}")
            print("Nome:", usuario.nome)
            print("CPF:", usuario.cpf)
            print("Login:", usuario.login)
            print("Pontos:", usuario.pontos)
            print("Acertos:", usuario.quantidade_acertos)
            print("Tipo:", usuario.tipo.value)
            print("Ativo:", usuario.ativo)