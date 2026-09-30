# decod7seg_f — tabela verdade e simulação

Bloco composto: junta `decod7seg_f_dezena` e `decod7seg_f_unidade` para mostrar |F| nos dois displays.

* **Circuito:** [`lib/decod7seg_f.bdf`](../../lib/decod7seg_f.bdf) (usa [`decod7seg_f_dezena`](../../lib/decod7seg_f_dezena.bdf) e [`decod7seg_f_unidade`](../../lib/decod7seg_f_unidade.bdf))
* **Entradas:** `S[4..0]` (magnitude de F, 0 a 30), `sinal_S` (sinal de F)
* **Saídas:** `aDEZ` … `gDEZ`, `aUNI` … `gUNI` (ativo em nível baixo), `led_negativo`
* **Simulação:** `decod7seg_f.vwf` (a criar)
* **Símbolo:** `lib/decod7seg_f.bsf` ainda não existe; gerar no Quartus (*File > Create/Update > Create Symbol Files for Current File*, salvando em `lib/`)

## Tabela verdade

| sinal_S | S[4..0] | Valor | Dezena | Unidade | led_negativo |
|:---:|:---:|:---:|:---:|:---:|:---:|
|   |   |   |   |   |   |

## Observações

