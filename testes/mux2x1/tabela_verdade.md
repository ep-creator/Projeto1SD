# mux2x1 — tabela verdade e simulação

* **Circuito:** [`lib/mux2x1.bdf`](../../lib/mux2x1.bdf)
* **Entradas:** `A`, `B`, `S`
* **Saídas:** `Y`
* **Figuras do relatório (nesta pasta):** `mux2x1_circuito.png` (esquemático) e `mux2x1_simulacao.png` (waveform do `mux2x1.vwf`)


## Funcionamento

Multiplexador 2:1 de 1 bit. Com `S = 0` a saída `Y` copia `A`; com `S = 1`, copia `B`. É usado no `comp2` e no `c2_para_sm` para escolher entre um número e o seu complemento a 2.

## Tabela verdade

| S | A | B | Y |
|:---:|:---:|:---:|:---:|
| 0 | 0 | 0 | 0 |
| 0 | 0 | 1 | 0 |
| 0 | 1 | 0 | 1 |
| 0 | 1 | 1 | 1 |
| 1 | 0 | 0 | 0 |
| 1 | 0 | 1 | 1 |
| 1 | 1 | 0 | 0 |
| 1 | 1 | 1 | 1 |

## Equações

* `Y = A·S' + B·S`

## Mapas de Karnaugh

| S \\ AB | 00 | 01 | 11 | 10 |
|:---:|:---:|:---:|:---:|:---:|
| 0 | 0 | 0 | 1 | 1 |
| 1 | 0 | 1 | 1 | 0 |

Grupos: `A·S'` (linha `S = 0`, colunas com `A = 1`) e `B·S` (linha `S = 1`, colunas com `B = 1`).

## Observações
