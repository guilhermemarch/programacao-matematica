"""Resolve problemas de programação linear com as regras do caderno, em frações exatas.

Uso: python3 resolver.py questoes/q1.txt

O formato do arquivo da questão está no prompt.md. A saída é a resolução enxuta em
Markdown, só o que se copia: modelo, forma padrão, um quadro por iteração (com pivô,
razões e operações) e resposta. As contas e a conferência são feitas por dentro.
Quando o caso não é coberto, o resolver para com uma mensagem de erro (código 1).
"""
import re
import sys
from dataclasses import dataclass, field
from fractions import Fraction

MODOS = ("primal", "dual", "ambos", "montar_dual")
MAX_PIVOS = 50
SIMBOLO = {"<=": "≤", ">=": "≥", "=": "="}
INVERSO = {"<=": ">=", ">=": "<=", "=": "="}


class ErroEntrada(Exception):
    """Erro de formato: o arquivo da questão precisa ser corrigido."""


class ErroResolver(Exception):
    """Caso não coberto: a questão não deve ser entregue."""


# ---------- números ----------

def fr(x):
    """Fração irredutível: 2/3, -1/4, 5."""
    x = Fraction(x)
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"


def fp(x):
    """Fração entre parênteses quando é negativa: (-2/5)."""
    return f"({fr(x)})" if x < 0 else fr(x)


def _casas_exatas(x):
    """Casas do decimal exato de x (até 6), ou None quando não há decimal exato."""
    for casas in range(7):
        if (Fraction(x) * 10 ** casas).denominator == 1:
            return casas
    return None


def decimal(x):
    """Decimal com vírgula: exato quando existe (0,125); senão, duas casas arredondadas (5,38)."""
    x = Fraction(x)
    casas = _casas_exatas(abs(x))
    casas = 2 if casas is None else casas
    n = int(abs(x) * 10 ** casas + Fraction(1, 2))
    s = str(n).rjust(casas + 1, "0")
    texto = f"{s[:-casas]},{s[-casas:]}" if casas else s
    return ("-" if x < 0 else "") + texto


def valor_com_decimal(x):
    """'70/13 ≈ 5,38', '1/8 = 0,125', '60'."""
    x = Fraction(x)
    if x.denominator == 1:
        return fr(x)
    return f"{fr(x)} {'=' if _casas_exatas(abs(x)) is not None else '≈'} {decimal(x)}"


def num(x, usa_decimal):
    """Número do modelo: em decimal se o enunciado usa decimais e o valor tem decimal exato."""
    x = Fraction(x)
    if usa_decimal and x.denominator != 1 and _casas_exatas(abs(x)) is not None:
        return decimal(x)
    return fr(x)


def expressao(coefs, nomes, usa_decimal, constante=None):
    """'2x1 + x2 - 0,5x3'. Coeficiente 0 não aparece; a constante, se houver, vem primeiro."""
    partes = [] if constante is None else [num(constante, usa_decimal)]
    for a, nome in zip(coefs, nomes):
        if a == 0:
            continue
        termo = nome if abs(a) == 1 else f"{num(abs(a), usa_decimal)}{nome}"
        if partes:
            partes.append(("- " if a < 0 else "+ ") + termo)
        else:
            partes.append(("-" if a < 0 else "") + termo)
    return " ".join(partes) if partes else "0"


def substituicao(coefs, nomes, valores, usa_decimal):
    """'3 × 9/4 + 4 × 3/2 = 51/4' (os valores vêm do dicionário)."""
    termos = [(a, valores[n]) for a, n in zip(coefs, nomes) if a != 0]
    texto = " + ".join(f"{num(a, usa_decimal) if i == 0 or a > 0 else '(' + num(a, usa_decimal) + ')'} × {fp(v)}"
                       for i, (a, v) in enumerate(termos))
    return f"{texto} = {fr(sum((a * v for a, v in termos), Fraction(0)))}"


# ---------- leitura do arquivo da questão ----------

@dataclass
class Problema:
    sentido: str            # "max" ou "min"
    variaveis: list         # ["x1", "x2", ...]
    c: list                 # coeficientes da função objetivo
    A: list                 # A[i][j]: coeficiente da variável j na restrição i
    ops: list               # "<=", ">=" ou "="
    b: list                 # lados direitos
    modo: str               # "primal", "dual", "ambos" ou "montar_dual"
    nome: str = "Z"         # Z no problema dado, Z1 no dual
    usa_decimal: bool = False
    sinais: list = None     # só no dual montado: ">=0", "<=0" ou "livre" para cada variável

    @property
    def letra(self):
        return self.variaveis[0][0]


_NUM = r"\d+(?:,\d+)?(?:/\d+)?"
_TERMO = re.compile(rf"([+-]?)({_NUM})?([a-z])(\d+)")
_OPERADOR = {"<=": "<=", ">=": ">=", "≤": "<=", "≥": ">=", "=": "="}


def _numero(texto):
    if "/" in texto:
        a, b = texto.split("/")
        return Fraction(a.replace(",", ".")) / Fraction(b)
    return Fraction(texto.replace(",", "."))


def _expressao(texto, n):
    s = texto.replace(" ", "")
    termos, pos = {}, 0
    while pos < len(s):
        m = _TERMO.match(s, pos)
        if not m or (pos > 0 and not m.group(1)):
            raise ErroEntrada(f"linha {n}: não entendi '{texto.strip()}'")
        sinal, numero, letra, indice = m.groups()
        nome = letra + indice
        if nome in termos:
            raise ErroEntrada(f"linha {n}: {nome} aparece duas vezes na mesma linha")
        valor = _numero(numero) if numero else Fraction(1)
        termos[nome] = -valor if sinal == "-" else valor
        pos = m.end()
    if not termos:
        raise ErroEntrada(f"linha {n}: expressão vazia")
    return termos


def ler(texto):
    """Lê o arquivo da questão (formato no prompt.md) e devolve o Problema."""
    objetivo, modo, restricoes, sinais, usa_decimal = None, None, [], set(), False
    for n, bruta in enumerate(texto.splitlines(), 1):
        linha = bruta.split("#")[0].strip()
        if not linha:
            continue
        if "." in linha:
            raise ErroEntrada(f"linha {n}: use vírgula para decimal e não use ponto (nem como separador de milhar)")
        usa_decimal = usa_decimal or re.search(r"\d,\d", linha) is not None
        if objetivo is None:
            m = re.fullmatch(r"(max|min)\s*Z\s*=\s*(.+)", linha, re.IGNORECASE)
            if not m:
                raise ErroEntrada(f"linha {n}: a primeira linha deve ser 'max Z = ...' ou 'min Z = ...'")
            objetivo = (m.group(1).lower(), _expressao(m.group(2), n))
            continue
        m = re.fullmatch(r"resolver:\s*(\S+)", linha)
        if m:
            if modo is not None:
                raise ErroEntrada(f"linha {n}: 'resolver:' aparece duas vezes")
            if m.group(1) not in MODOS:
                raise ErroEntrada(f"linha {n}: o modo deve ser primal, dual, ambos ou montar_dual")
            modo = m.group(1)
            continue
        m = re.fullmatch(r"(.+?)\s*(<=|>=|≤|≥|=)\s*(.+)", linha)
        if not m:
            raise ErroEntrada(f"linha {n}: não entendi '{linha}'")
        esquerda, op, direita = m.group(1), _OPERADOR[m.group(2)], m.group(3).replace(" ", "")
        if re.fullmatch(r"[a-z]\d+(\s*,\s*[a-z]\d+)*", esquerda) and direita == "0":
            if op != ">=":
                raise ErroResolver(f"linha {n}: variável ≤ 0 ou livre não suportada (o resolver só aceita variáveis ≥ 0)")
            sinais |= set(re.split(r"\s*,\s*", esquerda))
            continue
        if not re.fullmatch(rf"[+-]?{_NUM}", direita):
            raise ErroEntrada(f"linha {n}: o lado direito deve ser um número")
        restricoes.append((_expressao(esquerda, n), op, _numero(direita.lstrip("+"))))

    if objetivo is None:
        raise ErroEntrada("falta a linha 'max Z = ...' ou 'min Z = ...'")
    if modo is None:
        raise ErroEntrada("falta a linha 'resolver: primal' (ou dual, ambos, montar_dual)")
    if not restricoes:
        raise ErroEntrada("não há restrições")
    nomes = set(objetivo[1]).union(*(t for t, _, _ in restricoes))
    if len({v[0] for v in nomes}) != 1:
        raise ErroEntrada("todas as variáveis devem usar a mesma letra (x1, x2, ...)")
    if "a" in {v[0] for v in nomes}:
        raise ErroEntrada("não use a letra a nas variáveis (ela é das artificiais)")
    faltam, sobram = sorted(nomes - sinais), sorted(sinais - nomes)
    if faltam:
        raise ErroEntrada(f"falta a condição de sinal de {', '.join(faltam)} (ex.: x1, x2 >= 0)")
    if sobram:
        raise ErroEntrada(f"{', '.join(sobram)} está na condição de sinal, mas não aparece no problema")
    variaveis = sorted(nomes, key=lambda v: int(v[1:]))
    return Problema(
        sentido=objetivo[0],
        variaveis=variaveis,
        c=[objetivo[1].get(v, Fraction(0)) for v in variaveis],
        A=[[t.get(v, Fraction(0)) for v in variaveis] for t, _, _ in restricoes],
        ops=[op for _, op, _ in restricoes],
        b=[b for _, _, b in restricoes],
        modo=modo,
        usa_decimal=usa_decimal,
    )


# ---------- dual ----------

def montar_dual(p):
    """Dual pelas regras do caderno; os sinais das variáveis duais seguem a tabela da referência 2.6."""
    letra = "x" if p.letra == "y" else "y"
    m, n = len(p.b), len(p.c)
    natural = "<=" if p.sentido == "max" else ">="
    return Problema(
        sentido="min" if p.sentido == "max" else "max",
        variaveis=[f"{letra}{i}" for i in range(1, m + 1)],
        c=list(p.b),
        A=[[p.A[i][j] for i in range(m)] for j in range(n)],
        ops=[">=" if p.sentido == "max" else "<="] * n,
        b=list(p.c),
        modo=p.modo,
        nome="Z1",
        usa_decimal=p.usa_decimal,
        sinais=[">=0" if op == natural else "livre" if op == "=" else "<=0" for op in p.ops],
    )


# ---------- quadro e pivoteamento ----------

@dataclass
class Quadro:
    colunas: list   # nomes das colunas, sem Z e sem bn
    linhas: dict    # "LZ", "L1", ..., "LW" -> [coeficiente de Z, ..., bn]


@dataclass
class Resultado:
    status: str = "otimo"          # "otimo", "ilimitado" ou "inviavel"
    z: Fraction = None
    valores: dict = field(default_factory=dict)   # todas as variáveis do quadro final
    pivos: list = field(default_factory=list)     # (fase, coluna que entra, linha pivô)
    quadros: list = field(default_factory=list)   # na ordem em que aparecem na saída
    otimos_multiplos: bool = False
    alternativa: str = None        # variável não básica com 0 na LZ que indica outros ótimos
    degenerado: bool = False
    base: dict = None              # linha -> variável básica no quadro final
    lz_final: dict = None          # coluna -> coeficiente da LZ no quadro final
    w: Fraction = None             # valor de W no fim da Fase 1, quando houver
    texto: list = field(default_factory=list)     # seção de quadros, em Markdown
    forma_padrao: list = field(default_factory=list)
    notas: list = field(default_factory=list)     # conversões e normalizações
    algebra_w: list = field(default_factory=list)
    artificiais: list = field(default_factory=list)


class _Tabela:
    def __init__(self, nome_z, colunas, linhas, base, artificiais=()):
        self.nome_z, self.colunas, self.linhas, self.base = nome_z, colunas, linhas, base
        self.artificiais = set(artificiais)

    def restricoes(self):
        return [r for r in self.linhas if r not in ("LZ", "LW")]

    def quadro(self):
        return Quadro(list(self.colunas), {r: list(v) for r, v in self.linhas.items()})

    def markdown(self, piv=None):
        cab = ["Linha", self.nome_z] + self.colunas + ["bn"]
        out = ["| " + " | ".join(cab) + " |", "|" + "|".join([":--"] + [":-:"] * (len(cab) - 1)) + "|"]
        for rot, v in self.linhas.items():
            cel = [rot] + [f"**[{fr(x)}]**" if piv == (rot, j) else fr(x) for j, x in enumerate(v)]
            out.append("| " + " | ".join(cel) + " |")
        return "\n".join(out)

    def sem_artificiais(self):
        manter = [j for j, c in enumerate(self.colunas) if c not in self.artificiais]
        linhas = {r: [v[0]] + [v[1 + j] for j in manter] + [v[-1]] for r, v in self.linhas.items() if r != "LW"}
        return _Tabela(self.nome_z, [self.colunas[j] for j in manter], linhas, dict(self.base))


def _imprimir(t, k, res, piv=None):
    res.texto += [f"**Quadro {k}**", "", t.markdown(piv), ""]
    res.quadros.append(t.quadro())


def _pivotear(t, lp, jj, fase, res, k, txt):
    """Quadro k com o pivô marcado e as operações da iteração. Devolve o número do próximo quadro."""
    col, piv = t.colunas[jj - 1], t.linhas[lp][jj]
    _imprimir(t, k, res, (lp, jj))
    res.pivos.append((fase, col, lp))
    ops = [] if piv == 1 else [f"{lp} ÷ {fp(piv)}"]
    t.linhas[lp] = [v / piv for v in t.linhas[lp]]
    nova = t.linhas[lp]
    for r, v in t.linhas.items():
        m = -v[jj]
        if r == lp or m == 0:
            continue
        ops.append(f"{r} {'+' if m > 0 else '-'} {fr(abs(m))} × {lp}")
        t.linhas[r] = [a + m * p for a, p in zip(v, nova)]
    res.texto += txt + [f"- Operações: {'; '.join(ops)}", ""]
    t.base[lp] = col
    return k + 1


def _iterar(t, obj, fase, res, k):
    """Pivoteia até a linha obj (LZ ou LW) não ter negativo. Devolve (próximo quadro, status)."""
    for _ in range(MAX_PIVOS):
        linha_obj = t.linhas[obj]
        cand = [(linha_obj[1 + j], j) for j, c in enumerate(t.colunas) if c not in t.artificiais and linha_obj[1 + j] < 0]
        if not cand:
            return k, "otimo"
        valor, j = min(cand)  # o mais negativo; empate: a coluna mais à esquerda
        col, jj = t.colunas[j], 1 + j
        txt = [f"- Coluna pivô: **{col}** (o mais negativo da {obj}: {fr(valor)})"]
        razoes = [(t.linhas[r][-1] / t.linhas[r][jj], r) for r in t.restricoes() if t.linhas[r][jj] > 0]
        if not razoes:
            _imprimir(t, k, res)
            res.texto += [txt[0], f"- A coluna {col} não tem nenhum elemento positivo nas restrições → "
                                  f"**o problema é ilimitado** ({t.nome_z} cresce sem limite).", ""]
            return k, "ilimitado"
        menor = min(q for q, _ in razoes)
        empate = [r for q, r in razoes if q == menor]
        lp = empate[0]  # empate: a linha mais acima
        partes = []
        for r in t.restricoes():
            e, b = t.linhas[r][jj], t.linhas[r][-1]
            if e > 0:
                partes.append(f"{r}: {fr(b)} ÷ {fr(e)} = {valor_com_decimal(b / e)}" + (" ← menor" if r == lp else ""))
            else:
                partes.append(f"{r}: não entra ({fr(e)})")
        txt.append(f"- Razões: {' · '.join(partes)}")
        if len(empate) > 1:
            res.degenerado = True
            txt.append(f"- Empate na menor razão: fica a linha mais acima ({lp}); a solução é degenerada.")
        txt.append(f"- Linha pivô: **{lp}** · Pivô: **{fr(t.linhas[lp][jj])}**")
        k = _pivotear(t, lp, jj, fase, res, k, txt)
    raise ErroResolver(f"mais de {MAX_PIVOS} pivoteamentos.")


def _tirar_artificiais(t, res, k):
    """Fim da Fase 1 com W = 0: artificial que ficou na base sai por pivoteamento. Devolve o próximo quadro."""
    while True:
        alvo = None
        for lin, col in t.base.items():
            if col in t.artificiais:
                jj = next((1 + j for j, c in enumerate(t.colunas)
                           if c not in t.artificiais and t.linhas[lin][1 + j] != 0), None)
                if jj is not None:
                    alvo = (lin, col, jj)
                    break
        if alvo is None:
            return k
        lin, col, jj = alvo
        txt = [f"- A LW não tem negativo fora das colunas artificiais e W = 0, mas a artificial {col} ficou na base "
               f"({lin}) com valor 0. Ela sai por um pivoteamento na primeira coluna não artificial com elemento "
               f"diferente de 0 nessa linha: **{t.colunas[jj - 1]}**.",
               f"- Linha pivô: **{lin}** · Pivô: **{fr(t.linhas[lin][jj])}** "
               f"(o bn dessa linha é 0, então aqui o pivô pode ser negativo)"]
        k = _pivotear(t, lin, jj, "fase 1", res, k, txt)


def _montar(p, res):
    """Forma padrão e quadro 1. Lado direito negativo: a restrição é multiplicada por -1."""
    L, d = p.letra, p.usa_decimal
    normais = []
    for i, (a, op, b) in enumerate(zip(p.A, p.ops, p.b), 1):
        if b < 0:
            a, op, b = [-v for v in a], INVERSO[op], -b
            res.notas.append(f"Restrição {i}: lado direito negativo, multiplicada por -1: "
                             f"{expressao(a, p.variaveis, d)} {SIMBOLO[op]} {num(b, d)}")
        normais.append((a, op, b))
    colunas = list(p.variaveis)
    folga = {i: (f"{L}f{i}", 1 if op == "<=" else -1) for i, (_, op, _) in enumerate(normais, 1) if op != "="}
    colunas += [nome for nome, _ in folga.values()]
    artificial = {}
    for i, (_, op, _) in enumerate(normais, 1):
        if op != "<=":
            artificial[i] = f"a{len(artificial) + 1}"
    colunas += list(artificial.values())
    res.artificiais = list(artificial.values())
    pos = {c: 1 + j for j, c in enumerate(colunas)}

    s = 1 if p.sentido == "max" else -1
    linhas = {"LZ": [Fraction(s)] + [Fraction(0)] * len(colunas) + [Fraction(0)]}
    for j, cj in enumerate(p.c):
        linhas["LZ"][1 + j] = -s * cj
    base = {}
    for i, (a, op, b) in enumerate(normais, 1):
        row = [Fraction(0)] + list(a) + [Fraction(0)] * (len(colunas) - len(a)) + [b]
        if i in folga:
            row[pos[folga[i][0]]] = Fraction(folga[i][1])
        if i in artificial:
            row[pos[artificial[i]]] = Fraction(1)
        linhas[f"L{i}"] = row
        base[f"L{i}"] = artificial.get(i) or folga[i][0]

    res.forma_padrao.append(_linha_z(p))
    for i, (a, op, b) in enumerate(normais, 1):
        extra = ""
        if i in folga:
            extra += f" {'+' if folga[i][1] > 0 else '-'} {folga[i][0]}"
        if i in artificial:
            extra += f" + {artificial[i]}"
        res.forma_padrao.append(f"{expressao(a, p.variaveis, d)}{extra} = {num(b, d)}")

    if artificial:
        lw = [Fraction(0)] * (len(colunas) + 2)
        for i in artificial:
            lw = [w - v for w, v in zip(lw, linhas[f"L{i}"])]
        for nome in artificial.values():
            lw[pos[nome]] = Fraction(0)
        lw[0] = Fraction(0)
        linhas["LW"] = lw
        res.algebra_w = _algebra_w(p, normais, folga, artificial, lw)
    return _Tabela(p.nome, colunas, linhas, base, artificial.values())


def _continuar(texto):
    """Transforma '-3x1 - 4x2' em '- 3x1 - 4x2' e '3x1' em '+ 3x1', para vir depois de outro termo."""
    return f"- {texto[1:]}" if texto.startswith("-") else f"+ {texto}"


def _linha_z(p):
    """'Z - 3x1 - 4x2 = 0' (Max) ou '-Z + 3x1 + 4x2 = 0' (Min)."""
    s = 1 if p.sentido == "max" else -1
    inicio = p.nome if s == 1 else f"-{p.nome}"
    return f"{inicio} {_continuar(expressao([-s * c for c in p.c], p.variaveis, p.usa_decimal))} = 0"


def _algebra_w(p, normais, folga, artificial, lw):
    """As linhas da álgebra da função auxiliar, como na atividade 1."""
    d, nomes = p.usa_decimal, p.variaveis
    soma_a = " + ".join(artificial.values())
    out = [f"Min W = {soma_a}"]
    for i, nome in artificial.items():
        a, _, b = normais[i - 1]
        excesso = f" + {folga[i][0]}" if i in folga else ""
        out.append(f"{nome} = {expressao([-v for v in a], nomes, d, constante=b)}{excesso}")
    total_b = sum((normais[i - 1][2] for i in artificial), Fraction(0))
    somas = lw[1:1 + len(nomes)]  # = -(soma dos coeficientes das linhas com artificial)
    excessos = [folga[i][0] for i in artificial if i in folga]
    mais = "".join(f" + {e}" for e in excessos)
    menos = "".join(f" - {e}" for e in excessos)
    out.append(f"W = {soma_a} = {expressao(somas, nomes, d, constante=total_b)}{mais}")
    out.append(f"-W = {expressao([-v for v in somas], nomes, d, constante=-total_b)}{menos}")
    out.append(f"-W {_continuar(expressao(somas, nomes, d))}{mais} = {num(-total_b, d)}      ← linha LW")
    return out


def resolver_problema(p):
    """Resolve o problema como foi dado (Simplex ou duas fases) e devolve o Resultado."""
    res = Resultado()
    t = _montar(p, res)
    k = 1
    fase = "simplex"
    if "LW" in t.linhas:
        res.texto += ["**Fase 1** — entra o mais negativo da LW; coluna de artificial nunca entra.", ""]
        k, _ = _iterar(t, "LW", "fase 1", res, k)
        res.w = -t.linhas["LW"][-1]
        if res.w != 0:
            _imprimir(t, k, res)
            res.status = "inviavel"
            res.texto += [f"A LW não tem negativo fora das colunas artificiais, mas o bn da LW é {fr(-res.w)} → "
                          f"W = {fr(res.w)} > 0 → **o problema não tem solução viável**.", ""]
            return res
        k_antes = k
        k = _tirar_artificiais(t, res, k)
        _imprimir(t, k, res)
        if k == k_antes:
            res.texto += ["A LW não tem negativo fora das colunas artificiais e o bn da LW é 0 → W = 0 → **fim da Fase 1**.", ""]
        else:
            res.texto += ["O bn da LW continua 0 → W = 0 → **fim da Fase 1**.", ""]
        for lin in [lin for lin, col in t.base.items() if col in t.artificiais]:
            res.texto += [f"A artificial {t.base[lin]} ficou na base ({lin}) e essa linha só tem zeros fora das colunas "
                          f"artificiais: a restrição {lin[1:]} é redundante e a linha {lin} sai do quadro.", ""]
            del t.linhas[lin], t.base[lin]
        res.texto += [f"**Fase 2** — retiramos a linha LW e as colunas {', '.join(res.artificiais)}; segue com a LZ.", ""]
        t = t.sem_artificiais()
        k += 1
        fase = "fase 2"
    k, status = _iterar(t, "LZ", fase, res, k)
    if status == "ilimitado":
        res.status = "ilimitado"
        return res
    _imprimir(t, k, res)
    res.texto += ["A LZ não tem nenhum número negativo → **solução ótima**.", ""]

    res.base = dict(t.base)
    res.valores = {c: Fraction(0) for c in t.colunas}
    for r, c in t.base.items():
        res.valores[c] = t.linhas[r][-1]
    bn = t.linhas["LZ"][-1]
    res.z = bn if p.sentido == "max" else -bn
    res.lz_final = {c: t.linhas["LZ"][1 + j] for j, c in enumerate(t.colunas)}
    for j, c in enumerate(t.colunas):
        if c in t.base.values() or res.lz_final[c] != 0:
            continue
        razoes = [t.linhas[r][-1] / t.linhas[r][1 + j] for r in t.restricoes() if t.linhas[r][1 + j] > 0]
        if not razoes or min(razoes) > 0:  # entrar com c leva a outro ponto com o mesmo Z
            res.otimos_multiplos, res.alternativa = True, c
            break
    _conferir(p, {v: res.valores[v] for v in p.variaveis}, res.z)
    return res


def _conferir(p, x, z):
    """Trava de segurança: a solução satisfaz as restrições e dá o Z informado."""
    for a, op, b in zip(p.A, p.ops, p.b):
        lhs = sum((ai * x[v] for ai, v in zip(a, p.variaveis)), Fraction(0))
        if not {"<=": lhs <= b, ">=": lhs >= b, "=": lhs == b}[op]:
            raise ErroResolver("erro interno: a solução não satisfaz as restrições.")
    if sum((ci * x[v] for ci, v in zip(p.c, p.variaveis)), Fraction(0)) != z:
        raise ErroResolver("erro interno: o Z da substituição não bate com o quadro.")


@dataclass
class ResultadoDual:
    dual: Problema
    resultado: Resultado       # resolução do dual
    x: dict                    # solução do primal, lida na LZ final do dual
    z: Fraction
    status_primal: str


def resolver_pelo_dual(p):
    """Monta o dual, resolve o dual e lê a solução do primal na LZ final do dual."""
    d = montar_dual(p)
    if any(s != ">=0" for s in d.sinais):
        raise ErroResolver("o primal não está na forma padrão (Max só com ≤ ou Min só com ≥), "
                           "então o dual teria variável ≤ 0 ou livre.")
    res = resolver_problema(d)
    if res.status == "ilimitado":
        return ResultadoDual(d, res, None, None, "inviavel")
    if res.status == "inviavel":
        return ResultadoDual(d, res, None, None, resolver_problema(p).status)
    x = {v: res.lz_final[f"{d.letra}f{j}"] for j, v in enumerate(p.variaveis, 1)}
    _conferir(p, x, res.z)
    return ResultadoDual(d, res, x, res.z, "otimo")


# ---------- saída em Markdown ----------

def _metodo(r, p):
    """'Simplex', 'duas fases com a linha -Z', ..."""
    nome = "duas fases" if r.artificiais else "Simplex"
    return nome + (f" com a linha -{p.nome}" if p.sentido == "min" else "")


def _linhas_modelo(p):
    d = p.usa_decimal
    out = [f"{p.sentido.capitalize()} {p.nome} = {expressao(p.c, p.variaveis, d)}"]
    out += [f"{expressao(a, p.variaveis, d)} {SIMBOLO[op]} {num(b, d)}" for a, op, b in zip(p.A, p.ops, p.b)]
    if p.sinais is None or all(s == ">=0" for s in p.sinais):
        out.append(f"{', '.join(p.variaveis)} ≥ 0")
    else:
        out.append("; ".join(f"{v} {'≥ 0' if s == '>=0' else '≤ 0' if s == '<=0' else 'livre'}"
                             for v, s in zip(p.variaveis, p.sinais)))
    return out


def _decimais(p):
    vistos = []
    for v in p.c + [x for a in p.A for x in a] + p.b:
        v = abs(Fraction(v))
        if v.denominator != 1 and _casas_exatas(v) is not None and v not in vistos:
            vistos.append(v)
    return "; ".join(f"{decimal(v)} = {fr(v)}" for v in vistos)


def _bloco(linhas):
    return ["```"] + linhas + ["```"]


def _secoes_resolucao(p, r, n0, titulo_quadros="Quadros"):
    """Forma padrão e quadros (seções n0 e n0 + 1). Devolve as linhas."""
    out = [f"### {n0}. Forma padrão", ""]
    decimais = _decimais(p) if p.usa_decimal else ""
    if decimais:
        out += [f"Decimais em fração: {decimais}", ""]
    out += [f"{nota}" for nota in r.notas] + ([""] if r.notas else [])
    out += _bloco(r.forma_padrao) + [""]
    if r.algebra_w:
        out += ["Função auxiliar da Fase 1:", ""] + _bloco(r.algebra_w) + [""]
    out += [f"### {n0 + 1}. {titulo_quadros}", ""] + r.texto
    if r.status != "otimo":
        return out
    if p.sentido == "min":
        out += [f"A LZ diz -{p.nome} = {fr(-r.z)}, logo {p.nome} = {fr(r.z)}.", ""]
    if r.otimos_multiplos:
        out += [f"Observação: {r.alternativa} é não básica e tem 0 na LZ → há outras soluções ótimas "
                f"com o mesmo {p.nome}.", ""]
    return out


def _linha_substituicao(p, x):
    """'Z = 3x1 + 4x2 = 3 × 9/4 + 4 × 3/2 = 51/4'."""
    return f"{p.nome} = {expressao(p.c, p.variaveis, p.usa_decimal)} = {substituicao(p.c, p.variaveis, x, p.usa_decimal)}"


def _resposta(p, valores, z):
    partes = "; ".join(f"{v} = {valor_com_decimal(valores[v])}" for v in p.variaveis)
    return f"{partes}; {p.nome} = {valor_com_decimal(z)}"


def _texto_status(status):
    return {"ilimitado": "o problema é ilimitado (Z cresce sem limite); não há solução ótima.",
            "inviavel": "o problema não tem solução viável."}[status]


def _texto_primal(p):
    r = resolver_problema(p)
    metodo = _metodo(r, p)
    out = [f"**Método:** {metodo[0].upper()}{metodo[1:]}", "", "### 1. Modelo", ""] + _bloco(_linhas_modelo(p)) + [""]
    out += _secoes_resolucao(p, r, 2) + ["### 4. Resposta", ""]
    if r.status != "otimo":
        return "\n".join(out + [f"**Resposta:** {_texto_status(r.status)}", ""])
    x = {v: r.valores[v] for v in p.variaveis}
    out += _bloco([_linha_substituicao(p, x)]) + ["", f"**Resposta:** {_resposta(p, x, r.z)}", ""]
    return "\n".join(out)


def _lado_a_lado(p, d):
    mp, md = _linhas_modelo(p), _linhas_modelo(d)
    esq = ["PRIMAL", mp[0]] + [f"{y} → {linha}" for y, linha in zip(d.variaveis, mp[1:-1])] + [mp[-1]]
    dir_ = ["DUAL", md[0]] + [f"{linha}     (coluna de {x})" for x, linha in zip(p.variaveis, md[1:-1])] + [md[-1]]
    largura = max(len(s) for s in esq) + 4
    total = max(len(esq), len(dir_))
    esq += [""] * (total - len(esq))
    dir_ += [""] * (total - len(dir_))
    return [f"{a.ljust(largura)}{b}".rstrip() for a, b in zip(esq, dir_)]


def _texto_sinais(p, d):
    """Explica os sinais das variáveis duais quando o primal não está na forma padrão."""
    if all(s == ">=0" for s in d.sinais):
        return []
    tipo = "Max" if p.sentido == "max" else "Min"
    partes = []
    for i, (y, op, s) in enumerate(zip(d.variaveis, p.ops, d.sinais), 1):
        sinal = {">=0": "≥ 0", "<=0": "≤ 0", "livre": "livre"}[s]
        partes.append(f"- {y} {sinal}: a restrição {i} do primal é {SIMBOLO[op]} num {tipo}")
    return ["Sinais das variáveis do dual (tabela da referência 2.6):", ""] + partes + [""]


def _texto_montar_dual(p):
    d = montar_dual(p)
    out = ["**Método:** montar o dual", "", "### 1. Primal e dual", ""] + _bloco(_lado_a_lado(p, d)) + [""]
    return "\n".join(out + _texto_sinais(p, d))


def _texto_dual(p):
    rd = resolver_pelo_dual(p)
    d, r = rd.dual, rd.resultado
    out = [f"**Método:** dual, resolvido por {_metodo(r, d)}", "", "### 1. Primal e dual", ""]
    out += _bloco(_lado_a_lado(p, d)) + [""]
    out += _secoes_resolucao(d, r, 2, titulo_quadros="Quadros do dual") + ["### 4. Resposta", ""]
    if r.status != "otimo":
        texto = ("o dual é ilimitado, então o primal não tem solução viável." if r.status == "ilimitado"
                 else "o dual não tem solução viável e o primal "
                 + ("é ilimitado." if rd.status_primal == "ilimitado" else "também não tem solução viável."))
        return "\n".join(out + [f"**Resposta:** {texto}", ""])
    y = {v: r.valores[v] for v in d.variaveis}
    lidos = " · ".join(f"coluna {d.letra}f{j} → {v} = {fr(rd.x[v])}" for j, v in enumerate(p.variaveis, 1))
    out += [f"Primal lido na LZ final do dual: {lidos}", ""]
    out += _bloco([_linha_substituicao(p, rd.x)]) + [""]
    out += [f"**Resposta:** {_resposta(p, rd.x, rd.z)}", "", f"**Dual:** {_resposta(d, y, r.z)}", ""]
    return "\n".join(out)


def gerar_saida(p):
    """A resolução completa em Markdown, conforme o modo pedido no arquivo."""
    if p.modo == "primal":
        return _texto_primal(p)
    if p.modo == "montar_dual":
        return _texto_montar_dual(p)
    if p.modo == "dual":
        return _texto_dual(p)
    rp, rd = resolver_problema(p), resolver_pelo_dual(p)
    if rp.status == "otimo" and rd.status_primal == "otimo":
        if rp.z != rd.z:
            raise ErroResolver("erro interno: o Z do primal e o Z1 do dual são diferentes.")
        comparacao = f"- Z do primal (Parte A) = Z1 do dual (Parte B) = {valor_com_decimal(rp.z)} ✓"
    else:
        comparacao = "- Não há solução ótima (ver as respostas das partes A e B)."
    return "\n".join(["## Parte A — primal", "", _texto_primal(p), "## Parte B — dual", "", _texto_dual(p),
                      "## Comparação", "", comparacao, ""])


def main(argv):
    if len(argv) != 2:
        print("uso: python3 resolver.py questoes/q1.txt", file=sys.stderr)
        return 2
    try:
        with open(argv[1], encoding="utf-8") as f:
            print(gerar_saida(ler(f.read())))
    except ErroEntrada as e:
        print(f"ERRO DE FORMATO (corrija o arquivo da questão): {e}", file=sys.stderr)
        return 1
    except ErroResolver as e:
        print(f"CASO NÃO COBERTO (pare esta questão e avise): {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
