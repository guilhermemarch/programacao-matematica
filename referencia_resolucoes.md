# Referência — Programação Matemática

O que o caderno e as atividades ensinam, já corrigido, e a lista dos erros do material original. As contas das questões são sempre feitas pelo `resolver.py` (ver `prompt.md`). Este arquivo serve para entender o método, responder perguntas teóricas e ver como fica uma resposta.

As fotos originais não estão no repositório: tudo o que importa delas está aqui. Quando este arquivo e as fotos discordam, vale este arquivo.

## 1. Índice do material

| Material | Conteúdo | Situação |
|---|---|---|
| Caderno, p01 | Aula de 10/08/2026: formulação de problemas; mistura de carnes (Min custo) | Modelo com erro, corrigido em 2.1 |
| Caderno, p02 | Carpinteiro e biombos (Max lucro) | Modelo com erro, corrigido em 2.1 |
| Caderno, p03 | Fabricante de consoles, 4 modelos (Max lucro) | Modelo com erro, corrigido em 2.1 |
| Caderno, p04 | Mochila com 5 itens (Max valor) | Modelo com erro, corrigido em 2.1 |
| Caderno, p05 a p07 | Aula de 17/08/2026: método gráfico; exemplo Max Z = 2x1 + 3x2 | Certo: Z = 13,5 |
| Caderno, p08 e p09 | Aula de 14/09/2026: passos do Simplex | Certo; passos em 2.3 |
| Caderno, p10 a p12 | Simplex de Max Z = 2x1 + 3x2 | **Errado: parou antes do ótimo** (3.4) |
| Caderno, p12 e p13 | Simplex de Max Z = 2x1 + x2 + x3 | Contas certas; classificação das básicas errada (3.4) |
| Caderno, p13 a p15 | Simplex de Max Z = 10x1 + 11x2 | **Errado: o último quadro não foi feito** (3.4) |
| Caderno, p16 a p18 | Simplex e gráfico de Max Z = 3x1 + 4x2 | Certo; resolução completa em 3.1 |
| Caderno, p19 | Simplex de Max Z = 2x1 + 10x2 + x3 | Resposta certa; última linha do quadro errada (3.4) |
| Caderno, p20 e p21 | Dualidade: regras I a IV; exemplo de Max; enunciado de um Min | Regras certas; um coeficiente inconsistente (2.6) |
| Atividade 1 (1 foto) | Atividade 1: dual de Max Z = 3x1 + 2x2, resolvido por duas fases | Resposta certa; entradas erradas no meio (3.2) |
| Atividade 2 (2 fotos) | Atividade 2: dual de Min Z = 5x1 + 2x2 + x3, resolvido por Simplex | Resposta certa; coluna yf3 errada (3.3) |

## 2. Como o caderno ensina (corrigido)

### 2.1 Formulação (p01 a p04)

Um problema de programação matemática tem:

- uma **função objetivo** em valor monetário, para maximizar (lucro) ou minimizar (custo);
- **restrições técnicas**: inequações (≤ ou ≥) ou equações;
- a **não negatividade**: as variáveis nunca são negativas.

Cada variável é a **quantidade** de algo que se decide (quantos biombos, quantos kg). Nas páginas 02 a 04 o caderno define a variável como o recurso ("x1 = madeira", "x1 = tempo de montagem", "x1 = peso"); isso está errado.

Modelos corrigidos (o caderno não resolve nenhum deles):

**p01 — Mistura de carnes** (1 kg de mistura, custo mínimo, no máximo 25% de gordura; gado R$ 80/kg com 20% de gordura, porco R$ 60/kg com 32%)

```
x1 = kg de carne de gado      x2 = kg de carne de porco

Min Z = 80x1 + 60x2
0,20x1 + 0,32x2 ≤ 0,25        (gordura)
x1 + x2 = 1                   (1 kg de mistura)
x1, x2 ≥ 0
```

**p02 — Carpinteiro** (6 peças de madeira e 28 h de trabalho; modelo I: 2 peças, 7 h, R$ 120; modelo II: 1 peça, 8 h, R$ 80)

```
x1 = biombos do modelo I      x2 = biombos do modelo II

Max Z = 120x1 + 80x2
2x1 + x2 ≤ 6                  (peças de madeira)
7x1 + 8x2 ≤ 28                (horas de trabalho)
x1, x2 ≥ 0
```

**p03 — Consoles** (4 modelos; montagem de 4, 5, 3 e 5 h; decoração de 2; 1,5; 3 e 3 h; lucros de 7, 7, 6 e 9 dólares; 30 000 h de montagem e 20 000 h de decoração)

```
xi = consoles do modelo i (i = 1, 2, 3, 4)

Max Z = 7x1 + 7x2 + 6x3 + 9x4
4x1 + 5x2 + 3x3 + 5x4 ≤ 30000        (montagem)
2x1 + 1,5x2 + 3x3 + 3x4 ≤ 20000      (decoração)
x1, x2, x3, x4 ≥ 0
```

**p04 — Mochila** (capacidade de 60 libras; pesos 52, 23, 35, 15 e 7; valores 100, 60, 70, 15 e 15)

```
xi = quanto do item i vai na mochila (1 = o item inteiro, 0 = nada)

Max Z = 100x1 + 60x2 + 70x3 + 15x4 + 15x5
52x1 + 23x2 + 35x3 + 15x4 + 7x5 ≤ 60
x1 ≤ 1;  x2 ≤ 1;  x3 ≤ 1;  x4 ≤ 1;  x5 ≤ 1
x1, x2, x3, x4, x5 ≥ 0
```

### 2.2 Método gráfico (p05 a p07 e p18) — só com 2 variáveis

1. Monte o modelo.
2. Troque cada inequação por uma equação.
3. Em cada equação, faça x1 = 0 e depois x2 = 0 para achar os dois pontos de corte com os eixos, e trace a reta.
4. Teste o ponto P(0, 0) em cada inequação (se a reta passar pela origem, teste P(1, 0); se ele também estiver na reta, teste P(0, 1)). Se a inequação for verdadeira, vale o lado da reta que contém o ponto; se for falsa, esse lado é excluído.
5. A região que sobra tem infinitos pontos viáveis, e o ótimo está num vértice: na maximização, o de maior Z; na minimização, o de menor Z. O caderno acha esse vértice traçando uma reta da função objetivo (por exemplo, 2x1 + 3x2 = 6) e deslocando-a paralelamente até o último vértice da região. Também mostra o vetor gradiente u = (∂Z/∂x1, ∂Z/∂x2) e um vetor v ortogonal a ele (u · v = 0), que dá a direção da reta.
6. As coordenadas do vértice saem do sistema das duas retas, por eliminação: multiplique uma equação por -1 e some com a outra. Depois calcule Z.

### 2.3 Método Simplex (p08, p09 e p11)

1. Formule o modelo.
2. Na função objetivo, passe as variáveis para o lado esquerdo, igualando a zero: `Z - 2x1 - 3x2 = 0`.
3. Em cada restrição ≤, some uma variável de folga (xf1, xf2, …).
4. Monte o quadro: linha Z em cima, uma linha por restrição, coluna bn (termos independentes) à direita.
5. Coluna pivô: o número mais negativo da linha Z. Empate: a coluna mais à esquerda.
6. Linha pivô: divida o bn de cada restrição pelo elemento da coluna pivô, só quando esse elemento for positivo (elemento zero ou negativo não entra). A menor razão define a linha pivô; empate: a linha mais acima. O pivô nunca é negativo (p11).
7. Pivoteamento: divida a linha pivô pelo pivô. Depois zere o resto da coluna pivô: cada outra linha recebe ela mesma mais (o oposto do seu número na coluna pivô) × (a nova linha pivô).
8. Enquanto houver número negativo na linha Z, volte ao passo 5. Só pare quando não houver nenhum.
9. O quadro só começa direto quando todas as restrições são ≤ com lado direito ≥ 0, porque aí as folgas formam a matriz identidade (p09). Nos outros casos, use as duas fases (2.4).

Leitura do quadro final: **variável básica é a que tem coluna unitária** (um 1 numa linha de restrição e 0 em todo o resto, inclusive na linha Z); o valor dela é o bn dessa linha. As outras são não básicas e valem 0. Z é o bn da linha Z. O caderno (p11 e p13) diz que "básicas são as variáveis da função objetivo e não básicas são as de folga": está errado, e uma folga pode ser básica.

Casos especiais:

- No ótimo, uma variável não básica com 0 na linha Z indica outras soluções ótimas com o mesmo Z.
- Uma coluna pivô sem nenhum elemento positivo indica problema ilimitado: Z cresce sem limite.

### 2.4 Método das duas fases (atividade 1)

1. Restrição com lado direito negativo: multiplique por -1 (o sinal ≤/≥ inverte).
2. Restrição ≤ ganha folga (+xf). Restrição ≥ ganha excesso (-xf) e artificial (+a). Restrição = ganha só artificial (+a). Folga e excesso levam o número da restrição (xf2 é da restrição 2); as artificiais são a1, a2, … na ordem das restrições.
3. Fase 1: Min W = soma das artificiais. Isole cada artificial na sua restrição, some tudo e passe para a esquerda; isso dá a linha -W (LW), que fica embaixo do quadro. A álgebra completa está no exemplo 3.2.
4. Na Fase 1 entra o mais negativo da LW (coluna de artificial nunca entra), com as mesmas regras de razão. A linha Z também é atualizada em cada pivoteamento.
5. Fim da Fase 1: a LW não tem negativo fora das colunas artificiais. Se o bn da LW não for 0, W > 0 e o problema não tem solução viável. Se for 0, segue.
6. Se uma artificial ficou na base (com valor 0), ela sai por um pivoteamento na primeira coluna não artificial com elemento diferente de 0 na linha dela; aqui o pivô pode ser negativo, porque o bn dessa linha é 0. Se essa linha só tiver zeros fora das artificiais, a restrição é redundante e a linha sai do quadro.
7. Fase 2: retire a LW e as colunas artificiais e continue o Simplex com a linha Z.

### 2.5 Minimização

Min Z é o mesmo que Max (-Z). A linha da função objetivo fica `-Z + c1x1 + c2x2 + … = 0` (a coluna Z tem -1), e valem as mesmas regras da maximização: entra o mais negativo, e o Simplex para quando não houver negativo. No fim a linha Z diz `-Z = bn`, então Z = -(bn).

Regra do `prompt.md`: quando a questão não diz o método e o Min só tem restrições ≥, com todos os coeficientes da função objetivo ≥ 0, ele é resolvido pelo dual (um Max com restrições ≤, que sai no Simplex comum), como na p21 e na atividade 2.

### 2.6 Dualidade (p20 e p21)

A todo problema de maximização (o primal) corresponde um problema de minimização (o dual), e vice-versa. Os dois têm o mesmo valor ótimo da função objetivo.

Regras do caderno, na forma padrão (Max só com ≤, ou Min só com ≥; variáveis ≥ 0):

- I. A função objetivo do dual é montada com os termos independentes (bn) das restrições do primal.
- II. A 1ª restrição do primal gera y1, a 2ª gera y2, e assim por diante.
- III. As restrições do dual são montadas com os coeficientes de cada variável do primal (coluna por coluna); o lado direito de cada uma é o coeficiente dessa variável na função objetivo do primal; o sinal da desigualdade inverte.
- IV. Se o primal é de maximização, o dual é de minimização, e vice-versa.

Fora da forma padrão, o sinal de cada variável dual vem desta tabela (cada restrição de um problema corresponde a uma variável do outro):

| No problema de Max | No problema de Min |
|---|---|
| restrição ≤ | variável ≥ 0 |
| restrição ≥ | variável ≤ 0 |
| restrição = | variável livre |
| variável ≥ 0 | restrição ≥ |
| variável ≤ 0 | restrição ≤ |
| variável livre | restrição = |

O `resolver.py` monta o dual em qualquer um desses casos (`resolver: montar_dual`), mas só resolve o dual quando o primal está na forma padrão.

Solução do primal a partir do dual: no quadro final do dual, a linha Z tem, na coluna da folga (ou do excesso) da restrição j do dual, o valor de xj. Na atividade 2, por exemplo, a linha Z final tem 0, 5/2 e 25/2 nas colunas yf1, yf2 e yf3, então x1 = 0, x2 = 5/2 e x3 = 25/2.

Exemplo do caderno (p21), que é a atividade 1:

```
PRIMAL                                DUAL
Max Z = 3x1 + 2x2                     Min Z1 = 3y1 + y2 + 3y3
y1 → 0,5x1 + 0,3x2 ≤ 3                0,5y1 + 0,1y2 + 0,4y3 ≥ 3     (coluna de x1)
y2 → 0,1x1 + 0,2x2 ≤ 1                0,3y1 + 0,2y2 + 0,5y3 ≥ 2     (coluna de x2)
y3 → 0,4x1 + 0,5x2 ≤ 3                y1, y2, y3 ≥ 0
x1, x2 ≥ 0
```

Na foto da p21, a 3ª restrição do primal está escrita `0,4x1 + 0,3x2 ≤ 3`, mas o dual ao lado usa `0,5y3`. O certo é `0,5x2`, como na atividade 1.

### 2.7 Como a resolução fica no papel

1. Modelo com uma chave agrupando as restrições.
2. Função objetivo igualada a zero e restrições com folga.
3. Quadro com as colunas Z | variáveis | folgas | bn, a linha Z em cima e um traço vertical antes do bn. Nas duas fases aparecem as artificiais e a linha -W embaixo.
4. Coluna pivô circulada (um oval em volta da coluna) e pivô circulado.
5. Razões escritas abaixo do quadro (`9/3 = 3   4/2 = 2   6/1 = 6`); razão com divisor negativo é descartada.
6. `÷ 2` ao lado da linha pivô.
7. Dois quadros por iteração: primeiro só a linha pivô dividida (as outras copiadas iguais), com setas saindo dela para cada outra linha, cada seta com o multiplicador circulado e um "+"; depois o quadro com todas as linhas atualizadas.
8. Contas de fração no canto da página: `2 - 2/3 = (6 - 2)/3 = 4/3`.
9. No fim, os valores das variáveis, Z calculado por substituição e o resultado dentro de uma caixa.

A saída do `resolver.py` segue essa ordem e já vem no formato do papel, dentro de um único quadro de texto, e não há nada fora dele: tudo o que sai se copia (a legenda das marcas está no README). Os quadros vêm com grade, para facilitar a leitura das colunas. `(3)` é o número a circular, junto com a coluna dele; `÷3` vai ao lado da linha pivô; `← (4)` é a seta saindo da linha pivô até a linha, com o 4 circulado; `→ x1 = 9/4` é a leitura do quadro final, saindo do b da linha; e a caixa desenhada é a caixa do resultado. Quando o pivô já é 1, não há quadro só com a linha dividida: as setas vão no próprio quadro do pivô. As contas de fração do item 8 não aparecem, porque os números dos quadros já vêm calculados.

## 3. Exemplos resolvidos

### 3.1 Simplex: Max Z = 3x1 + 4x2 (p16 a p18)

O caderno resolve este exemplo corretamente. Arquivo da questão:

```
max Z = 3x1 + 4x2
2x1 + x2 <= 6
2x1 + 3x2 <= 9
x1, x2 >= 0
resolver: primal
```

Saída do `resolver.py`:

```text
Max Z = 3x1 + 4x2
{ 2x1 + x2 ≤ 6
{ 2x1 + 3x2 ≤ 9
{ x1, x2 ≥ 0

Z - 3x1 - 4x2 = 0
{ 2x1 + x2 + xf1 = 6
{ 2x1 + 3x2 + xf2 = 9

┌───┬────┬─────┬─────┬─────┬───┐
│ Z │ x1 │  x2 │ xf1 │ xf2 │ b │
├───┼────┼─────┼─────┼─────┼───┤
│ 1 │ -3 │  -4 │  0  │  0  │ 0 │
│ 0 │ 2  │  1  │  1  │  0  │ 6 │
│ 0 │ 2  │ (3) │  0  │  1  │ 9 │  ÷3
└───┴────┴─────┴─────┴─────┴───┘
razões: 6/1 = 6   9/3 = 3

┌───┬─────┬─────┬─────┬─────┬───┐
│ Z │  x1 │  x2 │ xf1 │ xf2 │ b │
├───┼─────┼─────┼─────┼─────┼───┤
│ 1 │  -3 │  -4 │  0  │  0  │ 0 │  ← (4)
│ 0 │  2  │  1  │  1  │  0  │ 6 │  ← (-1)
│ 0 │ 2/3 │ (1) │  0  │ 1/3 │ 3 │
└───┴─────┴─────┴─────┴─────┴───┘

┌───┬───────┬────┬─────┬──────┬────┐
│ Z │   x1  │ x2 │ xf1 │ xf2  │ b  │
├───┼───────┼────┼─────┼──────┼────┤
│ 1 │  -1/3 │ 0  │  0  │ 4/3  │ 12 │
│ 0 │ (4/3) │ 0  │  1  │ -1/3 │ 3  │  ÷4/3
│ 0 │  2/3  │ 1  │  0  │ 1/3  │ 3  │
└───┴───────┴────┴─────┴──────┴────┘
razões: 3 ÷ 4/3 = 9/4 = 2,25   3 ÷ 2/3 = 9/2 = 4,5

┌───┬──────┬────┬─────┬──────┬─────┐
│ Z │  x1  │ x2 │ xf1 │ xf2  │  b  │
├───┼──────┼────┼─────┼──────┼─────┤
│ 1 │ -1/3 │ 0  │  0  │ 4/3  │  12 │  ← (1/3)
│ 0 │ (1)  │ 0  │ 3/4 │ -1/4 │ 9/4 │
│ 0 │ 2/3  │ 1  │  0  │ 1/3  │  3  │  ← (-2/3)
└───┴──────┴────┴─────┴──────┴─────┘

┌───┬────┬────┬──────┬──────┬──────┐
│ Z │ x1 │ x2 │ xf1  │ xf2  │  b   │
├───┼────┼────┼──────┼──────┼──────┤
│ 1 │ 0  │ 0  │ 1/4  │ 5/4  │ 51/4 │  → Z = 51/4 = 12,75
│ 0 │ 1  │ 0  │ 3/4  │ -1/4 │ 9/4  │  → x1 = 9/4 = 2,25
│ 0 │ 0  │ 1  │ -1/2 │ 1/2  │ 3/2  │  → x2 = 3/2 = 1,5
└───┴────┴────┴──────┴──────┴──────┘
linha Z sem negativo → solução ótima

x1 = 9/4 = 2,25
x2 = 3/2 = 1,5

Z = 3x1 + 4x2
Z = 3 · 9/4 + 4 · 3/2
Z = 27/4 + 6
Z = 27/4 + 24/4
┌──────────────────┐
│ Z = 51/4 = 12,75 │
└──────────────────┘
```

### 3.2 Duas fases: atividade 1 (dual de Max Z = 3x1 + 2x2)

Arquivo da questão:

```
max Z = 3x1 + 2x2
0,5x1 + 0,3x2 <= 3
0,1x1 + 0,2x2 <= 1
0,4x1 + 0,5x2 <= 3
x1, x2 >= 0
resolver: dual
```

Saída do `resolver.py`:

```text
Max Z = 3x1 + 2x2         Min Z1 = 3y1 + y2 + 3y3
{ 0,5x1 + 0,3x2 ≤ 3   →   { 0,5y1 + 0,1y2 + 0,4y3 ≥ 3
{ 0,1x1 + 0,2x2 ≤ 1       { 0,3y1 + 0,2y2 + 0,5y3 ≥ 2
{ 0,4x1 + 0,5x2 ≤ 3       { y1, y2, y3 ≥ 0
{ x1, x2 ≥ 0

decimais em fração: 0,5 = 1/2; 0,1 = 1/10; 0,4 = 2/5; 0,3 = 3/10; 0,2 = 1/5

-Z1 + 3y1 + y2 + 3y3 = 0
{ 0,5y1 + 0,1y2 + 0,4y3 - yf1 + a1 = 3
{ 0,3y1 + 0,2y2 + 0,5y3 - yf2 + a2 = 2

Min W = a1 + a2
a1 = 3 - 0,5y1 - 0,1y2 - 0,4y3 + yf1
a2 = 2 - 0,3y1 - 0,2y2 - 0,5y3 + yf2
W = a1 + a2 = 5 - 0,8y1 - 0,3y2 - 0,9y3 + yf1 + yf2
-W = -5 + 0,8y1 + 0,3y2 + 0,9y3 - yf1 - yf2
-W - 0,8y1 - 0,3y2 - 0,9y3 + yf1 + yf2 = -5

Fase 1

┌────┬──────┬───────┬───────┬─────┬─────┬────┬────┬────┐
│ Z1 │  y1  │   y2  │   y3  │ yf1 │ yf2 │ a1 │ a2 │ b  │
├────┼──────┼───────┼───────┼─────┼─────┼────┼────┼────┤
│ -1 │  3   │   1   │   3   │  0  │  0  │ 0  │ 0  │ 0  │
│ 0  │ 1/2  │  1/10 │  2/5  │  -1 │  0  │ 1  │ 0  │ 3  │
│ 0  │ 3/10 │  1/5  │ (1/2) │  0  │  -1 │ 0  │ 1  │ 2  │  ÷1/2
├────┼──────┼───────┼───────┼─────┼─────┼────┼────┼────┤
│ -W │ -4/5 │ -3/10 │ -9/10 │  1  │  1  │ 0  │ 0  │ -5 │
└────┴──────┴───────┴───────┴─────┴─────┴────┴────┴────┘
razões: 3 ÷ 2/5 = 15/2 = 7,5   2 ÷ 1/2 = 4

┌────┬──────┬───────┬───────┬─────┬─────┬────┬────┬────┐
│ Z1 │  y1  │   y2  │   y3  │ yf1 │ yf2 │ a1 │ a2 │ b  │
├────┼──────┼───────┼───────┼─────┼─────┼────┼────┼────┤
│ -1 │  3   │   1   │   3   │  0  │  0  │ 0  │ 0  │ 0  │  ← (-3)
│ 0  │ 1/2  │  1/10 │  2/5  │  -1 │  0  │ 1  │ 0  │ 3  │  ← (-2/5)
│ 0  │ 3/5  │  2/5  │  (1)  │  0  │  -2 │ 0  │ 2  │ 4  │
├────┼──────┼───────┼───────┼─────┼─────┼────┼────┼────┤
│ -W │ -4/5 │ -3/10 │ -9/10 │  1  │  1  │ 0  │ 0  │ -5 │  ← (9/10)
└────┴──────┴───────┴───────┴─────┴─────┴────┴────┴────┘

┌────┬────────┬───────┬────┬─────┬───────┬────┬──────┬──────┐
│ Z1 │   y1   │   y2  │ y3 │ yf1 │  yf2  │ a1 │  a2  │  b   │
├────┼────────┼───────┼────┼─────┼───────┼────┼──────┼──────┤
│ -1 │  6/5   │  -1/5 │ 0  │  0  │   6   │ 0  │  -6  │ -12  │
│ 0  │ 13/50  │ -3/50 │ 0  │  -1 │ (4/5) │ 1  │ -4/5 │ 7/5  │  ÷4/5
│ 0  │  3/5   │  2/5  │ 1  │  0  │   -2  │ 0  │  2   │  4   │
├────┼────────┼───────┼────┼─────┼───────┼────┼──────┼──────┤
│ -W │ -13/50 │  3/50 │ 0  │  1  │  -4/5 │ 0  │ 9/5  │ -7/5 │
└────┴────────┴───────┴────┴─────┴───────┴────┴──────┴──────┘
razões: 7/5 ÷ 4/5 = 7/4 = 1,75

┌────┬────────┬───────┬────┬──────┬──────┬─────┬─────┬──────┐
│ Z1 │   y1   │   y2  │ y3 │ yf1  │ yf2  │  a1 │  a2 │  b   │
├────┼────────┼───────┼────┼──────┼──────┼─────┼─────┼──────┤
│ -1 │  6/5   │  -1/5 │ 0  │  0   │  6   │  0  │  -6 │ -12  │  ← (-6)
│ 0  │ 13/40  │ -3/40 │ 0  │ -5/4 │ (1)  │ 5/4 │  -1 │ 7/4  │
│ 0  │  3/5   │  2/5  │ 1  │  0   │  -2  │  0  │  2  │  4   │  ← (2)
├────┼────────┼───────┼────┼──────┼──────┼─────┼─────┼──────┤
│ -W │ -13/50 │  3/50 │ 0  │  1   │ -4/5 │  0  │ 9/5 │ -7/5 │  ← (4/5)
└────┴────────┴───────┴────┴──────┴──────┴─────┴─────┴──────┘

┌────┬───────┬───────┬────┬──────┬─────┬───────┬────┬───────┐
│ Z1 │   y1  │   y2  │ y3 │ yf1  │ yf2 │   a1  │ a2 │   b   │
├────┼───────┼───────┼────┼──────┼─────┼───────┼────┼───────┤
│ -1 │  -3/4 │  1/4  │ 0  │ 15/2 │  0  │ -15/2 │ 0  │ -45/2 │
│ 0  │ 13/40 │ -3/40 │ 0  │ -5/4 │  1  │  5/4  │ -1 │  7/4  │
│ 0  │  5/4  │  1/4  │ 1  │ -5/2 │  0  │  5/2  │ 0  │  15/2 │
├────┼───────┼───────┼────┼──────┼─────┼───────┼────┼───────┤
│ -W │   0   │   0   │ 0  │  0   │  0  │   1   │ 1  │   0   │
└────┴───────┴───────┴────┴──────┴─────┴───────┴────┴───────┘
W = 0 → fim da Fase 1

Fase 2 (sem a linha -W e sem as colunas a1, a2)

┌────┬─────────┬───────┬────┬──────┬─────┬───────┐
│ Z1 │    y1   │   y2  │ y3 │ yf1  │ yf2 │   b   │
├────┼─────────┼───────┼────┼──────┼─────┼───────┤
│ -1 │   -3/4  │  1/4  │ 0  │ 15/2 │  0  │ -45/2 │
│ 0  │ (13/40) │ -3/40 │ 0  │ -5/4 │  1  │  7/4  │  ÷13/40
│ 0  │   5/4   │  1/4  │ 1  │ -5/2 │  0  │  15/2 │
└────┴─────────┴───────┴────┴──────┴─────┴───────┘
razões: 7/4 ÷ 13/40 = 70/13 ≈ 5,38   15/2 ÷ 5/4 = 6

┌────┬──────┬───────┬────┬────────┬───────┬───────┐
│ Z1 │  y1  │   y2  │ y3 │  yf1   │  yf2  │   b   │
├────┼──────┼───────┼────┼────────┼───────┼───────┤
│ -1 │ -3/4 │  1/4  │ 0  │  15/2  │   0   │ -45/2 │  ← (3/4)
│ 0  │ (1)  │ -3/13 │ 0  │ -50/13 │ 40/13 │ 70/13 │
│ 0  │ 5/4  │  1/4  │ 1  │  -5/2  │   0   │  15/2 │  ← (-5/4)
└────┴──────┴───────┴────┴────────┴───────┴───────┘

┌────┬────┬───────┬────┬────────┬────────┬─────────┐
│ Z1 │ y1 │   y2  │ y3 │  yf1   │  yf2   │    b    │
├────┼────┼───────┼────┼────────┼────────┼─────────┤
│ -1 │ 0  │  1/13 │ 0  │ 60/13  │ 30/13  │ -240/13 │  → -Z1 = -240/13 → Z1 = 240/13 ≈ 18,46
│ 0  │ 1  │ -3/13 │ 0  │ -50/13 │ 40/13  │  70/13  │  → y1 = 70/13 ≈ 5,38
│ 0  │ 0  │  7/13 │ 1  │ 30/13  │ -50/13 │  10/13  │  → y3 = 10/13 ≈ 0,77
└────┴────┴───────┴────┴────────┴────────┴─────────┘
linha Z1 sem negativo → solução ótima

x1 = 60/13 ≈ 4,62 (linha Z1, coluna yf1)
x2 = 30/13 ≈ 2,31 (linha Z1, coluna yf2)

Z = 3x1 + 2x2
Z = 3 · 60/13 + 2 · 30/13
Z = 180/13 + 60/13
┌────────────────────┐
│ Z = 240/13 ≈ 18,46 │
└────────────────────┘
```

O que a foto da atividade 1 tem de diferente:

- Na 2ª iteração ela fez entrar y1 (-13/50), mas o mais negativo da LW era yf2 (-4/5). A regra é entrar o mais negativo, como acima.
- A coluna a2 está com o sinal trocado desde o 2º quadro.
- A Fase 1 termina com bn da LW = 6/65; o certo é 0.
- Ela escreve y1 = 5,37; o certo é 70/13 ≈ 5,38.
- Ela não dá a solução do primal (x1 e x2).

### 3.3 Minimização pelo dual: atividade 2 (Min Z = 5x1 + 2x2 + x3)

Arquivo da questão:

```
min Z = 5x1 + 2x2 + x3
2x1 + 3x2 + x3 >= 20
6x1 + 8x2 + 5x3 >= 30
7x1 + x2 + 3x3 >= 40
x1 + 2x2 + 4x3 >= 50
x1, x2, x3 >= 0
resolver: dual
```

Saída do `resolver.py`:

```text
Min Z = 5x1 + 2x2 + x3       Max Z1 = 20y1 + 30y2 + 40y3 + 50y4
{ 2x1 + 3x2 + x3 ≥ 20    →   { 2y1 + 6y2 + 7y3 + y4 ≤ 5
{ 6x1 + 8x2 + 5x3 ≥ 30       { 3y1 + 8y2 + y3 + 2y4 ≤ 2
{ 7x1 + x2 + 3x3 ≥ 40        { y1 + 5y2 + 3y3 + 4y4 ≤ 1
{ x1 + 2x2 + 4x3 ≥ 50        { y1, y2, y3, y4 ≥ 0
{ x1, x2, x3 ≥ 0

Z1 - 20y1 - 30y2 - 40y3 - 50y4 = 0
{ 2y1 + 6y2 + 7y3 + y4 + yf1 = 5
{ 3y1 + 8y2 + y3 + 2y4 + yf2 = 2
{ y1 + 5y2 + 3y3 + 4y4 + yf3 = 1

┌────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬───┐
│ Z1 │  y1 │  y2 │  y3 │  y4 │ yf1 │ yf2 │ yf3 │ b │
├────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼───┤
│ 1  │ -20 │ -30 │ -40 │ -50 │  0  │  0  │  0  │ 0 │
│ 0  │  2  │  6  │  7  │  1  │  1  │  0  │  0  │ 5 │
│ 0  │  3  │  8  │  1  │  2  │  0  │  1  │  0  │ 2 │
│ 0  │  1  │  5  │  3  │ (4) │  0  │  0  │  1  │ 1 │  ÷4
└────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴───┘
razões: 5/1 = 5   2/2 = 1   1/4 = 0,25

┌────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┐
│ Z1 │  y1 │  y2 │  y3 │  y4 │ yf1 │ yf2 │ yf3 │  b  │
├────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤
│ 1  │ -20 │ -30 │ -40 │ -50 │  0  │  0  │  0  │  0  │  ← (50)
│ 0  │  2  │  6  │  7  │  1  │  1  │  0  │  0  │  5  │  ← (-1)
│ 0  │  3  │  8  │  1  │  2  │  0  │  1  │  0  │  2  │  ← (-2)
│ 0  │ 1/4 │ 5/4 │ 3/4 │ (1) │  0  │  0  │ 1/4 │ 1/4 │
└────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┘

┌────┬───────┬──────┬──────┬────┬─────┬─────┬──────┬──────┐
│ Z1 │   y1  │  y2  │  y3  │ y4 │ yf1 │ yf2 │ yf3  │  b   │
├────┼───────┼──────┼──────┼────┼─────┼─────┼──────┼──────┤
│ 1  │ -15/2 │ 65/2 │ -5/2 │ 0  │  0  │  0  │ 25/2 │ 25/2 │
│ 0  │  7/4  │ 19/4 │ 25/4 │ 0  │  1  │  0  │ -1/4 │ 19/4 │
│ 0  │ (5/2) │ 11/2 │ -1/2 │ 0  │  0  │  1  │ -1/2 │ 3/2  │  ÷5/2
│ 0  │  1/4  │ 5/4  │ 3/4  │ 1  │  0  │  0  │ 1/4  │ 1/4  │
└────┴───────┴──────┴──────┴────┴─────┴─────┴──────┴──────┘
razões: 19/4 ÷ 7/4 = 19/7 ≈ 2,71   3/2 ÷ 5/2 = 3/5 = 0,6   1/4 ÷ 1/4 = 1

┌────┬───────┬──────┬──────┬────┬─────┬─────┬──────┬──────┐
│ Z1 │   y1  │  y2  │  y3  │ y4 │ yf1 │ yf2 │ yf3  │  b   │
├────┼───────┼──────┼──────┼────┼─────┼─────┼──────┼──────┤
│ 1  │ -15/2 │ 65/2 │ -5/2 │ 0  │  0  │  0  │ 25/2 │ 25/2 │  ← (15/2)
│ 0  │  7/4  │ 19/4 │ 25/4 │ 0  │  1  │  0  │ -1/4 │ 19/4 │  ← (-7/4)
│ 0  │  (1)  │ 11/5 │ -1/5 │ 0  │  0  │ 2/5 │ -1/5 │ 3/5  │
│ 0  │  1/4  │ 5/4  │ 3/4  │ 1  │  0  │  0  │ 1/4  │ 1/4  │  ← (-1/4)
└────┴───────┴──────┴──────┴────┴─────┴─────┴──────┴──────┘

┌────┬────┬──────┬───────┬────┬─────┬───────┬──────┬───────┐
│ Z1 │ y1 │  y2  │   y3  │ y4 │ yf1 │  yf2  │ yf3  │   b   │
├────┼────┼──────┼───────┼────┼─────┼───────┼──────┼───────┤
│ 1  │ 0  │  49  │   -4  │ 0  │  0  │   3   │  11  │   17  │
│ 0  │ 0  │ 9/10 │  33/5 │ 0  │  1  │ -7/10 │ 1/10 │ 37/10 │
│ 0  │ 1  │ 11/5 │  -1/5 │ 0  │  0  │  2/5  │ -1/5 │  3/5  │
│ 0  │ 0  │ 7/10 │ (4/5) │ 1  │  0  │ -1/10 │ 3/10 │  1/10 │  ÷4/5
└────┴────┴──────┴───────┴────┴─────┴───────┴──────┴───────┘
razões: 37/10 ÷ 33/5 = 37/66 ≈ 0,56   1/10 ÷ 4/5 = 1/8 = 0,125

┌────┬────┬──────┬──────┬─────┬─────┬───────┬──────┬───────┐
│ Z1 │ y1 │  y2  │  y3  │  y4 │ yf1 │  yf2  │ yf3  │   b   │
├────┼────┼──────┼──────┼─────┼─────┼───────┼──────┼───────┤
│ 1  │ 0  │  49  │  -4  │  0  │  0  │   3   │  11  │   17  │  ← (4)
│ 0  │ 0  │ 9/10 │ 33/5 │  0  │  1  │ -7/10 │ 1/10 │ 37/10 │  ← (-33/5)
│ 0  │ 1  │ 11/5 │ -1/5 │  0  │  0  │  2/5  │ -1/5 │  3/5  │  ← (1/5)
│ 0  │ 0  │ 7/8  │ (1)  │ 5/4 │  0  │  -1/8 │ 3/8  │  1/8  │
└────┴────┴──────┴──────┴─────┴─────┴───────┴──────┴───────┘

┌────┬────┬───────┬────┬───────┬─────┬──────┬───────┬──────┐
│ Z1 │ y1 │   y2  │ y3 │   y4  │ yf1 │ yf2  │  yf3  │  b   │
├────┼────┼───────┼────┼───────┼─────┼──────┼───────┼──────┤
│ 1  │ 0  │ 105/2 │ 0  │   5   │  0  │ 5/2  │  25/2 │ 35/2 │  → Z1 = 35/2 = 17,5
│ 0  │ 0  │ -39/8 │ 0  │ -33/4 │  1  │ 1/8  │ -19/8 │ 23/8 │  → yf1 = 23/8 = 2,875
│ 0  │ 1  │  19/8 │ 0  │  1/4  │  0  │ 3/8  │  -1/8 │ 5/8  │  → y1 = 5/8 = 0,625
│ 0  │ 0  │  7/8  │ 1  │  5/4  │  0  │ -1/8 │  3/8  │ 1/8  │  → y3 = 1/8 = 0,125
└────┴────┴───────┴────┴───────┴─────┴──────┴───────┴──────┘
linha Z1 sem negativo → solução ótima

x1 = 0 (linha Z1, coluna yf1)
x2 = 5/2 = 2,5 (linha Z1, coluna yf2)
x3 = 25/2 = 12,5 (linha Z1, coluna yf3)

Z = 5x1 + 2x2 + x3
Z = 2 · 5/2 + 25/2
Z = 5 + 25/2
Z = 10/2 + 25/2
┌─────────────────┐
│ Z = 35/2 = 17,5 │
└─────────────────┘
```

O que as fotos da atividade 2 têm de diferente:

- A coluna yf3 está errada a partir do 5º quadro (14 no lugar de 11 na linha Z), até o fim (15 no lugar de 25/2). Quem lesse a solução do primal na foto tiraria x3 = 15, que está errado.
- Na linha Z final, coluna y2: 103/2 no lugar de 105/2. Na L1 final, coluna y4: 33/4 no lugar de -33/4.
- Ela não dá a solução do primal (x1, x2 e x3), que é a resposta da questão.

### 3.4 Outros exemplos do caderno

Para ver a resolução completa de qualquer um, salve o arquivo mostrado e rode o `resolver.py` com ele.

**Max Z = 2x1 + 3x2 (p06, p07 e p10 a p12)**

```
max Z = 2x1 + 3x2
x1 + 3x2 <= 9
-x1 + 2x2 <= 4
x1 + x2 <= 6
x1, x2 >= 0
resolver: primal
```

**Resultado:** x1 = 9/2 = 4,5; x2 = 3/2 = 1,5; Z = 27/2 = 13,5

O caderno parou no 5º quadro, que ainda tem um negativo na linha Z (coluna xf2; ele escreveu -0,9 e o certo é -3/5). A resposta dele, Z = 10,2 (x1 = 1,2; x2 = 2,6), é um vértice da região, mas não o ótimo. O próprio método gráfico do caderno (p07) dá Z = 13,5.

**Max Z = 2x1 + x2 + x3 (p12 e p13)**

```
max Z = 2x1 + x2 + x3
x1 + x2 + x3 <= 50
2x1 + x2 + 2x3 <= 60
3x1 + x2 <= 93
x1, x2, x3 >= 0
resolver: primal
```

**Resultado:** x1 = 30; x2 = 0; x3 = 0; Z = 60

Observação: x2 é não básica e tem 0 na LZ → há outras soluções ótimas com o mesmo Z.

As contas do caderno estão certas, mas ele chama x1, x2 e x3 de básicas e as folgas de não básicas. No quadro final, as básicas são x1, xf1 e xf3.

**Max Z = 10x1 + 11x2 (p13 a p15)**

```
max Z = 10x1 + 11x2
x1 + 2x2 <= 150
3x1 + 4x2 <= 200
6x1 + x2 <= 175
x1, x2 >= 0
resolver: primal
```

**Resultado:** x1 = 500/21 ≈ 23,81; x2 = 225/7 ≈ 32,14; Z = 1775/3 ≈ 591,67

O último quadro do caderno (p15) não foi calculado: as restrições foram copiadas do quadro anterior e a linha Z ficou com bn = -2200/7. A 2ª restrição é ≤: na foto da p13 o sinal está mal escrito, e a resolução do caderno na p14 usa folga nessa restrição.

**Max Z = 2x1 + 10x2 + x3 (p19)**

```
max Z = 2x1 + 10x2 + x3
5x1 + 2x2 + x3 <= 15
2x1 + x2 + 7x3 <= 20
x1 + 3x2 + 2x3 <= 25
x1, x2, x3 >= 0
resolver: primal
```

**Resultado:** x1 = 0; x2 = 15/2 = 7,5; x3 = 0; Z = 75

A resposta do caderno está certa, mas a última linha do quadro final está com sinais errados (x3 = -1/2, xf3 = 0 e bn = -5/2; o certo é 1/2, 1 e 5/2). Um bn negativo numa linha de restrição é sempre sinal de erro.

## 4. Erros do material original

### 4.1 Caderno

| Página | O que está no caderno | O certo |
|---|---|---|
| p01 | gordura do porco `0,30x2` | `0,32x2` (o texto diz 32%) |
| p02 | `2x1 + 1x1 ≤ 6`; "x1 = madeira", "x1 = 120" | `2x1 + x2 ≤ 6`; x1 e x2 são os biombos de cada modelo; 120 e 80 são os coeficientes de Z |
| p03 | x1 e x2 como "tempo de montagem" e "tempo de decoração"; não negatividade só de x1 e x2 | xi = consoles do modelo i; x1, …, x4 ≥ 0 |
| p04 | `7x5` na função objetivo; "x1 = peso" | `15x5`; xi = quanto do item i vai na mochila |
| p10 a p12 | parou com negativo na linha Z; Z = 10,2 | mais uma iteração: Z = 27/2 = 13,5 |
| p11 e p13 | "básicas são as variáveis da função objetivo; não básicas, as de folga" | básica é a variável com coluna unitária no quadro |
| p15 | último quadro sem pivoteamento | Z = 1775/3 ≈ 591,67 |
| p19 | última linha com x3 = -1/2, xf3 = 0 e bn = -5/2 | 1/2, 1 e 5/2 |
| p21 | primal com `0,3x2` na 3ª restrição e dual com `0,5y3` | `0,5x2`, como na atividade 1 |

### 4.2 Atividades

| Atividade | O que está na foto | O certo |
|---|---|---|
| 1 | na 2ª iteração entra y1 | entra yf2, o mais negativo da LW |
| 1 | coluna a2 com o sinal trocado | ver 3.2 |
| 1 | Fase 1 termina com bn da LW = 6/65 | 0 |
| 1 | y1 = 5,37 | 70/13 ≈ 5,38 |
| 1 | não dá x1 e x2 | x1 = 60/13; x2 = 30/13 |
| 2 | coluna yf3 errada desde o 5º quadro | ver 3.3 |
| 2 | linha Z final: 103/2 em y2; L1 final: 33/4 em y4 | 105/2; -33/4 |
| 2 | não dá x1, x2 e x3 | x1 = 0; x2 = 5/2; x3 = 25/2 |
