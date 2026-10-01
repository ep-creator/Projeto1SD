# comp_mag — tabela verdade e simulação

* **Circuito:** [`lib/comp_mag.bdf`](../../lib/comp_mag.bdf)
* **Entradas:** `A[3..0]`, `B[3..0]` (magnitudes, sem sinal)
* **Saídas:** `O` = 1 quando |A| > |B|
* **Figuras do relatório (nesta pasta):** `comp_mag_circuito.png` (esquemático) e `comp_mag_simulacao.png` (waveform do `comp_mag.vwf`)


## Funcionamento

Compara duas magnitudes de 4 bits, do bit mais alto para o mais baixo: o primeiro bit em que A e B diferem decide. Se todos são iguais, A não é maior (O = 0). É a base do `comp_maior`. A tabela completa tem 256 linhas; abaixo, a forma compacta (X = qualquer valor) e alguns exemplos.

## Tabela verdade

| A3 B3 | A2 B2 | A1 B1 | A0 B0 | O |
|:---:|:---:|:---:|:---:|:---:|
| 1 0 | X | X | X | 1 |
| 0 1 | X | X | X | 0 |
| iguais | 1 0 | X | X | 1 |
| iguais | 0 1 | X | X | 0 |
| iguais | iguais | 1 0 | X | 1 |
| iguais | iguais | 0 1 | X | 0 |
| iguais | iguais | iguais | 1 0 | 1 |
| iguais | iguais | iguais | 0 1 | 0 |
| iguais | iguais | iguais | iguais | 0 |

**Exemplos**

| A[3..0] | B[3..0] | Comparação | O |
|:---:|:---:|:---:|:---:|
| 1001 | 0111 | 9 > 7 | 1 |
| 0111 | 1001 | 7 > 9 | 0 |
| 1100 | 1100 | 12 > 12 | 0 |
| 0101 | 0100 | 5 > 4 | 1 |
| 0000 | 0000 | 0 > 0 | 0 |
| 1111 | 0000 | 15 > 0 | 1 |
| 0000 | 0001 | 0 > 1 | 0 |

## Equações

Com `ek = Ak ⊙ Bk` (XNOR: bits iguais):

* `O = A3·B3' + e3·A2·B2' + e3·e2·A1·B1' + e3·e2·e1·A0·B0'`

## Observações
