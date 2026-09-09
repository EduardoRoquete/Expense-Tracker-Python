import uuid
from datetime import datetime

from src.expense_tracker.modelos.categoria import Categoria


class Despesa:

    def __init__(self, descricao:str, preco:float, categoria:Categoria, data:datetime|None=None):
        self.id = uuid.uuid4()
        self.categoria = categoria
        self.__preco = 0.0
        self.descricao = descricao
        self.data = data if data is not None else datetime.now()

        self.preco = preco

    @property
    def preco(self):
        return self.__preco

    @preco.setter
    def preco(self, valor_preco:float):

        if valor_preco > 0.0:
            self.__preco = valor_preco
        else:
            raise ValueError("Só são aceitos valores positivos!")


    def para_dicionario(self):

        return {
            "id": str(self.id),
            "categoria": self.categoria.value,
            "preco": self.preco,
            "descricao": self.descricao,
            "data": self.data.isoformat()
        }

    @classmethod
    def de_dicionario(cls, dados:dict):

        despesa = cls(dados["descricao"], dados["preco"], Categoria.de_string(dados["categoria"]))
        despesa.id = uuid.UUID(dados["id"])
        despesa.data = datetime.fromisoformat(dados["data"])

        return despesa