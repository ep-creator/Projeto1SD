# somador_subtrator — tabela verdade e simulação

* **Circuito:** [`lib/somador_subtrator.bdf`](../../lib/somador_subtrator.bdf) ([`comp2`](../../lib/comp2.bdf) ×2, `XOR`, [`somador6`](../../lib/somador6.bdf), [`c2_para_sm`](../../lib/c2_para_sm.bdf))
* **Entradas:** `sinal_a`, `W[3..0]` (A), `sinal_b`, `X[3..0]` (B), `sinal_op` (0 = soma, 1 = subtração)
* **Saídas:** `R[5..0]` = A ± B em sinal-magnitude
* **Figuras do relatório (nesta pasta):** `somador_subtrator_circuito.png` (esquemático) e `somador_subtrator_simulacao.png` (waveform do `somador_subtrator.vwf`)


## Funcionamento

Faz a soma e a subtração da ULA (`S = 000` e `001`, com `sinal_op = S[0]`). A subtração vira soma: A − B = A + (−B), e trocar o sinal de B em sinal-magnitude é só inverter o bit de sinal (`sinal_b ⊕ sinal_op`). Depois, os dois operandos passam por `comp2` (SM → C2), são somados no `somador6` e o resultado volta para sinal-magnitude no `c2_para_sm`. A tabela completa tem 512 linhas; abaixo, casos representativos.

## Tabela verdade

| sinal_op | A (SM) | B (SM) | Conta | R[5..0] | R |
|:---:|:---:|:---:|:---:|:---:|:---:|
| 0 | 00101 | 10011 | (+5) + (−3) | 000010 | +2 |
| 0 | 10101 | 00011 | (−5) + (+3) | 100010 | −2 |
| 1 | 00010 | 00101 | (+2) − (+5) | 100011 | −3 |
| 1 | 11001 | 01100 | (−9) − (+12) | 110101 | −21 |
| 0 | 11000 | 11000 | (−8) + (−8) | 110000 | −16 |
| 0 | 11111 | 11111 | (−15) + (−15) | 111110 | −30 |
| 0 | 01111 | 01111 | (+15) + (+15) | 011110 | +30 |
| 1 | 01111 | 11111 | (+15) − (−15) | 011110 | +30 |
| 1 | 00111 | 00111 | (+7) − (+7) | 000000 | 0 |
| 0 | 00110 | 10110 | (+6) + (−6) | 000000 | 0 |
| 1 | 10100 | 10100 | (−4) − (−4) | 000000 | 0 |
| 0 | 00000 | 00000 | (0) + (0) | 000000 | 0 |
| 0 | 10000 | 00000 | (−0) + (+0) | 000000 | 0 |

## Equações

* `sinal_b' = sinal_b ⊕ sinal_op`
* `R = c2_para_sm( somador6( comp2(sinal_a, W), comp2(sinal_b', X) ) )`

## Observações
