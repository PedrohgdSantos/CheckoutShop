'''
Gabriel Oliveira Sampaio
João Pedro Xavier Lopes
Pedro Henrique Santos
'''

'''
Módulo responsável pela classe Produto.
Este módulo representa o item comercializado e implementa:
- Os três níveis de visibilidade (público, protegido e privado);
- Propriedade ativa preco com @property / @preco.setter;
- Validação defensiva do preço com ValueError;
- Métodos especiais __str__ e __repr__.
'''


class Produto:

    # nome        -> público    (acesso livre, sem restrição)
    # _categoria  -> protegido  (convenção de um underline: "não use fora da classe")
    # __preco     -> privado    (name mangling: vira _Produto__preco)
    def __init__(self, nome: str, categoria: str, preco: float):
        self.nome = nome
        self._categoria = categoria
        # a atribuição abaixo NÃO cria o atributo diretamente:
        # ela passa pelo @preco.setter, garantindo que nenhum produto
        # nasça com preço inválido
        self.preco = preco

    '''DECORADORES PREÇO'''

    @property
    def preco(self) -> float:
        # getter para o atributo privado __preco
        return self.__preco

    @preco.setter
    def preco(self, novo_preco: float):
        # setter com a regra de negócio: o preço deve ser estritamente positivo

        # bool é subclasse de int em Python, por isso True/False são recusados
        # explicitamente para não serem lidos como 1 e 0
        if isinstance(novo_preco, bool) or not isinstance(novo_preco, (int, float)):
            raise ValueError("Preço inválido: o valor deve ser numérico (int ou float).")

        if novo_preco <= 0:
            raise ValueError(
                f"Preço inválido: o valor deve ser maior que zero (recebido: {novo_preco})."
            )

        # armazena no atributo privado; usar self.preco aqui geraria
        # chamada infinita do próprio setter (RecursionError)
        self.__preco = float(novo_preco)

    '''MÉTODOS DUNDER'''

    # público-alvo: usuários do sistema
    def __str__(self) -> str:
        # exibição amigável: "Camiseta (Vestuário) - R$ 49.90"
        return f"{self.nome} ({self._categoria}) - R$ {self.__preco:.2f}"

    # público-alvo: desenvolvedores
    def __repr__(self) -> str:
        # representação técnica para depuração:
        # Produto(nome='Camiseta', categoria='Vestuário', preco=49.9)
        return (f"Produto(nome='{self.nome}', "
                f"categoria='{self._categoria}', "
                f"preco={self.__preco})")
