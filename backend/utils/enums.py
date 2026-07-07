from enum import Enum


class TipoUsuario(Enum):
    USUARIO = "USUARIO"
    ADMIN = "ADMIN"


class StatusPartida(Enum):
    AGENDADA = "AGENDADA"
    EM_ANDAMENTO = "EM_ANDAMENTO"
    FINALIZADA = "FINALIZADA"


class StatusAposta(Enum):
    ATIVA = "ATIVA"
    GANHA = "GANHA"
    PERDIDA = "PERDIDA"
    ENCERRADA = "ENCERRADA"


class Palpite(Enum):
    TIME_A = "TIME_A"
    TIME_B = "TIME_B"