'''
Gabriel Oliveira Sampaio
João Pedro Xavier Lopes
Pedro Henrique Santos
'''

'''
Módulo responsável pela classe CarrinhoDeCompras.
Este módulo faz a composição do sistema e implementa:
- Associação entre um Cliente e sua lista privada de Produtos;
- Métodos de manipulação da lista (adicionar/remover);
- Propriedade calculada total;
- Método de listagem dos itens;
- Métodos especiais __str__ e __repr__.
'''


from cliente import Cliente
from produto import Produto


class CarrinhoDeCompras:

    # cliente -> público  (instância válida da classe Cliente)
    # __itens -> privado  (lista de objetos Produto, protegida por name mangling)
    def __init__(self, cliente: Cliente):
        # composição: o carrinho só existe associado a um cliente válido
        if not isinstance(cliente, Cliente):
            raise ValueError("Carrinho inválido: é necessário informar uma instância de Cliente.")

        self.cliente = cliente
        self.__itens = []

    # ---------------------------------------
    # Manipulação da lista privada
    # ---------------------------------------
    def adicionar_produto(self, produto: Produto):
        # aceita somente objetos Produto para não corromper o cálculo do total
        if not isinstance(produto, Produto):
            raise ValueError("Item inválido: apenas instâncias de Produto podem ser adicionadas.")

        self.__itens.append(produto)

    def remover_produto(self, produto: Produto):
        # remove a instância indicada apenas se ela estiver na lista,
        # evitando o ValueError nativo do list.remove()
        if produto in self.__itens:
            self.__itens.remove(produto)

    # ---------------------------------------
    # Propriedade de cálculo automático do valor
    # ---------------------------------------
    @property
    def total(self) -> float:
        # percorre a lista privada e soma o preço de cada produto;
        # não há setter, pois o total é derivado dos itens e nunca atribuído
        return float(sum(produto.preco for produto in self.__itens))

    # ---------------------------------------
    # Exibição para o usuário
    # ---------------------------------------
    def listar_itens(self):
        if not self.__itens:
            print("Carrinho vazio.")
            return

        for produto in self.__itens:
            print(produto)  # aciona Produto.__str__ automaticamente

    '''MÉTODOS DUNDER'''

    # público-alvo: usuários do sistema
    def __str__(self) -> str:
        # "Carrinho de Maria Silva | 3 item(ns) | Total: R$ 374.80"
        return (f"Carrinho de {self.cliente.nome} | "
                f"{len(self.__itens)} item(ns) | "
                f"Total: R$ {self.total:.2f}")

    # público-alvo: desenvolvedores
    def __repr__(self) -> str:
        # aciona Cliente.__repr__ dentro da própria representação do carrinho
        return (f"CarrinhoDeCompras(cliente={repr(self.cliente)}, "
                f"total_itens={len(self.__itens)})")
