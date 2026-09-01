# main.py -- script de homologacao (roteiro item 3)
#
# Gabriel Oliveira Sampaio
# Joao Pedro Xavier Lopes
# Pedro Henrique Santos
#
# Este arquivo NAO e a loja: e o roteiro de testes que comprova, em 4 etapas,
# que os tres modulos funcionam. Por isso a execucao e automatica e sempre
# produz o mesmo resultado (nao pede nada digitado).

# importa cada classe do seu proprio modulo (arquivos separados)
from produto import Produto
from cliente import Cliente
from carrinho import CarrinhoDeCompras

# =====================================================================
# PASSO 1 - Instanciacao e inspecao de representacao (__str__ / __repr__)
# Objetivo: provar que os objetos nascem corretos e se exibem como o esperado
# =====================================================================
print("=" * 70)
print("PASSO 1: INSTANCIACAO E REPRESENTACAO (__str__ / __repr__)")
print("=" * 70)

# cria 3 objetos Produto; cada preco passa pelo @preco.setter antes de ser aceito
p1 = Produto("Camiseta", "Vestuario", 49.90)
p2 = Produto("Tenis", "Calcados", 199.90)
p3 = Produto("Bone", "Acessorios", 125.00)

# cria 1 objeto Cliente; o e-mail e o CPF passam pelos setters da classe.
# CPF valido segundo o algoritmo dos digitos verificadores (DV1=3, DV2=5)
cliente1 = Cliente("Maria Silva", "maria@email.com", "111.444.777-35")

# percorre os 4 objetos mostrando as duas representacoes de cada um
for obj in (p1, p2, p3, cliente1):
    print(f"  str  -> {obj}")        # aciona __str__ (versao para o usuario)
    print(f"  repr -> {repr(obj)}")  # aciona __repr__ (versao para o dev)
    print("  " + "-" * 66)

# =====================================================================
# PASSO 2 - Validacoes e captura de excecoes (ValueError)
# Objetivo: provar que dados invalidos sao recusados pelos setters.
# O padrao try/except repete a mesma ideia: tentamos algo proibido e
# capturamos o erro, para o programa continuar rodando em vez de parar.
# =====================================================================
print()
print("=" * 70)
print("PASSO 2: VALIDACOES E CAPTURA DE ValueError")
print("=" * 70)

# 2.1 - preco negativo e preco nulo: a regra exige preco > 0
for preco_invalido in (-10.0, 0):
    try:
        p1.preco = preco_invalido        # tentativa proibida -> dispara ValueError
    except ValueError as e:
        print(f"  [OK] preco = {preco_invalido} recusado -> {e}")

# 2.2 - CPF: curto demais, com letras, com digito verificador errado
# e sequencia de digitos identicos (cada caso cai numa etapa diferente da validacao)
for cpf_invalido in ("1234", "abc.def.ghi-jk", "111.444.777-99", "111.111.111-11"):
    try:
        cliente1.cpf = cpf_invalido
    except ValueError as e:
        print(f"  [OK] cpf = '{cpf_invalido}' recusado -> {e}")

# 2.3 - e-mail: sem '@', sem texto antes do '@' e sem texto depois do '@'
for email_invalido in ("sememail.com", "@email.com", "maria@"):
    try:
        cliente1.email = email_invalido
    except ValueError as e:
        print(f"  [OK] email = '{email_invalido}' recusado -> {e}")

# 2.4 - cupom com valor negativo: o metodo tradicional exige valor > 0
try:
    cliente1.adicionar_cupom(-5.0)
except ValueError as e:
    print(f"  [OK] cupom = -5.0 recusado -> {e}")

# conferencia final do passo: os objetos continuam com os valores originais,
# ou seja, nenhuma tentativa invalida conseguiu corromper o estado interno
print(f"  Estado preservado: {repr(p1)}")
print(f"  Estado preservado: {repr(cliente1)}")

# =====================================================================
# PASSO 3 - Modificadores de visibilidade e name mangling
# Objetivo: mostrar na pratica a diferenca entre privado e protegido
# =====================================================================
print()
print("=" * 70)
print("PASSO 3: VISIBILIDADE E NAME MANGLING")
print("=" * 70)

# 3.1 - ATRIBUTOS PRIVADOS (dois underlines)
# o Python renomeia __preco para _Produto__preco e __cpf para _Cliente__cpf.
# Como o nome original deixa de existir fora da classe, o acesso direto
# levanta AttributeError -- que capturamos abaixo para exibir a prova.
try:
    print(p1.__preco)
except AttributeError as e:
    print(f"  [OK] p1.__preco bloqueado -> {e}")

try:
    print(cliente1.__cpf)
except AttributeError as e:
    print(f"  [OK] cliente1.__cpf bloqueado -> {e}")

# o dado continua disponivel pelo caminho correto: a property e o getter
print(f"  Via property: p1.preco = {p1.preco}")
print(f"  Via property: cliente1.cpf = {cliente1.cpf}")

# 3.2 - ATRIBUTO PROTEGIDO (um underline): o acesso funciona normalmente.
# O underline unico (_categoria) e apenas uma CONVENCAO entre programadores,
# nao um mecanismo da linguagem: o interpretador nao renomeia nem bloqueia o
# nome, entao a sintaxe e valida mesmo violando a boa pratica de encapsulamento.
print(f"  Protegido (acessivel por convencao): p1._categoria = {p1._categoria}")

# =====================================================================
# PASSO 4 - Fluxo do carrinho e composicao
# Objetivo: mostrar objetos cooperando -- o carrinho usa Cliente e Produto
# =====================================================================
print()
print("=" * 70)
print("PASSO 4: FLUXO DO CARRINHO (COMPOSICAO)")
print("=" * 70)

# COMPOSICAO: o carrinho recebe o objeto Cliente inteiro dentro de si
carrinho = CarrinhoDeCompras(cliente1)

# guarda os 3 objetos Produto na lista privada __itens
carrinho.adicionar_produto(p1)
carrinho.adicionar_produto(p2)
carrinho.adicionar_produto(p3)

print("  Itens do carrinho:")
carrinho.listar_itens()  # imprime item por item usando o __str__ de Produto

# leitura da propriedade calculada: soma os precos na hora da consulta
print(f"  Total (@property): R$ {carrinho.total:.2f}")

# prova de que o total nao e um valor fixo guardado, e sim recalculado:
# ao remover e devolver um item, ele acompanha a mudanca sozinho
carrinho.remover_produto(p3)
print(f"  Apos remover '{p3.nome}': R$ {carrinho.total:.2f}")
carrinho.adicionar_produto(p3)
print(f"  Apos devolver '{p3.nome}': R$ {carrinho.total:.2f}")

print(f"  str  -> {carrinho}")        # resumo do carrinho
print(f"  repr -> {repr(carrinho)}")  # repr do carrinho contendo o repr do cliente

# ENCAPSULAMENTO TRADICIONAL: saldo de cupons acessado por metodos, nao por property
print()
print("  Cupons do cliente:")
print(f"    Saldo inicial: R$ {cliente1.get_saldo_cupom():.2f}")  # getter tradicional

cliente1.adicionar_cupom(10.0)   # cada chamada SOMA ao saldo (+=), nao substitui
cliente1.adicionar_cupom(15.50)
print(f"    Saldo acumulado: R$ {cliente1.get_saldo_cupom():.2f}")

# USO do saldo: o cupom abate do total do carrinho.
# max(..., 0.0) evita que a conta fique negativa se o cupom for maior que a compra
total_com_desconto = max(carrinho.total - cliente1.get_saldo_cupom(), 0.0)
print(f"    Total do carrinho:  R$ {carrinho.total:.2f}")
print(f"    Desconto (cupons): -R$ {cliente1.get_saldo_cupom():.2f}")
print(f"    Valor a pagar:      R$ {total_com_desconto:.2f}")

print()
print("=" * 70)
print("HOMOLOGACAO CONCLUIDA COM SUCESSO")
print("=" * 70)
