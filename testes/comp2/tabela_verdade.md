# comp2 — tabela verdade e simulação

* **Circuito:** [`lib/comp2.bdf`](../../lib/comp2.bdf) ([`inversor`](../../lib/inversor.bdf), [`mux2x1`](../../lib/mux2x1.bdf) ×4)
* **Entradas:** `IS` (sinal), `I[3..0]` (magnitude)
* **Saídas:** `OS`, `O[3..0]` (complemento a 2 de 5 bits)
* **Figuras do relatório (nesta pasta):** `comp2_circuito.png` (esquemático) e `comp2_simulacao.png` (waveform do `comp2.vwf`)


## Funcionamento

Converte um número de sinal-magnitude para complemento a 2 de 5 bits. Se o número é positivo, a magnitude passa direto; se é negativo, sai o complemento a 2 da magnitude (bloco `inversor`). Quatro `mux2x1` com seletor `IS` fazem essa escolha. O sinal de saída só é 1 quando a magnitude não é zero, então o −0 (`IS = 1`, `I = 0000`) sai como +0. Na ULA, é usado no `somador_subtrator` (×2) e na operação `010`.

## Tabela verdade

| IS | I[3..0] | Entrada (SM) | OS | O[3..0] | Saída (C2) |
|:---:|:---:|:---:|:---:|:---:|:---:|
| 0 | 0000 | 0 | 0 | 0000 | 0 |
| 0 | 0001 | +1 | 0 | 0001 | +1 |
| 0 | 0010 | +2 | 0 | 0010 | +2 |
| 0 | 0011 | +3 | 0 | 0011 | +3 |
| 0 | 0100 | +4 | 0 | 0100 | +4 |
| 0 | 0101 | +5 | 0 | 0101 | +5 |
| 0 | 0110 | +6 | 0 | 0110 | +6 |
| 0 | 0111 | +7 | 0 | 0111 | +7 |
| 0 | 1000 | +8 | 0 | 1000 | +8 |
| 0 | 1001 | +9 | 0 | 1001 | +9 |
| 0 | 1010 | +10 | 0 | 1010 | +10 |
| 0 | 1011 | +11 | 0 | 1011 | +11 |
| 0 | 1100 | +12 | 0 | 1100 | +12 |
| 0 | 1101 | +13 | 0 | 1101 | +13 |
| 0 | 1110 | +14 | 0 | 1110 | +14 |
| 0 | 1111 | +15 | 0 | 1111 | +15 |
| 1 | 0000 | −0 | 0 | 0000 | 0 |
| 1 | 0001 | −1 | 1 | 1111 | −1 |
| 1 | 0010 | −2 | 1 | 1110 | −2 |
| 1 | 0011 | −3 | 1 | 1101 | −3 |
| 1 | 0100 | −4 | 1 | 1100 | −4 |
| 1 | 0101 | −5 | 1 | 1011 | −5 |
| 1 | 0110 | −6 | 1 | 1010 | −6 |
| 1 | 0111 | −7 | 1 | 1001 | −7 |
| 1 | 1000 | −8 | 1 | 1000 | −8 |
| 1 | 1001 | −9 | 1 | 0111 | −9 |
| 1 | 1010 | −10 | 1 | 0110 | −10 |
| 1 | 1011 | −11 | 1 | 0101 | −11 |
| 1 | 1100 | −12 | 1 | 0100 | −12 |
| 1 | 1101 | −13 | 1 | 0011 | −13 |
| 1 | 1110 | −14 | 1 | 0010 | −14 |
| 1 | 1111 | −15 | 1 | 0001 | −15 |

## Equações

* `O[k] = I[k]·IS' + inversor(I)[k]·IS` (um `mux2x1` por bit)
* `OS = IS·(I3 + I2 + I1 + I0)`

## Observações
