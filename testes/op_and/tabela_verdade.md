# op_and — tabela verdade e simulação

* **Circuito:** [`lib/op_and.bdf`](../../lib/op_and.bdf)
* **Entradas:** `SA`, `A[3..0]`, `SB`, `B[3..0]`
* **Saídas:** `F[5..0]`
* **Figuras do relatório (nesta pasta):** `op_and_circuito.png` (esquemático) e `op_and_simulacao.png` (waveform do `op_and.vwf`)


## Funcionamento

Operação `110`: A AND B. A operação é bit a bit sobre os 5 bits de entrada: as magnitudes vão para `F[3..0]` e os sinais, para `F[5]`. `F[4]` fica sempre em 0, porque a magnitude de entrada tem só 4 bits. A tabela completa tem 1024 linhas; como cada bit é independente, basta a tabela de um bit e alguns exemplos.

## Tabela verdade

**Um bit**

| a | b | a · b |
|:---:|:---:|:---:|
| 0 | 0 | 0 |
| 0 | 1 | 0 |
| 1 | 0 | 0 |
| 1 | 1 | 1 |

**Exemplos**

| A (SM) | B (SM) | F[5..0] |
|:---:|:---:|:---:|
| 00101 | 00011 | 000001 |
| 10101 | 10011 | 100001 |
| 10101 | 00011 | 000001 |
| 01111 | 01001 | 001001 |
| 11100 | 11010 | 101000 |
| 00000 | 10111 | 000000 |

## Equações

* `F[k] = A[k] · B[k]`, para `k` = 0 … 3
* `F[4] = 0`
* `F[5] = SA · SB`

## Observações
