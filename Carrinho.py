#Criação da classe de carrinho

class CarrinhoDeCompras:

    #---------------------------------------
    #Propriedade de  calculo do valor automático
    #---------------------------------------
    @property
    def total(self):
        return sum(produto.preco for produto in self.__itens)\

    #---------------------------------------
    # Manipulaação da lista
    #---------------------------------------            
    def __init__(self, cliente):
        self.cliente =  cliente
        self.__itens = []

    def remove_produto(self, produto):
        if produto in  self.__itens:
            self.__itens.remove(produto)

    #---------------------------------------
    #Exibição para o usuário
    #---------------------------------------
    def listar_itens(self):
        for produto in self.__itens:
            print(produto)  #aciona Produto.__str__ de forma automatica

    def __str__(self):
        return (f"Carrinho de {self.cliente.nome} |"
                f"{len(self.__itens)} item(ns) |"
                f"Total: R$ {self.total:.2f}")

    #Utilizado para fazer depuração
    def __repr__(self):
        return  (f"CarrinhoDeCompras(cliente={repr(self.cliente)}, " 
                 f"total_itens={len(self.__itens)})")

    

    