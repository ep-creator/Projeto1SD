# somador6 — tabela verdade e simulação

* **Circuito:** [`lib/somador6.bdf`](../../lib/somador6.bdf) ([`somador_completo`](../../lib/somador_completo.bdf) ×6)
* **Entradas:** `A[4..0]`, `B[4..0]` (complemento a 2)
* **Saídas:** `O[5..0]` = A + B (complemento a 2 de 6 bits)
* **Figuras do relatório (nesta pasta):** `somador6_circuito.png` (esquemático) e `somador6_simulacao.png` (waveform do `somador6.vwf`)


## Funcionamento

Soma dois números em complemento a 2 de 5 bits (−15 a +15, vindos do `comp2`). Como a soma vai de −30 a +30 e não cabe em 5 bits, os operandos são estendidos para 6 bits repetindo o bit de sinal: o sexto `somador_completo` recebe `A[4]` e `B[4]` de novo. São seis somadores em cascata (*ripple carry*), com vai-um inicial 0; em 6 bits não há overflow. A tabela completa tem 1024 linhas; abaixo, casos representativos (sinais iguais e diferentes, zero e os extremos ±30).

## Tabela verdade

| A[4..0] | A | B[4..0] | B | O[5..0] | O |
|:---:|:---:|:---:|:---:|:---:|:---:|
| 00000 | 0 | 00000 | 0 | 000000 | 0 |
| 00101 | +5 | 11101 | −3 | 000010 | +2 |
| 11011 | −5 | 00011 | +3 | 111110 | −2 |
| 00111 | +7 | 11001 | −7 | 000000 | 0 |
| 01111 | +15 | 01111 | +15 | 011110 | +30 |
| 10001 | −15 | 10001 | −15 | 100010 | −30 |
| 11000 | −8 | 11000 | −8 | 110000 | −16 |
| 10111 | −9 | 10100 | −12 | 101011 | −21 |
| 01100 | +12 | 10111 | −9 | 000011 | +3 |
| 00001 | +1 | 11111 | −1 | 000000 | 0 |
| 11111 | −1 | 11111 | −1 | 111110 | −2 |
| 01111 | +15 | 10001 | −15 | 000000 | 0 |

## Equações

Para cada etapa `i` = 0 … 5, com `A5 = A4`, `B5 = B4` (extensão de sinal) e `C0 = 0`:

* `O[i] = A[i] ⊕ B[i] ⊕ C[i]`
* `C[i+1] = A[i]·B[i] + (A[i] ⊕ B[i])·C[i]`

O vai-um final `C6` é descartado.

## Observações
