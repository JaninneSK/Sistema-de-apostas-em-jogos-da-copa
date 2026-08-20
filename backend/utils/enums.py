from enum import Enum


class TipoUsuario(str, Enum):
    """
    Define os tipos de usuário existentes no sistema.
    """

    USUARIO = "USUARIO"
    ADMIN = "ADMIN"


class StatusPartida(str, Enum):
    """
    Define os possíveis estados de uma partida no sistema.
    """

    AGENDADA = "AGENDADA"
    EM_ANDAMENTO = "EM_ANDAMENTO"
    FINALIZADA = "FINALIZADA"


class StatusAposta(str, Enum):
    """
    Define os possíveis estados de uma aposta.
    """

    ATIVA = "ATIVA"
    GANHA = "GANHA"
    PERDIDA = "PERDIDA"
    EMPATADA = "EMPATADA"


class Palpite(str, Enum):
    """
    Define em qual dos dois times da partida o usuário apostou.
    """

    TIME_A = "TIME_A"
    TIME_B = "TIME_B"


class Multiplicador(int, Enum):
    """
    Define os multiplicadores disponíveis para aumentar o valor de uma aposta.
    """

    X1 = 1
    X2 = 2
    X3 = 3
    X4 = 4
    X5 = 5
    X10 = 10
    X50 = 50
    X100 = 100
    X1000 = 1000