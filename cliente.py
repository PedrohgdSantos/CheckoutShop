'''
Gabriel Oliveira Sampaio
João Pedro Xavier Lopes
Pedro Henrique Santos
'''

'''
Módulo responsável pela classe Cliente.
Este módulo representa o comprador do sistema e implementa:
- Encapsulamento de atributos;
- Validação de e-mail;
- Validação completa de CPF;
- Controle de saldo de cupons;
- Métodos getters/setters;
- Métodos especiais __str__ e __repr__.
'''


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

    '''DECORADORES EMAIL'''

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

    '''DECORADORES CPF'''

    @property
    def cpf(self) -> str:
        # Getter para o atributo privado __cpf.
        return self.__cpf

    @cpf.setter
    def cpf(self, valor: str):
        # setter para o algoritmo de validação do CPF

        # condição que avalia se o dado recebido NÃO é uma string no formato 999.999.999-99
        # not isinstance valida se não é uma string
        # not re.match valida se não está coerente ao formato necessário,
        # testa o texto na Expressão Regular (Regex), se não corresponder ao padrão,
        # o método re.match() retorna None, o not inverte o None para True, acionando a exceção
        if not isinstance(valor, str) or not re.match(
            # ^ garante que a verificação começe do primeiro caractere
            # \d{3} exige exatamente 3 dígitos numéricos (0-9)
            # \. exige um ponto literal (A barra \ cancela o significado especial do ponto na Regex)
            # \d{3}\.: Exige mais 3 dígitos e outro ponto
            # \d{3}: Exige mais 3 dígitos
            # -: Exige um hífen literal
            # \d{2}: Exige exatamente 2 dígitos finais
            # $: Fim da string. Impede que o usuário insira caracteres extras no final do texto (ex: "123.456.789-01123")
            r"^\d{3}\.\d{3}\.\d{3}-\d{2}$", valor):
                raise ValueError(
                    "CPF inválido: formato deve ser '999.999.999-99' com 14 caracteres."
                )

        # extração de apenas os caracteres numéricos, feita com List Comprehension

        # for c in valor: percorre a string valor caractere por caractere 
        # a cada passada do loop a variável c recebe um caractere, ex: 123.456.789-01,
        # recebe 1, depois 2, depois 3, depois .

        # if c.isdigit(): o método retorna True apenas para números de 0 a 9, 
        # descartando símbolos e pontos como . e -

        # int(c): transforma cada caractere numérico aprovado pelo filtro (que até então era uma string '1'), 
        # em um tipo numérico inteiro (1), pois retornam True
        # os símbolos como . e - retornam False e são descartados da montagem da lista
        # ex: 123.456.789-01 -> digitos: [1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1] 
        digitos = [int(c) for c in valor if c.isdigit()]

        # rejeição de sequências com dígitos repetidos (ex: '111.111.111-11')
        if len(set(digitos)) == 1:
            raise ValueError("CPF inválido: não é permitida sequência de dígitos idênticos.")

        # etapas de validação matemática dos 2 últimos números do CPF (DV)
        # a comparação é necessária para comprovar se a sequência segue as regras da Receita Federal

        # cálculo do primeiro dígito verificador (DV1), o 10º número da string do CPF (digitos), (digitos[9])
        # multiplicação regressiva: utiliza os primeiros 9 dígitos do CPF,
        # multiplicando-os por pesos decrescentes de 10 a 2 (10 - i)
        # obtenção de resto: multiplica a soma acumulada por 10 e 
        # extrai o resto da divisão por 11 (% 11)
        # regra da borda: se o resto for igual a 10, a regra determina que o DV1 esperado é 0, se não o próprio resto é assumido
        # checagem: Compara o resultado calculado com o dígito gravado na posição digitos[9], 
        # se forem diferentes, o código interrompe a execução com um ValueError
        soma1 = sum(digitos[i] * (10 - i) for i in range(9))
        resto1 = (soma1 * 10) % 11
        dv1_esperado = 0 if resto1 == 10 else resto1

        if digitos[9] != dv1_esperado:
            raise ValueError(
                "CPF inválido: primeiro dígito verificador incorreto."
            )  #[cite: 1]

        # cálculo do segundo dígito verificador (DV1), o 11º número da string do CPF (digitos), (digitos[9])
        # inclusão do DV1: Repete a lógica de soma, porém agora incluindo 10 dígitos (os 9 base + o primeiro dígito verificador)
        # pesos ajustados: Devido ao elemento extra, as multiplicações passam a usar pesos decrescentes de 11 a 2 (11 - i)
        # obtenção do resto e validação: aplica a mesma fórmula (soma2 * 10) % 11 e compara o dv2_esperado com digitos[10], 
        # se não coincidirem, lança a exceção.
        soma2 = sum(digitos[i] * (11 - i) for i in range(10))
        resto2 = (soma2 * 10) % 11
        dv2_esperado = 0 if resto2 == 10 else resto2

        if digitos[10] != dv2_esperado:
            raise ValueError(
                "CPF inválido: segundo dígito verificador incorreto."
            )

        # atributo privado só é lançado se a string tiver sucesso com a máscara, filtragem de dígitos idênticos e
        # as checagens de DV, o valor validado é armazenado no atributo privado __cpf utilizando a convenção com duplo underline.
        self.__cpf = valor

    ''' ENCAPSULAMENTO TRADICIONAL '''

    def get_saldo_cupom(self) -> float:
        """Getter tradicional para retorno do saldo privado de cupons."""
        return self.__saldo_cupom

    def adicionar_cupom(self, valor: float):
        """Método para adicionar saldo de cupom, garantindo que o valor seja maior que zero."""
        if valor <= 0:
            raise ValueError(
                "O valor do cupom deve ser estritamente maior que zero."
            )
        self.__saldo_cupom += valor

    '''MÉTODOS DUNDER'''

    def __str__(self) -> str:
        """Retorna resumo amigável formatando o CPF sem pontuação conforme especificação."""
        # Remove os pontos e o hífen para corresponder ao retorno esperado: "12345678901"[cite: 1]
        cpf_limpo = "".join(c for c in self.__cpf if c.isdigit())
        return f"Cliente: {self.nome} | CPF: {cpf_limpo}"

    def __repr__(self) -> str:
        """Retorna representação técnica do objeto para depuração."""
        return f"Cliente(nome='{self.nome}', email='{self._email}', cpf='{self.__cpf}')"  #[cite: 1]