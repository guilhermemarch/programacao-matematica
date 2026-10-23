# Programação Matemática

Resolve questões de programação linear (modelagem, Simplex, duas fases e dualidade) com as regras do caderno, em frações exatas, e entrega a resolução pronta para copiar no caderno.

## Como usar

1. Abra uma **conversa nova** num agente que roda comandos no terminal (Codex, Claude Code). Conversa nova importa: pedidos antigos da conversa, como "mostra em tabela", fazem o agente fugir do formato.
2. Anexe a imagem (ou as imagens) das questões e mande o prompt abaixo, sem mudar nada.
3. O agente clona o repositório, roda o `resolver.py` e responde só com os quadros para copiar.

Não use um chat sem terminal, como o ChatGPT na web: ele não consegue rodar o resolver e faz as contas à mão.

### Prompt para o agente

```text
Clone https://github.com/guilhermemarch/programacao-matematica.git (se a pasta já existir, entre nela e rode git pull). Dentro da pasta, leia o prompt.md e siga-o à risca para resolver as questões das imagens anexas: toda conta sai do resolver.py, nunca à mão. Responda só com o que a seção "Resposta" do prompt.md manda: os quadros de texto do resolver, um por questão, sem nada antes, depois ou entre eles.
```

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
