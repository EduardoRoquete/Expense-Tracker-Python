from uuid import UUID

from src.expense_tracker.modelos.categoria import Categoria
from src.expense_tracker.modelos.despesa import Despesa
from src.expense_tracker.repositorios.despesa_repositorio import DespesaRepositorio


class DespesaServico:

    def __init__(self, instancia_repositorio:DespesaRepositorio):
        self.repositorio = instancia_repositorio

    def adicionar_despesa(self, descricao:str, preco:float, categoria:Categoria) -> Despesa:

        despesa_para_adicionar = Despesa(descricao, preco, categoria)
        self.repositorio.adicionar(despesa_para_adicionar)
        return despesa_para_adicionar

    def listar_todas_despesas(self) -> list[Despesa]:

        todas_despesas = self.repositorio.carregar_lista_de_despesa()
        return todas_despesas

    def atualizar_despesa(self, id_para_busca:UUID, nova_descricao:str|None, novo_preco:float|None, nova_categoria:Categoria|None):

        despesa = self.repositorio.buscar_por_id(id_para_busca)

        if despesa is None:
            return False

        if novo_preco is not None:
            despesa.preco = novo_preco

        if nova_descricao is not None:
            despesa.descricao = nova_descricao

        if nova_categoria is not None:
            despesa.categoria = nova_categoria

        self.repositorio.atualizar(id_para_busca, despesa)

        return True

    def remover_despesa(self, id_para_busca:UUID):

        return self.repositorio.remover_por_id(id_para_busca)

    def total_gasto(self):

        total_gasto = 0.0
        todas_despesas = self.listar_todas_despesas()

        for despesa in todas_despesas:
            total_gasto += despesa.preco

        return total_gasto

    def total_gasto_por_mes(self, mes:int, ano:int):

        total_gasto_por_mes = 0.0
        todas_despesas = self.listar_todas_despesas()

        for despesa in todas_despesas:
            if despesa.data.year == ano and despesa.data.month == mes:
                total_gasto_por_mes += despesa.preco

        return total_gasto_por_mes

    def total_gasto_por_categoria(self):

        relacao_categoria_gasto = {}

        todas_despesas = self.listar_todas_despesas()

        for despesa in todas_despesas:
            categoria = despesa.categoria
            if categoria in  relacao_categoria_gasto:
                relacao_categoria_gasto[categoria] += despesa.preco
            else:
                relacao_categoria_gasto[categoria] = despesa.preco

        return relacao_categoria_gasto