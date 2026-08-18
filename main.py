from datetime import date, datetime

import backend.models

from backend.config.database import SessionLocal
from backend.dao.usuario_dao import UsuarioDAO
from backend.dao.partida_dao import PartidaDAO
from backend.dao.aposta_dao import ApostaDAO
from backend.services.usuario_service import UsuarioService
from backend.services.aposta_service import ApostaService
from backend.models.partida import Partida
from backend.schemas.usuario_schema import UsuarioCadastroSchema
from backend.schemas.aposta_schema import ApostaCadastroSchema
from backend.utils.enums import StatusPartida, Palpite, Multiplicador


def main():
    session = SessionLocal()

    try:
        usuario_dao = UsuarioDAO(session)
        partida_dao = PartidaDAO(session)
        aposta_dao = ApostaDAO(session)

        usuario_service = UsuarioService(usuario_dao)
        aposta_service = ApostaService(aposta_dao, usuario_dao, partida_dao)

        partida = partida_dao.buscar_por_id_api(1001)

        if not partida:
            partida = Partida(
                id_api=1001,
                time_a="Espanha",
                time_b="Portugal",
                data_hora=datetime(2026, 7, 2, 16, 0),
                status=StatusPartida.AGENDADA
            )

            partida = partida_dao.salvar(partida)

        usuario1 = usuario_service.buscar_usuario_por_login("teste")
        usuario2 = usuario_service.buscar_usuario_por_login("teste2")

        usuario3 = usuario_service.buscar_usuario_por_login("teste3")

        if not usuario3:
            dados_usuario3 = UsuarioCadastroSchema(
                nome="Terceiro Usuario",
                email="teste3@email.com",
                cpf="11122233344",
                data_nascimento=date(2000, 1, 1),
                login="teste3",
                senha="Teste@123"
            )

            usuario3 = usuario_service.cadastrar_usuario(dados_usuario3)

        print("Odds iniciais:")

        odds = aposta_service.consultar_odds(partida.id)

        print(partida.time_a, "-", odds[Palpite.TIME_A])
        print(partida.time_b, "-", odds[Palpite.TIME_B])

        if not aposta_dao.buscar_por_usuario_e_partida(usuario1.id, partida.id):

            aposta_service.registrar_aposta(
                usuario1.id,
                ApostaCadastroSchema(
                    partida_id=partida.id,
                    valor_apostado=10,
                    multiplicador=Multiplicador.X1,
                    palpite=Palpite.TIME_A
                )
            )

        print("\nApós 1 aposta no Time A:")

        odds = aposta_service.consultar_odds(partida.id)

        print(partida.time_a, "-", odds[Palpite.TIME_A])
        print(partida.time_b, "-", odds[Palpite.TIME_B])

        if not aposta_dao.buscar_por_usuario_e_partida(usuario2.id, partida.id):

            aposta_service.registrar_aposta(
                usuario2.id,
                ApostaCadastroSchema(
                    partida_id=partida.id,
                    valor_apostado=10,
                    multiplicador=Multiplicador.X1,
                    palpite=Palpite.TIME_B
                )
            )

        print("\nApós 1 aposta em cada time:")

        odds = aposta_service.consultar_odds(partida.id)

        print(partida.time_a, "-", odds[Palpite.TIME_A])
        print(partida.time_b, "-", odds[Palpite.TIME_B])

        if not aposta_dao.buscar_por_usuario_e_partida(usuario3.id, partida.id):

            aposta_service.registrar_aposta(
                usuario3.id,
                ApostaCadastroSchema(
                    partida_id=partida.id,
                    valor_apostado=10,
                    multiplicador=Multiplicador.X1,
                    palpite=Palpite.TIME_A
                )
            )

        print("\nApós 2 apostas no A e 1 no B:")

        odds = aposta_service.consultar_odds(partida.id)

        print(partida.time_a, "-", odds[Palpite.TIME_A])
        print(partida.time_b, "-", odds[Palpite.TIME_B])

        aposta1 = aposta_dao.buscar_por_usuario_e_partida(usuario1.id, partida.id)
        aposta2 = aposta_dao.buscar_por_usuario_e_partida(usuario2.id, partida.id)
        aposta3 = aposta_dao.buscar_por_usuario_e_partida(usuario3.id, partida.id)

        print("\nOdds armazenadas nas apostas:")
        print(usuario1.nome, "-", aposta1.palpite.value, "- Odd:", aposta1.odd_aplicada)
        print(usuario2.nome, "-", aposta2.palpite.value, "- Odd:", aposta2.odd_aplicada)
        print(usuario3.nome, "-", aposta3.palpite.value, "- Odd:", aposta3.odd_aplicada)

    except Exception as erro:
        print("Erro:", erro)

    finally:
        session.close()


if __name__ == "__main__":
    main()