# somador6 — tabela verdade e simulação

* **Circuito:** [`lib/somador6.bdf`](../../lib/somador6.bdf) (usa [`somador_completo`](../../lib/somador_completo.bdf) ×6)
* **Entradas:** `A[4..0]`, `B[4..0]` em complemento a 2 (bit 4 = sinal)
* **Saída:** `O[5..0]` = A + B em complemento a 2 de 6 bits (o sinal é estendido internamente: o 6º somador recebe `A[4]` e `B[4]`)
* **Simulação:** `somador6.vwf` (print: `somador6_simulacao.png`)

## Tabela verdade (casos de teste)

| A (C2) | A (dec) | B (C2) | B (dec) | O (C2) | O (dec) |
|:---:|:---:|:---:|:---:|:---:|:---:|
|   |   |   |   |   |   |

## Observações

