# decod7seg_f — tabela verdade e simulação

* **Circuito:** [`lib/decod7seg_f.bdf`](../../lib/decod7seg_f.bdf) ([`decod7seg_f_dezena`](../../lib/decod7seg_f_dezena.bdf), [`decod7seg_f_unidade`](../../lib/decod7seg_f_unidade.bdf))
* **Entradas:** `S[4..0]` (|F|, 0 a 30), `sinal_S`
* **Saídas:** `aDEZ` … `gDEZ`, `aUNI` … `gUNI`, `led_negativo`
* **Figuras do relatório (nesta pasta):** `decod7seg_f_circuito.png` (esquemático) e `decod7seg_f_simulacao.png` (waveform do `decod7seg_f.vwf`)


## Funcionamento

Junta os decodificadores de dezena e unidade de |F|. O sinal de F é tratado à parte, como pede o enunciado: `led_negativo = sinal_S`. No toplevel, as saídas passam pelo `apaga_display` antes de chegar ao HEX1 e ao HEX0.

## Tabela verdade

| S[4..0] | |F| | Dezena | aDEZ…gDEZ | Unidade | aUNI…gUNI |
|:---:|:---:|:---:|:---:|:---:|:---:|
| 00000 | 0 | 0 | 0000001 | 0 | 0000001 |
| 00001 | 1 | 0 | 0000001 | 1 | 1001111 |
| 00010 | 2 | 0 | 0000001 | 2 | 0010010 |
| 00011 | 3 | 0 | 0000001 | 3 | 0000110 |
| 00100 | 4 | 0 | 0000001 | 4 | 1001100 |
| 00101 | 5 | 0 | 0000001 | 5 | 0100100 |
| 00110 | 6 | 0 | 0000001 | 6 | 0100000 |
| 00111 | 7 | 0 | 0000001 | 7 | 0001111 |
| 01000 | 8 | 0 | 0000001 | 8 | 0000000 |
| 01001 | 9 | 0 | 0000001 | 9 | 0000100 |
| 01010 | 10 | 1 | 1001111 | 0 | 0000001 |
| 01011 | 11 | 1 | 1001111 | 1 | 1001111 |
| 01100 | 12 | 1 | 1001111 | 2 | 0010010 |
| 01101 | 13 | 1 | 1001111 | 3 | 0000110 |
| 01110 | 14 | 1 | 1001111 | 4 | 1001100 |
| 01111 | 15 | 1 | 1001111 | 5 | 0100100 |
| 10000 | 16 | 1 | 1001111 | 6 | 0100000 |
| 10001 | 17 | 1 | 1001111 | 7 | 0001111 |
| 10010 | 18 | 1 | 1001111 | 8 | 0000000 |
| 10011 | 19 | 1 | 1001111 | 9 | 0000100 |
| 10100 | 20 | 2 | 0010010 | 0 | 0000001 |
| 10101 | 21 | 2 | 0010010 | 1 | 1001111 |
| 10110 | 22 | 2 | 0010010 | 2 | 0010010 |
| 10111 | 23 | 2 | 0010010 | 3 | 0000110 |
| 11000 | 24 | 2 | 0010010 | 4 | 1001100 |
| 11001 | 25 | 2 | 0010010 | 5 | 0100100 |
| 11010 | 26 | 2 | 0010010 | 6 | 0100000 |
| 11011 | 27 | 2 | 0010010 | 7 | 0001111 |
| 11100 | 28 | 2 | 0010010 | 8 | 0000000 |
| 11101 | 29 | 2 | 0010010 | 9 | 0000100 |
| 11110 | 30 | 3 | 0000110 | 0 | 0000001 |

## Equações

* `led_negativo = sinal_S`
* dezena e unidade: ver `decod7seg_f_dezena` e `decod7seg_f_unidade`

## Observações
