from enum import Enum


class TipoUsuario(str, Enum):
    USUARIO = "USUARIO"
    ADMIN = "ADMIN"


class StatusPartida(str, Enum):
    AGENDADA = "AGENDADA"
    EM_ANDAMENTO = "EM_ANDAMENTO"
    FINALIZADA = "FINALIZADA"


class StatusAposta(str, Enum):
    ATIVA = "ATIVA"
    GANHA = "GANHA"
    PERDIDA = "PERDIDA"
    EMPATADA = "EMPATADA"


class Palpite(str, Enum):
    TIME_A = "TIME_A"
    TIME_B = "TIME_B"


class Multiplicador(int, Enum):
    X1 = 1
    X2 = 2
    X3 = 3
    X4 = 4
    X5 = 5
    X10 = 10
    X50 = 50
    X100 = 100
    X1000 = 1000