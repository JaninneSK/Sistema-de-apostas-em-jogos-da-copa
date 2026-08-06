import re
from datetime import date

TAMANHO_MINIMO_SENHA = 8
IDADE_MINIMA = 18

def validar_senha(senha: str) -> bool:

    if len(senha) < TAMANHO_MINIMO_SENHA:
        return False

    if not re.search(r"[A-Z]", senha):
        return False

    if not re.search(r"[a-z]", senha):
        return False

    if not re.search(r"\d", senha):
        return False

    if not re.search(r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>/?]", senha):
        return False

    return True


def validar_cpf(cpf: str) -> bool:

    return (
        cpf.isdigit()
        and len(cpf) == 11
    )


def validar_idade(data_nascimento: date, idade_minima: int = IDADE_MINIMA) -> bool:

    hoje = date.today()

    idade = (hoje.year - data_nascimento.year)

    if (hoje.month, hoje.day) < (data_nascimento.month, data_nascimento.day):
        idade -= 1

    return idade >= idade_minima

