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
    # molde (classe) usado para criar cada item vendido na loja

    # MÉTODO INICIALIZADOR
    # executa automaticamente toda vez que escrevemos Produto(...)
    # é aqui que os três atributos do objeto nascem
    def __init__(self, nome: str, categoria: str, preco: float):
        # PÚBLICO: sem underline -> pode ser lido e alterado livremente de fora
        self.nome = nome

        # PROTEGIDO: um underline -> convenção que avisa "uso interno",
        # mas o Python NÃO bloqueia o acesso externo
        self._categoria = categoria

        # PRIVADO: a linha abaixo não cria o atributo diretamente.
        # Como existe uma property chamada "preco", esta atribuição é
        # desviada para o @preco.setter, que valida antes de guardar.
        # Resultado: nenhum produto consegue nascer com preço inválido.
        self.preco = preco

    '''DECORADORES PREÇO'''

    # GETTER (leitura)
    # @property faz o método ser chamado como se fosse um atributo:
    # escrevemos p1.preco (sem parênteses) e este código roda
    @property
    def preco(self) -> float:
        # devolve o valor guardado no atributo privado
        return self.__preco

    # SETTER (escrita)
    # roda sempre que alguém faz p1.preco = algum_valor
    # é o "porteiro" do atributo: só deixa passar valor válido
    @preco.setter
    def preco(self, novo_preco: float):
        # 1ª checagem: o valor precisa ser um número.
        # bool é subclasse de int em Python, por isso True/False são recusados
        # explicitamente, senão seriam lidos como 1 e 0.
        if isinstance(novo_preco, bool) or not isinstance(novo_preco, (int, float)):
            raise ValueError("Preço inválido: o valor deve ser numérico (int ou float).")

        # 2ª checagem: regra de negócio -> preço tem de ser maior que zero.
        # raise interrompe a execução na hora; o atributo NÃO chega a ser alterado
        if novo_preco <= 0:
            raise ValueError(
                f"Preço inválido: o valor deve ser maior que zero (recebido: {novo_preco})."
            )

        # aprovado nas duas checagens: grava no atributo privado.
        # usar self.preco aqui chamaria este mesmo setter sem parar (RecursionError),
        # por isso escrevemos direto em self.__preco
        self.__preco = float(novo_preco)

    '''MÉTODOS DUNDER'''
    # métodos de nome __x__ são chamados pelo próprio Python em situações padrão

    # chamado por print(produto) e por str(produto)
    # público-alvo: o usuário final -> texto limpo e legível
    def __str__(self) -> str:
        # :.2f força a exibição com duas casas decimais (ex: 49.9 vira 49.90)
        return f"{self.nome} ({self._categoria}) - R$ {self.__preco:.2f}"

    # chamado por repr(produto) e ao inspecionar o objeto no console
    # público-alvo: o desenvolvedor -> mostra a estrutura, útil para depurar
    def __repr__(self) -> str:
        return (f"Produto(nome='{self.nome}', "
                f"categoria='{self._categoria}', "
                f"preco={self.__preco})")
