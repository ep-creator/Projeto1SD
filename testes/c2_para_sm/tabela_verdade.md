# c2_para_sm — tabela verdade e simulação

* **Circuito:** [`lib/c2_para_sm.bdf`](../../lib/c2_para_sm.bdf) (usa [`inversor5`](../../lib/inversor5.bdf) e [`mux2x1`](../../lib/mux2x1.bdf) ×5)
* **Entrada:** `I[5..0]` em complemento a 2 (saída do `somador6`)
* **Saída:** `O[5..0]` em sinal-magnitude: `O[5]` = sinal, `O[4..0]` = magnitude (até 30)
* **Como funciona:** `O[5] = I[5]`. Se `I[5] = 0`, `O[4..0] = I[4..0]`; se `I[5] = 1`, `O[4..0]` = C2 de `I[4..0]` (`inversor5`). Os `mux2x1` usam `I[5]` como seletor.
* **Simulação:** `c2_para_sm.vwf` (a criar)

## Tabela verdade (casos de teste)

| I[5..0] (C2) | I (dec) | O[5..0] (SM) | Sinal | Magnitude |
|:---:|:---:|:---:|:---:|:---:|
| `000000` | 0 |   |   |   |
| `000111` | +7 |   |   |   |
| `011110` | +30 |   |   |   |
| `111111` | −1 |   |   |   |
| `110001` | −15 |   |   |   |
| `100010` | −30 |   |   |   |

## Observações

