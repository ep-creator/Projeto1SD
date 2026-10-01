# Visão geral do projeto

## Operações

A ULA recebe dois números de 5 bits, A e B, e um seletor de 3 bits, S. Conforme S, ela calcula uma das operações da tabela abaixo e mostra o resultado em LEDs e displays.

| S₂ S₁ S₀ | Operação | Resultado aparece em |
|:---:|:---:|:---:|
| 000 | F = A + B | LEDs verdes (F) e displays HEX2, HEX1 e HEX0 |
| 001 | F = A − B | LEDs verdes (F) e displays HEX2, HEX1 e HEX0 |
| 010 | F = complemento a 2 de B | LEDs verdes (F) |
| 011 | A = B ? | LED de STATUS |
| 100 | A > B ? | LED de STATUS |
| 101 | A < B ? | LED de STATUS |
| 110 | F = A AND B (bit a bit) | LEDs verdes (F) |
| 111 | F = A XOR B (bit a bit) | LEDs verdes (F) |

## Entradas e saídas

**Entradas**

* **A** e **B**: 5 bits em sinal-magnitude, `[sinal, M3, M2, M1, M0]`. O bit de sinal é 1 para negativo e 0 para positivo; a magnitude vai de 0 a 15. Quem usa a placa não precisa saber complemento a 2: toda conversão é feita dentro da ULA.
* **S**: 3 bits, seleciona a operação.

**Saídas**

* **F**: 6 bits em sinal-magnitude, `[sinal, F4, F3, F2, F1, F0]`. O resultado da soma e da subtração vai de −30 a +30.
* **STATUS**: 1 bit (LED), verdadeiro ou falso nas comparações.
* **Displays**: |A|, |B| e |F| em dezena e unidade; o sinal de F aparece como "−" no HEX2. Os displays de F só acendem na soma e na subtração.
* **LEDs**: F nos LEDs verdes, as chaves replicadas nos LEDs vermelhos (com os sinais de A e B em LEDR17 e LEDR12).

## Diagrama em blocos

A Figura abaixo mostra o sistema completo: as chaves da placa alimentam a `ula` e os decodificadores de |A| e |B|; a saída F vai para os LEDs verdes e, passando pelo decodificador de F e pelo bloco que apaga os displays, para HEX1 e HEX0.

<!-- FIGURA: docs/relatorio/figuras/visao_geral.png | Visão geral do sistema em blocos -->

Internamente, a `ula` calcula todos os resultados em paralelo e escolhe um deles com multiplexadores controlados por S:

<!-- FIGURA: docs/relatorio/figuras/ula_interna.png | Organização interna da ULA -->

## Módulos desenvolvidos

| Grupo | Módulo | Função |
|:---:|:---|:---|
| Comuns | `mux2x1`, `mux4x1` | multiplexadores de 1 bit (2:1 e 4:1) |
| Complemento a 2 | `inversor`, `inversor5` | complemento a 2 de 4 e de 5 bits |
| | `comp2` | sinal-magnitude → complemento a 2 (−0 vira +0) |
| Soma e subtração | `somador_completo` | soma de 3 bits (célula do somador) |
| | `somador6` | soma em complemento a 2 de 6 bits (−30 a +30) |
| | `c2_para_sm` | complemento a 2 → sinal-magnitude |
| | `somador_subtrator` | A ± B em sinal-magnitude (operações 000 e 001) |
| Lógica | `op_and`, `op_xor` | AND e XOR bit a bit (110 e 111) |
| Comparações | `comp_mag` | \|A\| > \|B\| (magnitudes de 4 bits) |
| | `comp_maior` | A > B em sinal-magnitude (100; trocando A e B, 101) |
| | `comparador_igual` | A = B, com +0 = −0 (011) |
| | `decodificador_comparadores`, `mux_comparadores` | escolhem a comparação que vai para o STATUS |
| Seleção | `decodificador_saida`, `mux_saida` | escolhem o resultado que vai para F |
| Displays | `decod7seg_ab_dezena`, `decod7seg_ab_unidade` | dezena e unidade de \|A\| e \|B\| (0 a 15) |
| | `decod7seg_f_dezena`, `decod7seg_f_unidade`, `decod7seg_f` | dezena e unidade de \|F\| (0 a 30) |
| | `apaga_display` | apaga os displays de F fora da soma e da subtração |
| Sistema | `ula` | liga todos os blocos e gera F, STATUS e DISP_EN |
| | `toplevel` | liga a `ula` e os decodificadores aos pinos da placa |

A hierarquia de instâncias é:

```
toplevel
├── ula
│   ├── somador_subtrator ───── 000 / 001
│   │   ├── comp2 ×2 ── inversor, mux2x1 ×4
│   │   ├── XOR (inverte o sinal de B na subtração)
│   │   ├── somador6 ── somador_completo ×6
│   │   └── c2_para_sm ── inversor5, mux2x1 ×5
│   ├── comp2 ───────────────── 010
│   ├── op_and, op_xor ──────── 110 / 111
│   ├── decodificador_saida + mux_saida (mux4x1 ×6)
│   ├── comparador_igual ────── 011
│   ├── comp_maior ×2 (comp_mag ×2 cada) ── 100 / 101
│   └── decodificador_comparadores + mux_comparadores
├── decod7seg_ab_dezena ×2, decod7seg_ab_unidade ×2
├── decod7seg_f (decod7seg_f_dezena + decod7seg_f_unidade)
├── apaga_display ×2
└── NAND (sinal de F no HEX2)
```
