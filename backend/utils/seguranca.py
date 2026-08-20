import hashlib


def gerar_hash_senha(senha: str) -> str:
    """
    Gera o hash da senha para evitar que ela seja salva diretamente no banco.
    """

    return hashlib.sha256(senha.encode()).hexdigest()