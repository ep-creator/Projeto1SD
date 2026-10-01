# mux4x1 — tabela verdade e simulação

* **Circuito:** [`lib/mux4x1.bdf`](../../lib/mux4x1.bdf)
* **Entradas:** `I[3..0]`, `S[1..0]`
* **Saídas:** `yi`
* **Figuras do relatório (nesta pasta):** `mux4x1_circuito.png` (esquemático) e `mux4x1_simulacao.png` (waveform do `mux4x1.vwf`)


## Funcionamento

Multiplexador 4:1 de 1 bit: o seletor `S[1..0]` escolhe qual das quatro entradas vai para `yi`. O `mux_saida` usa seis deles, um por bit de F. A tabela completa tem 64 linhas; abaixo, a forma compacta (cada linha vale para qualquer valor das entradas não selecionadas).

## Tabela verdade

| S[1] | S[0] | yi |
|:---:|:---:|:---:|
| 0 | 0 | I[0] |
| 0 | 1 | I[1] |
| 1 | 0 | I[2] |
| 1 | 1 | I[3] |

## Equações

* `yi = I0·S1'·S0' + I1·S1'·S0 + I2·S1·S0' + I3·S1·S0`

Cada termo é uma porta AND que só deixa passar a entrada cujo índice é igual a `S`; a porta OR junta os quatro termos.

## Observações
