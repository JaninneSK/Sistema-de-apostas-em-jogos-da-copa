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
    ENCERRADA = "ENCERRADA"


class Palpite(str, Enum):
    TIME_A = "TIME_A"
    TIME_B = "TIME_B"