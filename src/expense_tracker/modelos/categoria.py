from enum import Enum


class Categoria(Enum):

    ALIMENTACAO = 'ALIMENTAÇÃO'
    TRANSPORTE = 'TRANSPORTE'
    LAZER = 'LAZER'
    SAUDE = 'SAÚDE'
    MORADIA = 'MORADIA'
    INVESTIMENTO = 'INVESTIMENTO'

    @classmethod
    def valido(cls, valor:str):

        return any(categoria.value == valor.strip().upper()
                   for categoria in cls)

    @classmethod
    def valores_categoria(cls):

        return [categorias.value for categorias in cls]

    @classmethod
    def de_string(cls, valor:str):

        for categoria in cls:
            if categoria.value == valor.strip().upper():
                return categoria

        raise ValueError(f"Valor informado '{valor}' não é uma categoria")