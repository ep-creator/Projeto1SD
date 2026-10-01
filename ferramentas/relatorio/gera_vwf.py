#!/usr/bin/env python3
"""Gera os .vwf (University Program VWF) de cada bloco em testes/<bloco>/.

Cada vetor de entrada fica T ns; as saídas ficam em X (o simulador preenche).
Uso: python3 gera_vwf.py <raiz do repositório> [bloco ...]
"""
import os
import sys

T = 20.0
CAB = """/*
WARNING: Do NOT edit the input and output ports in this file in a text
editor if you plan to continue editing the block that represents it in
the Block Editor! File corruption is VERY likely to occur.
*/

/*
Gerado por ferramentas/relatorio/gera_vwf.py (Projeto1SD).
*/

HEADER
{
	VERSION = 1;
	TIME_UNIT = ns;
	DATA_OFFSET = 0.0;
	DATA_DURATION = %.1f;
	SIMULATION_TIME = 0.0;
	GRID_PHASE = 0.0;
	GRID_PERIOD = %.1f;
	GRID_DUTY_CYCLE = 50;
}
"""


def sinal(nome, largura, direcao, pai=""):
    bus = largura > 1
    return (f'SIGNAL("{nome}")\n{{\n\tVALUE_TYPE = NINE_LEVEL_BIT;\n'
            f'\tSIGNAL_TYPE = {"BUS" if bus else "SINGLE_BIT"};\n\tWIDTH = {largura};\n'
            f'\tLSB_INDEX = {0 if bus else -1};\n\tDIRECTION = {direcao};\n\tPARENT = "{pai}";\n}}\n')


def transicoes(nome, niveis):
    linhas = []
    atual, dur = niveis[0], 0.0
    for n in niveis:
        if n == atual:
            dur += T
        else:
            linhas.append(f"\t\tLEVEL {atual} FOR {dur:.1f};")
            atual, dur = n, T
    linhas.append(f"\t\tLEVEL {atual} FOR {dur:.1f};")
    return (f'TRANSITION_LIST("{nome}")\n{{\n\tNODE\n\t{{\n\t\tREPEAT = 1;\n' + "\n".join(linhas) + "\n\t}\n}\n")


def vwf(entradas, saidas, vetores, radix=None):
    """entradas/saidas: lista de (nome, largura); vetores: lista de dict nome->int"""
    radix = radix or {}
    n = len(vetores)
    out = [CAB % (n * T, T)]
    for nome, w in entradas:
        out.append(sinal(nome, w, "INPUT"))
        for k in range(w - 1, -1, -1) if w > 1 else []:
            out.append(sinal(f"{nome}[{k}]", 1, "INPUT", nome))
    for nome, w in saidas:
        out.append(sinal(nome, w, "OUTPUT"))
        for k in range(w - 1, -1, -1) if w > 1 else []:
            out.append(sinal(f"{nome}[{k}]", 1, "OUTPUT", nome))
    for nome, w in entradas:
        bits = [f"{nome}[{k}]" for k in range(w - 1, -1, -1)] if w > 1 else [nome]
        for i, bn in enumerate(bits):
            k = w - 1 - i
            out.append(transicoes(bn, [(v[nome] >> k) & 1 for v in vetores]))
    for nome, w in saidas:
        bits = [f"{nome}[{k}]" for k in range(w - 1, -1, -1)] if w > 1 else [nome]
        for bn in bits:
            out.append(f'TRANSITION_LIST("{bn}")\n{{\n\tNODE\n\t{{\n\t\tREPEAT = 1;\n'
                       f'\t\tLEVEL X FOR {n * T:.1f};\n\t}}\n}}\n')
    idx = 0
    for nome, w in entradas + saidas:
        r = radix.get(nome, "Binary")
        if w > 1:
            filhos = ", ".join(str(idx + 1 + j) for j in range(w))
            out.append(f'DISPLAY_LINE\n{{\n\tCHANNEL = "{nome}";\n\tEXPAND_STATUS = COLLAPSED;\n\tRADIX = {r};\n'
                       f'\tTREE_INDEX = {idx};\n\tTREE_LEVEL = 0;\n\tCHILDREN = {filhos};\n}}\n')
            pai = idx
            idx += 1
            for k in range(w - 1, -1, -1):
                out.append(f'DISPLAY_LINE\n{{\n\tCHANNEL = "{nome}[{k}]";\n\tEXPAND_STATUS = COLLAPSED;\n\tRADIX = {r};\n'
                           f'\tTREE_INDEX = {idx};\n\tTREE_LEVEL = 1;\n\tPARENT = {pai};\n}}\n')
                idx += 1
        else:
            out.append(f'DISPLAY_LINE\n{{\n\tCHANNEL = "{nome}";\n\tEXPAND_STATUS = COLLAPSED;\n\tRADIX = {r};\n'
                       f'\tTREE_INDEX = {idx};\n\tTREE_LEVEL = 0;\n}}\n')
            idx += 1
    out.append("TIME_BAR\n{\n\tTIME = 0;\n\tMASTER = TRUE;\n}\n;\n")
    return "\n".join(out)


def conta(nomes, n=None):
    """vetores contando de 0 a 2^k-1 sobre a concatenação dos sinais (MSB primeiro)"""
    total = sum(w for _, w in nomes)
    vs = []
    for v in range(n if n is not None else 1 << total):
        d, desl = {}, total
        for nome, w in nomes:
            desl -= w
            d[nome] = (v >> desl) & ((1 << w) - 1)
        vs.append(d)
    return vs


def sm(v):
    return (16 if v < 0 else 0) | abs(v) if not isinstance(v, str) else (16 | int(v[1:]) if v.startswith("-") else int(v))


def c2_6(v):
    return v & 63


B = {}

# ---------------------------------------------------------------- blocos
B["mux2x1"] = lambda: vwf([("S", 1), ("A", 1), ("B", 1)], [("Y", 1)], conta([("S", 1), ("A", 1), ("B", 1)]))

B["mux4x1"] = lambda: vwf(
    [("I", 4), ("S", 2)], [("yi", 1)],
    [{"I": i, "S": s} for i in (0b0101, 0b1010, 0b0001, 0b0010, 0b0100, 0b1000) for s in range(4)])

B["inversor"] = lambda: vwf(
    [("I3", 1), ("I2", 1), ("I1", 1), ("I0", 1)], [("F3", 1), ("F2", 1), ("F1", 1), ("F0", 1)],
    conta([("I3", 1), ("I2", 1), ("I1", 1), ("I0", 1)]))

B["inversor5"] = lambda: vwf([("I", 5)], [("O", 5)], conta([("I", 5)]), {"I": "Unsigned", "O": "Unsigned"})

B["somador_completo"] = lambda: vwf([("A", 1), ("B", 1), ("Cin", 1)], [("S", 1), ("Cout", 1)],
                                    conta([("A", 1), ("B", 1), ("Cin", 1)]))

_c2sm = [0, 1, 2, 5, 9, 10, 15, 16, 20, 25, 29, 30, -1, -2, -5, -9, -10, -15, -16, -20, -21, -25, -29, -30]
B["c2_para_sm"] = lambda: vwf([("I", 6)], [("O", 6)], [{"I": c2_6(v)} for v in _c2sm], {"I": "Signed", "O": "Binary"})

_ss = [(0, 5, -3), (0, -5, 3), (1, 2, 5), (1, -9, 12), (0, -8, -8), (0, -15, -15), (0, 15, 15), (1, 15, -15),
       (1, 7, 7), (0, 6, -6), (1, -4, -4), (0, "-0", 0), (0, 0, 0), (1, 0, 9), (0, 12, -1), (1, -15, 15)]


def _ss_vet():
    vs = []
    for op, a, b in _ss:
        a, b = sm(a), sm(b)
        vs.append({"sinal_a": a >> 4, "W": a & 15, "sinal_b": b >> 4, "X": b & 15, "sinal_op": op})
    return vs


B["somador_subtrator"] = lambda: vwf(
    [("sinal_op", 1), ("sinal_a", 1), ("W", 4), ("sinal_b", 1), ("X", 4)], [("R", 6)], _ss_vet(),
    {"W": "Unsigned", "X": "Unsigned", "R": "Binary"})

_log = [(5, 3), (-5, -3), (-5, 3), (15, 9), (-12, -10), (0, -7), (10, 5), (-15, -15), (7, 0), (-1, 14), (9, -6), (3, 3)]


def _log_vet():
    vs = []
    for a, b in _log:
        a, b = sm(a), sm(b)
        vs.append({"SA": a >> 4, "A": a & 15, "SB": b >> 4, "B": b & 15})
    return vs


B["op_and"] = lambda: vwf([("SA", 1), ("A", 4), ("SB", 1), ("B", 4)], [("F", 6)], _log_vet())
B["op_xor"] = lambda: vwf([("SA", 1), ("A", 4), ("SB", 1), ("B", 4)], [("F", 6)], _log_vet())

_cm = [(5, 3), (3, 5), (2, -5), (-2, -5), (-5, -2), (-7, 1), (0, 0), (0, "-0"), ("-0", 0), (4, 4), (-4, -4),
       (15, -15), (-15, 15), (0, -1), (-1, 0), (9, 8)]


def _cm_vet():
    vs = []
    for a, b in _cm:
        a, b = sm(a), sm(b)
        vs.append({"SA": a >> 4, "A": a & 15, "SB": b >> 4, "B": b & 15})
    return vs


B["comp_maior"] = lambda: vwf([("SA", 1), ("A", 4), ("SB", 1), ("B", 4)], [("O", 1)], _cm_vet(),
                              {"A": "Unsigned", "B": "Unsigned"})

B["mux_saida"] = lambda: vwf(
    [("SOMA_OU_SUB", 6), ("Comp2B", 6), ("OP_AND", 6), ("OP_XOR", 6), ("S", 2)], [("F", 6)],
    [{"SOMA_OU_SUB": 0b000001, "Comp2B": 0b000010, "OP_AND": 0b000100, "OP_XOR": 0b001000, "S": s} for s in range(4)] +
    [{"SOMA_OU_SUB": 0b110101, "Comp2B": 0b111101, "OP_AND": 0b100001, "OP_XOR": 0b000110, "S": s} for s in range(4)])

_abcd = [("A", 1), ("B", 1), ("C", 1), ("D", 1)]
B["decod7seg_ab_dezena"] = lambda: vwf(_abcd, [(f"seg_{s}", 1) for s in "abcdefg"], conta(_abcd))
B["decod7seg_ab_unidade"] = lambda: vwf(_abcd, [(f"{s}u_seg", 1) for s in "abcdefg"], conta(_abcd))

_r = [("R4", 1), ("R3", 1), ("R2", 1), ("R1", 1), ("R0", 1)]
B["decod7seg_f_unidade"] = lambda: vwf(_r, [(f"{s}UNI", 1) for s in "abcdefg"], conta(_r, 31))

B["decod7seg_f"] = lambda: vwf(
    [("sinal_S", 1), ("S", 5)], [(f"{s}DEZ", 1) for s in "abcdefg"] + [(f"{s}UNI", 1) for s in "abcdefg"] + [("led_negativo", 1)],
    [{"sinal_S": v & 1, "S": v} for v in range(31)], {"S": "Unsigned"})

B["apaga_display"] = lambda: vwf(
    [("EN", 1), ("I", 7)], [("O", 7)],
    [{"EN": en, "I": i} for en in (1, 0) for i in (0b1000000, 0b1111001, 0b0010010, 0b0000000)])

_ula = [(0, "00101", "10011"), (1, "00010", "00101"), (1, "11001", "01100"), (0, "11000", "11000"),
        (0, "11111", "11111"), (0, "01111", "01111"), (1, "00111", "00111"), (0, "10000", "00000"),
        (2, "00000", "10011"), (2, "00000", "00101"), (2, "00000", "11000"), (3, "10000", "00000"), (3, "00011", "10011"),
        (4, "00010", "10101"), (4, "10010", "10101"), (5, "10011", "10011"), (5, "10111", "00001"),
        (6, "00101", "00011"), (6, "10101", "10011"), (7, "00101", "00011"), (7, "11010", "00110")]
B["ula"] = lambda: vwf([("S", 3), ("A", 5), ("B", 5)], [("F", 6), ("STATUS", 1), ("DISP_EN", 1)],
                       [{"S": s, "A": int(a, 2), "B": int(b, 2)} for s, a, b in _ula], {"S": "Unsigned"})


if __name__ == "__main__":
    raiz = sys.argv[1] if len(sys.argv) > 1 else "."
    nomes = sys.argv[2:] or list(B)
    for nome in nomes:
        p = os.path.join(raiz, "testes", nome, f"{nome}.vwf")
        with open(p, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(B[nome]())
        print("gerado", p)
