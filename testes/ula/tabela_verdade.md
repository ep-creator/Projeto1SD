# ula — tabela verdade e simulação

* **Circuito:** [`lib/ula.bdf`](../../lib/ula.bdf) (todos os blocos da ULA)
* **Entradas:** `A[4..0]`, `B[4..0]` (sinal-magnitude, bit 4 = sinal), `S[2..0]`
* **Saídas:** `F[5..0]` (sinal-magnitude, `F[5]` = sinal), `STATUS`, `DISP_EN`
* **Figuras do relatório (nesta pasta):** `ula_circuito.png` (esquemático) e `ula_simulacao.png` (waveform do `ula.vwf`)


## Funcionamento

Liga todos os blocos: `somador_subtrator` (soma e subtração), `comp2` (C2 de B), `op_and`, `op_xor`, `comparador_igual` e duas instâncias do `comp_maior` (comparações), `decodificador_saida` + `mux_saida` (escolhem F) e `decodificador_comparadores` + `mux_comparadores` (escolhem STATUS). Acrescenta dois sinais de controle: `F_EN`, que zera F nas comparações (seis portas AND), e `DISP_EN`, que só deixa os displays de F acesos na soma e na subtração. A tabela completa tem 8192 linhas (2¹³); abaixo, o comportamento por operação e casos de teste, que também foram conferidos na placa.

## Tabela verdade

**Por operação**

| S | Operação | F | STATUS | F_EN | DISP_EN |
|:---:|:---:|:---:|:---:|:---:|:---:|
| 000 | A + B | `somador_subtrator` | 0 | 1 | 1 |
| 001 | A − B | `somador_subtrator` | 0 | 1 | 1 |
| 010 | C2 de B | `{OS, OS, O[3..0]}` do `comp2` | 0 | 1 | 0 |
| 011 | A = B | 000000 | `comparador_igual` | 0 | 0 |
| 100 | A > B | 000000 | `comp_maior(A, B)` | 0 | 0 |
| 101 | A < B | 000000 | `comp_maior(B, A)` | 0 | 0 |
| 110 | A AND B | `op_and` | 0 | 1 | 0 |
| 111 | A XOR B | `op_xor` | 0 | 1 | 0 |

**Casos de teste**

| S | A | B | F[5..0] | STATUS | DISP_EN |
|:---:|:---:|:---:|:---:|:---:|:---:|
| 000 | 00101 (+5) | 10011 (−3) | 000010 | 0 | 1 |
| 001 | 00010 (+2) | 00101 (+5) | 100011 | 0 | 1 |
| 001 | 11001 (−9) | 01100 (+12) | 110101 | 0 | 1 |
| 000 | 11000 (−8) | 11000 (−8) | 110000 | 0 | 1 |
| 000 | 11111 (−15) | 11111 (−15) | 111110 | 0 | 1 |
| 000 | 01111 (+15) | 01111 (+15) | 011110 | 0 | 1 |
| 001 | 00111 (+7) | 00111 (+7) | 000000 | 0 | 1 |
| 000 | 10000 (−0) | 00000 (+0) | 000000 | 0 | 1 |
| 010 | 00000 (+0) | 10011 (−3) | 111101 | 0 | 0 |
| 010 | 00000 (+0) | 00101 (+5) | 000101 | 0 | 0 |
| 010 | 00000 (+0) | 11000 (−8) | 111000 | 0 | 0 |
| 011 | 10000 (−0) | 00000 (+0) | 000000 | 1 | 0 |
| 011 | 00011 (+3) | 10011 (−3) | 000000 | 0 | 0 |
| 100 | 00010 (+2) | 10101 (−5) | 000000 | 1 | 0 |
| 100 | 10010 (−2) | 10101 (−5) | 000000 | 1 | 0 |
| 101 | 10011 (−3) | 10011 (−3) | 000000 | 0 | 0 |
| 101 | 10111 (−7) | 00001 (+1) | 000000 | 1 | 0 |
| 110 | 00101 (+5) | 00011 (+3) | 000001 | 0 | 0 |
| 110 | 10101 (−5) | 10011 (−3) | 100001 | 0 | 0 |
| 111 | 00101 (+5) | 00011 (+3) | 000110 | 0 | 0 |
| 111 | 11010 (−10) | 00110 (+6) | 101100 | 0 | 0 |

## Equações

* `F_EN = (S2 ⊙ S1) + S2'·S0'` e `F[k] = FM[k]·F_EN` (FM = saída do `mux_saida`)
* `DISP_EN = S2'·S1'`

## Mapas de Karnaugh

**F_EN**

| S2 \\ S1S0 | 00 | 01 | 11 | 10 |
|:---:|:---:|:---:|:---:|:---:|
| 0 | 1 | 1 | 0 | 1 |
| 1 | 0 | 0 | 1 | 1 |

Grupos: `S2'·S1'`, `S2·S1` (que juntos formam `S2 ⊙ S1`) e `S2'·S0'`.

**DISP_EN**

| S2 \\ S1S0 | 00 | 01 | 11 | 10 |
|:---:|:---:|:---:|:---:|:---:|
| 0 | 1 | 1 | 0 | 0 |
| 1 | 0 | 0 | 0 | 0 |

Um grupo de dois: `S2'·S1'`.

## Observações
