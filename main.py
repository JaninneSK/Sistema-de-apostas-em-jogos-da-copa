import backend.models

from backend.config.database import SessionLocal
from backend.dao.aposta_dao import ApostaDAO
from backend.dao.partida_dao import PartidaDAO
from backend.dao.usuario_dao import UsuarioDAO
from backend.services.aposta_service import ApostaService
from backend.services.usuario_service import UsuarioService
from backend.schemas.aposta_schema import ApostaCadastroSchema
from backend.utils.enums import Multiplicador, Palpite


def main():
    session = SessionLocal()

    try:
        usuario_dao = UsuarioDAO(session)
        partida_dao = PartidaDAO(session)
        aposta_dao = ApostaDAO(session)

        usuario_service = UsuarioService(usuario_dao)
        aposta_service = ApostaService(aposta_dao, usuario_dao, partida_dao)

        usuario = usuario_service.buscar_usuario_por_login("teste")

        if not usuario:
            print("Usuário de teste não encontrado.")
            return

        partida = None

        for partida_agendada in partida_dao.listar_agendadas():

            aposta_existente = aposta_dao.buscar_por_usuario_e_partida(
                usuario.id,
                partida_agendada.id
            )

            if not aposta_existente:
                partida = partida_agendada
                break

        if not partida:
            print("Nenhuma partida disponível para o teste.")
            return

        print("Partida escolhida:")
        print(partida.id, "-", partida.time_a, "x", partida.time_b)

        print("\nSaldo inicial:")
        print(usuario.pontos)

        odds = aposta_service.consultar_odds(partida.id)

        print("\nOdds antes da aposta:")
        print(partida.time_a, "-", odds[Palpite.TIME_A])
        print(partida.time_b, "-", odds[Palpite.TIME_B])

        dados_aposta = ApostaCadastroSchema(
            partida_id=partida.id,
            valor_apostado=10,
            palpite=Palpite.TIME_A
        )

        aposta = aposta_service.registrar_aposta(
            usuario.id,
            dados_aposta
        )

        print("\nHU2 - Aposta registrada:")
        print("ID:", aposta.id)
        print("Palpite:", aposta.palpite.value)
        print("Valor apostado:", aposta.valor_apostado)
        print("Multiplicador:", aposta.multiplicador)
        print("Odd armazenada:", aposta.odd_aplicada)
        print("Saldo após aposta:", usuario.pontos)

        status = aposta_service.consultar_status_aposta(aposta.id)

        print("\nHU3 - Status da aposta:")
        print(status)

        aposta = aposta_service.multiplicar_aposta(
            usuario.id,
            aposta.id,
            Multiplicador.X5
        )

        print("\nHU4 - Aposta multiplicada:")
        print("Novo multiplicador:", aposta.multiplicador)
        print("Valor base:", aposta.valor_apostado)
        print("Valor total comprometido:", aposta.valor_apostado * aposta.multiplicador)
        print("Odd continua:", aposta.odd_aplicada)

        usuario = usuario_service.buscar_usuario_por_id(usuario.id)

        print("\nHU9 - Saldo após multiplicação:")
        print(usuario.pontos)
        

    except Exception as erro:
        print("Erro:", erro)

    print("\nTeste 1 - Tentar diminuir o multiplicador:")

    try:
        aposta_service.multiplicar_aposta(
            usuario.id,
            aposta.id,
            Multiplicador.X2
        )

        print("Erro: o sistema permitiu diminuir o multiplicador.")

    except ValueError as erro:
        print("Bloqueio correto:", erro)


    print("\nTeste 2 - Tentar multiplicar além do saldo:")

    try:
        aposta_service.multiplicar_aposta(
            usuario.id,
            aposta.id,
            Multiplicador.X100
        )

        print("Erro: o sistema permitiu multiplicar sem saldo suficiente.")

    except ValueError as erro:
        print("Bloqueio correto:", erro)

    finally:
        session.close()


if __name__ == "__main__":
    main()