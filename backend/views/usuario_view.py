from pydantic import ValidationError
from backend.controllers.aposta_controller import ApostaController
from backend.controllers.partida_controller import PartidaController
from backend.controllers.usuario_controller import UsuarioController
from backend.models.usuario import Usuario
from backend.schemas.aposta_schema import ApostaCadastroSchema
from backend.schemas.usuario_schema import UsuarioAtualizacaoSchema
from backend.utils.enums import Multiplicador, Palpite
from backend.exceptions.usuario_exception import UsuarioException
from backend.exceptions.aposta_exception import ApostaException
from backend.exceptions.partida_exception import PartidaException
from backend.exceptions.permissao_exception import PermissaoException


class UsuarioView:
    """
    Exibe o menu e as funcionalidades disponíveis para os usuários comuns.
    """

    def __init__(self, usuario_controller: UsuarioController, aposta_controller: ApostaController, partida_controller: PartidaController):
        self.usuario_controller = usuario_controller
        self.aposta_controller = aposta_controller
        self.partida_controller = partida_controller

    def executar(self, usuario: Usuario) -> None:
        """
        Mantém o menu do usuário em execução até que ele faça logout
        ou cancele sua participação.
        """

        while True:

            print(f"\n=== MENU DO USUÁRIO - {usuario.nome} ===")
            print("1 - Ver perfil")
            print("2 - Alterar senha")
            print("3 - Ver resultados anteriores de uma seleção")
            print("4 - Ver apostas disponíveis")
            print("5 - Registrar aposta")
            print("6 - Ver minhas apostas")
            print("7 - Consultar status de uma aposta")
            print("8 - Multiplicar aposta")
            print("9 - Consultar saldo")
            print("10 - Ver ranking")
            print("11 - Cancelar participação")
            print("0 - Logout")

            opcao = input("\nEscolha uma opção: ")

            try:

                if opcao == "1":
                    self._mostrar_perfil(usuario.id)

                elif opcao == "2":
                    self._alterar_senha(usuario.id)

                elif opcao == "3":
                    self._mostrar_resultados_selecao()

                elif opcao == "4":
                    self._mostrar_apostas_disponiveis()

                elif opcao == "5":
                    self._registrar_aposta(usuario.id)

                elif opcao == "6":
                    self._mostrar_apostas_usuario(usuario.id)

                elif opcao == "7":
                    self._consultar_status_aposta(usuario.id)

                elif opcao == "8":
                    self._multiplicar_aposta(usuario.id)

                elif opcao == "9":
                    self._mostrar_saldo(usuario.id)

                elif opcao == "10":
                    self._mostrar_ranking()

                elif opcao == "11":

                    if self._cancelar_participacao(usuario.id):
                        return

                elif opcao == "0":
                    print("\nLogout realizado.")
                    return

                else:
                    print("\nOpção inválida.")

            except UsuarioException as erro:
                print("\nErro:", erro)

            except ApostaException as erro:
                print("\nErro:", erro)

            except PartidaException as erro:
                print("\nErro:", erro)

            except PermissaoException as erro:
                print("\nErro:", erro)

            except ValueError as erro:
                print("\nErro:", erro)

            except ValidationError as erro:
                print("\nDados inválidos:")

                for erro_validacao in erro.errors():
                    campo = erro_validacao["loc"][0]
                    mensagem = erro_validacao["msg"]

                    print(f"- {campo}: {mensagem}")

    def _mostrar_perfil(self, usuario_id: int) -> None:
        """
        Exibe os dados do perfil do usuário.
        """

        usuario = self.usuario_controller.consultar_perfil(usuario_id)

        if not usuario:
            raise ValueError("Usuário não encontrado.")

        print("\n=== PERFIL ===")
        print("ID:", usuario.id)
        print("Nome:", usuario.nome)
        print("E-mail:", usuario.email)
        print("CPF:", usuario.cpf)
        print("Login:", usuario.login)
        print("Pontos:", usuario.pontos)
        print("Acertos:", usuario.quantidade_acertos)
        print("Status:", "Ativo" if usuario.ativo else "Inativo")

    def _alterar_senha(self, usuario_id: int) -> None:
        """
        Solicita uma nova senha e envia os dados para atualização.
        """

        print("\n=== ALTERAR SENHA ===")

        nova_senha = input("Nova senha: ")

        dados = UsuarioAtualizacaoSchema(
            senha=nova_senha
        )

        self.usuario_controller.atualizar_perfil(
            usuario_id,
            dados
        )

        print("\nSenha alterada com sucesso.")

    def _mostrar_resultados_selecao(self) -> None:
        """
        Busca e exibe os resultados anteriores de uma seleção.
        """

        print("\n=== RESULTADOS ANTERIORES ===")

        selecao = input("Digite o nome da seleção: ")

        resultados = self.partida_controller.buscar_resultados_por_selecao(
            selecao
        )

        if not resultados:
            print("\nNenhum resultado encontrado.")
            return

        for partida in resultados:

            print(
                f"\n{partida.time_a} "
                f"{partida.placar_time_a} x "
                f"{partida.placar_time_b} "
                f"{partida.time_b}"
            )

            print("Data:", partida.data_hora)

    def _mostrar_apostas_disponiveis(self) -> None:
        """
        Exibe as partidas disponíveis para apostas junto com suas odds.
        """

        print("\n=== APOSTAS DISPONÍVEIS ===")

        apostas_disponiveis = self.aposta_controller.listar_disponiveis()

        if not apostas_disponiveis:
            print("\nNenhuma partida disponível para apostas.")
            return

        for dados in apostas_disponiveis:

            partida = dados["partida"]

            print(f"\nID da partida: {partida.id}")
            print(partida.time_a, "x", partida.time_b)
            print(f"{partida.time_a} - Odd: {dados['odd_time_a']}")
            print(f"{partida.time_b} - Odd: {dados['odd_time_b']}")

    def _registrar_aposta(self, usuario_id: int) -> None:
        """
        Coleta os dados necessários e registra uma nova aposta.
        """

        print("\n=== REGISTRAR APOSTA ===")

        partida_id = int(input("ID da partida: "))
        valor_apostado = int(input("Quantidade de pontos: "))

        partida = self.partida_controller.buscar(partida_id)

        if not partida:
            raise ValueError("Partida não encontrada.")

        odds = self.aposta_controller.consultar_odds(partida_id)

        print("\n1 -", partida.time_a, "- Odd:", odds[Palpite.TIME_A])
        print("2 -", partida.time_b, "- Odd:", odds[Palpite.TIME_B])

        opcao_palpite = input("\nEscolha o time: ")

        if opcao_palpite == "1":
            palpite = Palpite.TIME_A

        elif opcao_palpite == "2":
            palpite = Palpite.TIME_B

        else:
            raise ValueError("Palpite inválido.")

        dados = ApostaCadastroSchema(
            partida_id=partida_id,
            valor_apostado=valor_apostado,
            palpite=palpite
        )

        aposta = self.aposta_controller.registrar(
            usuario_id,
            dados
        )

        print("\nAposta registrada com sucesso!")
        print("ID da aposta:", aposta.id)
        print("Odd aplicada:", aposta.odd_aplicada)
        print("Multiplicador:", aposta.multiplicador)

    def _mostrar_apostas_usuario(self, usuario_id: int) -> None:
        """
        Exibe todas as apostas realizadas pelo usuário.
        """

        print("\n=== MINHAS APOSTAS ===")

        apostas = self.aposta_controller.listar_apostas_do_usuario(usuario_id)

        if not apostas:
            print("\nVocê ainda não realizou apostas.")
            return

        for aposta in apostas:

            partida = self.partida_controller.buscar(aposta.partida_id)

            print(f"\nID da aposta: {aposta.id}")

            if partida:
                print("Partida:", partida.time_a, "x", partida.time_b)

            # O palpite é armazenado como TIME_A ou TIME_B, mas aqui é mostrado
            # o nome do time para deixar a informação mais clara para o usuário
            if aposta.palpite == Palpite.TIME_A:
                time_apostado = partida.time_a
            else:
                time_apostado = partida.time_b

            print("Palpite:", time_apostado)
            print("Valor:", aposta.valor_apostado)
            print("Multiplicador:", aposta.multiplicador)
            print("Odd:", aposta.odd_aplicada)
            print("Status:", aposta.status.value)

    def _consultar_status_aposta(self, usuario_id: int) -> None:
        """
        Exibe o status de uma aposta pertencente ao usuário.
        """

        print("\n=== STATUS DA APOSTA ===")

        aposta_id = int(input("ID da aposta: "))

        aposta = self.aposta_controller.consultar_aposta_por_id(aposta_id)

        if not aposta:
            raise ValueError("Aposta não encontrada.")

        if aposta.usuario_id != usuario_id:
            raise ValueError("Essa aposta não pertence ao usuário.")

        status = self.aposta_controller.consultar_status(aposta_id)

        print("\nStatus:", status.value)

    def _multiplicar_aposta(self, usuario_id: int) -> None:
        """
        Permite aumentar o multiplicador de uma aposta ativa.
        """

        print("\n=== MULTIPLICAR APOSTA ===")

        aposta_id = int(input("ID da aposta: "))

        multiplicadores = ", ".join(
            f"{multiplicador.value}x"
            for multiplicador in Multiplicador
            if multiplicador.value > 1
        )

        print("Multiplicadores disponíveis:", multiplicadores)

        valor_multiplicador = int(input("Novo multiplicador: "))

        try:
            multiplicador = Multiplicador(valor_multiplicador)

        except ValueError:
            raise ValueError("Multiplicador inválido.")

        aposta = self.aposta_controller.multiplicar(
            usuario_id,
            aposta_id,
            multiplicador
        )

        print("\nAposta multiplicada com sucesso!")
        print("Novo multiplicador:", aposta.multiplicador)

    def _mostrar_saldo(self, usuario_id: int) -> None:
        """
        Exibe a quantidade de pontos disponíveis do usuário.
        """

        saldo = self.usuario_controller.consultar_saldo(usuario_id)

        print("\n=== SALDO ===")
        print("Pontos disponíveis:", saldo)

    def _mostrar_ranking(self) -> None:
        """
        Exibe o ranking dos usuários de acordo com seus acertos e pontos.
        """

        ranking = self.usuario_controller.consultar_ranking()

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

    def _cancelar_participacao(self, usuario_id: int) -> bool:
        """
        Confirma a decisão do usuário e desativa sua participação no sistema.
        """

        print("\n=== CANCELAR PARTICIPAÇÃO ===")
        print("Sua conta ficará inativa e você não poderá mais realizar login.")

        confirmacao = input("Deseja continuar? (s/n): ").lower()

        if confirmacao != "s":
            print("\nOperação cancelada.")
            return False

        self.usuario_controller.desativar_conta(usuario_id)

        print("\nParticipação cancelada. Sua conta agora está inativa.")

        return True