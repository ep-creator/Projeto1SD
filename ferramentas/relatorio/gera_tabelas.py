#!/usr/bin/env python3
"""Gera testes/<bloco>/tabela_verdade.md a partir da ESPECIFICACAO de cada bloco.

As tabelas sao calculadas pelo comportamento esperado (enunciado + decisoes do
projeto), nao pela simulacao do circuito. As equacoes sao as implementadas nos
.bdf. Uso: python3 gera_tabelas.py <raiz do repositorio>
"""
import os
import re
import sys

ROOT = sys.argv[1] if len(sys.argv) > 1 else "."

# ----------------------------------------------------------------- utilidades


def b(n, w):
    return format(n & ((1 << w) - 1), f"0{w}b")


def bits(n, w):
    """lista de bits, MSB primeiro"""
    return [int(c) for c in b(n, w)]


def dec(v):
    if v > 0:
        return f"+{v}"
    if v < 0:
        return f"−{-v}"
    return "0"


def sm(v, w):
    """valor com sinal -> string sinal-magnitude de w bits"""
    return ("1" if v < 0 else "0") + b(abs(v), w - 1)


def table(headers, rows):
    out = ["| " + " | ".join(headers) + " |",
           "|" + "|".join([":---:"] * len(headers)) + "|"]
    for r in rows:
        out.append("| " + " | ".join(str(c) for c in r) + " |")
    return "\n".join(out)


def fold(headers, rows):
    """divide uma tabela longa em duas metades lado a lado"""
    h = (len(rows) + 1) // 2
    left, right = rows[:h], rows[h:]
    out = []
    for i in range(h):
        r = right[i] if i < len(right) else [""] * len(headers)
        out.append(list(left[i]) + list(r))
    return table(headers + headers, out)


GRAY = {1: ["0", "1"], 2: ["00", "01", "11", "10"]}


def kmap(f, names, titulo=None):
    """f(dict nome->bit) -> 0/1/None(X). 3 ou 4 variaveis; 5 vira 2 mapas."""
    n = len(names)
    if n == 5:
        partes = []
        for v in (0, 1):
            g = (lambda v: (lambda d: f({**d, names[0]: v})))(v)
            partes.append(f"*{names[0]} = {v}*\n\n" + kmap(g, names[1:]))
        return "\n\n".join(partes)
    rv, cv = names[: n // 2], names[n // 2:]
    head = ["".join(rv) + " \\\\ " + "".join(cv)] + GRAY[len(cv)]
    rows = []
    for rg in GRAY[len(rv)]:
        row = [rg]
        for cg in GRAY[len(cv)]:
            d = {k: int(x) for k, x in zip(rv + cv, rg + cg)}
            y = f(d)
            row.append("X" if y is None else str(y))
        rows.append(row)
    return table(head, rows)


# avaliador de soma de produtos escrita no texto (confere as equacoes)
LIT = re.compile(r"(Cin|[A-Z][0-9]?)('?)")


def sop(expr):
    terms = [t.strip() for t in expr.split("+")]

    def f(d):
        for t in terms:
            if t == "1":
                return 1
            if t == "0":
                continue
            ok = True
            for name, neg in LIT.findall(t):
                v = d[name]
                if neg:
                    v = 1 - v
                ok = ok and v == 1
            if ok:
                return 1
        return 0
    return f


def confere(nome, spec, expr, names):
    f = sop(expr)
    for i in range(1 << len(names)):
        d = dict(zip(names, bits(i, len(names))))
        s = spec(d)
        if s is None:
            continue
        if f(d) != s:
            raise SystemExit(f"ERRO {nome}: {expr} difere em {d}: {f(d)} != {s}")


# segmentos a b c d e f g, ativo baixo (0 = aceso)
SEG = {0: "0000001", 1: "1001111", 2: "0010010", 3: "0000110", 4: "1001100",
       5: "0100100", 6: "0100000", 7: "0001111", 8: "0000000", 9: "0000100"}
SEGN = "abcdefg"

# ------------------------------------------------------------------ blocos
BLOCOS = {}


def bloco(nome):
    def deco(fn):
        BLOCOS[nome] = fn
        return fn
    return deco


def cabecalho(nome, usa, entradas, saidas):
    usa = f" ({usa})" if usa else ""
    return (f"# {nome} — tabela verdade e simulação\n\n"
            f"* **Circuito:** [`lib/{nome}.bdf`](../../lib/{nome}.bdf){usa}\n"
            f"* **Entradas:** {entradas}\n"
            f"* **Saídas:** {saidas}\n"
            f"* **Figuras do relatório (nesta pasta):** `{nome}_circuito.png` (esquemático) "
            f"e `{nome}_simulacao.png` (waveform do `{nome}.vwf`)\n")


def lib(n):
    return f"[`{n}`](../../lib/{n}.bdf)"


@bloco("mux2x1")
def _():
    rows = []
    for i in range(8):
        s, a, bb = bits(i, 3)
        rows.append([s, a, bb, bb if s else a])
    names = ["S", "A", "B"]
    spec = lambda d: d["B"] if d["S"] else d["A"]
    eq = "A·S' + B·S"
    confere("mux2x1", spec, "AS' + BS", names)
    return dict(
        cab=cabecalho("mux2x1", "", "`A`, `B`, `S`", "`Y`"),
        func="Multiplexador 2:1 de 1 bit. Com `S = 0` a saída `Y` copia `A`; com `S = 1`, copia `B`. "
             "É usado no `comp2` e no `c2_para_sm` para escolher entre um número e o seu complemento a 2.",
        tabela=table(["S", "A", "B", "Y"], rows),
        eq=f"* `Y = {eq}`",
        kmap=kmap(spec, names) + "\n\nGrupos: `A·S'` (linha `S = 0`, colunas com `A = 1`) e `B·S` "
             "(linha `S = 1`, colunas com `B = 1`).",
    )


@bloco("mux4x1")
def _():
    rows = [[0, 0, "I[0]"], [0, 1, "I[1]"], [1, 0, "I[2]"], [1, 1, "I[3]"]]
    return dict(
        cab=cabecalho("mux4x1", "", "`I[3..0]`, `S[1..0]`", "`yi`"),
        func="Multiplexador 4:1 de 1 bit: o seletor `S[1..0]` escolhe qual das quatro entradas vai para `yi`. "
             "O `mux_saida` usa seis deles, um por bit de F. A tabela completa tem 64 linhas; abaixo, a forma "
             "compacta (cada linha vale para qualquer valor das entradas não selecionadas).",
        tabela=table(["S[1]", "S[0]", "yi"], rows),
        eq="* `yi = I0·S1'·S0' + I1·S1'·S0 + I2·S1·S0' + I3·S1·S0`\n\n"
           "Cada termo é uma porta AND que só deixa passar a entrada cujo índice é igual a `S`; "
           "a porta OR junta os quatro termos.",
    )


def c2_4(i):
    return (16 - i) % 16


@bloco("inversor")
def _():
    rows = []
    for i in range(16):
        o = c2_4(i)
        rows.append(bits(i, 4) + bits(o, 4) + [i, ("−" + str(i)) if i else "0"])
    return dict(
        cab=cabecalho("inversor", "", "`I3`, `I2`, `I1`, `I0`", "`F3`, `F2`, `F1`, `F0`"),
        func="Calcula o complemento a 2 de um número de 4 bits (inverte e soma 1). Em vez de um somador, usa o atalho: "
             "da direita para a esquerda, copia os bits até o primeiro `1` (inclusive) e inverte os outros. "
             "Assim, cada bit é invertido quando existe algum `1` abaixo dele. É usado pelo `comp2`.",
        tabela=table(["I3", "I2", "I1", "I0", "F3", "F2", "F1", "F0", "I", "F (C2)"], rows),
        eq="* `F0 = I0`\n* `F1 = I1 ⊕ I0`\n* `F2 = I2 ⊕ (I1 + I0)`\n* `F3 = I3 ⊕ (I2 + I1 + I0)`\n\n"
           "Pelo mapa-K, `F1`, `F2` e `F3` não se reduzem bem em soma de produtos (padrão de tabuleiro, típico de XOR); "
           "a forma com XOR sai direto da regra \"inverte se há um 1 abaixo\".",
    )


@bloco("inversor5")
def _():
    rows = []
    for i in range(32):
        o = (32 - i) % 32
        rows.append([b(i, 5), i, b(o, 5)])
    return dict(
        cab=cabecalho("inversor5", "", "`I[4..0]`", "`O[4..0]`"),
        func="Complemento a 2 de 5 bits, com a mesma regra do `inversor`. É usado no `c2_para_sm`, em que a magnitude "
             "do resultado chega a 30 e precisa de 5 bits.",
        tabela=fold(["I[4..0]", "I", "O[4..0]"], rows),
        eq="* `O[0] = I[0]`\n* `O[1] = I[1] ⊕ I[0]`\n* `O[2] = I[2] ⊕ (I[1] + I[0])`\n"
           "* `O[3] = I[3] ⊕ (I[2] + I[1] + I[0])`\n* `O[4] = I[4] ⊕ (I[3] + I[2] + I[1] + I[0])`",
    )


@bloco("comp2")
def _():
    rows = []
    for i in range(32):
        s, m = i >> 4, i & 15
        v = -m if s else m
        o = c2_4(m) if s else m
        os_ = 1 if (s and m) else 0
        rows.append([s, b(m, 4), dec(v) if not (s and m == 0) else "−0", os_, b(o, 4), dec(v)])
    return dict(
        cab=cabecalho("comp2", lib("inversor") + ", " + lib("mux2x1") + " ×4",
                      "`IS` (sinal), `I[3..0]` (magnitude)", "`OS`, `O[3..0]` (complemento a 2 de 5 bits)"),
        func="Converte um número de sinal-magnitude para complemento a 2 de 5 bits. Se o número é positivo, a magnitude "
             "passa direto; se é negativo, sai o complemento a 2 da magnitude (bloco `inversor`). Quatro `mux2x1` com "
             "seletor `IS` fazem essa escolha. O sinal de saída só é 1 quando a magnitude não é zero, então o −0 "
             "(`IS = 1`, `I = 0000`) sai como +0. Na ULA, é usado no `somador_subtrator` (×2) e na operação `010`.",
        tabela=table(["IS", "I[3..0]", "Entrada (SM)", "OS", "O[3..0]", "Saída (C2)"], rows),
        eq="* `O[k] = I[k]·IS' + inversor(I)[k]·IS` (um `mux2x1` por bit)\n* `OS = IS·(I3 + I2 + I1 + I0)`",
    )


@bloco("somador_completo")
def _():
    rows = []
    names = ["A", "B", "Cin"]
    for i in range(8):
        a, bb, c = bits(i, 3)
        t = a + bb + c
        rows.append([a, bb, c, t & 1, t >> 1])
    s_spec = lambda d: (d["A"] + d["B"] + d["Cin"]) & 1
    c_spec = lambda d: (d["A"] + d["B"] + d["Cin"]) >> 1
    confere("somador_completo Cout", c_spec, "AB + ACin + BCin", ["A", "B", "Cin"])
    return dict(
        cab=cabecalho("somador_completo", "", "`A`, `B`, `Cin`", "`S`, `Cout`"),
        func="Soma três bits (dois operandos e o vai-um da etapa anterior), gerando o bit de soma `S` e o vai-um `Cout`. "
             "É a célula do `somador6`.",
        tabela=table(["A", "B", "Cin", "S", "Cout"], rows),
        eq="* `S = A ⊕ B ⊕ Cin`\n* `Cout = A·B + (A ⊕ B)·Cin`",
        kmap="**S**\n\n" + kmap(lambda d: s_spec(d), ["A", "B", "Cin"]) +
             "\n\nNenhum par de 1s é adjacente (tabuleiro): `S` não se reduz em soma de produtos e vira `A ⊕ B ⊕ Cin`.\n\n"
             "**Cout**\n\n" + kmap(lambda d: c_spec(d), ["A", "B", "Cin"]) +
             "\n\nTrês grupos de dois: `Cout = A·B + A·Cin + B·Cin`. O circuito usa a forma equivalente "
             "`A·B + (A ⊕ B)·Cin`, que reaproveita a porta XOR de `S`.",
    )


@bloco("somador6")
def _():
    casos = [(0, 0), (5, -3), (-5, 3), (7, -7), (15, 15), (-15, -15), (-8, -8), (-9, -12), (12, -9), (1, -1), (-1, -1), (15, -15)]
    rows = []
    for a, bb in casos:
        rows.append([b(a, 5), dec(a), b(bb, 5), dec(bb), b(a + bb, 6), dec(a + bb)])
    return dict(
        cab=cabecalho("somador6", lib("somador_completo") + " ×6", "`A[4..0]`, `B[4..0]` (complemento a 2)",
                      "`O[5..0]` = A + B (complemento a 2 de 6 bits)"),
        func="Soma dois números em complemento a 2 de 5 bits (−15 a +15, vindos do `comp2`). Como a soma vai de −30 a +30 "
             "e não cabe em 5 bits, os operandos são estendidos para 6 bits repetindo o bit de sinal: o sexto "
             "`somador_completo` recebe `A[4]` e `B[4]` de novo. São seis somadores em cascata (*ripple carry*), "
             "com vai-um inicial 0; em 6 bits não há overflow. A tabela completa tem 1024 linhas; abaixo, casos "
             "representativos (sinais iguais e diferentes, zero e os extremos ±30).",
        tabela=table(["A[4..0]", "A", "B[4..0]", "B", "O[5..0]", "O"], rows),
        eq="Para cada etapa `i` = 0 … 5, com `A5 = A4`, `B5 = B4` (extensão de sinal) e `C0 = 0`:\n\n"
           "* `O[i] = A[i] ⊕ B[i] ⊕ C[i]`\n* `C[i+1] = A[i]·B[i] + (A[i] ⊕ B[i])·C[i]`\n\n"
           "O vai-um final `C6` é descartado.",
    )


def c2_para_sm_spec(i):
    v = i - 64 if i >= 32 else i
    if v == -32:
        return v, None
    return v, sm(v, 6)


@bloco("c2_para_sm")
def _():
    rows = []
    for i in range(64):
        v, o = c2_para_sm_spec(i)
        rows.append([b(i, 6), dec(v), o if o else "X"])
    return dict(
        cab=cabecalho("c2_para_sm", lib("inversor5") + ", " + lib("mux2x1") + " ×5",
                      "`I[5..0]` (complemento a 2, saída do `somador6`)", "`O[5..0]` (sinal-magnitude: `O[5]` = sinal)"),
        func="Converte o resultado do `somador6` de volta para sinal-magnitude, que é o formato pedido para F. O sinal "
             "passa direto (`O[5] = I[5]`). Se o número é positivo, a magnitude são os 5 bits de baixo; se é negativo, "
             "é o complemento a 2 desses 5 bits (`inversor5`). Cinco `mux2x1` com seletor `I[5]` fazem a escolha. "
             "Na ULA só aparecem valores de −30 a +30; a entrada −32 (`100000`) não ocorre (X).",
        tabela=fold(["I[5..0]", "Valor", "O[5..0]"], rows),
        eq="* `O[5] = I[5]`\n* `O[k] = I[k]·I5' + inversor5(I[4..0])[k]·I5`, para `k` = 0 … 4",
    )


@bloco("somador_subtrator")
def _():
    casos = [(0, 5, -3), (0, -5, 3), (1, 2, 5), (1, -9, 12), (0, -8, -8), (0, -15, -15), (0, 15, 15),
             (1, 15, -15), (1, 7, 7), (0, 6, -6), (1, -4, -4), (0, 0, 0)]
    rows = []
    for op, a, bb in casos:
        r = a - bb if op else a + bb
        conta = f"({dec(a)}) {'−' if op else '+'} ({dec(bb)})"
        rows.append([op, sm(a, 5), sm(bb, 5), conta, sm(r, 6), dec(r)])
    rows.append([0, "10000", "00000", "(−0) + (+0)", "000000", "0"])
    return dict(
        cab=cabecalho("somador_subtrator", lib("comp2") + " ×2, `XOR`, " + lib("somador6") + ", " + lib("c2_para_sm"),
                      "`sinal_a`, `W[3..0]` (A), `sinal_b`, `X[3..0]` (B), `sinal_op` (0 = soma, 1 = subtração)",
                      "`R[5..0]` = A ± B em sinal-magnitude"),
        func="Faz a soma e a subtração da ULA (`S = 000` e `001`, com `sinal_op = S[0]`). A subtração vira soma: "
             "A − B = A + (−B), e trocar o sinal de B em sinal-magnitude é só inverter o bit de sinal "
             "(`sinal_b ⊕ sinal_op`). Depois, os dois operandos passam por `comp2` (SM → C2), são somados no "
             "`somador6` e o resultado volta para sinal-magnitude no `c2_para_sm`. A tabela completa tem 512 linhas; "
             "abaixo, casos representativos.",
        tabela=table(["sinal_op", "A (SM)", "B (SM)", "Conta", "R[5..0]", "R"], rows),
        eq="* `sinal_b' = sinal_b ⊕ sinal_op`\n"
           "* `R = c2_para_sm( somador6( comp2(sinal_a, W), comp2(sinal_b', X) ) )`",
    )


def logico(nome, op, simb, desc):
    rows_bit = [[x, y, op(x, y)] for x in (0, 1) for y in (0, 1)]
    casos = [(5, 3), (-5, -3), (-5, 3), (15, 9), (-12, -10), (0, -7)]
    ex = []
    for a, bb in casos:
        sa, ma = int(a < 0), abs(a)
        sb, mb = int(bb < 0), abs(bb)
        f = (op(sa, sb) << 5) | (op(ma, mb) & 15)
        ex.append([sm(a, 5), sm(bb, 5), b(f, 6)])
    return dict(
        cab=cabecalho(nome, "", "`SA`, `A[3..0]`, `SB`, `B[3..0]`", "`F[5..0]`"),
        func=desc + " A operação é bit a bit sobre os 5 bits de entrada: as magnitudes vão para `F[3..0]` e os sinais, "
                    "para `F[5]`. `F[4]` fica sempre em 0, porque a magnitude de entrada tem só 4 bits. "
                    "A tabela completa tem 1024 linhas; como cada bit é independente, basta a tabela de um bit e alguns exemplos.",
        tabela="**Um bit**\n\n" + table(["a", "b", f"a {simb} b"], rows_bit) +
               "\n\n**Exemplos**\n\n" + table(["A (SM)", "B (SM)", "F[5..0]"], ex),
        eq=f"* `F[k] = A[k] {simb} B[k]`, para `k` = 0 … 3\n* `F[4] = 0`\n* `F[5] = SA {simb} SB`",
    )


@bloco("op_and")
def _():
    return logico("op_and", lambda x, y: x & y, "·", "Operação `110`: A AND B.")


@bloco("op_xor")
def _():
    return logico("op_xor", lambda x, y: x ^ y, "⊕", "Operação `111`: A XOR B.")


@bloco("comp_mag")
def _():
    rows = [["1 0", "X", "X", "X", 1], ["0 1", "X", "X", "X", 0],
            ["iguais", "1 0", "X", "X", 1], ["iguais", "0 1", "X", "X", 0],
            ["iguais", "iguais", "1 0", "X", 1], ["iguais", "iguais", "0 1", "X", 0],
            ["iguais", "iguais", "iguais", "1 0", 1], ["iguais", "iguais", "iguais", "0 1", 0],
            ["iguais", "iguais", "iguais", "iguais", 0]]
    casos = [(9, 7), (7, 9), (12, 12), (5, 4), (0, 0), (15, 0), (0, 1)]
    ex = [[b(a, 4), b(bb, 4), f"{a} > {bb}", int(a > bb)] for a, bb in casos]
    return dict(
        cab=cabecalho("comp_mag", "", "`A[3..0]`, `B[3..0]` (magnitudes, sem sinal)", "`O` = 1 quando |A| > |B|"),
        func="Compara duas magnitudes de 4 bits, do bit mais alto para o mais baixo: o primeiro bit em que A e B diferem "
             "decide. Se todos são iguais, A não é maior (O = 0). É a base do `comp_maior`. A tabela completa tem 256 "
             "linhas; abaixo, a forma compacta (X = qualquer valor) e alguns exemplos.",
        tabela=table(["A3 B3", "A2 B2", "A1 B1", "A0 B0", "O"], rows) + "\n\n**Exemplos**\n\n" +
               table(["A[3..0]", "B[3..0]", "Comparação", "O"], ex),
        eq="Com `ek = Ak ⊙ Bk` (XNOR: bits iguais):\n\n"
           "* `O = A3·B3' + e3·A2·B2' + e3·e2·A1·B1' + e3·e2·e1·A0·B0'`",
    )


@bloco("comp_maior")
def _():
    rows = [[0, 0, "|A| > |B|"], [1, 1, "|A| < |B|"], [0, 1, "1, exceto se A = B = 0 (+0 = −0)"], [1, 0, "0 (nunca)"]]
    casos = [(5, 3), (3, 5), (2, -5), (-2, -5), (-5, -2), (-7, 1), (0, 0), (0, -0.0), (-0.0, 0), (4, 4)]
    ex = []
    for a, bb in casos:
        sa = 1 if (a < 0 or (a == 0 and str(a).startswith("-"))) else 0
        sb = 1 if (bb < 0 or (bb == 0 and str(bb).startswith("-"))) else 0
        ma, mb = int(abs(a)), int(abs(bb))
        va, vb = (-ma if sa else ma), (-mb if sb else mb)
        la = ("−" if sa else "+") + str(ma)
        lb = ("−" if sb else "+") + str(mb)
        ex.append([sa, b(ma, 4), sb, b(mb, 4), f"{la} > {lb}", int(va > vb)])
    return dict(
        cab=cabecalho("comp_maior", lib("comp_mag") + " ×2",
                      "`SA`, `A[3..0]`, `SB`, `B[3..0]` (sinal-magnitude)", "`O` = 1 quando A > B"),
        func="Diz se A > B em sinal-magnitude. Compara os sinais primeiro e as magnitudes depois: entre dois positivos, "
             "ganha a maior magnitude; entre dois negativos, a menor; positivo é maior que negativo, exceto quando os "
             "dois são zero (+0 = −0). Usa dois `comp_mag`: `GT = comp_mag(A, B)` e `LT = comp_mag(B, A)`. "
             "Na ULA há duas instâncias: `comp_maior(A, B)` para A > B e `comp_maior(B, A)` para A < B. "
             "A tabela completa tem 1024 linhas; abaixo, a forma compacta por sinais e exemplos.",
        tabela=table(["SA", "SB", "O"], rows) + "\n\n**Exemplos**\n\n" +
               table(["SA", "A[3..0]", "SB", "B[3..0]", "Comparação", "O"], ex),
        eq="Com `GT = comp_mag(A, B)`, `LT = comp_mag(B, A)` e `NZB = B3 + B2 + B1 + B0` (B ≠ 0):\n\n"
           "* `O = SA'·(GT + SB·NZB) + SA·SB·LT`",
    )


@bloco("comparador_igual")
def _():
    rows = [["diferentes", "X", 0], ["iguais e = 0000", "X", 1], ["iguais e ≠ 0000", "iguais", 1], ["iguais e ≠ 0000", "diferentes", 0]]
    casos = [("00101", "00101"), ("00101", "10101"), ("10000", "00000"), ("10000", "10000"), ("01100", "01101"), ("11111", "11111")]

    def val(s):
        m = int(s[1:], 2)
        return ("−" if s[0] == "1" else "+") + str(m), (-m if s[0] == "1" else m)
    ex = []
    for x, y in casos:
        lx, vx = val(x)
        ly, vy = val(y)
        ex.append([x, y, f"{lx} = {ly}", int(vx == vy)])
    return dict(
        cab=cabecalho("comparador_igual", "", "`A[4..0]`, `B[4..0]` (sinal-magnitude, bit 4 = sinal)", "`F` = 1 quando A = B"),
        func="Operação `011`: diz se A = B. As magnitudes têm de ser iguais e, se não forem zero, os sinais também; "
             "assim +0 e −0 são considerados iguais. A tabela completa tem 1024 linhas; abaixo, a forma compacta e exemplos.",
        tabela=table(["Magnitudes", "Sinais", "F"], rows) + "\n\n**Exemplos**\n\n" +
               table(["A[4..0]", "B[4..0]", "Comparação", "F"], ex),
        eq="* `F = [ (A3 ⊕ B3) + (A2 ⊕ B2) + (A1 ⊕ B1) + (A0 ⊕ B0) + (B3 + B2 + B1 + B0)·(A4 ⊕ B4) ]'`",
    )


OPS = {0: "A + B", 1: "A − B", 2: "C2 de B", 3: "A = B", 4: "A > B", 5: "A < B", 6: "A AND B", 7: "A XOR B"}


@bloco("decodificador_comparadores")
def _():
    want = {3: (1, 0), 4: (0, 1), 5: (1, 1)}
    names = ["S3", "S2", "S1"]
    rows = []
    for i in range(8):
        f2, f1 = want.get(i, (0, 0))
        rows.append(bits(i, 3) + [OPS[i], f2, f1])
    idx = lambda d: d["S3"] * 4 + d["S2"] * 2 + d["S1"]
    f1 = lambda d: want.get(idx(d), (0, 0))[1]
    f2 = lambda d: want.get(idx(d), (0, 0))[0]
    confere("decod_comp F1", f1, "S3S2'", names)
    confere("decod_comp F2", f2, "S3'S2S1 + S3S2'S1", names)
    return dict(
        cab=cabecalho("decodificador_comparadores", "", "`S3`, `S2`, `S1` (= `S[2]`, `S[1]`, `S[0]`)", "`F2`, `F1` (seletor do `mux_comparadores`)"),
        func="Traduz o código da operação no seletor do `mux_comparadores`: `F2 F1 = 10` em `011` (A = B), `01` em "
             "`100` (A > B), `11` em `101` (A < B) e `00` nas operações que não são comparações (STATUS = 0).",
        tabela=table(["S3", "S2", "S1", "Operação", "F2", "F1"], rows),
        eq="* `F1 = S3·S2'`\n* `F2 = S3'·S2·S1 + S3·S2'·S1 = S1·(S2 ⊕ S3)`",
        kmap="**F1**\n\n" + kmap(f1, names) + "\n\nUm grupo de dois: `S3·S2'`.\n\n**F2**\n\n" + kmap(f2, names) +
             "\n\nDois 1s isolados: `S3'·S2·S1 + S3·S2'·S1`, que se fatora em `S1·(S2 ⊕ S3)`.",
    )


@bloco("mux_comparadores")
def _():
    rows = [[0, 0, "0", "outras"], [0, 1, "compMaior", "`100`"], [1, 0, "compIgual", "`011`"], [1, 1, "compMenor", "`101`"]]
    return dict(
        cab=cabecalho("mux_comparadores", "", "`compIgual`, `compMaior`, `compMenor`, `F2`, `F1`", "`STATUS`"),
        func="Escolhe qual comparação vai para o LED de STATUS, conforme o seletor gerado pelo "
             "`decodificador_comparadores`. Com `F2 F1 = 00`, STATUS = 0. A tabela completa tem 32 linhas; abaixo, a forma compacta.",
        tabela=table(["F2", "F1", "STATUS", "Operação (S)"], rows),
        eq="* `STATUS = compIgual·F2·F1' + compMaior·F2'·F1 + compMenor·F2·F1`",
    )


@bloco("decodificador_saida")
def _():
    want = {0: (0, 0), 1: (0, 0), 2: (0, 1), 6: (1, 0), 7: (1, 1)}
    names = ["S3", "S2", "S1"]
    idx = lambda d: d["S3"] * 4 + d["S2"] * 2 + d["S1"]
    f1 = lambda d: want[idx(d)][0] if idx(d) in want else None
    f2 = lambda d: want[idx(d)][1] if idx(d) in want else None
    confere("decod_saida F1", f1, "S3", names)
    confere("decod_saida F2", f2, "S3'S2 + S2S1", names)
    rows = []
    escolhe = {0: "soma/subtração", 1: "soma/subtração", 2: "C2 de B", 6: "AND", 7: "XOR"}
    for i in range(8):
        d = dict(zip(names, bits(i, 3)))
        c1, c2 = sop("S3")(d), sop("S3'S2 + S2S1")(d)
        if i in want:
            rows.append(bits(i, 3) + [OPS[i], want[i][0], want[i][1], escolhe[i]])
        else:
            rows.append(bits(i, 3) + [OPS[i], f"X ({c1})", f"X ({c2})", "— (F zerado por F_EN)"])
    return dict(
        cab=cabecalho("decodificador_saida", "", "`S3`, `S2`, `S1` (= `S[2]`, `S[1]`, `S[0]`)",
                      "`F1`, `F2` (`F1` → `S[1]` e `F2` → `S[0]` do `mux_saida`)"),
        func="Traduz o código da operação no seletor do `mux_saida`, que escolhe entre soma/subtração (`00`), C2 de B "
             "(`01`), AND (`10`) e XOR (`11`). Nas comparações (`011`, `100`, `101`) a saída não importa (X), porque "
             "F é zerado pelo sinal `F_EN` da `ula`; esses X foram usados para simplificar. Entre parênteses, o valor "
             "que o circuito gera nesses casos.",
        tabela=table(["S3", "S2", "S1", "Operação", "F1", "F2", "mux_saida escolhe"], rows),
        eq="* `F1 = S3`\n* `F2 = S3'·S2 + S2·S1 = S2·(S3' + S1)`",
        kmap="**F1**\n\n" + kmap(f1, names) + "\n\nUsando os X, a linha `S3 = 1` inteira vira um grupo de quatro: `F1 = S3`.\n\n"
             "**F2**\n\n" + kmap(f2, names) + "\n\nDois grupos de dois (com X): `S3'·S2` e `S2·S1`.",
    )


@bloco("mux_saida")
def _():
    rows = [[0, 0, "SOMA_OU_SUB[5..0]", "`000`, `001`"], [0, 1, "Comp2B[5..0]", "`010`"],
            [1, 0, "OP_AND[5..0]", "`110`"], [1, 1, "OP_XOR[5..0]", "`111`"]]
    return dict(
        cab=cabecalho("mux_saida", lib("mux4x1") + " ×6",
                      "`SOMA_OU_SUB[5..0]`, `Comp2B[5..0]`, `OP_AND[5..0]`, `OP_XOR[5..0]`, `S[1..0]`", "`F[5..0]`"),
        func="Multiplexador 4:1 de 6 bits: seis `mux4x1`, um por bit, com o mesmo seletor `S[1..0]` (vindo do "
             "`decodificador_saida`). Escolhe qual dos quatro resultados vetoriais vai para F.",
        tabela=table(["S[1]", "S[0]", "F[5..0]", "Operação"], rows),
        eq="Para cada bit `k` = 0 … 5:\n\n"
           "* `F[k] = SOMA_OU_SUB[k]·S1'·S0' + Comp2B[k]·S1'·S0 + OP_AND[k]·S1·S0' + OP_XOR[k]·S1·S0`",
    )


@bloco("apaga_display")
def _():
    rows = [[0, 0, 1], [0, 1, 1], [1, 0, 0], [1, 1, 1]]
    return dict(
        cab=cabecalho("apaga_display", "", "`I[6..0]` (segmentos; `I[0]` = a … `I[6]` = g), `EN`", "`O[6..0]`"),
        func="Apaga um display quando `EN = 0`. Como os segmentos acendem com 0, basta forçar todos em 1: cada segmento "
             "passa por uma porta OR com `EN'`. Com `EN = 1`, os segmentos passam sem alteração. Na placa, `EN = DISP_EN`, "
             "então os displays de F só acendem na soma e na subtração.",
        tabela="**Um segmento**\n\n" + table(["EN", "I[k]", "O[k]"], rows) + "\n\n**Barramento**\n\n" +
               table(["EN", "O[6..0]"], [[0, "1111111 (apagado)"], [1, "I[6..0]"]]),
        eq="* `O[k] = I[k] + EN'`, para `k` = 0 … 6",
    )


# ---------------------------------------------------------- displays

AB_UNI = {
    "a": "A'B'C'D + A'BC'D' + AB'CD + ABCD'",
    "b": "ABCD + A'BCD' + A'BC'D",
    "c": "A'B'CD' + ABC'D'",
    "d": "AB'CD + A'BC'D' + A'B'C'D + A'BCD + ABCD'",
    "e": "D + A'BC' + ABC",
    "f": "B'CD + A'B'D + A'B'C + A'CD + ABC'",
    "g": "AB'C + A'B'C' + A'BCD",
}
AB_DEZ = {"a": "AB + AC", "b": "0", "c": "0", "d": "AB + AC", "e": "AB + AC", "f": "AB + AC", "g": "1"}

F_DEZ = {
    "a": "R4'R3R1 + R4'R3R2 + R4R3'R2'",
    "b": "0",
    "c": "R4R3R2' + R4R3'R2 + R4R3R1'",
    "d": "R4'R3R1 + R4'R3R2 + R4R3'R2'",
    "e": "R3R2R1 + R4'R3R1 + R4'R3R2 + R4R3'R2'",
    "f": "R4 + R3R2 + R3R1",
    "g": "R4' + R3'R2'",
}
F_UNI = {
    "a": "R4R3R2'R1'R0' + R4'R3R2R1R0' + R4R3'R2R1'R0 + R4'R3R2'R1R0 + R4'R3'R2R1'R0' + R4'R3'R2'R1'R0 + R4R3R2R1R0",
    "b": "R4R3R2'R1R0' + R4R3'R2'R1'R0' + R4R3R2'R1'R0 + R4'R3R2R1R0 + R4'R3'R2R1R0' + R4'R3'R2R1'R0",
    "c": "R4'R3R2R1'R0' + R4'R3'R2'R1R0' + R4R3'R2R1R0'",
    "d": "R4R3R2'R1'R0' + R4'R3'R2R1R0 + R4'R3R2R1R0' + R4'R3'R2R1'R0' + R4R3'R1'R0 + R4R3R1R0 + R3R2'R1R0 + R3'R2'R1'R0",
    "e": "R0 + R4R3R2'R1' + R4'R3'R2R1' + R4'R3R2R1",
    "f": "R4R2R1R0 + R4R3'R1'R0 + R4R3'R2R1 + R4'R3R2R1' + R4'R3'R1R0 + R3R2'R1R0 + R4'R3'R2'R1 + R4'R3'R2'R0",
    "g": "R4R3R2R1 + R3R2'R1R0 + R4R3'R2R1' + R4'R3R2'R1 + R3'R2'R1'R0 + R4'R3'R2'R1' + R4'R3'R2R1R0",
}


def seg_spec(names, digito, maximo):
    """spec de cada segmento: valor -> digito -> bit do segmento"""
    def mk(k):
        def f(d):
            v = 0
            for n in names:
                v = v * 2 + d[n]
            if v > maximo:
                return None
            return int(SEG[digito(v)][k])
        return f
    return {SEGN[k]: mk(k) for k in range(7)}


def disp_bloco(nome, names, digito, maximo, eqs, outnames, func, entradas, grupos_txt):
    w = len(names)
    specs = seg_spec(names, digito, maximo)
    for s, e in eqs.items():
        confere(f"{nome} {s}", specs[s], e, names)
    rows = []
    for v in range(1 << w):
        if v > maximo:
            rows.append(bits(v, w) + [v, "—"] + ["X"] * 7)
        else:
            dg = digito(v)
            rows.append(bits(v, w) + [v, dg] + list(SEG[dg]))
    km = []
    feitos = {}
    for s in SEGN:
        e = eqs[s]
        if e in ("0", "1"):
            km.append(f"**{outnames[s]}** = {e} (constante)")
            continue
        if e in feitos:
            km.append(f"**{outnames[s]}**: mesmo mapa de **{outnames[feitos[e]]}**.")
            continue
        feitos[e] = s
        km.append(f"**{outnames[s]}**\n\n" + kmap(specs[s], names))
    eq = "\n".join(f"* `{outnames[s]} = {eqs[s].replace(' + ', ' + ')}`" for s in SEGN)
    return dict(
        cab=cabecalho(nome, "", entradas, ", ".join(f"`{outnames[s]}`" for s in SEGN) + " (ativo em nível baixo: 0 acende)"),
        func=func,
        tabela=table(names + ["Valor", "Dígito"] + [outnames[s] for s in SEGN], rows),
        eq="Equações implementadas no circuito (`'` = NOT; cada termo é um grupo do mapa-K):\n\n" + eq,
        kmap=grupos_txt + "\n\n" + "\n\n".join(km),
    )


@bloco("decod7seg_ab_dezena")
def _():
    names = ["A", "B", "C", "D"]
    out = {s: f"seg_{s}" for s in SEGN}
    return disp_bloco(
        "decod7seg_ab_dezena", names, lambda v: v // 10, 15, AB_DEZ, out,
        "Gera os segmentos da dezena de uma magnitude de 0 a 15 (|A| no HEX7 e |B| no HEX5). A dezena é `1` quando o "
        "valor é ≥ 10 e `0` nos outros casos. Os segmentos b e c acendem nos dois dígitos (sempre 0), g nunca acende "
        "(sempre 1), e a, d, e, f só apagam quando o dígito é 1.",
        "`A`, `B`, `C`, `D` (`A` = bit mais significativo, peso 8)",
        "Linhas `AB`, colunas `CD`. Os segmentos a, d, e e f têm o mesmo mapa: 1 de 10 a 15, ou seja, `A·B + A·C = A·(B + C)`.")


@bloco("decod7seg_ab_unidade")
def _():
    names = ["A", "B", "C", "D"]
    out = {s: f"{s}u_seg" for s in SEGN}
    return disp_bloco(
        "decod7seg_ab_unidade", names, lambda v: v % 10, 15, AB_UNI, out,
        "Gera os segmentos da unidade de uma magnitude de 0 a 15 (|A| no HEX6 e |B| no HEX4): o dígito é o valor "
        "módulo 10. Em vez de converter para BCD, cada segmento é uma soma de produtos tirada direto da tabela abaixo.",
        "`A`, `B`, `C`, `D` (`A` = bit mais significativo, peso 8)",
        "Linhas `AB`, colunas `CD`. Cada mapa marca com 1 os valores em que o segmento fica apagado.")


@bloco("decod7seg_f_dezena")
def _():
    names = ["R4", "R3", "R2", "R1", "R0"]
    out = {s: f"{s}DEZ" for s in SEGN}
    return disp_bloco(
        "decod7seg_f_dezena", names, lambda v: v // 10, 30, F_DEZ, out,
        "Gera os segmentos da dezena de |F| (0 a 30), mostrada no HEX1: o dígito vai de 0 a 3. A entrada 31 não "
        "ocorre (X) e foi usada para simplificar.",
        "`R4` … `R0` (`R4` = bit mais significativo, peso 16)",
        "Cinco variáveis: um mapa para `R4 = 0` e outro para `R4 = 1`; linhas `R3R2`, colunas `R1R0`. "
        "A dezena só depende de `R4`, `R3`, `R2` e `R1`, porque `R0` não muda a dezena.")


@bloco("decod7seg_f_unidade")
def _():
    names = ["R4", "R3", "R2", "R1", "R0"]
    out = {s: f"{s}UNI" for s in SEGN}
    return disp_bloco(
        "decod7seg_f_unidade", names, lambda v: v % 10, 30, F_UNI, out,
        "Gera os segmentos da unidade de |F| (0 a 30), mostrada no HEX0: o dígito é o valor módulo 10. "
        "A entrada 31 não ocorre (X).",
        "`R4` … `R0` (`R4` = bit mais significativo, peso 16)",
        "Cinco variáveis: um mapa para `R4 = 0` e outro para `R4 = 1`; linhas `R3R2`, colunas `R1R0`. "
        "Como os 1s se repetem de 10 em 10, poucos ficam adjacentes, e várias equações têm termos com as cinco variáveis.")


@bloco("decod7seg_f")
def _():
    rows = []
    for v in range(31):
        rows.append([b(v, 5), v, v // 10, SEG[v // 10], v % 10, SEG[v % 10]])
    return dict(
        cab=cabecalho("decod7seg_f", lib("decod7seg_f_dezena") + ", " + lib("decod7seg_f_unidade"),
                      "`S[4..0]` (|F|, 0 a 30), `sinal_S`", "`aDEZ` … `gDEZ`, `aUNI` … `gUNI`, `led_negativo`"),
        func="Junta os decodificadores de dezena e unidade de |F|. O sinal de F é tratado à parte, como pede o "
             "enunciado: `led_negativo = sinal_S`. No toplevel, as saídas passam pelo `apaga_display` antes de chegar "
             "ao HEX1 e ao HEX0.",
        tabela=table(["S[4..0]", "|F|", "Dezena", "aDEZ…gDEZ", "Unidade", "aUNI…gUNI"], rows),
        eq="* `led_negativo = sinal_S`\n* dezena e unidade: ver `decod7seg_f_dezena` e `decod7seg_f_unidade`",
    )


# ------------------------------------------------------------------ ula

def ula_spec(a, bb, s):
    sa, ma = a >> 4, a & 15
    sb, mb = bb >> 4, bb & 15
    va, vb = (-ma if sa else ma), (-mb if sb else mb)
    st, f = 0, 0
    if s in (0, 1):
        r = va + vb if s == 0 else va - vb
        f = int(sm(r, 6), 2)
    elif s == 2:
        if sb and mb:
            c = (32 - mb) & 31
            f = (1 << 5) | c
        else:
            f = mb
    elif s == 3:
        st = int(va == vb)
    elif s == 4:
        st = int(va > vb)
    elif s == 5:
        st = int(va < vb)
    elif s == 6:
        f = ((sa & sb) << 5) | (ma & mb)
    else:
        f = ((sa ^ sb) << 5) | (ma ^ mb)
    return f, st, int(s in (0, 1))


@bloco("ula")
def _():
    names = ["S2", "S1", "S0"]
    idx = lambda d: d["S2"] * 4 + d["S1"] * 2 + d["S0"]
    fen = lambda d: int(idx(d) not in (3, 4, 5))
    den = lambda d: int(idx(d) in (0, 1))
    confere("F_EN", fen, "S2S1 + S2'S1' + S2'S0'", names)
    confere("DISP_EN", den, "S2'S1'", names)
    ops = [["000", "A + B", "`somador_subtrator`", 0, 1, 1],
           ["001", "A − B", "`somador_subtrator`", 0, 1, 1],
           ["010", "C2 de B", "`{OS, OS, O[3..0]}` do `comp2`", 0, 1, 0],
           ["011", "A = B", "000000", "`comparador_igual`", 0, 0],
           ["100", "A > B", "000000", "`comp_maior(A, B)`", 0, 0],
           ["101", "A < B", "000000", "`comp_maior(B, A)`", 0, 0],
           ["110", "A AND B", "`op_and`", 0, 1, 0],
           ["111", "A XOR B", "`op_xor`", 0, 1, 0]]
    casos = [(0, "00101", "10011"), (1, "00010", "00101"), (1, "11001", "01100"), (0, "11000", "11000"),
             (0, "11111", "11111"), (0, "01111", "01111"), (1, "00111", "00111"), (0, "10000", "00000"),
             (2, "00000", "10011"), (2, "00000", "00101"), (2, "00000", "11000"), (3, "10000", "00000"), (3, "00011", "10011"),
             (4, "00010", "10101"), (4, "10010", "10101"), (5, "10011", "10011"), (5, "10111", "00001"),
             (6, "00101", "00011"), (6, "10101", "10011"), (7, "00101", "00011"), (7, "11010", "00110")]

    def v(sx):
        m = int(sx[1:], 2)
        return ("−" if sx[0] == "1" else "+") + str(m)
    ex = []
    for s, a, bb in casos:
        f, st, de = ula_spec(int(a, 2), int(bb, 2), s)
        ex.append([b(s, 3), f"{a} ({v(a)})", f"{bb} ({v(bb)})", b(f, 6), st, de])
    return dict(
        cab=cabecalho("ula", "todos os blocos da ULA", "`A[4..0]`, `B[4..0]` (sinal-magnitude, bit 4 = sinal), `S[2..0]`",
                      "`F[5..0]` (sinal-magnitude, `F[5]` = sinal), `STATUS`, `DISP_EN`"),
        func="Liga todos os blocos: `somador_subtrator` (soma e subtração), `comp2` (C2 de B), `op_and`, `op_xor`, "
             "`comparador_igual` e duas instâncias do `comp_maior` (comparações), `decodificador_saida` + `mux_saida` "
             "(escolhem F) e `decodificador_comparadores` + `mux_comparadores` (escolhem STATUS). Acrescenta dois sinais "
             "de controle: `F_EN`, que zera F nas comparações (seis portas AND), e `DISP_EN`, que só deixa os displays de F "
             "acesos na soma e na subtração. A tabela completa tem 8192 linhas (2¹³); abaixo, o comportamento por "
             "operação e casos de teste, que também foram conferidos na placa.",
        tabela="**Por operação**\n\n" + table(["S", "Operação", "F", "STATUS", "F_EN", "DISP_EN"], ops) +
               "\n\n**Casos de teste**\n\n" + table(["S", "A", "B", "F[5..0]", "STATUS", "DISP_EN"], ex),
        eq="* `F_EN = (S2 ⊙ S1) + S2'·S0'` e `F[k] = FM[k]·F_EN` (FM = saída do `mux_saida`)\n"
           "* `DISP_EN = S2'·S1'`",
        kmap="**F_EN**\n\n" + kmap(fen, names) +
             "\n\nGrupos: `S2'·S1'`, `S2·S1` (que juntos formam `S2 ⊙ S1`) e `S2'·S0'`.\n\n**DISP_EN**\n\n" +
             kmap(den, names) + "\n\nUm grupo de dois: `S2'·S1'`.",
    )


ORDEM = list(BLOCOS)


def escreve(nome, d):
    partes = [d["cab"], "## Funcionamento\n\n" + d["func"], "## Tabela verdade\n\n" + d["tabela"],
              "## Equações\n\n" + d["eq"]]
    if d.get("kmap"):
        partes.append("## Mapas de Karnaugh\n\n" + d["kmap"])
    partes.append("## Observações\n")
    path = os.path.join(ROOT, "testes", nome, "tabela_verdade.md")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n\n".join(partes))


if __name__ == "__main__":
    for nome, fn in BLOCOS.items():
        escreve(nome, fn())
    print(f"{len(BLOCOS)} blocos gerados em {ROOT}/testes")
