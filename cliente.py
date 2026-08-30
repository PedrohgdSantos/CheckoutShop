'''
Gabriel Oliveira Sampaio
João Pedro Xavier Lopes
Pedro Henrique Santos
'''


"""
Módulo responsável pela classe Cliente.

Este módulo representa o comprador do sistema e implementa:
- Encapsulamento de atributos;
- Validação de e-mail;
- Validação completa de CPF;
- Controle de saldo de cupons;
- Métodos getters/setters;
- Métodos especiais __str__ e __repr__.
"""

import re

class Cliente:

    # modelagem do comprador e validação dos seus dados cadastrais
    # atributos estão sem restrição de visibilidade pois serão definidas nos métodos

    # __saldo_cupom foi definido com restrição diretamente no método inicializador pois não possui método setter,
    # isso ocorreu porque um setter permitiria atribuir um valor direto utilizando o sinal = 
    # ex: cliente.saldo_cupom = 20.0), isso sobrescreveria qualquer saldo acumulado pelo cliente
    # na prática de sistemas, saldos não devem ser substituídos diretamente, mas sim incrementados via transação,
    # fato que acontecerá por meio do método adicionar_cupom(valor) que força a regra somar (+=) ao saldo anterior e impede depósitos inválidos
    # também foi requisito do roteiro realizar dessa forma
    def __init__(self, nome: str, email: str, cpf: str):
        self.nome = nome
        self.email = email
        self.cpf = cpf
        self.__saldo_cupom = 0.0

    @property
    def email(self):

        # getter para o atributo email
        return self._email

    @email.setter
    def email(self, valor: str):

    # setter que exige texto antes e depois de @
        if not isinstance(valor, str) or "@" not in valor:
                raise ValueError("E-mail inválido: o endereço deve conter o caractere '@'.")
        
        partes = valor.split("@")
        # verifica se o e-mail digitado é valido
        # garante que existe exatamente uma parte antes e outra depois do @ e que nenhuma delas é vazia
        # divide uma string em uma lista com 2 valores, utilizando @ como separador
        # exemplo: Se valor = "jorge@email.com", a variável partes será: ["jorge", "email.com"]
        # or not = se não existe. Se a primeira parte (antes do @) ou a segunda parte (depois do @) for vazia, o e-mail é inválido
        # .strip() remove todos os espaços em branco do início e do fim de uma string.
        if len(partes) != 2 or not partes[0].strip() or not partes[1].strip():
             raise ValueError(
                "E-mail inválido: deve haver texto antes e depois do caractere '@'."
            )

        # utilizado _email e não email para não causar loop (RecursionError), 
        # pois senão o método @email.setter seria chamado infinitas vezes
        self._email = valor


    @property
    def cpf(self) -> str:
        # Getter para o atributo privado __cpf.
        return self.__cpf