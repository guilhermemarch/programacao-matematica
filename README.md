# Programação Matemática

Resolve questões de programação linear (modelagem, Simplex, duas fases e dualidade) com as regras do caderno, em frações exatas, e entrega a resolução pronta para copiar no caderno.

## Como usar

1. Use um agente que roda comandos no terminal (Codex, Claude Code) com este repositório clonado.
2. Mande a imagem da questão e peça: **"Siga o `prompt.md` deste repositório."**
3. O agente lê a questão, roda o `resolver.py` e devolve a resposta.

Não use um chat sem terminal, como o ChatGPT na web: ele não consegue rodar o resolver e faz as contas à mão.

## O que copiar no caderno

**Tudo o que o agente responde, de cima a baixo.** A resposta é só um quadro de texto por questão, começando por `Questão N`. Confira os números do modelo, no topo do quadro, com os da imagem da questão.

A única exceção é uma linha `⚠ NÃO COPIE — Questão N: ...` fora de quadro: o agente parou nessa questão (dúvida de leitura ou caso não coberto) e não há nada para copiar dela.

Dentro do quadro, as marcas viram desenho no papel:

| No quadro | No caderno |
|---|---|
| grade da tabela | desenhe a tabela com as linhas |
| `(2)` | circule o número e a coluna dele |
| `÷2` ao lado da linha | escreva `÷2` ao lado da linha |
| `← (12)` ao lado da linha | seta saindo da linha do pivô até esta linha, com o 12 circulado |
| `→ y1 = 2` ao lado da linha | seta saindo do b da linha, com o valor |
| caixa desenhada | o resultado dentro de uma caixa |

Exemplo: a Questão 1 (Min Z = 5x1 + 4x2 pelo dual) está inteira no teste `SAIDA_Q1` do `testes.py`. Há outros exemplos na seção 3 da `referencia_resolucoes.md`.

## Arquivos

| Arquivo | Para quê |
|---|---|
| `prompt.md` | Instruções para o agente: passo a passo, formato do arquivo da questão e da resposta. |
| `resolver.py` | Faz as contas e escreve o quadro de copiar. Uso: `python3 resolver.py questoes/q1.txt`. |
| `referencia_resolucoes.md` | Como o caderno ensina (já corrigido), exemplos resolvidos e erros do material original. |
| `testes.py` | Testes do resolver. Rode `python3 testes.py`: tem de terminar com `OK`. |

Precisa só de Python 3.9 ou mais novo, sem bibliotecas extras.
