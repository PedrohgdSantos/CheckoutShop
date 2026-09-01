# Anatomia do CheckoutShop

Documentação técnica detalhada: como cada arquivo `.py` deste projeto funciona por dentro,
linha a linha, decisão por decisão.

Cinco arquivos, três classes, nenhuma herança — tudo se sustenta em **encapsulamento** e
**composição**.

> Para uma visão geral rápida (como executar, estrutura, requisitos), veja o [README.md](README.md).
> Este documento é o aprofundamento.

**Integrantes:** Gabriel Oliveira Sampaio · João Pedro Xavier Lopes · Pedro Henrique Santos
**Disciplina:** Programação Orientada a Objetos — Prof. Lucio Nunes de Lira — 2026-2

---

## Índice

1. [Mapa do sistema](#1-mapa-do-sistema)
2. [Os três níveis de visibilidade](#2-os-três-níveis-de-visibilidade)
3. [`produto.py`](#3-produtopy)
4. [`cliente.py`](#4-clientepy)
   - [O algoritmo do CPF, em 4 etapas](#41-o-algoritmo-do-cpf-em-4-etapas)
5. [`carrinho.py`](#5-carrinhopy)
6. [`main.py`](#6-mainpy)
7. [`loja.py`](#7-lojapy)
8. [Mapa de exceções](#8-mapa-de-exceções)
9. [Glossário](#9-glossário)

---

## 1. Mapa do sistema

Três classes de negócio, um script de testes e um demo interativo. Cada classe mora no seu
próprio arquivo e conhece apenas o que precisa conhecer.

| Arquivo | Contém | Papel | Linhas |
|---|---|---|---:|
| `produto.py` | `Produto` | O item vendido. Guarda nome, categoria e preço válido. | 84 |
| `cliente.py` | `Cliente` | O comprador. Valida e-mail e CPF, acumula cupons. | 212 |
| `carrinho.py` | `CarrinhoDeCompras` | A composição. Une um cliente a uma lista de produtos. | 108 |
| `main.py` | script | Homologação automática em 4 passos. É o que o professor roda. | 160 |
| `loja.py` | script | Extra: loja interativa com menu. Reaproveita as três classes. | 215 |

### Quem importa quem

A direção das dependências importa: `produto.py` e `cliente.py` **não importam ninguém** — são
as folhas do sistema. O carrinho importa os dois para conferir os tipos que recebe. Os dois
scripts ficam no topo, importando tudo.

```
main.py / loja.py
        │
        ├──────────────► produto.py   (Produto)
        ├──────────────► cliente.py   (Cliente)
        └──────────────► carrinho.py  (CarrinhoDeCompras)
                              │
                              ├──► cliente.py   (só para isinstance)
                              └──► produto.py   (só para isinstance)
```

### A composição em si

```
CarrinhoDeCompras
├── cliente ──────► Cliente                        (1 objeto, público)
└── __itens ──────► [Produto, Produto, Produto]    (lista privada)
```

**Por que isso é composição, e não herança:** o carrinho **não é** um cliente nem um produto —
ele **tem** um cliente e **tem** produtos. Quando a relação é "tem um", a ferramenta certa é
guardar o objeto dentro do outro e chamar os métodos dele. Herança seria para "é um", que não
acontece em nenhum ponto deste sistema.

---

## 2. Os três níveis de visibilidade

O projeto inteiro gira em torno de uma pergunta: quem pode mexer em quê. Python responde isso
de três formas, e **só uma delas é uma trava de verdade**.

| Escrita | Nível | O que o Python faz | De fora da classe |
|---|---|---|---|
| `nome` | Público | Nada. Acesso totalmente livre. | `p1.nome` → funciona |
| `_categoria` | Protegido | **Nada.** O underline é só um combinado entre programadores. | `p1._categoria` → funciona, mas viola a convenção |
| `__preco` | Privado | Renomeia o atributo para `_Produto__preco`. | `p1.__preco` → `AttributeError` |

### Name mangling na prática

Quando o Python encontra um atributo com dois underlines dentro de uma classe, ele reescreve o
nome colando o nome da classe na frente. O nome original simplesmente deixa de existir — não é
que o acesso seja "proibido", é que não há mais nada com aquele nome.

```python
>>> p1 = Produto("Camiseta", "Vestuário", 49.90)

>>> p1.__preco                 # o nome que escrevemos
AttributeError: 'Produto' object has no attribute '__preco'

>>> p1._Produto__preco         # o nome que existe de verdade
49.9

>>> p1.preco                   # o caminho correto: a property
49.9
```

> **O detalhe que cai na prova:** o privado não é uma trava de segurança — é uma trava de
> *acidente*. Quem souber o nome mangled ainda consegue chegar lá. A diferença é que ninguém
> faz isso por engano, enquanto `p1._categoria` qualquer um faz sem perceber.

---

## 3. `produto.py`

**Módulo 1 — Integrante 1.** Modela o item comercializado. Toda a responsabilidade da classe é
uma só: garantir que não exista produto com preço inválido no sistema, em nenhum momento.

### O construtor e os três atributos

```python
def __init__(self, nome: str, categoria: str, preco: float):
    self.nome = nome              # público
    self._categoria = categoria   # protegido
    self.preco = preco            # NÃO grava direto — vai para o setter
```

A terceira linha é a mais importante do arquivo e a mais fácil de ler errado. Ela parece criar
um atributo `preco`, mas **não cria**: como a classe define uma property com esse nome, o Python
desvia a atribuição para o `@preco.setter`. A validação roda antes de qualquer coisa ser
guardada.

A consequência prática: **não existe caminho para criar um `Produto` com preço inválido.** Nem
pelo construtor, nem depois. É o mesmo porteiro nos dois casos.

### Membro por membro

#### `nome` — público

String livre. Não tem validação porque não tem regra de negócio: qualquer texto é um nome de
produto aceitável.

#### `_categoria` — protegido

O segmento do produto ("Vestuário", "Eletrônicos"). Marcado como protegido para sinalizar uso
interno — é lido pelos dunders da própria classe. O `main.py` acessa esse atributo de fora
*de propósito*, para demonstrar que o Python permite.

#### `preco` — `@property` (getter)

Devolve `self.__preco`. Chamado **sem parênteses**: escrevemos `p1.preco` e o método roda por
baixo. Para quem usa a classe, parece um atributo comum — essa é exatamente a intenção do
`@property`.

#### `preco` — `@preco.setter`

Roda em toda atribuição `p1.preco = x`. Faz duas checagens em sequência e só grava se as duas
passarem:

```python
# 1ª — precisa ser número (bool é subclasse de int, então é barrado à parte)
if isinstance(novo_preco, bool) or not isinstance(novo_preco, (int, float)):
    raise ValueError("Preço inválido: o valor deve ser numérico (int ou float).")

# 2ª — regra de negócio do enunciado: preco > 0
if novo_preco <= 0:
    raise ValueError(f"Preço inválido: ... (recebido: {novo_preco}).")

self.__preco = float(novo_preco)   # aprovado
```

**Por que `self.__preco` e não `self.preco` na última linha:** escrever `self.preco` chamaria
este mesmo setter de novo, e de novo, até estourar com `RecursionError`. Dentro do setter,
sempre se grava no atributo privado.

**Por que `bool` é barrado à parte:** em Python, `bool` é subclasse de `int`. Sem essa checagem,
`p1.preco = True` seria lido como `1` e passaria como preço válido.

#### `__str__` — dunder

Chamado por `print(p1)` e `str(p1)`. Formato do enunciado:

```
Camiseta (Vestuário) - R$ 49.90
```

O `:.2f` força as duas casas decimais — sem ele, `49.9` apareceria com um dígito só, e preço com
uma casa decimal parece erro.

#### `__repr__` — dunder

Chamado por `repr(p1)`. Mostra a estrutura em vez da aparência:

```
Produto(nome='Camiseta', categoria='Vestuário', preco=49.9)
```

A convenção é imitar a chamada do construtor: lendo o `repr`, dá para recriar o objeto. Por isso
o preço aparece cru (`49.9`) e não formatado — é o valor real na memória.

---

## 4. `cliente.py`

**Módulo 2 — Integrante 2.** O arquivo mais denso do projeto. Modela o comprador e carrega a
validação mais rigorosa: o algoritmo oficial de CPF, com máscara e dois dígitos verificadores.

É o único módulo que importa alguma coisa: `re`, da biblioteca padrão, para expressões
regulares. Nada externo, nada instalado via `pip`.

### Os quatro atributos

| Atributo | Nível | Conteúdo | Como se escreve nele |
|---|---|---|---|
| `nome` | Público | Nome completo | Direto |
| `_email` | Protegido | E-mail validado | Só pelo `@email.setter` |
| `__cpf` | Privado | CPF com máscara | Só pelo `@cpf.setter` |
| `__saldo_cupom` | Privado | Saldo acumulado, inicia em `0.0` | Só por `adicionar_cupom()` |

> **Decisão de projeto — por que o saldo não tem setter:** um `@saldo_cupom.setter` permitiria
> `cliente.saldo_cupom = 20.0`, apagando tudo que o cliente já tinha acumulado. Saldo não se
> substitui, se movimenta. Por isso a única porta é `adicionar_cupom()`, que obriga a soma
> (`+=`). O enunciado pede encapsulamento tradicional aqui justamente para contrastar com as
> properties usadas nos outros campos.

### Validação do e-mail

```python
if not isinstance(valor, str) or "@" not in valor:
    raise ValueError("E-mail inválido: o endereço deve conter o caractere '@'.")

partes = valor.split("@")      # "jorge@email.com" → ["jorge", "email.com"]

if len(partes) != 2 or not partes[0].strip() or not partes[1].strip():
    raise ValueError("E-mail inválido: deve haver texto antes e depois do '@'.")

self._email = valor
```

A segunda condição faz três trabalhos de uma vez:

- `len(partes) != 2` derruba `a@b@c` — dois arrobas geram três pedaços;
- `partes[0].strip()` vazio derruba `@email.com`;
- `partes[1].strip()` vazio derruba `maria@`.

O `.strip()` está ali para que um espaço em branco não conte como "texto".

E, como no `Produto`, a gravação é em `self._email` e não em `self.email` — senão o setter
chamaria a si mesmo indefinidamente.

### 4.1 O algoritmo do CPF, em 4 etapas

Cada etapa é uma peneira: o valor só chega no atributo privado se passar por todas. Qualquer
falha dispara `ValueError` com uma mensagem **diferente** — o que ajuda a saber *onde* o CPF
falhou.

#### Etapa 1 — Máscara

```python
r"^\d{3}\.\d{3}\.\d{3}-\d{2}$"
```

- `^` ancora no início e `$` no fim. Sem eles, `"123.456.789-01123"` passaria.
- `\d{3}` exige exatamente três dígitos numéricos.
- `\.` exige um ponto **literal** — a barra tira o significado especial que o ponto tem em
  regex, onde ele significaria "qualquer caractere".

Isso garante os 14 caracteres no formato `999.999.999-99`.

#### Etapa 2 — Sequências idênticas

Os dígitos são extraídos com uma list comprehension:

```python
digitos = [int(c) for c in valor if c.isdigit()]
# "111.444.777-35" → [1, 1, 1, 4, 4, 4, 7, 7, 7, 3, 5]
```

O `if c.isdigit()` descarta os pontos e o hífen; o `int(c)` converte cada caractere aprovado em
número. Então:

```python
if len(set(digitos)) == 1:
    raise ValueError("CPF inválido: não é permitida sequência de dígitos idênticos.")
```

`set()` elimina repetições. Se sobrou **um** valor distinto, é `111.111.111-11` ou similar. A
Receita Federal considera esses CPFs inválidos mesmo quando a matemática dos dígitos fecha.

#### Etapa 3 — Primeiro dígito verificador (DV1)

```python
soma1 = sum(digitos[i] * (10 - i) for i in range(9))
resto1 = (soma1 * 10) % 11
dv1_esperado = 0 if resto1 == 10 else resto1

if digitos[9] != dv1_esperado:
    raise ValueError("CPF inválido: primeiro dígito verificador incorreto.")
```

Pega os 9 primeiros dígitos e multiplica por pesos que caem de 10 até 2. `10 - i` produz
exatamente essa sequência conforme `i` vai de 0 a 8.

#### Etapa 4 — Segundo dígito verificador (DV2)

Mesma conta, agora com **10 dígitos** (os 9 originais mais o DV1 já confirmado) e pesos de 11
até 2:

```python
soma2 = sum(digitos[i] * (11 - i) for i in range(10))
resto2 = (soma2 * 10) % 11
dv2_esperado = 0 if resto2 == 10 else resto2

if digitos[10] != dv2_esperado:
    raise ValueError("CPF inválido: segundo dígito verificador incorreto.")

self.__cpf = valor   # só chega aqui se passou pelas 4 etapas
```

Repare que o CPF é guardado **com** a máscara — é o `__str__` que remove a pontuação na hora de
exibir.

#### A conta com números reais: `111.444.777-35`

Esse é o CPF usado na homologação. Vale conferir na mão por que ele passa.

**DV1** — os 9 primeiros dígitos, pesos de 10 a 2:

| | | | | | | | | | | Σ |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Dígito | 1 | 1 | 1 | 4 | 4 | 4 | 7 | 7 | 7 | |
| Peso | 10 | 9 | 8 | 7 | 6 | 5 | 4 | 3 | 2 | |
| Produto | 10 | 9 | 8 | 28 | 24 | 20 | 28 | 21 | 14 | **162** |

`(162 × 10) % 11 = 1620 % 11 = 3` → confere com o 10º dígito ✅

**DV2** — os 10 primeiros dígitos (incluindo o DV1 = 3), pesos de 11 a 2:

| | | | | | | | | | | | Σ |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Dígito | 1 | 1 | 1 | 4 | 4 | 4 | 7 | 7 | 7 | **3** | |
| Peso | 11 | 10 | 9 | 8 | 7 | 6 | 5 | 4 | 3 | **2** | |
| Produto | 11 | 10 | 9 | 32 | 28 | 24 | 35 | 28 | 21 | **6** | **204** |

`(204 × 10) % 11 = 2040 % 11 = 5` → confere com o 11º dígito ✅

> **O bug que essa conta revelou:** o `main.py` usava `123.456.789-01`, o exemplo que aparece no
> enunciado. Esse CPF passa na máscara, mas **reprova no DV2** — e o script morria com traceback
> logo no Passo 1, antes de imprimir qualquer teste. Foi trocado por `111.444.777-35`, que fecha
> a conta acima.

### Encapsulamento tradicional: os cupons

#### `get_saldo_cupom()`

Devolve `self.__saldo_cupom`. Repare que aqui se usa **parênteses** — é um método comum, não uma
property. O enunciado pede os dois estilos no mesmo projeto justamente para a diferença ficar
visível.

#### `adicionar_cupom(valor)`

Confere se é número, confere se é `> 0` e então **soma**:

```python
self.__saldo_cupom += valor
```

Duas chamadas de R$ 10,00 e R$ 15,50 resultam em R$ 25,50, não em R$ 15,50. É essa acumulação
que um setter comum destruiria.

### Os dois dunders

```python
# __str__ — CPF sem pontuação, conforme o enunciado
Cliente: Maria Silva | CPF: 11144477735

# __repr__ — CPF com a máscara, como está guardado
Cliente(nome='Maria Silva', email='maria@email.com', cpf='111.444.777-35')
```

A limpeza do CPF no `__str__` é feita com `"".join(c for c in self.__cpf if c.isdigit())`:
percorre a string, mantém só os dígitos e cola tudo sem separador. Os dois formatos convivem de
propósito — um é para ler, o outro é para depurar.

---

## 5. `carrinho.py`

**Módulo 3 — Integrante 3.** O módulo que amarra o sistema. É aqui que a composição acontece e
que dois objetos de classes diferentes passam a cooperar.

### Por que este arquivo importa os outros dois

```python
from cliente import Cliente
from produto import Produto
```

Não é para criar objetos — o carrinho nunca instancia nada. É para poder **conferir tipos** com
`isinstance()`. Sem esses imports, não haveria como recusar um item errado.

### O construtor: a porta de entrada da composição

```python
def __init__(self, cliente: Cliente):
    if not isinstance(cliente, Cliente):
        raise ValueError("Carrinho inválido: é necessário informar uma instância de Cliente.")

    self.cliente = cliente   # público — o objeto inteiro, não só o nome
    self.__itens = []        # privado — vira _CarrinhoDeCompras__itens
```

Guardar o objeto `Cliente` **inteiro** (e não apenas `cliente.nome`) é o que torna isso
composição de verdade: mais adiante o carrinho consegue chamar `self.cliente.get_saldo_cupom()`
e `repr(self.cliente)`. Se guardasse só o nome, seria uma cópia de dado, não uma associação
entre objetos.

### Membro por membro

#### `adicionar_produto(produto)`

Recusa qualquer coisa que não seja `Produto` e então faz `self.__itens.append(produto)`.

**Por que o filtro existe:** se um texto entrasse na lista, o `total` quebraria mais tarde ao
procurar `produto.preco` em algo que não tem preço. O erro apareceria longe da causa. Barrar na
entrada faz a mensagem apontar para o lugar certo.

#### `remover_produto(produto)`

```python
if produto in self.__itens:
    self.__itens.remove(produto)
```

Sem esse `if`, o `list.remove()` nativo levantaria `ValueError` ao não encontrar o item. O
enunciado pede "remove se existente" — então a ausência é um caso normal, não um erro.

#### `total` — `@property`

```python
return float(sum(produto.preco for produto in self.__itens))
```

**É calculada, não armazenada.** A soma acontece no instante da consulta, percorrendo a lista.
Por isso não existe um `@total.setter`: um total atribuído poderia discordar dos itens. Assim é
impossível o carrinho mostrar R$ 374,80 com dois produtos na lista.

O `float()` em volta garante o tipo mesmo com o carrinho vazio — sem ele, `sum([])` devolveria
o inteiro `0`.

#### `listar_itens()`

Imprime um produto por linha com `print(produto)`, o que aciona o `__str__` de `Produto`
automaticamente. O formato do item está definido em um lugar só — se mudar lá, muda aqui junto,
sem tocar neste arquivo.

Com a lista vazia, imprime `Carrinho vazio.` em vez de não imprimir nada.

#### `__str__` — dunder

```
Carrinho de Maria Silva | 3 item(ns) | Total: R$ 374.80
```

Três informações de três fontes distintas: o nome vem do objeto `Cliente`, a contagem vem de
`len()` na lista privada, o valor vem da property calculada.

#### `__repr__` — dunder

```
CarrinhoDeCompras(cliente=Cliente(nome='Maria Silva', email='maria@email.com',
                  cpf='111.444.777-35'), total_itens=3)
```

O `repr(self.cliente)` aciona o `__repr__` da outra classe, encaixando uma representação dentro
da outra. A composição fica visível na própria saída de depuração.

---

## 6. `main.py`

**Homologação.** Não é a loja: é o roteiro de testes exigido pelo enunciado. Roda sozinho, não
pede nada digitado e produz sempre exatamente a mesma saída.

> **Por que estático é o certo aqui:** o item 3 do enunciado diz que a execução deve seguir
> *estritamente* os quatro passos. Um teste de homologação precisa ser **determinístico**: o
> professor roda `python main.py` e vê os mesmos resultados, na mesma ordem, sem digitar nada.
> A parte interativa existe — mora no `loja.py`.

### Passo 1 — Instanciação e representação

Cria 3 `Produto` e 1 `Cliente`, depois percorre os quatro objetos imprimindo `__str__` e
`__repr__` de cada um. Um único laço cobre objetos de classes diferentes — funciona porque as
duas classes implementam os mesmos dunders.

### Passo 2 — Validações e captura de `ValueError`

Dez tentativas inválidas, cada uma dentro de um `try/except ValueError`:

- **Preço:** `-10.0` e `0` — cobre negativo e nulo
- **CPF:** `"1234"` (máscara), `"abc.def.ghi-jk"` (letras), `"111.444.777-99"` (DV errado),
  `"111.111.111-11"` (repetido) — cada um cai numa etapa diferente do algoritmo
- **E-mail:** `"sememail.com"`, `"@email.com"`, `"maria@"`
- **Cupom:** `-5.0`

O passo fecha imprimindo o `repr` dos objetos. Essa linha é a prova de que nenhuma das dez
tentativas conseguiu alterar o estado interno — o `raise` acontece *antes* da atribuição,
sempre.

### Passo 3 — Visibilidade e name mangling

Dois `try/except AttributeError` — para `p1.__preco` e `cliente1.__cpf` — provam o bloqueio do
privado. Em seguida os mesmos dados são lidos pelo caminho correto (property e getter),
mostrando que o dado não sumiu, só mudou de porta.

Por fim, `p1._categoria` é impresso sem erro nenhum, acompanhado do comentário que o enunciado
pede: o underline único é convenção, não trava.

### Passo 4 — Carrinho e composição

Monta o carrinho com o cliente, adiciona os três produtos, chama `listar_itens()` e lê o
`total`. Então remove e devolve um item — essa ida e volta é o que *prova* que o total é
recalculado e não guardado.

Fecha com os cupons: duas chamadas de `adicionar_cupom()` acumulando R$ 25,50, abatidos do total
no valor a pagar.

| Saída esperada | Valor |
|---|---:|
| Total do carrinho (3 itens) | R$ 374,80 |
| Após remover o boné | R$ 249,80 |
| Cupons acumulados | R$ 25,50 |
| **Valor a pagar** | **R$ 349,30** |

---

## 7. `loja.py`

**Extra — fora do roteiro avaliado.** A mesma camada de negócio, agora com o cliente escolhendo
os produtos. Existe para mostrar que as classes servem a dois programas diferentes sem nenhuma
alteração.

### As seis funções

#### `perguntar(rotulo)`

Todo `input()` do programa passa por aqui. Aplica `.strip()` e trata `Ctrl+C` / fim de arquivo
em um lugar só, em vez de repetir o mesmo `try` em cada pergunta do menu.

#### `cadastrar_cliente()`

Monta o `Cliente` com dados provisórios e depois aplica os reais um a um, dentro de laços
`while True`. Se o setter recusar, o `break` não é alcançado e a pergunta se repete. Quem valida
continua sendo a classe — esta função só insiste.

#### `mostrar_catalogo()`

Percorre a lista `CATALOGO` com `enumerate(..., start=1)`, numerando a partir de 1 para o
cliente escolher pelo número.

#### `escolher_produto(rotulo)`

Traduz o número digitado no objeto `Produto`. Usa `.isdigit()` antes do `int()` para não estourar
com texto, confere o intervalo e devolve `CATALOGO[indice - 1]` — o `-1` porque a lista começa no
índice 0.

#### `finalizar_compra(carrinho)`

Lista os itens, lê o saldo de cupons através de `carrinho.cliente.get_saldo_cupom()` —
composição em ação — e imprime subtotal, desconto e valor a pagar. O `min(saldo, total)` impede
conta negativa.

#### `main()`

Cadastra, cria o carrinho e roda o menu em laço até o cliente finalizar ou sair. Protegida por
`if __name__ == "__main__":`, para o menu não disparar se o arquivo for importado.

> **O que este arquivo demonstra:** o `loja.py` **não valida nada por conta própria**. Nenhuma
> regra de e-mail, CPF, preço ou cupom foi reescrita aqui — ele chama os métodos e captura os
> `ValueError`. É a prova prática de por que encapsular compensa: a mesma regra atende dois
> programas, e uma correção feita na classe corrige os dois.

---

## 8. Mapa de exceções

Toda entrada inválida do sistema, onde ela é barrada e com qual mensagem.

| Ação | Onde é barrada | Exceção |
|---|---|---|
| `p1.preco = -10.0` | `@preco.setter` | `ValueError` — preço deve ser maior que zero |
| `p1.preco = 0` | `@preco.setter` | `ValueError` — preço deve ser maior que zero |
| `p1.preco = "caro"` | `@preco.setter` | `ValueError` — valor deve ser numérico |
| `cliente.email = "sememail.com"` | `@email.setter` | `ValueError` — deve conter '@' |
| `cliente.email = "@email.com"` | `@email.setter` | `ValueError` — texto antes e depois do '@' |
| `cliente.cpf = "1234"` | `@cpf.setter` · etapa 1 | `ValueError` — formato deve ser '999.999.999-99' |
| `cliente.cpf = "111.111.111-11"` | `@cpf.setter` · etapa 2 | `ValueError` — sequência de dígitos idênticos |
| `cliente.cpf = "111.444.777-99"` | `@cpf.setter` · etapa 3 | `ValueError` — primeiro dígito verificador incorreto |
| `cliente.adicionar_cupom(-5.0)` | `adicionar_cupom()` | `ValueError` — cupom deve ser maior que zero |
| `CarrinhoDeCompras("Maria")` | `__init__` | `ValueError` — é necessário informar uma instância de Cliente |
| `carrinho.adicionar_produto("Camiseta")` | `adicionar_produto()` | `ValueError` — apenas instâncias de Produto |
| `p1.__preco` | name mangling | `AttributeError` — object has no attribute |
| `cliente.__cpf` | name mangling | `AttributeError` — object has no attribute |

---

## 9. Glossário

Os termos que aparecem nos comentários do código, em uma frase cada.

**`@property`** — Decorador que faz um método ser chamado como se fosse atributo (`p1.preco`,
sem parênteses). Permite trocar um atributo público por código validado sem quebrar quem já
usava a classe.

**setter** — O par do getter: roda na atribuição `objeto.campo = valor`. É onde a regra de
negócio mora, porque é o único caminho até o dado.

**name mangling** — A renomeação automática que o Python aplica a atributos com dois underlines:
`__preco` vira `_Produto__preco`. É o que transforma a convenção em bloqueio real.

**dunder** — Abreviação de *double underscore*. Métodos como `__init__`, `__str__` e `__repr__`,
que o Python chama sozinho em situações padrão: criar objeto, imprimir, inspecionar.

**composição** — Relação "tem um": um objeto guarda outro dentro de si e usa os métodos dele.
Alternativa à herança, que modela "é um".

**`ValueError`** — Exceção padrão do Python para "o tipo até está certo, mas o valor não serve".
É a escolha correta para regras de negócio — e a que o enunciado exige.

**`try` / `except`** — Bloco que tenta executar algo e, se der o erro esperado, desvia para um
tratamento em vez de encerrar o programa. É o que permite ao `main.py` testar dez falhas
seguidas e continuar rodando.

**`isinstance()`** — Função que pergunta se um objeto pertence a uma classe. Usada no carrinho
para recusar qualquer coisa que não seja `Cliente` ou `Produto`.

**list comprehension** — Sintaxe compacta para montar uma lista percorrendo outra sequência com
filtro embutido: `[int(c) for c in valor if c.isdigit()]`.
