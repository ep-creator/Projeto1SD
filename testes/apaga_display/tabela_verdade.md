# apaga_display — tabela verdade e simulação

* **Circuito:** [`lib/apaga_display.bdf`](../../lib/apaga_display.bdf)
* **Entradas:** `I[6..0]` (segmentos vindos do decodificador; `I[0]` = a … `I[6]` = g), `EN`
* **Saída:** `O[6..0]` = `I[6..0]` quando `EN = 1`; `1111111` (apagado, ativo baixo) quando `EN = 0`
* **Como funciona:** `O[k] = I[k] OR (NOT EN)`
* **Simulação:** `apaga_display.vwf` (a criar)

## Tabela verdade

| EN | I[k] | O[k] |
|:---:|:---:|:---:|
| 0 | 0 | 1 |
| 0 | 1 | 1 |
| 1 | 0 | 0 |
| 1 | 1 | 1 |

## Observações

