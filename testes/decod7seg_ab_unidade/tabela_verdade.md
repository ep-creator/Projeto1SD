# decod7seg_ab_unidade — tabela verdade e simulação

* **Circuito:** [`lib/decod7seg_ab_unidade.bdf`](../../lib/decod7seg_ab_unidade.bdf)
* **Entradas:** `A`, `B`, `C`, `D` (`A` = bit mais significativo, peso 8)
* **Saídas:** `au_seg`, `bu_seg`, `cu_seg`, `du_seg`, `eu_seg`, `fu_seg`, `gu_seg` (ativo em nível baixo: 0 acende)
* **Figuras do relatório (nesta pasta):** `decod7seg_ab_unidade_circuito.png` (esquemático) e `decod7seg_ab_unidade_simulacao.png` (waveform do `decod7seg_ab_unidade.vwf`)


## Funcionamento

Gera os segmentos da unidade de uma magnitude de 0 a 15 (|A| no HEX6 e |B| no HEX4): o dígito é o valor módulo 10. Em vez de converter para BCD, cada segmento é uma soma de produtos tirada direto da tabela abaixo.

## Tabela verdade

| A | B | C | D | Valor | Dígito | au_seg | bu_seg | cu_seg | du_seg | eu_seg | fu_seg | gu_seg |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
| 0 | 0 | 0 | 1 | 1 | 1 | 1 | 0 | 0 | 1 | 1 | 1 | 1 |
| 0 | 0 | 1 | 0 | 2 | 2 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |
| 0 | 0 | 1 | 1 | 3 | 3 | 0 | 0 | 0 | 0 | 1 | 1 | 0 |
| 0 | 1 | 0 | 0 | 4 | 4 | 1 | 0 | 0 | 1 | 1 | 0 | 0 |
| 0 | 1 | 0 | 1 | 5 | 5 | 0 | 1 | 0 | 0 | 1 | 0 | 0 |
| 0 | 1 | 1 | 0 | 6 | 6 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| 0 | 1 | 1 | 1 | 7 | 7 | 0 | 0 | 0 | 1 | 1 | 1 | 1 |
| 1 | 0 | 0 | 0 | 8 | 8 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 1 | 0 | 0 | 1 | 9 | 9 | 0 | 0 | 0 | 0 | 1 | 0 | 0 |
| 1 | 0 | 1 | 0 | 10 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
| 1 | 0 | 1 | 1 | 11 | 1 | 1 | 0 | 0 | 1 | 1 | 1 | 1 |
| 1 | 1 | 0 | 0 | 12 | 2 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |
| 1 | 1 | 0 | 1 | 13 | 3 | 0 | 0 | 0 | 0 | 1 | 1 | 0 |
| 1 | 1 | 1 | 0 | 14 | 4 | 1 | 0 | 0 | 1 | 1 | 0 | 0 |
| 1 | 1 | 1 | 1 | 15 | 5 | 0 | 1 | 0 | 0 | 1 | 0 | 0 |

## Equações

Equações implementadas no circuito (`'` = NOT; cada termo é um grupo do mapa-K):

* `au_seg = A'B'C'D + A'BC'D' + AB'CD + ABCD'`
* `bu_seg = ABCD + A'BCD' + A'BC'D`
* `cu_seg = A'B'CD' + ABC'D'`
* `du_seg = AB'CD + A'BC'D' + A'B'C'D + A'BCD + ABCD'`
* `eu_seg = D + A'BC' + ABC`
* `fu_seg = B'CD + A'B'D + A'B'C + A'CD + ABC'`
* `gu_seg = AB'C + A'B'C' + A'BCD`

## Mapas de Karnaugh

Linhas `AB`, colunas `CD`. Cada mapa marca com 1 os valores em que o segmento fica apagado.

**au_seg**

| AB \\ CD | 00 | 01 | 11 | 10 |
|:---:|:---:|:---:|:---:|:---:|
| 00 | 0 | 1 | 0 | 0 |
| 01 | 1 | 0 | 0 | 0 |
| 11 | 0 | 0 | 0 | 1 |
| 10 | 0 | 0 | 1 | 0 |

**bu_seg**

| AB \\ CD | 00 | 01 | 11 | 10 |
|:---:|:---:|:---:|:---:|:---:|
| 00 | 0 | 0 | 0 | 0 |
| 01 | 0 | 1 | 0 | 1 |
| 11 | 0 | 0 | 1 | 0 |
| 10 | 0 | 0 | 0 | 0 |

**cu_seg**

| AB \\ CD | 00 | 01 | 11 | 10 |
|:---:|:---:|:---:|:---:|:---:|
| 00 | 0 | 0 | 0 | 1 |
| 01 | 0 | 0 | 0 | 0 |
| 11 | 1 | 0 | 0 | 0 |
| 10 | 0 | 0 | 0 | 0 |

**du_seg**

| AB \\ CD | 00 | 01 | 11 | 10 |
|:---:|:---:|:---:|:---:|:---:|
| 00 | 0 | 1 | 0 | 0 |
| 01 | 1 | 0 | 1 | 0 |
| 11 | 0 | 0 | 0 | 1 |
| 10 | 0 | 0 | 1 | 0 |

**eu_seg**

| AB \\ CD | 00 | 01 | 11 | 10 |
|:---:|:---:|:---:|:---:|:---:|
| 00 | 0 | 1 | 1 | 0 |
| 01 | 1 | 1 | 1 | 0 |
| 11 | 0 | 1 | 1 | 1 |
| 10 | 0 | 1 | 1 | 0 |

**fu_seg**

| AB \\ CD | 00 | 01 | 11 | 10 |
|:---:|:---:|:---:|:---:|:---:|
| 00 | 0 | 1 | 1 | 1 |
| 01 | 0 | 0 | 1 | 0 |
| 11 | 1 | 1 | 0 | 0 |
| 10 | 0 | 0 | 1 | 0 |

**gu_seg**

| AB \\ CD | 00 | 01 | 11 | 10 |
|:---:|:---:|:---:|:---:|:---:|
| 00 | 1 | 1 | 0 | 0 |
| 01 | 0 | 0 | 1 | 0 |
| 11 | 0 | 0 | 0 | 0 |
| 10 | 0 | 0 | 1 | 1 |

## Observações
