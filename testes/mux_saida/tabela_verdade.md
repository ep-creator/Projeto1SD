# mux_saida — tabela verdade e simulação

* **Circuito:** [`lib/mux_saida.bdf`](../../lib/mux_saida.bdf) (6× [`mux4x1`](../../lib/mux4x1.bdf), um por bit)
* **Entradas:** `SOMA_OU_SUB[5..0]`, `Comp2B[5..0]`, `OP_AND[5..0]`, `OP_XOR[5..0]`, `S[1..0]` (vem do `decodificador_saida`: `S[1]` = `F1`, `S[0]` = `F2`)
* **Saída:** `F[5..0]`
* **Simulação:** `mux_saida.vwf` (a criar)

## Tabela verdade

| S[1] | S[0] | F[5..0] |
|:---:|:---:|:---|
| 0 | 0 | `SOMA_OU_SUB[5..0]` |
| 0 | 1 | `Comp2B[5..0]` |
| 1 | 0 | `OP_AND[5..0]` |
| 1 | 1 | `OP_XOR[5..0]` |

## Observações

* Antes de 01/10/2026 as entradas eram de 1 bit e as 6 saídas saíam iguais; agora cada entrada é um barramento de 6 bits.
