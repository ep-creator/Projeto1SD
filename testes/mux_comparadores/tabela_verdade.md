# mux_comparadores — tabela verdade e simulação

* **Circuito:** [`lib/mux_comparadores.bdf`](../../lib/mux_comparadores.bdf)
* **Entradas:** `compIgual`, `compMaior`, `compMenor`, `F2`, `F1`
* **Saídas:** `STATUS`
* **Figuras do relatório (nesta pasta):** `mux_comparadores_circuito.png` (esquemático) e `mux_comparadores_simulacao.png` (waveform do `mux_comparadores.vwf`)


## Funcionamento

Escolhe qual comparação vai para o LED de STATUS, conforme o seletor gerado pelo `decodificador_comparadores`. Com `F2 F1 = 00`, STATUS = 0. A tabela completa tem 32 linhas; abaixo, a forma compacta.

## Tabela verdade

| F2 | F1 | STATUS | Operação (S) |
|:---:|:---:|:---:|:---:|
| 0 | 0 | 0 | outras |
| 0 | 1 | compMaior | `100` |
| 1 | 0 | compIgual | `011` |
| 1 | 1 | compMenor | `101` |

## Equações

* `STATUS = compIgual·F2·F1' + compMaior·F2'·F1 + compMenor·F2·F1`

## Observações
