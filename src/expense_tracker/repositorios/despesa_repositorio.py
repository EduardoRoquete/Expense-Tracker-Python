import json
from pathlib import Path
from uuid import UUID

from src.expense_tracker.modelos.despesa import Despesa


class DespesaRepositorio:

    def __init__(self, caminho_arquivo:str):
        raiz_src = Path(__file__).resolve().parent.parent
        self._caminho_arquivo = raiz_src / caminho_arquivo
        self._despesas = self.carregar_lista_de_despesa()

    def _garantir_arquivo(self):

        if not self._caminho_arquivo.exists():
            self._caminho_arquivo.parent.mkdir(parents=True, exist_ok=True)
            self._caminho_arquivo.write_text("[]", encoding="utf-8")

    def carregar_lista_de_despesa(self):

        self._garantir_arquivo()

        try:
            with open(self._caminho_arquivo, "r", encoding="utf-8") as arquivo:
                if arquivo.read().strip() == "":
                    return []

                arquivo.seek(0)
                dados_despesas = json.load(arquivo)

                return [
                    Despesa.de_dicionario(dado)
                    for dado in dados_despesas
                ]
        except (json.JSONDecodeError, OSError, KeyError, ValueError) as erro:
            raise ValueError(
                f"Não foi possível carregar as despesas: arquivo de dados corrompido ou incompatíveis ({erro}).")

    def salvar_lista_de_despesas(self, lista_de_despesas:list[Despesa]):
        self._garantir_arquivo()

        dados_despesas = []
        for despesa in lista_de_despesas:
            dados_despesas.append(despesa.para_dicionario())

        with open(self._caminho_arquivo, "w", encoding="utf-8") as arquivo:
            json.dump(dados_despesas, arquivo, ensure_ascii=False, indent=4)

    def adicionar(self, despesa:Despesa):

        todas_despesas = self._despesas
        todas_despesas.append(despesa)
        self.salvar_lista_de_despesas(todas_despesas)

    def buscar_por_id(self, valor_id:UUID):

        todas_despesas = self._despesas

        for despesa in todas_despesas:
            if despesa.id == valor_id:
                return despesa

        return None

    def remover_por_id(self, valor_id:UUID):

        todas_despesas = self._despesas

        for despesa in todas_despesas:
            if despesa.id == valor_id:
                todas_despesas.remove(despesa)
                self.salvar_lista_de_despesas(todas_despesas)
                return True

        return False

    def atualizar(self, valor_id:UUID, nova_despesa:Despesa):

        todas_despesas = self._despesas

        for indice, despesa in enumerate(todas_despesas):
            if despesa.id == valor_id:
                todas_despesas[indice] = nova_despesa
                self.salvar_lista_de_despesas(todas_despesas)
                return True

        return False

