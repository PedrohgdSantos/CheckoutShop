# loja.py -- modo interativo (EXTRA, fora do roteiro de homologacao)
#
# Gabriel Oliveira Sampaio
# Joao Pedro Xavier Lopes
# Pedro Henrique Santos
#
# O main.py continua sendo o script de homologacao exigido pelo roteiro
# (4 etapas, execucao automatica e determinstica). Este arquivo e um extra:
# reaproveita EXATAMENTE as mesmas classes para simular a loja, com o cliente
# escolhendo os produtos. Nenhuma regra de negocio e reescrita aqui -- toda
# validacao continua morando dentro de Produto, Cliente e CarrinhoDeCompras.

import sys

from produto import Produto
from cliente import Cliente
from carrinho import CarrinhoDeCompras

# garante que os acentos das mensagens de erro apaream corretamente no console
try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, OSError):
    pass


# catalogo fixo da loja: instancias de Produto disponiveis para venda
CATALOGO = [
    Produto("Camiseta", "Vestuário", 49.90),
    Produto("Tênis", "Calçados", 199.90),
    Produto("Boné", "Acessórios", 125.00),
    Produto("Mochila", "Acessórios", 89.90),
    Produto("Fone Bluetooth", "Eletrônicos", 249.00),
]


# FUNCAO DE ENTRADA
# centraliza todo input() do programa em um lugar so, para nao repetir
# o tratamento de Ctrl+C em cada pergunta do menu
def perguntar(rotulo: str) -> str:
    """Le uma entrada do usuario, tratando Ctrl+C / fim de arquivo."""
    try:
        # .strip() remove espacos sobrando no comeco e no fim do que foi digitado
        return input(rotulo).strip()
    except (EOFError, KeyboardInterrupt):
        print("\nEncerrando a loja. Ate logo!")
        sys.exit(0)


def cadastrar_cliente() -> Cliente:
    """Monta um Cliente pedindo os dados ate que todos passem nas validacoes.

    Repare que quem valida e a propria classe Cliente: aqui so capturamos o
    ValueError disparado pelos setters e pedimos o dado de novo.
    """
    print("=" * 60)
    print("CADASTRO DO CLIENTE")
    print("=" * 60)

    # laco 1: o nome nao pode ficar vazio
    nome = ""
    while not nome:
        nome = perguntar("Nome completo: ")
        if not nome:
            print("  ! O nome nao pode ficar em branco.")

    # cria o cliente com dados provisorios validos e depois aplica os reais,
    # aproveitando os setters (@email.setter e @cpf.setter) um de cada vez
    cliente = Cliente(nome, "provisorio@email.com", "111.444.777-35")

    while True:
        try:
            # repete a pergunta ate o @email.setter aceitar o endereco
            cliente.email = perguntar("E-mail: ")
            break
        except ValueError as e:
            print(f"  ! {e}")

    while True:
        try:
            # mesma ideia para o CPF, agora contra o @cpf.setter
            cliente.cpf = perguntar("CPF (999.999.999-99): ")
            break
        except ValueError as e:
            print(f"  ! {e}")

    print(f"\nCadastro concluido -> {cliente}\n")
    return cliente


# FUNCAO DE VITRINE: mostra tudo que esta a venda
def mostrar_catalogo():
    """Exibe os produtos disponiveis usando o __str__ de Produto."""
    print("\n--- CATALOGO ---")
    # enumerate(..., start=1) numera a lista de 1 em diante,
    # para o cliente escolher pelo numero em vez de digitar o nome
    for indice, produto in enumerate(CATALOGO, start=1):
        print(f"  {indice}. {produto}")
    print()


# FUNCAO DE SELECAO: traduz o numero digitado no objeto Produto correspondente
def escolher_produto(rotulo: str):
    """Pede o numero de um produto do catalogo e devolve a instancia (ou None)."""
    escolha = perguntar(rotulo)

    # .isdigit() confere se veio so numero, evitando erro na conversao int()
    if not escolha.isdigit():
        print("  ! Digite o numero do produto.")
        return None

    # converte o texto para numero e confere se existe no catalogo
    indice = int(escolha)
    if not 1 <= indice <= len(CATALOGO):
        print(f"  ! Escolha um numero entre 1 e {len(CATALOGO)}.")
        return None

    # -1 porque a lista comeca no indice 0, mas exibimos a partir do 1
    return CATALOGO[indice - 1]


# FUNCAO DE FECHAMENTO: monta o resumo e cobra o valor final
def finalizar_compra(carrinho: CarrinhoDeCompras):
    """Fecha o pedido aplicando o saldo de cupons sobre o total do carrinho."""
    print("\n" + "=" * 60)
    print("RESUMO DO PEDIDO")
    print("=" * 60)

    carrinho.listar_itens()

    # nada foi escolhido -> nao ha o que cobrar
    if carrinho.total == 0:
        print("Nada a pagar.\n")
        return

    # o carrinho guarda o objeto Cliente inteiro, entao chamamos o getter dele aqui
    saldo = carrinho.cliente.get_saldo_cupom()
    desconto = min(saldo, carrinho.total)       # o cupom nunca zera abaixo de R$ 0,00
    a_pagar = carrinho.total - desconto         # valor final da compra

    print("-" * 60)
    print(f"  Subtotal:      R$ {carrinho.total:>8.2f}")
    print(f"  Cupons:       -R$ {desconto:>8.2f}")
    print(f"  Valor a pagar: R$ {a_pagar:>8.2f}")
    print("-" * 60)
    print(f"Obrigado pela compra, {carrinho.cliente.nome}!\n")


# FUNCAO PRINCIPAL: cadastra o cliente, cria o carrinho e roda o menu
def main():
    print("\n" + "=" * 60)
    print("CHECKOUTSHOP -- MODO INTERATIVO")
    print("=" * 60 + "\n")

    cliente = cadastrar_cliente()

    # COMPOSICAO: o carrinho so existe a partir de um Cliente valido
    carrinho = CarrinhoDeCompras(cliente)

    opcoes = (
        "\n=============== MENU ===============\n"
        "  1 - Ver catalogo\n"
        "  2 - Adicionar produto ao carrinho\n"
        "  3 - Remover produto do carrinho\n"
        "  4 - Ver carrinho\n"
        "  5 - Adicionar cupom\n"
        "  6 - Finalizar compra\n"
        "  0 - Sair\n"
        "===================================="
    )

    while True:
        print(opcoes)
        opcao = perguntar("Opcao: ")   # cada numero abaixo dispara uma acao

        if opcao == "1":
            mostrar_catalogo()

        elif opcao == "2":
            mostrar_catalogo()
            produto = escolher_produto("Numero do produto a adicionar: ")
            if produto:
                carrinho.adicionar_produto(produto)
                print(f"  + '{produto.nome}' adicionado. Total: R$ {carrinho.total:.2f}")

        elif opcao == "3":
            mostrar_catalogo()
            produto = escolher_produto("Numero do produto a remover: ")
            if produto:
                carrinho.remover_produto(produto)  # ignora item que nao esta no carrinho
                print(f"  - '{produto.nome}' removido. Total: R$ {carrinho.total:.2f}")

        elif opcao == "4":
            print()
            carrinho.listar_itens()               # usa o __str__ de Produto
            print(carrinho)                       # usa o __str__ do carrinho

        elif opcao == "5":
            # troca virgula por ponto para aceitar "25,50" alem de "25.50"
            valor = perguntar("Valor do cupom: R$ ").replace(",", ".")
            try:
                cliente.adicionar_cupom(float(valor))
                print(f"  Saldo de cupons: R$ {cliente.get_saldo_cupom():.2f}")
            except ValueError as e:
                # cobre tanto o float() invalido quanto a regra valor > 0 do Cliente
                print(f"  ! {e}")

        elif opcao == "6":
            finalizar_compra(carrinho)
            break

        elif opcao == "0":
            print("\nSaindo sem finalizar a compra. Ate logo!\n")
            break

        else:
            print("  ! Opcao invalida.")


# so executa o menu quando este arquivo e rodado direto (python loja.py);
# se ele fosse importado por outro modulo, nada seria disparado sozinho
if __name__ == "__main__":
    main()
