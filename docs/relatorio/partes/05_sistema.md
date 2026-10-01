# Sistema completo

## ULA

<!-- BLOCO: ula | 0 -->

## Toplevel

O toplevel (`src/toplevel.bdf`) é o circuito que vai para a placa: liga a `ula`, os decodificadores e os LEDs aos pinos da DE2-115.

| De | Para |
|:---|:---|
| SW[17..13], SW[12..8], SW[2..0] | `ula`: A, B e S |
| SW[17..0] | LEDR[17..0] (cópia das chaves) |
| `ula`.F[5..0] | LEDG[5..0] |
| `ula`.STATUS | LEDG8 |
| SW[16..13] (\|A\|) | `decod7seg_ab_dezena` → HEX7 e `decod7seg_ab_unidade` → HEX6 |
| SW[11..8] (\|B\|) | `decod7seg_ab_dezena` → HEX5 e `decod7seg_ab_unidade` → HEX4 |
| `ula`.F[4..0] e F[5] | `decod7seg_f` → `apaga_display` (EN = DISP_EN) → HEX1 (dezena) e HEX0 (unidade) |
| NAND(F[5], DISP_EN) | HEX2[6] (segmento g, o "−"); HEX2[5..0] em VCC (apagados) |

<!-- FIGURA: docs/relatorio/figuras/toplevel_circuito.png | Circuito do toplevel (src/toplevel.bdf) -->

## Pinagem

A pinagem do FPGA Cyclone IV E EP4CE115F29C7 está em `src/Projeto1SD.qsf` (92 pinos). O ponto decimal dos displays não é ligado à FPGA na DE2-115; por isso os sinais de A e de B são mostrados nos LEDs LEDR17 e LEDR12.

**Chaves**

| Sinal | Pino | Função | Sinal | Pino | Função |
|:---:|:---:|:---:|:---:|:---:|:---:|
| SW[0] | PIN_AB28 | S[0] | SW[9] | PIN_AB25 | B[1] |
| SW[1] | PIN_AC28 | S[1] | SW[10] | PIN_AC24 | B[2] |
| SW[2] | PIN_AC27 | S[2] | SW[11] | PIN_AB24 | B[3] |
| SW[3] | PIN_AD27 | — | SW[12] | PIN_AB23 | sinal de B |
| SW[4] | PIN_AB27 | — | SW[13] | PIN_AA24 | A[0] |
| SW[5] | PIN_AC26 | — | SW[14] | PIN_AA23 | A[1] |
| SW[6] | PIN_AD26 | — | SW[15] | PIN_AA22 | A[2] |
| SW[7] | PIN_AB26 | — | SW[16] | PIN_Y24 | A[3] |
| SW[8] | PIN_AC25 | B[0] | SW[17] | PIN_Y23 | sinal de A |

**LEDs**

| Sinal | Pino | Sinal | Pino | Sinal | Pino |
|:---:|:---:|:---:|:---:|:---:|:---:|
| LEDR[0] | PIN_G19 | LEDR[9] | PIN_G17 | LEDG[0] (F0) | PIN_E21 |
| LEDR[1] | PIN_F19 | LEDR[10] | PIN_J15 | LEDG[1] (F1) | PIN_E22 |
| LEDR[2] | PIN_E19 | LEDR[11] | PIN_H16 | LEDG[2] (F2) | PIN_E25 |
| LEDR[3] | PIN_F21 | LEDR[12] | PIN_J16 | LEDG[3] (F3) | PIN_E24 |
| LEDR[4] | PIN_F18 | LEDR[13] | PIN_H17 | LEDG[4] (F4) | PIN_H21 |
| LEDR[5] | PIN_E18 | LEDR[14] | PIN_F15 | LEDG[5] (sinal de F) | PIN_G20 |
| LEDR[6] | PIN_J19 | LEDR[15] | PIN_G15 | LEDG[8] (STATUS) | PIN_F17 |
| LEDR[7] | PIN_H19 | LEDR[16] | PIN_G16 | | |
| LEDR[8] | PIN_J17 | LEDR[17] | PIN_H15 | | |

**Displays** (índice 0 = segmento a … 6 = segmento g; acendem com 0)

| Display | Função | [0] | [1] | [2] | [3] | [4] | [5] | [6] |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| HEX7 | dezena de \|A\| | AD17 | AE17 | AG17 | AH17 | AF17 | AG18 | AA14 |
| HEX6 | unidade de \|A\| | AA17 | AB16 | AA16 | AB17 | AB15 | AA15 | AC17 |
| HEX5 | dezena de \|B\| | AD18 | AC18 | AB18 | AH19 | AG19 | AF18 | AH18 |
| HEX4 | unidade de \|B\| | AB19 | AA19 | AG21 | AH21 | AE19 | AF19 | AE18 |
| HEX2 | sinal de F | AA25 | AA26 | Y25 | W26 | Y26 | W27 | W28 |
| HEX1 | dezena de \|F\| | M24 | Y22 | W21 | W22 | W25 | U23 | U24 |
| HEX0 | unidade de \|F\| | G18 | F22 | E17 | L26 | L25 | J22 | H22 |

## Teste na placa

O projeto completo (`src/Projeto1SD.qpf`) foi compilado sem erros e gravado na DE2-115 por JTAG. Os casos abaixo foram conferidos na placa (A nas chaves SW17..SW13, B em SW12..SW8 e S em SW2..SW0):

| S | A | B | Conta | HEX2 HEX1 HEX0 | LEDG5..LEDG0 | LEDG8 |
|:---:|:---:|:---:|:---|:---:|:---:|:---:|
| 000 | 00101 (+5) | 10011 (−3) | 5 + (−3) = +2 | _ 0 2 | 000010 | apagado |
| 001 | 00010 (+2) | 00101 (+5) | 2 − 5 = −3 | − 0 3 | 100011 | apagado |
| 001 | 11001 (−9) | 01100 (+12) | −9 − 12 = −21 | − 2 1 | 110101 | apagado |
| 000 | 11000 (−8) | 11000 (−8) | −8 + (−8) = −16 | − 1 6 | 110000 | apagado |
| 000 | 11111 (−15) | 11111 (−15) | −15 + (−15) = −30 | − 3 0 | 111110 | apagado |
| 000 | 01111 (+15) | 01111 (+15) | 15 + 15 = +30 | _ 3 0 | 011110 | apagado |
| 001 | 00111 (+7) | 00111 (+7) | 7 − 7 = 0 | _ 0 0 | 000000 | apagado |
| 000 | 10000 (−0) | 00000 (+0) | −0 + 0 = 0 | _ 0 0 | 000000 | apagado |
| 010 | qualquer | 10011 (−3) | C2(−3) = 11101 | apagados | 111101 | apagado |
| 010 | qualquer | 00101 (+5) | C2(+5) = 00101 | apagados | 000101 | apagado |
| 011 | 10000 (−0) | 00000 (+0) | −0 = +0 ? sim | apagados | 000000 | aceso |
| 011 | 00011 (+3) | 10011 (−3) | +3 = −3 ? não | apagados | 000000 | apagado |
| 100 | 00010 (+2) | 10101 (−5) | +2 > −5 ? sim | apagados | 000000 | aceso |
| 100 | 10010 (−2) | 10101 (−5) | −2 > −5 ? sim | apagados | 000000 | aceso |
| 101 | 10011 (−3) | 10011 (−3) | −3 < −3 ? não | apagados | 000000 | apagado |
| 101 | 10111 (−7) | 00001 (+1) | −7 < +1 ? sim | apagados | 000000 | aceso |
| 110 | 00101 (+5) | 00011 (+3) | 0101 AND 0011 | apagados | 000001 | apagado |
| 110 | 10101 (−5) | 10011 (−3) | sinais 1 AND 1 | apagados | 100001 | apagado |
| 111 | 00101 (+5) | 00011 (+3) | 0101 XOR 0011 | apagados | 000110 | apagado |

Na coluna dos displays, "_" indica HEX2 apagado (resultado positivo).

<!-- FIGURA: docs/relatorio/figuras/placa.jpg | ULA funcionando na DE2-115 -->
