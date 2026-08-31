# main.py — script de homologacao (roteiro item 3)
from produto import Produto
from cliente import Cliente
from carrinho import CarrinhoDeCompras

print("=== Passo 1: instanciacao e __str__/__repr__ ===")
p1 = Produto("Camiseta", "Vestuario", 49.90)
p2 = Produto("Tenis", "Calcados", 199.90)
p3 = Produto("Bone", "Acessorios", 125.00)
cliente1 = Cliente("Maria Silva", "maria@email.com", "123.456.789-01")

for obj in (p1, p2, p3, cliente1):
    print(obj) # aciona __str__
    print(repr(obj)) # aciona __repr__
print("\n=== Passo 2: validacoes e ValueError ===")

try:
    p1.preco = -10.0
except ValueError as e:
    print(f"Erro esperado (preco): {e}")

try:
    cliente1.cpf = "1234"
except ValueError as e:
    print(f"Erro esperado (cpf): {e}")

try:
    cliente1.email = "sememail.com"
except ValueError as e:
    print(f"Erro esperado (email): {e}")

print("\n=== Passo 3: visibilidade e name mangling ===")

try:
    print(p1.__preco)
except AttributeError as e:
    print(f"Erro esperado (atributo privado): {e}")

# _categoria e "protegido": Python nao impede o acesso de fora da classe,
# a convencao (um unico underscore) so avisa que nao deveria ser usado
# diretamente -- e apenas uma boa pratica, nao uma restricao da linguagem.
print(p1._categoria)

print("\n=== Passo 4: fluxo do carrinho (composicao) ===")
carrinho = CarrinhoDeCompras(cliente1)
carrinho.adicionar_produto(p1)
carrinho.adicionar_produto(p2)
carrinho.adicionar_produto(p3)

carrinho.listar_itens()
print(f"Total: R$ {carrinho.total:.2f}")
print(carrinho)
print(repr(carrinho))

cliente1.adicionar_cupom(10.0)
print(f"Saldo de cupons: {cliente1.get_saldo_cupom():.2f}")
