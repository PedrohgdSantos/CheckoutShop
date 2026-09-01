# main.py -- script de homologacao (roteiro item 3)
#
# Gabriel Oliveira Sampaio
# Joao Pedro Xavier Lopes
# Pedro Henrique Santos

from produto import Produto
from cliente import Cliente
from carrinho import CarrinhoDeCompras

# =====================================================================
# PASSO 1 - Instanciacao e inspecao de representacao (__str__ / __repr__)
# =====================================================================
print("=" * 70)
print("PASSO 1: INSTANCIACAO E REPRESENTACAO (__str__ / __repr__)")
print("=" * 70)

p1 = Produto("Camiseta", "Vestuario", 49.90)
p2 = Produto("Tenis", "Calcados", 199.90)
p3 = Produto("Bone", "Acessorios", 125.00)

# CPF valido segundo o algoritmo dos digitos verificadores (DV1=3, DV2=5)
cliente1 = Cliente("Maria Silva", "maria@email.com", "111.444.777-35")

for obj in (p1, p2, p3, cliente1):
    print(f"  str  -> {obj}")        # aciona __str__
    print(f"  repr -> {repr(obj)}")  # aciona __repr__
    print("  " + "-" * 66)

# =====================================================================
# PASSO 2 - Validacoes e captura de excecoes (ValueError)
# =====================================================================
print()
print("=" * 70)
print("PASSO 2: VALIDACOES E CAPTURA DE ValueError")
print("=" * 70)

# 2.1 - preco negativo e preco nulo
for preco_invalido in (-10.0, 0):
    try:
        p1.preco = preco_invalido
    except ValueError as e:
        print(f"  [OK] preco = {preco_invalido} recusado -> {e}")

# 2.2 - CPF fora da mascara, com letras e com digito verificador errado
for cpf_invalido in ("1234", "abc.def.ghi-jk", "111.444.777-99", "111.111.111-11"):
    try:
        cliente1.cpf = cpf_invalido
    except ValueError as e:
        print(f"  [OK] cpf = '{cpf_invalido}' recusado -> {e}")

# 2.3 - e-mail sem '@', sem texto antes e sem texto depois
for email_invalido in ("sememail.com", "@email.com", "maria@"):
    try:
        cliente1.email = email_invalido
    except ValueError as e:
        print(f"  [OK] email = '{email_invalido}' recusado -> {e}")

# 2.4 - cupom com valor nulo ou negativo
try:
    cliente1.adicionar_cupom(-5.0)
except ValueError as e:
    print(f"  [OK] cupom = -5.0 recusado -> {e}")

# comprova que nenhuma tentativa invalida alterou o estado do objeto
print(f"  Estado preservado: {repr(p1)}")
print(f"  Estado preservado: {repr(cliente1)}")

# =====================================================================
# PASSO 3 - Modificadores de visibilidade e name mangling
# =====================================================================
print()
print("=" * 70)
print("PASSO 3: VISIBILIDADE E NAME MANGLING")
print("=" * 70)

# 3.1 - atributos privados: o acesso direto de fora da classe gera AttributeError,
# porque o Python renomeia __preco para _Produto__preco e __cpf para _Cliente__cpf
try:
    print(p1.__preco)
except AttributeError as e:
    print(f"  [OK] p1.__preco bloqueado -> {e}")

try:
    print(cliente1.__cpf)
except AttributeError as e:
    print(f"  [OK] cliente1.__cpf bloqueado -> {e}")

# o valor continua acessivel pela via correta (property / getter tradicional)
print(f"  Via property: p1.preco = {p1.preco}")
print(f"  Via property: cliente1.cpf = {cliente1.cpf}")

# 3.2 - atributo protegido: o acesso funciona normalmente.
# O underline unico (_categoria) e apenas uma CONVENCAO entre programadores,
# nao um mecanismo da linguagem: o interpretador nao renomeia nem bloqueia o
# nome, entao a sintaxe e valida mesmo violando a boa pratica de encapsulamento.
print(f"  Protegido (acessivel por convencao): p1._categoria = {p1._categoria}")

# =====================================================================
# PASSO 4 - Fluxo do carrinho e composicao
# =====================================================================
print()
print("=" * 70)
print("PASSO 4: FLUXO DO CARRINHO (COMPOSICAO)")
print("=" * 70)

carrinho = CarrinhoDeCompras(cliente1)  # composicao: carrinho recebe o Cliente
carrinho.adicionar_produto(p1)
carrinho.adicionar_produto(p2)
carrinho.adicionar_produto(p3)

print("  Itens do carrinho:")
carrinho.listar_itens()  # usa o __str__ de Produto

print(f"  Total (@property): R$ {carrinho.total:.2f}")

# remocao de um item -> o total e recalculado automaticamente
carrinho.remover_produto(p3)
print(f"  Apos remover '{p3.nome}': R$ {carrinho.total:.2f}")
carrinho.adicionar_produto(p3)
print(f"  Apos devolver '{p3.nome}': R$ {carrinho.total:.2f}")

print(f"  str  -> {carrinho}")
print(f"  repr -> {repr(carrinho)}")

# saldo de cupons do cliente (encapsulamento tradicional)
print()
print("  Cupons do cliente:")
print(f"    Saldo inicial: R$ {cliente1.get_saldo_cupom():.2f}")
cliente1.adicionar_cupom(10.0)
cliente1.adicionar_cupom(15.50)
print(f"    Saldo acumulado: R$ {cliente1.get_saldo_cupom():.2f}")

# uso do saldo: abate o cupom do total do carrinho
total_com_desconto = max(carrinho.total - cliente1.get_saldo_cupom(), 0.0)
print(f"    Total do carrinho:  R$ {carrinho.total:.2f}")
print(f"    Desconto (cupons): -R$ {cliente1.get_saldo_cupom():.2f}")
print(f"    Valor a pagar:      R$ {total_com_desconto:.2f}")

print()
print("=" * 70)
print("HOMOLOGACAO CONCLUIDA COM SUCESSO")
print("=" * 70)
