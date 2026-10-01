# somador_subtrator — tabela verdade e simulação

* **Circuito:** [`lib/somador_subtrator.bdf`](../../lib/somador_subtrator.bdf) (usa [`comp2`](../../lib/comp2.bdf) ×2, `XOR` e [`somador6`](../../lib/somador6.bdf))
* **Entradas:** `sinal_a`, `W[3..0]` (A em sinal-magnitude), `sinal_b`, `X[3..0]` (B em sinal-magnitude), `sinal_op` (0 = soma, 1 = subtração)
* **Saída:** `R[5..0]` = A ± B **em complemento a 2** (ainda falta o `c2_para_sm` para voltar a sinal-magnitude)
* **Simulação:** `somador_subtrator.vwf` (veio do grupo como `src/Waveform.vwf`)
* **Símbolo:** `lib/somador_subtrator.bsf` ainda não existe; gerar no Quartus

## Tabela verdade (casos de teste)

| Operação | A | B | R (C2) | R (dec) |
|:---:|:---:|:---:|:---:|:---:|
| +5 + (−3) |   |   |   |   |
| (−9) − (+12) |   |   |   |   |
| (−8) + (−8) |   |   |   |   |
| (−15) + (−15) |   |   |   |   |
| (+7) − (+7) |   |   |   |   |
| (−0) + (+0) |   |   |   |   |

## Observações

