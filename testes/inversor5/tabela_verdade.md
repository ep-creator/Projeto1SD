# inversor5 — tabela verdade e simulação

* **Circuito:** [`lib/inversor5.bdf`](../../lib/inversor5.bdf)
* **Entradas:** `I[4..0]`
* **Saídas:** `O[4..0]`
* **Figuras do relatório (nesta pasta):** `inversor5_circuito.png` (esquemático) e `inversor5_simulacao.png` (waveform do `inversor5.vwf`)


## Funcionamento

Complemento a 2 de 5 bits, com a mesma regra do `inversor`. É usado no `c2_para_sm`, em que a magnitude do resultado chega a 30 e precisa de 5 bits.

## Tabela verdade

| I[4..0] | I | O[4..0] | I[4..0] | I | O[4..0] |
|:---:|:---:|:---:|:---:|:---:|:---:|
| 00000 | 0 | 00000 | 10000 | 16 | 10000 |
| 00001 | 1 | 11111 | 10001 | 17 | 01111 |
| 00010 | 2 | 11110 | 10010 | 18 | 01110 |
| 00011 | 3 | 11101 | 10011 | 19 | 01101 |
| 00100 | 4 | 11100 | 10100 | 20 | 01100 |
| 00101 | 5 | 11011 | 10101 | 21 | 01011 |
| 00110 | 6 | 11010 | 10110 | 22 | 01010 |
| 00111 | 7 | 11001 | 10111 | 23 | 01001 |
| 01000 | 8 | 11000 | 11000 | 24 | 01000 |
| 01001 | 9 | 10111 | 11001 | 25 | 00111 |
| 01010 | 10 | 10110 | 11010 | 26 | 00110 |
| 01011 | 11 | 10101 | 11011 | 27 | 00101 |
| 01100 | 12 | 10100 | 11100 | 28 | 00100 |
| 01101 | 13 | 10011 | 11101 | 29 | 00011 |
| 01110 | 14 | 10010 | 11110 | 30 | 00010 |
| 01111 | 15 | 10001 | 11111 | 31 | 00001 |

## Equações

* `O[0] = I[0]`
* `O[1] = I[1] ⊕ I[0]`
* `O[2] = I[2] ⊕ (I[1] + I[0])`
* `O[3] = I[3] ⊕ (I[2] + I[1] + I[0])`
* `O[4] = I[4] ⊕ (I[3] + I[2] + I[1] + I[0])`

## Observações
