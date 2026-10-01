# somador_completo — tabela verdade e simulação

* **Circuito:** [`lib/somador_completo.bdf`](../../lib/somador_completo.bdf)
* **Entradas:** `A`, `B`, `Cin`
* **Saídas:** `S`, `Cout`
* **Figuras do relatório (nesta pasta):** `somador_completo_circuito.png` (esquemático) e `somador_completo_simulacao.png` (waveform do `somador_completo.vwf`)


## Funcionamento

Soma três bits (dois operandos e o vai-um da etapa anterior), gerando o bit de soma `S` e o vai-um `Cout`. É a célula do `somador6`.

## Tabela verdade

| A | B | Cin | S | Cout |
|:---:|:---:|:---:|:---:|:---:|
| 0 | 0 | 0 | 0 | 0 |
| 0 | 0 | 1 | 1 | 0 |
| 0 | 1 | 0 | 1 | 0 |
| 0 | 1 | 1 | 0 | 1 |
| 1 | 0 | 0 | 1 | 0 |
| 1 | 0 | 1 | 0 | 1 |
| 1 | 1 | 0 | 0 | 1 |
| 1 | 1 | 1 | 1 | 1 |

## Equações

* `S = A ⊕ B ⊕ Cin`
* `Cout = A·B + (A ⊕ B)·Cin`

## Mapas de Karnaugh

**S**

| A \\ BCin | 00 | 01 | 11 | 10 |
|:---:|:---:|:---:|:---:|:---:|
| 0 | 0 | 1 | 0 | 1 |
| 1 | 1 | 0 | 1 | 0 |

Nenhum par de 1s é adjacente (tabuleiro): `S` não se reduz em soma de produtos e vira `A ⊕ B ⊕ Cin`.

**Cout**

| A \\ BCin | 00 | 01 | 11 | 10 |
|:---:|:---:|:---:|:---:|:---:|
| 0 | 0 | 0 | 1 | 0 |
| 1 | 0 | 1 | 1 | 1 |

Três grupos de dois: `Cout = A·B + A·Cin + B·Cin`. O circuito usa a forma equivalente `A·B + (A ⊕ B)·Cin`, que reaproveita a porta XOR de `S`.

## Observações
