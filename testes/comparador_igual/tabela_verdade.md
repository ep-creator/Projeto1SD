# comparador_igual — tabela verdade e simulação

* **Circuito:** [`lib/comparador_igual.bdf`](../../lib/comparador_igual.bdf)
* **Entradas:** `A[4..0]`, `B[4..0]` (sinal-magnitude, bit 4 = sinal)
* **Saídas:** `F` = 1 quando A = B
* **Figuras do relatório (nesta pasta):** `comparador_igual_circuito.png` (esquemático) e `comparador_igual_simulacao.png` (waveform do `comparador_igual.vwf`)


## Funcionamento

Operação `011`: diz se A = B. As magnitudes têm de ser iguais e, se não forem zero, os sinais também; assim +0 e −0 são considerados iguais. A tabela completa tem 1024 linhas; abaixo, a forma compacta e exemplos.

## Tabela verdade

| Magnitudes | Sinais | F |
|:---:|:---:|:---:|
| diferentes | X | 0 |
| iguais e = 0000 | X | 1 |
| iguais e ≠ 0000 | iguais | 1 |
| iguais e ≠ 0000 | diferentes | 0 |

**Exemplos**

| A[4..0] | B[4..0] | Comparação | F |
|:---:|:---:|:---:|:---:|
| 00101 | 00101 | +5 = +5 | 1 |
| 00101 | 10101 | +5 = −5 | 0 |
| 10000 | 00000 | −0 = +0 | 1 |
| 10000 | 10000 | −0 = −0 | 1 |
| 01100 | 01101 | +12 = +13 | 0 |
| 11111 | 11111 | −15 = −15 | 1 |

## Equações

* `F = [ (A3 ⊕ B3) + (A2 ⊕ B2) + (A1 ⊕ B1) + (A0 ⊕ B0) + (B3 + B2 + B1 + B0)·(A4 ⊕ B4) ]'`

## Observações
