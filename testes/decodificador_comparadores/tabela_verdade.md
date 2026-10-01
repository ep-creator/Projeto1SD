# decodificador_comparadores — tabela verdade e simulação

* **Circuito:** [`lib/decodificador_comparadores.bdf`](../../lib/decodificador_comparadores.bdf)
* **Entradas:** `S3`, `S2`, `S1` (= `S[2]`, `S[1]`, `S[0]`)
* **Saídas:** `F2`, `F1` (seletor do `mux_comparadores`)
* **Figuras do relatório (nesta pasta):** `decodificador_comparadores_circuito.png` (esquemático) e `decodificador_comparadores_simulacao.png` (waveform do `decodificador_comparadores.vwf`)


## Funcionamento

Traduz o código da operação no seletor do `mux_comparadores`: `F2 F1 = 10` em `011` (A = B), `01` em `100` (A > B), `11` em `101` (A < B) e `00` nas operações que não são comparações (STATUS = 0).

## Tabela verdade

| S3 | S2 | S1 | Operação | F2 | F1 |
|:---:|:---:|:---:|:---:|:---:|:---:|
| 0 | 0 | 0 | A + B | 0 | 0 |
| 0 | 0 | 1 | A − B | 0 | 0 |
| 0 | 1 | 0 | C2 de B | 0 | 0 |
| 0 | 1 | 1 | A = B | 1 | 0 |
| 1 | 0 | 0 | A > B | 0 | 1 |
| 1 | 0 | 1 | A < B | 1 | 1 |
| 1 | 1 | 0 | A AND B | 0 | 0 |
| 1 | 1 | 1 | A XOR B | 0 | 0 |

## Equações

* `F1 = S3·S2'`
* `F2 = S3'·S2·S1 + S3·S2'·S1 = S1·(S2 ⊕ S3)`

## Mapas de Karnaugh

**F1**

| S3 \\ S2S1 | 00 | 01 | 11 | 10 |
|:---:|:---:|:---:|:---:|:---:|
| 0 | 0 | 0 | 0 | 0 |
| 1 | 1 | 1 | 0 | 0 |

Um grupo de dois: `S3·S2'`.

**F2**

| S3 \\ S2S1 | 00 | 01 | 11 | 10 |
|:---:|:---:|:---:|:---:|:---:|
| 0 | 0 | 0 | 1 | 0 |
| 1 | 0 | 1 | 0 | 0 |

Dois 1s isolados: `S3'·S2·S1 + S3·S2'·S1`, que se fatora em `S1·(S2 ⊕ S3)`.

## Observações
