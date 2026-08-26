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
    def __init__(self, nome: str, email: str, cpf: str, saldo_cupom: float = 0.0):
        self.nome = nome
        self._email = email
        self.__cpf = cpf
        self.__saldo_cupom = saldo_cupom

    @property
    def email(self)