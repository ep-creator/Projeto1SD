# inversor — tabela verdade e simulação

* **Circuito:** [`lib/inversor.bdf`](../../lib/inversor.bdf)
* **Entradas:** `I3`, `I2`, `I1`, `I0`
* **Saídas:** `F3`, `F2`, `F1`, `F0`
* **Figuras do relatório (nesta pasta):** `inversor_circuito.png` (esquemático) e `inversor_simulacao.png` (waveform do `inversor.vwf`)


## Funcionamento

Calcula o complemento a 2 de um número de 4 bits (inverte e soma 1). Em vez de um somador, usa o atalho: da direita para a esquerda, copia os bits até o primeiro `1` (inclusive) e inverte os outros. Assim, cada bit é invertido quando existe algum `1` abaixo dele. É usado pelo `comp2`.

## Tabela verdade

| I3 | I2 | I1 | I0 | F3 | F2 | F1 | F0 | I | F (C2) |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 0 | 0 | 0 | 1 | 1 | 1 | 1 | 1 | 1 | −1 |
| 0 | 0 | 1 | 0 | 1 | 1 | 1 | 0 | 2 | −2 |
| 0 | 0 | 1 | 1 | 1 | 1 | 0 | 1 | 3 | −3 |
| 0 | 1 | 0 | 0 | 1 | 1 | 0 | 0 | 4 | −4 |
| 0 | 1 | 0 | 1 | 1 | 0 | 1 | 1 | 5 | −5 |
| 0 | 1 | 1 | 0 | 1 | 0 | 1 | 0 | 6 | −6 |
| 0 | 1 | 1 | 1 | 1 | 0 | 0 | 1 | 7 | −7 |
| 1 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 8 | −8 |
| 1 | 0 | 0 | 1 | 0 | 1 | 1 | 1 | 9 | −9 |
| 1 | 0 | 1 | 0 | 0 | 1 | 1 | 0 | 10 | −10 |
| 1 | 0 | 1 | 1 | 0 | 1 | 0 | 1 | 11 | −11 |
| 1 | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 12 | −12 |
| 1 | 1 | 0 | 1 | 0 | 0 | 1 | 1 | 13 | −13 |
| 1 | 1 | 1 | 0 | 0 | 0 | 1 | 0 | 14 | −14 |
| 1 | 1 | 1 | 1 | 0 | 0 | 0 | 1 | 15 | −15 |

## Equações

* `F0 = I0`
* `F1 = I1 ⊕ I0`
* `F2 = I2 ⊕ (I1 + I0)`
* `F3 = I3 ⊕ (I2 + I1 + I0)`

Pelo mapa-K, `F1`, `F2` e `F3` não se reduzem bem em soma de produtos (padrão de tabuleiro, típico de XOR); a forma com XOR sai direto da regra "inverte se há um 1 abaixo".

## Observações
