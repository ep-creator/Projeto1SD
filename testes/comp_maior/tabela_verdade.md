# comp_maior — tabela verdade e simulação

* **Circuito:** [`lib/comp_maior.bdf`](../../lib/comp_maior.bdf) ([`comp_mag`](../../lib/comp_mag.bdf) ×2)
* **Entradas:** `SA`, `A[3..0]`, `SB`, `B[3..0]` (sinal-magnitude)
* **Saídas:** `O` = 1 quando A > B
* **Figuras do relatório (nesta pasta):** `comp_maior_circuito.png` (esquemático) e `comp_maior_simulacao.png` (waveform do `comp_maior.vwf`)


## Funcionamento

Diz se A > B em sinal-magnitude. Compara os sinais primeiro e as magnitudes depois: entre dois positivos, ganha a maior magnitude; entre dois negativos, a menor; positivo é maior que negativo, exceto quando os dois são zero (+0 = −0). Usa dois `comp_mag`: `GT = comp_mag(A, B)` e `LT = comp_mag(B, A)`. Na ULA há duas instâncias: `comp_maior(A, B)` para A > B e `comp_maior(B, A)` para A < B. A tabela completa tem 1024 linhas; abaixo, a forma compacta por sinais e exemplos.

## Tabela verdade

| SA | SB | O |
|:---:|:---:|:---:|
| 0 | 0 | |A| > |B| |
| 1 | 1 | |A| < |B| |
| 0 | 1 | 1, exceto se A = B = 0 (+0 = −0) |
| 1 | 0 | 0 (nunca) |

**Exemplos**

| SA | A[3..0] | SB | B[3..0] | Comparação | O |
|:---:|:---:|:---:|:---:|:---:|:---:|
| 0 | 0101 | 0 | 0011 | +5 > +3 | 1 |
| 0 | 0011 | 0 | 0101 | +3 > +5 | 0 |
| 0 | 0010 | 1 | 0101 | +2 > −5 | 1 |
| 1 | 0010 | 1 | 0101 | −2 > −5 | 1 |
| 1 | 0101 | 1 | 0010 | −5 > −2 | 0 |
| 1 | 0111 | 0 | 0001 | −7 > +1 | 0 |
| 0 | 0000 | 0 | 0000 | +0 > +0 | 0 |
| 0 | 0000 | 1 | 0000 | +0 > −0 | 0 |
| 1 | 0000 | 0 | 0000 | −0 > +0 | 0 |
| 0 | 0100 | 0 | 0100 | +4 > +4 | 0 |

## Equações

Com `GT = comp_mag(A, B)`, `LT = comp_mag(B, A)` e `NZB = B3 + B2 + B1 + B0` (B ≠ 0):

* `O = SA'·(GT + SB·NZB) + SA·SB·LT`

## Observações
