# CheckoutShop

Protótipo da camada de negócios de um e-commerce, feito em Python **sem herança**, usando encapsulamento e composição entre objetos.

Trabalho 1 de Programação Orientada a Objetos — Prof. Lucio Nunes de Lira — 2026-2.

**Integrantes:** Gabriel Oliveira Sampaio · João Pedro Xavier Lopes · Pedro Henrique Santos

---

## Como executar

Abra o terminal **dentro da pasta do projeto** (os módulos se importam entre si, então o diretório importa):

```bash
cd CheckoutShop
python main.py
```

Se os acentos das mensagens saírem embaralhados no Windows, rode uma vez por sessão:

```powershell
$env:PYTHONIOENCODING='utf-8'
python main.py
```

Requisito: Python 3.7 ou superior. Nenhuma biblioteca externa — só a `re`, que já vem com o Python.

---

## Estrutura do projeto

| Arquivo | Papel |
|---|---|
| `produto.py` | Classe `Produto` — o item vendido |
| `cliente.py` | Classe `Cliente` — o comprador |
| `carrinho.py` | Classe `CarrinhoDeCompras` — junta cliente e produtos |
| `main.py` | Script de homologação: roda os testes das 4 etapas automaticamente |
| `loja.py` | **Extra** — loja interativa, fora do roteiro avaliado |

Como os objetos se relacionam:

```
CarrinhoDeCompras
├── cliente ──────► Cliente   (1 objeto)
└── __itens ──────► [Produto, Produto, Produto]   (lista privada)
```

Isso é **composição**: o carrinho não herda nada, ele *contém* objetos das outras classes e usa os métodos delas.

---

## Os três níveis de visibilidade

O projeto usa os três, e a diferença entre eles é o coração do trabalho:

| Escrita | Nome | O que o Python faz | Exemplo |
|---|---|---|---|
| `nome` | público | nada, acesso livre | `p1.nome` funciona |
| `_categoria` | protegido | **nada** — é só convenção entre programadores | `p1._categoria` funciona, mas não deveria ser usado |
| `__preco` | privado | renomeia para `_Produto__preco` (*name mangling*) | `p1.__preco` gera `AttributeError` |

Ou seja: só o privado tem proteção real. O protegido é um acordo de boas práticas, não uma trava da linguagem.

---

## `produto.py` — classe `Produto`

Representa um item à venda.

**Atributos**

- `nome` (público) — nome do produto
- `_categoria` (protegido) — segmento, ex: "Vestuário"
- `__preco` (privado) — preço unitário

**Funcionalidades**

| Membro | O que faz |
|---|---|
| `preco` (`@property`) | Lê o preço privado: `p1.preco`, sem parênteses |
| `preco` (`@preco.setter`) | Valida antes de gravar: recusa não numérico e recusa `preco <= 0`, disparando `ValueError` |
| `__str__` | Texto para o usuário: `Camiseta (Vestuário) - R$ 49.90` |
| `__repr__` | Texto técnico: `Produto(nome='Camiseta', categoria='Vestuário', preco=49.9)` |

O setter é o ponto central: como o `__init__` faz `self.preco = preco`, a atribuição é desviada para ele. **Nenhum produto consegue nascer com preço inválido.**

---

## `cliente.py` — classe `Cliente`

Representa o comprador, com validação rigorosa dos dados cadastrais.

**Atributos**

- `nome` (público)
- `_email` (protegido)
- `__cpf` (privado) — no formato `999.999.999-99`
- `__saldo_cupom` (privado) — começa em `0.0`

**Funcionalidades**

| Membro | O que faz |
|---|---|
| `email` (property + setter) | Exige o `@` **e** texto antes e depois dele |
| `cpf` (property + setter) | Aplica as 4 etapas oficiais de validação (abaixo) |
| `get_saldo_cupom()` | Getter tradicional do saldo privado |
| `adicionar_cupom(valor)` | Soma ao saldo (`+=`); recusa valor `<= 0` |
| `__str__` | `Cliente: Maria Silva \| CPF: 11144477735` |
| `__repr__` | `Cliente(nome='Maria Silva', email='maria@email.com', cpf='111.444.777-35')` |

**Validação do CPF, em 4 etapas** — qualquer falha dispara `ValueError`:

1. **Máscara** — a regex `^\d{3}\.\d{3}\.\d{3}-\d{2}$` garante 14 caracteres no formato exato
2. **Sequência repetida** — rejeita `111.111.111-11` e similares, inválidos pela Receita Federal
3. **1º dígito verificador** — soma os 9 primeiros dígitos com pesos de 10 a 2, e compara `(soma × 10) % 11` com o 10º dígito
4. **2º dígito verificador** — mesma conta com 10 dígitos e pesos de 11 a 2, comparando com o 11º dígito

> CPF válido para testes: `111.444.777-35`

**Por que o saldo de cupom não tem setter?** Um setter permitiria `cliente.saldo_cupom = 20.0`, apagando o saldo acumulado. Saldo não se substitui, se movimenta — por isso só existe `adicionar_cupom()`, que obriga a soma e barra valores inválidos.

---

## `carrinho.py` — classe `CarrinhoDeCompras`

Faz a composição do sistema.

**Atributos**

- `cliente` (público) — o objeto `Cliente` inteiro, não só o nome
- `__itens` (privado) — lista dos objetos `Produto`

**Funcionalidades**

| Membro | O que faz |
|---|---|
| `adicionar_produto(produto)` | Insere na lista privada; recusa o que não for `Produto` |
| `remover_produto(produto)` | Remove **se** o item estiver na lista (não quebra se não estiver) |
| `total` (`@property`) | Propriedade **calculada**: percorre a lista e soma os preços |
| `listar_itens()` | Imprime um produto por linha, usando o `__str__` de `Produto` |
| `__str__` | `Carrinho de Maria Silva \| 3 item(ns) \| Total: R$ 374.80` |
| `__repr__` | `CarrinhoDeCompras(cliente=Cliente(...), total_itens=3)` |

`total` não tem setter de propósito: ele é **derivado** dos itens, calculado no momento da consulta. Por isso nunca fica desatualizado — remova um item e o total já muda sozinho.

---

## `main.py` — homologação em 4 etapas

Não é a loja: é o roteiro de testes. Roda sozinho, sem pedir nada digitado, e sempre produz a mesma saída.

**Passo 1 — Instanciação e representação**
Cria 3 produtos e 1 cliente, imprimindo `__str__` e `__repr__` de cada um.

**Passo 2 — Validações e `ValueError`**
Dez tentativas inválidas, todas capturadas com `try/except`:

- preço `-10.0` e preço `0`
- CPF `"1234"` (curto), `"abc.def.ghi-jk"` (letras), `"111.444.777-99"` (DV errado), `"111.111.111-11"` (repetido)
- e-mail `"sememail.com"` (sem `@`), `"@email.com"` (sem texto antes), `"maria@"` (sem texto depois)
- cupom `-5.0`

Ao final, imprime o `repr` dos objetos para provar que **nenhuma tentativa inválida alterou o estado interno**.

**Passo 3 — Visibilidade e name mangling**
Mostra o `AttributeError` de `p1.__preco` e de `cliente1.__cpf`, o acesso correto pela property, e o acesso livre a `p1._categoria` — com o comentário explicando por que a linguagem permite.

**Passo 4 — Carrinho e composição**
Monta o carrinho com o cliente, adiciona os 3 produtos, lista os itens, lê o `total`, remove e devolve um item para provar o recálculo automático, acumula cupons e abate do valor a pagar.

Saída esperada no fim: total **R$ 374,80**, cupons **R$ 25,50**, a pagar **R$ 349,30**.

---

## `loja.py` — modo interativo (extra)

Fora do roteiro avaliado. Aqui o cliente escolhe os produtos de verdade:

```bash
python loja.py
```

- Cadastro que **repergunta** enquanto o e-mail ou o CPF forem inválidos
- Catálogo com 5 produtos, escolhidos por número
- Menu: ver catálogo · adicionar · remover · ver carrinho · adicionar cupom · finalizar
- Fechamento com subtotal, desconto e valor a pagar

O ponto importante: o `loja.py` **não valida nada por conta própria**. Toda regra continua dentro de `Produto`, `Cliente` e `CarrinhoDeCompras` — ele apenas chama os métodos e captura os `ValueError`. É a demonstração prática de por que encapsular compensa: a mesma regra serve os dois programas sem ser reescrita.

---

## Conceitos de POO demonstrados

| Conceito | Onde ver |
|---|---|
| Módulos separados | um arquivo por classe |
| Visibilidade (público/protegido/privado) | atributos das 3 classes |
| `@property` / `@setter` | `Produto.preco`, `Cliente.email`, `Cliente.cpf` |
| Getter/setter tradicional | `get_saldo_cupom()` / `adicionar_cupom()` |
| Propriedade calculada | `CarrinhoDeCompras.total` |
| Tratamento defensivo com `ValueError` | todos os setters |
| Dunder methods | `__init__`, `__str__`, `__repr__` nas 3 classes |
| Composição | `CarrinhoDeCompras` contendo `Cliente` e `Produto` |
| `try/except` | `main.py`, passos 2 e 3 |
