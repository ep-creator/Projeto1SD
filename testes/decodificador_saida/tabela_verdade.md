# decodificador_saida — tabela verdade e simulação

* **Circuito:** [`lib/decodificador_saida.bdf`](../../lib/decodificador_saida.bdf)
* **Entradas:** `S3`, `S2`, `S1` (= `S[2]`, `S[1]`, `S[0]`)
* **Saídas:** `F1`, `F2` (`F1` → `S[1]` e `F2` → `S[0]` do `mux_saida`)
* **Figuras do relatório (nesta pasta):** `decodificador_saida_circuito.png` (esquemático) e `decodificador_saida_simulacao.png` (waveform do `decodificador_saida.vwf`)


## Funcionamento

Traduz o código da operação no seletor do `mux_saida`, que escolhe entre soma/subtração (`00`), C2 de B (`01`), AND (`10`) e XOR (`11`). Nas comparações (`011`, `100`, `101`) a saída não importa (X), porque F é zerado pelo sinal `F_EN` da `ula`; esses X foram usados para simplificar. Entre parênteses, o valor que o circuito gera nesses casos.

## Tabela verdade

| S3 | S2 | S1 | Operação | F1 | F2 | mux_saida escolhe |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 0 | 0 | 0 | A + B | 0 | 0 | soma/subtração |
| 0 | 0 | 1 | A − B | 0 | 0 | soma/subtração |
| 0 | 1 | 0 | C2 de B | 0 | 1 | C2 de B |
| 0 | 1 | 1 | A = B | X (0) | X (1) | — (F zerado por F_EN) |
| 1 | 0 | 0 | A > B | X (1) | X (0) | — (F zerado por F_EN) |
| 1 | 0 | 1 | A < B | X (1) | X (0) | — (F zerado por F_EN) |
| 1 | 1 | 0 | A AND B | 1 | 0 | AND |
| 1 | 1 | 1 | A XOR B | 1 | 1 | XOR |

## Equações

* `F1 = S3`
* `F2 = S3'·S2 + S2·S1 = S2·(S3' + S1)`

## Mapas de Karnaugh

**F1**

| S3 \\ S2S1 | 00 | 01 | 11 | 10 |
|:---:|:---:|:---:|:---:|:---:|
| 0 | 0 | 0 | X | 0 |
| 1 | X | X | 1 | 1 |

Usando os X, a linha `S3 = 1` inteira vira um grupo de quatro: `F1 = S3`.

**F2**

| S3 \\ S2S1 | 00 | 01 | 11 | 10 |
|:---:|:---:|:---:|:---:|:---:|
| 0 | 0 | 0 | X | 1 |
| 1 | X | X | 1 | 0 |

Dois grupos de dois (com X): `S3'·S2` e `S2·S1`.

## Observações
