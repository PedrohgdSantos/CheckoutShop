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


# importamos as outras duas classes para poder CONFERIR os tipos recebidos
# (é isso que garante que o carrinho só trabalhe com objetos corretos)
from cliente import Cliente
from produto import Produto


class CarrinhoDeCompras:
    # classe que faz a COMPOSIÇÃO: junta um Cliente com vários Produtos

    # MÉTODO INICIALIZADOR
    # roda ao escrever CarrinhoDeCompras(cliente)
    def __init__(self, cliente: Cliente):
        # porta de entrada da composição: sem um Cliente válido não há carrinho.
        # isinstance() pergunta "este objeto é da classe Cliente?"
        if not isinstance(cliente, Cliente):
            raise ValueError("Carrinho inválido: é necessário informar uma instância de Cliente.")

        # PÚBLICO: guarda o objeto Cliente inteiro (não só o nome),
        # por isso conseguimos usar self.cliente.nome e os métodos dele depois
        self.cliente = cliente

        # PRIVADO: lista que começa vazia e vai receber os objetos Produto.
        # o duplo underline aciona o name mangling (vira _CarrinhoDeCompras__itens),
        # impedindo que alguém de fora mexa na lista sem passar pelos métodos
        self.__itens = []

    # ---------------------------------------
    # Manipulação da lista privada
    # ---------------------------------------

    # coloca um produto no carrinho
    def adicionar_produto(self, produto: Produto):
        # filtro de segurança: se entrasse um texto ou número na lista,
        # o cálculo do total quebraria ao procurar produto.preco
        if not isinstance(produto, Produto):
            raise ValueError("Item inválido: apenas instâncias de Produto podem ser adicionadas.")

        # .append() insere o objeto no fim da lista privada
        self.__itens.append(produto)

    # tira um produto do carrinho
    def remover_produto(self, produto: Produto):
        # só remove se o item realmente estiver na lista.
        # sem esse "if", o list.remove() lançaria um erro quando não encontrasse
        if produto in self.__itens:
            self.__itens.remove(produto)

    # ---------------------------------------
    # Propriedade de cálculo automático do valor
    # ---------------------------------------

    # PROPRIEDADE CALCULADA (só leitura)
    # usada como carrinho.total, sem parênteses.
    # não existe setter: o total é sempre deduzido dos itens, nunca atribuído,
    # então ele nunca fica desatualizado em relação à lista
    @property
    def total(self) -> float:
        # percorre a lista privada pegando o preco de cada produto
        # e sum() soma todos esses valores de uma vez
        return float(sum(produto.preco for produto in self.__itens))

    # ---------------------------------------
    # Exibição para o usuário
    # ---------------------------------------

    # imprime na tela um produto por linha
    def listar_itens(self):
        # caso de borda: lista vazia -> avisa em vez de não imprimir nada
        if not self.__itens:
            print("Carrinho vazio.")
            return  # encerra o método aqui

        for produto in self.__itens:
            # print() de um objeto aciona o __str__ de Produto automaticamente,
            # por isso o formato do item é definido lá e não é repetido aqui
            print(produto)

    '''MÉTODOS DUNDER'''

    # chamado por print(carrinho) -> resumo para o usuário final
    def __str__(self) -> str:
        return (f"Carrinho de {self.cliente.nome} | "     # nome vem do objeto Cliente
                f"{len(self.__itens)} item(ns) | "        # len() conta os itens da lista
                f"Total: R$ {self.total:.2f}")            # usa a propriedade calculada

    # chamado por repr(carrinho) -> visão técnica para depuração
    def __repr__(self) -> str:
        # repr(self.cliente) aciona o __repr__ da classe Cliente,
        # encaixando a representação de um objeto dentro da do outro
        return (f"CarrinhoDeCompras(cliente={repr(self.cliente)}, "
                f"total_itens={len(self.__itens)})")
