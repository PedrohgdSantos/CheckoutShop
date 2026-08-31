class Produto:
    def __init__(self, nome: str, categoria: str, preco: float):
        self.nome = nome
        self._categoria = categoria
        self.__preco = preco

    def __str__(self):
        formato = f'{self.nome} ({self._categoria}) - R$ {self.__preco:.2f}'
        return formato

    def __repr__(self):
        formato = f'Produto(\n' + \
                f'  nome: {self.nome}, \n' + \
                f'  categoria: {self._categoria}, \n' + \
                f'  preco: {self.__preco:.2f}\n)'
        return formato

    @property
    def preco(self) -> float:
        return self.__preco

    @preco.setter
    def preco(self, novo_preco: float):
        if novo_preco > 0:
            self.__preco = novo_preco
        else:
            raise ValueError("O preço não pode ser negativo.")