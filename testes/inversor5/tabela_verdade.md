# inversor5 — tabela verdade e simulação

* **Circuito:** [`lib/inversor5.bdf`](../../lib/inversor5.bdf)
* **Entrada:** `I[4..0]`
* **Saída:** `O[4..0]` = complemento a 2 de `I` em 5 bits (inverte e soma 1)
* **Como funciona:** mesmo padrão do `inversor` de 4 bits. Cada bit é invertido quando existe algum `1` abaixo dele: `O[k] = I[k] XOR (I[k-1] + … + I[0])`. O bit 0 nunca inverte (`O[0] = I[0] XOR 0`).
* **Simulação:** `inversor5.vwf` (a criar)

## Tabela verdade (casos de teste)

| I[4..0] | I (dec) | O[4..0] | O (dec) |
|:---:|:---:|:---:|:---:|
|   |   |   |   |

## Observações

