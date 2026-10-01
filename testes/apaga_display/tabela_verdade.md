# apaga_display — tabela verdade e simulação

* **Circuito:** [`lib/apaga_display.bdf`](../../lib/apaga_display.bdf)
* **Entradas:** `I[6..0]` (segmentos; `I[0]` = a … `I[6]` = g), `EN`
* **Saídas:** `O[6..0]`
* **Figuras do relatório (nesta pasta):** `apaga_display_circuito.png` (esquemático) e `apaga_display_simulacao.png` (waveform do `apaga_display.vwf`)


## Funcionamento

Apaga um display quando `EN = 0`. Como os segmentos acendem com 0, basta forçar todos em 1: cada segmento passa por uma porta OR com `EN'`. Com `EN = 1`, os segmentos passam sem alteração. Na placa, `EN = DISP_EN`, então os displays de F só acendem na soma e na subtração.

## Tabela verdade

**Um segmento**

| EN | I[k] | O[k] |
|:---:|:---:|:---:|
| 0 | 0 | 1 |
| 0 | 1 | 1 |
| 1 | 0 | 0 |
| 1 | 1 | 1 |

**Barramento**

| EN | O[6..0] |
|:---:|:---:|
| 0 | 1111111 (apagado) |
| 1 | I[6..0] |

## Equações

* `O[k] = I[k] + EN'`, para `k` = 0 … 6

## Observações
