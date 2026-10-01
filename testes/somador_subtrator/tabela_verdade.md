# somador_subtrator — tabela verdade e simulação

* **Circuito:** [`lib/somador_subtrator.bdf`](../../lib/somador_subtrator.bdf) (usa [`comp2`](../../lib/comp2.bdf) ×2, `XOR`, [`somador6`](../../lib/somador6.bdf) e [`c2_para_sm`](../../lib/c2_para_sm.bdf))
* **Entradas:** `sinal_a`, `W[3..0]` (A em sinal-magnitude), `sinal_b`, `X[3..0]` (B em sinal-magnitude), `sinal_op` (0 = soma, 1 = subtração)
* **Saída:** `R[5..0]` = A ± B em sinal-magnitude (`R[5]` = sinal, `R[4..0]` = magnitude até 30)
* **Simulação:** `somador_subtrator.vwf` (veio do grupo como `src/Waveform.vwf`, gravada quando a saída ainda era em C2: rodar de novo)

## Tabela verdade (casos de teste)

| Operação | A | B | R (SM) | R (dec) |
|:---:|:---:|:---:|:---:|:---:|
| +5 + (−3) |   |   |   |   |
| (−9) − (+12) |   |   |   |   |
| (−8) + (−8) |   |   |   |   |
| (−15) + (−15) |   |   |   |   |
| (+7) − (+7) |   |   |   |   |
| (−0) + (+0) |   |   |   |   |

## Observações

