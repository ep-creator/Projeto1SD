# decod7seg_ab_dezena — tabela verdade e simulação

* **Circuito:** [`lib/decod7seg_ab_dezena.bdf`](../../lib/decod7seg_ab_dezena.bdf)
* **Entradas:** `A`, `B`, `C`, `D` (`A` = bit mais significativo, peso 8)
* **Saídas:** `seg_a`, `seg_b`, `seg_c`, `seg_d`, `seg_e`, `seg_f`, `seg_g` (ativo em nível baixo: 0 acende)
* **Figuras do relatório (nesta pasta):** `decod7seg_ab_dezena_circuito.png` (esquemático) e `decod7seg_ab_dezena_simulacao.png` (waveform do `decod7seg_ab_dezena.vwf`)


## Funcionamento

Gera os segmentos da dezena de uma magnitude de 0 a 15 (|A| no HEX7 e |B| no HEX5). A dezena é `1` quando o valor é ≥ 10 e `0` nos outros casos. Os segmentos b e c acendem nos dois dígitos (sempre 0), g nunca acende (sempre 1), e a, d, e, f só apagam quando o dígito é 1.

## Tabela verdade

| A | B | C | D | Valor | Dígito | seg_a | seg_b | seg_c | seg_d | seg_e | seg_f | seg_g |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
| 0 | 0 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
| 0 | 0 | 1 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
| 0 | 0 | 1 | 1 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
| 0 | 1 | 0 | 0 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
| 0 | 1 | 0 | 1 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
| 0 | 1 | 1 | 0 | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
| 0 | 1 | 1 | 1 | 7 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
| 1 | 0 | 0 | 0 | 8 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
| 1 | 0 | 0 | 1 | 9 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
| 1 | 0 | 1 | 0 | 10 | 1 | 1 | 0 | 0 | 1 | 1 | 1 | 1 |
| 1 | 0 | 1 | 1 | 11 | 1 | 1 | 0 | 0 | 1 | 1 | 1 | 1 |
| 1 | 1 | 0 | 0 | 12 | 1 | 1 | 0 | 0 | 1 | 1 | 1 | 1 |
| 1 | 1 | 0 | 1 | 13 | 1 | 1 | 0 | 0 | 1 | 1 | 1 | 1 |
| 1 | 1 | 1 | 0 | 14 | 1 | 1 | 0 | 0 | 1 | 1 | 1 | 1 |
| 1 | 1 | 1 | 1 | 15 | 1 | 1 | 0 | 0 | 1 | 1 | 1 | 1 |

## Equações

Equações implementadas no circuito (`'` = NOT; cada termo é um grupo do mapa-K):

* `seg_a = AB + AC`
* `seg_b = 0`
* `seg_c = 0`
* `seg_d = AB + AC`
* `seg_e = AB + AC`
* `seg_f = AB + AC`
* `seg_g = 1`

## Mapas de Karnaugh

Linhas `AB`, colunas `CD`. Os segmentos a, d, e e f têm o mesmo mapa: 1 de 10 a 15, ou seja, `A·B + A·C = A·(B + C)`.

**seg_a**

| AB \\ CD | 00 | 01 | 11 | 10 |
|:---:|:---:|:---:|:---:|:---:|
| 00 | 0 | 0 | 0 | 0 |
| 01 | 0 | 0 | 0 | 0 |
| 11 | 1 | 1 | 1 | 1 |
| 10 | 0 | 0 | 1 | 1 |

**seg_b** = 0 (constante)

**seg_c** = 0 (constante)

**seg_d**: mesmo mapa de **seg_a**.

**seg_e**: mesmo mapa de **seg_a**.

**seg_f**: mesmo mapa de **seg_a**.

**seg_g** = 1 (constante)

## Observações
