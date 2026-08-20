import re
from datetime import date


TAMANHO_MINIMO_SENHA = 8
IDADE_MINIMA = 18


def validar_senha(senha: str) -> bool:
    """
    Verifica se a senha possui o tamanho mínimo e todos os tipos de
    caracteres exigidos pelo sistema.
    """

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
    """
    Verifica se o CPF possui somente números e exatamente 11 dígitos.
    """

    return (
        cpf.isdigit()
        and len(cpf) == 11
    )


def validar_idade(data_nascimento: date, idade_minima: int = IDADE_MINIMA) -> bool:
    """
    Calcula a idade do usuário e verifica se ele possui a idade mínima
    exigida para participar do sistema.
    """

    hoje = date.today()

    idade = (hoje.year - data_nascimento.year)

    # Se o aniversário ainda não aconteceu neste ano, é retirado um ano
    # da idade calculada inicialmente
    if (hoje.month, hoje.day) < (data_nascimento.month, data_nascimento.day):
        idade -= 1

    return idade >= idade_minima