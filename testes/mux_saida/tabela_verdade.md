# mux_saida — tabela verdade e simulação

* **Circuito:** [`lib/mux_saida.bdf`](../../lib/mux_saida.bdf) ([`mux4x1`](../../lib/mux4x1.bdf) ×6)
* **Entradas:** `SOMA_OU_SUB[5..0]`, `Comp2B[5..0]`, `OP_AND[5..0]`, `OP_XOR[5..0]`, `S[1..0]`
* **Saídas:** `F[5..0]`
* **Figuras do relatório (nesta pasta):** `mux_saida_circuito.png` (esquemático) e `mux_saida_simulacao.png` (waveform do `mux_saida.vwf`)


## Funcionamento

Multiplexador 4:1 de 6 bits: seis `mux4x1`, um por bit, com o mesmo seletor `S[1..0]` (vindo do `decodificador_saida`). Escolhe qual dos quatro resultados vetoriais vai para F.

## Tabela verdade

| S[1] | S[0] | F[5..0] | Operação |
|:---:|:---:|:---:|:---:|
| 0 | 0 | SOMA_OU_SUB[5..0] | `000`, `001` |
| 0 | 1 | Comp2B[5..0] | `010` |
| 1 | 0 | OP_AND[5..0] | `110` |
| 1 | 1 | OP_XOR[5..0] | `111` |

## Equações

Para cada bit `k` = 0 … 5:

* `F[k] = SOMA_OU_SUB[k]·S1'·S0' + Comp2B[k]·S1'·S0 + OP_AND[k]·S1·S0' + OP_XOR[k]·S1·S0`

## Observações
