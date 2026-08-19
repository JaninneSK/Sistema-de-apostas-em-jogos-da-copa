from backend.models.usuario import Usuario
from backend.dao.aposta_dao import ApostaDAO
from backend.dao.partida_dao import PartidaDAO
from backend.dao.usuario_dao import UsuarioDAO
from backend.models.aposta import Aposta
from backend.schemas.aposta_schema import ApostaCadastroSchema
from backend.utils.enums import Palpite, StatusAposta, StatusPartida, TipoUsuario, Multiplicador
from backend.exceptions.aposta_exception import ApostaException
from backend.exceptions.partida_exception import PartidaException
from backend.exceptions.usuario_exception import UsuarioException
from backend.exceptions.permissao_exception import PermissaoException


class ApostaService:

    def __init__(self, aposta_dao: ApostaDAO, usuario_dao: UsuarioDAO, partida_dao: PartidaDAO):
        self.aposta_dao = aposta_dao
        self.usuario_dao = usuario_dao
        self.partida_dao = partida_dao
    
    def buscar_aposta(self, aposta_id: int) -> Aposta | None:
        return self.aposta_dao.buscar_por_id(aposta_id)

    def buscar_aposta_por_usuario_e_partida(self, usuario_id: int, partida_id: int) -> Aposta | None:
        return self.aposta_dao.buscar_por_usuario_e_partida(usuario_id, partida_id)

    def listar_apostas(self) -> list[Aposta]:
        return self.aposta_dao.listar()

    def listar_apostas_por_usuario(self, usuario_id: int) -> list[Aposta]:

        usuario = self.usuario_dao.buscar_por_id(usuario_id)

        if not usuario:
            raise UsuarioException("Usuário não encontrado.")

        return self.aposta_dao.listar_por_usuario(usuario_id)

    def listar_apostas_por_partida(self, partida_id: int) -> list[Aposta]:

        partida = self.partida_dao.buscar_por_id(partida_id)

        if not partida:
            raise PartidaException("Partida não encontrada.")

        return self.aposta_dao.listar_por_partida(partida_id)

    def listar_apostas_ativas(self) -> list[Aposta]:
        return self.aposta_dao.listar_ativas()

    def listar_apostas_disponiveis(self) -> list[dict]:

        partidas = self.partida_dao.listar_agendadas()

        apostas_disponiveis = []

        for partida in partidas:

            odds = self.calcular_odds(partida.id)

            apostas_disponiveis.append({
                "partida": partida,
                "odd_time_a": odds[Palpite.TIME_A],
                "odd_time_b": odds[Palpite.TIME_B]
            })

        return apostas_disponiveis

    def consultar_detalhes_partida(self, partida_id: int) -> dict:

        partida = self.partida_dao.buscar_por_id(partida_id)

        if not partida:
            raise PartidaException("Partida não encontrada.")

        quantidade_time_a = self.aposta_dao.contar_apostas_time_a(partida_id)
        quantidade_time_b = self.aposta_dao.contar_apostas_time_b(partida_id)

        odds = self.calcular_odds(partida_id)

        return {
            "partida": partida,
            "quantidade_time_a": quantidade_time_a,
            "quantidade_time_b": quantidade_time_b,
            "odd_time_a": odds[Palpite.TIME_A],
            "odd_time_b": odds[Palpite.TIME_B]
        }

    def consultar_status_aposta(self, aposta_id: int) -> StatusAposta:

        aposta = self.aposta_dao.buscar_por_id(aposta_id)

        if not aposta:
            raise ApostaException("Aposta não encontrada.")

        return aposta.status
    
    def calcular_odds(self, partida_id: int) -> dict[Palpite, float]:

        quantidade_time_a = self.aposta_dao.contar_apostas_time_a(partida_id) + 1
        quantidade_time_b = self.aposta_dao.contar_apostas_time_b(partida_id) + 1

        # Esse +1 na quantidade de cada time serve para que, quando as apostas
        # de um time ou dos dois sejam 0, o cálculo abaixo não transforme a odd
        # do time riival em 1, pois isso não seria atrativo para o usuário

        odd_time_a = 1 + (quantidade_time_b / quantidade_time_a)
        odd_time_b = 1 + (quantidade_time_a / quantidade_time_b)

        return {
            Palpite.TIME_A: round(odd_time_a, 2),
            Palpite.TIME_B: round(odd_time_b, 2)
        }
    
    def consultar_odds(self, partida_id: int) -> dict[Palpite, float]:

        partida = self.partida_dao.buscar_por_id(partida_id)

        if not partida:
            raise PartidaException("Partida não encontrada.")

        if partida.status != StatusPartida.AGENDADA:
            raise PartidaException("As apostas desta partida não estão disponíveis.")

        return self.calcular_odds(partida_id)

    def registrar_aposta(self, usuario_id: int, dados: ApostaCadastroSchema) -> Aposta:

        usuario = self.usuario_dao.buscar_por_id(usuario_id)

        if not usuario:
            raise UsuarioException("Usuário não encontrado.")

        if not usuario.ativo:
            raise PermissaoException("Usuário inativo não pode realizar apostas.")

        if usuario.tipo == TipoUsuario.ADMIN:
            raise PermissaoException("Administrador não pode realizar apostas.")

        partida = self.partida_dao.buscar_por_id(dados.partida_id)

        if not partida:
            raise PartidaException("Partida não encontrada.")

        if partida.status != StatusPartida.AGENDADA:
            raise PartidaException("Só é possível apostar em partidas agendadas.")

        aposta_existente = self.aposta_dao.buscar_por_usuario_e_partida(
            usuario_id,
            dados.partida_id
        )

        if aposta_existente:
            raise ApostaException(
                "O usuário já realizou uma aposta nesta partida."
            )

        multiplicador = Multiplicador.X1.value
        valor_total = dados.valor_apostado

        if valor_total > usuario.pontos:
            raise ApostaException(
                "O usuário não possui pontos suficientes para realizar essa aposta."
            )

        odds = self.calcular_odds(dados.partida_id)
        odd_aplicada = odds[dados.palpite]

        aposta = Aposta(
            usuario_id=usuario_id,
            partida_id=dados.partida_id,
            valor_apostado=dados.valor_apostado,
            odd_aplicada=odd_aplicada,
            multiplicador=multiplicador,
            palpite=dados.palpite,
            status=StatusAposta.ATIVA,
            acertou=None,
            pontos_ganhos=0
        )

        usuario.pontos -= valor_total
        self.usuario_dao.atualizar(usuario)

        return self.aposta_dao.salvar(aposta)

    def multiplicar_aposta(self, usuario_id: int, aposta_id: int, novo_multiplicador: Multiplicador) -> Aposta:

        aposta = self.aposta_dao.buscar_por_id(aposta_id)

        if not aposta:
            raise ApostaException("Aposta não encontrada.")

        if aposta.usuario_id != usuario_id:
            raise PermissaoException("Essa aposta não pertence ao usuário.")

        if aposta.status != StatusAposta.ATIVA:
            raise ApostaException("Só é possível multiplicar uma aposta ativa.")

        partida = self.partida_dao.buscar_por_id(aposta.partida_id)

        if not partida:
            raise PartidaException("Partida não encontrada.")

        if partida.status != StatusPartida.AGENDADA:
            raise PartidaException(
                "Não é possível multiplicar a aposta após o início da partida."
            )

        multiplicador_atual = aposta.multiplicador
        multiplicador_novo = novo_multiplicador.value

        if multiplicador_novo <= multiplicador_atual:
            raise ApostaException(
                "O novo multiplicador deve ser maior que o atual."
            )

        usuario = self.usuario_dao.buscar_por_id(usuario_id)

        if not usuario:
            raise UsuarioException("Usuário não encontrado.")

        valor_adicional = aposta.valor_apostado * (
            multiplicador_novo - multiplicador_atual
        )

        if valor_adicional > usuario.pontos:
            raise ApostaException(
                "O usuário não possui pontos suficientes para multiplicar essa aposta."
            )

        usuario.pontos -= valor_adicional
        aposta.multiplicador = multiplicador_novo

        self.usuario_dao.atualizar(usuario)

        return self.aposta_dao.atualizar(aposta)
    
    def identificar_vencedor(self, partida_id: int) -> Palpite | None:

        partida = self.partida_dao.buscar_por_id(partida_id)

        if not partida:
            raise PartidaException("Partida não encontrada.")

        if partida.status != StatusPartida.FINALIZADA:
            raise PartidaException("A partida ainda não foi finalizada.")

        if partida.placar_time_a is None or partida.placar_time_b is None:
            raise PartidaException("O placar da partida não foi informado.")

        if partida.placar_time_a > partida.placar_time_b:
            return Palpite.TIME_A

        if partida.placar_time_b > partida.placar_time_a:
            return Palpite.TIME_B

        return None

    def calcular_retorno(self, aposta: Aposta) -> int:

        valor_total_apostado = aposta.valor_apostado * aposta.multiplicador
        retorno = valor_total_apostado * aposta.odd_aplicada

        return round(retorno)


    def encerrar_apostas_da_partida(self, partida_id: int) -> list[Aposta]:

        partida = self.partida_dao.buscar_por_id(partida_id)

        if not partida:
            raise PartidaException("Partida não encontrada.")

        if partida.status != StatusPartida.FINALIZADA:
            raise PartidaException("A partida ainda não foi finalizada.")

        vencedor = self.identificar_vencedor(partida_id)
        apostas = self.aposta_dao.listar_por_partida(partida_id)

        for aposta in apostas:

            if aposta.status != StatusAposta.ATIVA:
                continue

            usuario = self.usuario_dao.buscar_por_id(aposta.usuario_id)

            if not usuario:
                raise UsuarioException(f"Usuário da aposta {aposta.id} não encontrado.")

            valor_total_apostado = aposta.valor_apostado * aposta.multiplicador

            if vencedor is None:
                aposta.acertou = None
                aposta.status = StatusAposta.EMPATADA
                aposta.pontos_ganhos = valor_total_apostado

                usuario.pontos += valor_total_apostado

            elif aposta.palpite == vencedor:
                retorno = self.calcular_retorno(aposta)

                aposta.acertou = True
                aposta.status = StatusAposta.GANHA
                aposta.pontos_ganhos = retorno

                usuario.pontos += retorno
                usuario.quantidade_acertos += 1

            else:
                aposta.acertou = False
                aposta.status = StatusAposta.PERDIDA
                aposta.pontos_ganhos = 0

            self.aposta_dao.atualizar(aposta)
            self._verificar_inativacao_usuario(usuario)
            self.usuario_dao.atualizar(usuario)

        return apostas
    
    def _verificar_inativacao_usuario(self, usuario: Usuario) -> None:

        possui_aposta_ativa = self.aposta_dao.possui_aposta_ativa(usuario.id)

        if usuario.pontos == 0 and not possui_aposta_ativa:
            usuario.ativo = False