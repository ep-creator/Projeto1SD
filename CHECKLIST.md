# ✅ Checklist do Projeto1SD

Lista de tudo que a ULA precisa, bloco por bloco. Marque `[x]` quando o item estiver pronto (no VS Code ou direto no GitHub).
Um bloco está **concluído** quando todos os subitens dele estão marcados.

**Etiquetas:** 🟢 já existe e serve · 🟡 existe, mas precisa alterar · 🔴 falta criar · 🔌 só ligação (portas/fios dentro do bloco pai, sem bloco próprio)

## Visão geral

```text
toplevel ─────────────────── chaves, LEDs e displays da DE2-115
├── ula ──────────────────── A[4..0], B[4..0], S[2..0] → F[5..0], STATUS, DISP_EN
│   ├── somador_subtrator ── 000 / 001
│   ├── comp2 ────────────── 010
│   ├── op_and, op_xor ───── 110 / 111
│   ├── comparadores ─────── 011 / 100 / 101 → STATUS
│   └── seleção ──────────── escolhe F[5..0]
└── displays ─────────────── |A|, |B| e |F| em dezena e unidade (7 segmentos)
```

---

## 0. Estrutura do repositório

- [x] Biblioteca `lib/` e testes em `testes/<bloco>/` (branch `feat/biblioteca`)
- [x] Validar no Quartus: projeto de teste acha os blocos em `lib/`
- [x] Validar no Quartus: montagem em `src/` e edição de um bloco valendo para todos
- [ ] Validar no Quartus: criar um bloco novo pelo *New Project Wizard* (ponto 4)
- [ ] Merge da `feat/biblioteca` na `develop`
- [ ] Trazer a `develop` para as branches `feat/*` antigas (`git merge develop`)

---

## 1. Aritmética: soma e subtração (`000`, `001`)

Caminho: A e B em sinal-magnitude → `comp2` → soma em C2 de 6 bits → volta para sinal-magnitude.

- [ ] 🔴 **`somador_subtrator`**: bloco que junta os itens abaixo (`SUB = S[0]`)
  - [ ] 🟡 **`comp2`** ×2 (A e B), sinal-magnitude → C2
    - [x] na biblioteca
    - [ ] corrigir o zero negativo: hoje `−0` sai `10000` (= −16 em C2 e estraga a soma); correção `FS = SB AND (B≠0)` (bloco do Enzo)
    - [ ] tabela verdade + simulação
  - [ ] 🔌 inverter o sinal de B na subtração: `SB' = SB XOR SUB`
  - [ ] 🟢 **`somador_completo`**, 1 bit (`A`, `B`, `Cin` → `S`, `Cout`)
    - [x] na biblioteca (enviado pelo grupo como `soma1`)
    - [ ] compilar `testes/somador_completo`
    - [ ] tabela verdade + simulação
  - [ ] 🔴 **`somador6`**: 6× `somador_completo`; estende o sinal de 5 para 6 bits repetindo o bit 4
    - [ ] criar na biblioteca
    - [ ] tabela verdade + simulação
  - [ ] 🔴 **`c2_para_sm`**: resultado em C2 (6 bits) → sinal-magnitude (`F[5]` = sinal, `F[4..0]` = magnitude até 30)
    - [ ] 🔴 **`inversor5`**: C2 de 5 bits (o `inversor` atual só tem 4, e a magnitude chega a 30)
    - [ ] 🟢 `mux2x1` ×5: escolhe entre o valor direto e o invertido, com seletor = bit de sinal
    - [ ] tabela verdade + simulação
  - [ ] tabela verdade + simulação do `somador_subtrator`: +5+(−3), (−9)−(+12), (−8)+(−8), (−15)+(−15), (+7)−(+7), (−0)+(+0)

---

## 2. Complemento a 2 de B (`010`)

- [ ] 🟡 **`comp2`**: é o mesmo bloco do item 1 (a correção do −0 vale para os dois)
- [ ] 🔌 saída em 6 bits na `ula`: `F = {FS, FS, F3, F2, F1, F0}` (sinal repetido no bit 5)

---

## 3. Lógica: AND e XOR (`110`, `111`)

- [ ] 🟡 **`op_and`**
  - [x] na biblioteca
  - [ ] corrigir `F[4]`/`F[5]` trocados (o sinal sai em `F[4]`), feito pelo autor; ou ligar trocado na `ula`
  - [ ] tabela verdade + simulação
- [ ] 🟡 **`op_xor`**
  - [x] na biblioteca
  - [ ] corrigir `F[4]`/`F[5]` trocados, feito pelo autor; ou ligar trocado na `ula`
  - [ ] tabela verdade + simulação

---

## 4. Comparadores → `STATUS` (`011`, `100`, `101`)

- [ ] 🟢 **`comparador_igual`**
  - [x] na biblioteca
  - [ ] conferir o zero negativo: `00000` × `10000` deve dar `1` (se não der: OR com "A = 0 e B = 0" na `ula`)
  - [ ] tabela verdade + simulação
- [ ] 🔴 **`comparador_maior`**, sinal-magnitude, com +0 = −0
  - [ ] criar: sinais diferentes → o positivo é maior; os dois positivos → \|A\| > \|B\|; os dois negativos → \|A\| < \|B\|
  - [ ] tabela verdade + simulação
  - [ ] 🔌 na `ula`: `GT = comparador_maior(A, B)` e `LT = comparador_maior(B, A)` (não precisa de `comparador_menor`)
- [ ] 🟢 **`decodificador_comparadores`**: `S` → seleção do `mux_comparadores`
  - [x] na biblioteca
  - [ ] tabela verdade + simulação
- [ ] 🟢 **`mux_comparadores`**: escolhe EQ/GT/LT para o `STATUS`
  - [x] na biblioteca
  - [ ] tabela verdade + simulação

---

## 5. Seleção da saída F

- [ ] 🟢 **`decodificador_saida`**: `S3 S2 S1` (= `S[2..0]`) → `F1 F2` (seletor do `mux_saida`: `F1` → `S[1]`, `F2` → `S[0]`)
  - [x] na biblioteca (enviado pelo grupo como `DecodificadorAritimeticos`)
  - [ ] compilar `testes/decodificador_saida` e rodar a simulação que veio junto
  - [ ] tabela verdade
- [ ] 🟡 **`mux_saida`**: MUX 4:1 de 6 bits (`00` soma/sub, `01` C2, `10` AND, `11` XOR)
  - [x] na biblioteca
  - [ ] entradas viram barramentos `[5..0]` (hoje são de 1 bit e as 6 saídas ficam iguais), feito pelo autor; ou usar 6× `mux4x1` na `ula`
  - [ ] tabela verdade + simulação
- [ ] 🟢 **`mux4x1`**
  - [x] na biblioteca
  - [ ] tabela verdade + simulação
- [ ] 🔌 `DISP_EN = S[2]' · S[1]'` na `ula` (liga os displays de F só em `000`/`001`)
- [ ] ❓ F nas comparações: ver [Em aberto](#em-aberto)

---

## 6. ULA

- [ ] 🔴 **`ula`**: liga os itens 1 a 5 (`A[4..0]`, `B[4..0]`, `S[2..0]` → `F[5..0]`, `STATUS`, `DISP_EN`)
  - [ ] criar na biblioteca
  - [ ] simulação das 8 operações

---

## 7. Displays (7 segmentos, ativo em nível baixo)

Os decodificadores vão direto do binário para os segmentos, sem passar por BCD.

- [ ] 🟢 **`decod7seg_ab_dezena`**: magnitude 0–15 → dígito da dezena (`0` ou `1`), ×2 (A e B)
  - [x] na biblioteca (enviado pelo grupo como `decodificadores`)
  - [ ] compilar `testes/decod7seg_ab_dezena`
  - [ ] tabela verdade + simulação
- [ ] 🟡 **`decod7seg_ab_unidade`**: magnitude 0–15 → dígito da unidade, ×2 (A e B)
  - [x] na biblioteca (enviado pelo grupo como `Block4`)
  - [ ] conferir o valor 9: pela leitura do esquemático, o segmento b apaga e aparece **5** (termo `D·C'·B'·A` em `bu_seg`); corrigir, feito pelo autor
  - [ ] tabela verdade + simulação
- [ ] 🟢 **`decod7seg_f_dezena`**: magnitude de F, 0–30 → dezena (`0` a `3`)
  - [x] na biblioteca (enviado pelo grupo como `decod7segDezena`)
  - [ ] compilar `testes/decod7seg_f_dezena` e rodar a simulação que veio junto
  - [ ] tabela verdade
- [ ] 🔴 **`decod7seg_f_unidade`**: magnitude de F, 0–30 → unidade
  - [ ] pedir ao colega: o projeto dele cita `decod7segUnidade.bdf`, mas o arquivo não veio no zip
  - [ ] colocar na biblioteca
  - [ ] tabela verdade + simulação
- [ ] 🔴 **`apaga_display`**: 7 portas OR (`seg = seg OR BLANK`); ×2, nos displays de F, com `BLANK = NOT DISP_EN`
  - [ ] criar na biblioteca
  - [ ] tabela verdade + simulação

---

## 8. Top-level e placa

- [ ] 🔴 **`src/toplevel.bdf`**: `ula` + displays + LEDs
- [ ] 🔴 Pinagem em `src/Projeto1SD.qsf` (branch `feat/toplevel-pinagem`)
  - A[4..0] = `SW[17..13]` · B[4..0] = `SW[12..8]` · S[2..0] = `SW[2..0]`
  - `LEDR[17..0]` repetem as chaves · F[5..0] = `LEDG[5..0]` · STATUS = `LEDG[8]`
  - \|A\| = `HEX7`/`HEX6` · \|B\| = `HEX5`/`HEX4` · \|F\| = `HEX1`/`HEX0`
- [ ] Simulação do sistema completo (`src/toplevel.vwf`)
- [ ] Teste na placa → merge na `main`

---

## Decisões

- **Zero negativo:** +0 e −0 são iguais.
- **Soma/subtração:** via `comp2` (sinal-magnitude → C2 → soma → volta para sinal-magnitude).
- **Volta para sinal-magnitude:** `inversor5` + `mux2x1`, no mesmo padrão do `comp2`.
- **Operação `010`:** F em 6 bits = `{FS, FS, F3..F0}`.
- **`A < B`:** segunda instância do `comparador_maior` com A e B trocados.
- **Displays:** decodificadores binário → 7 segmentos do grupo, sem BCD.

## Em aberto

- **F nas comparações (`011`, `100`, `101`):** nessas operações só o LED de `STATUS` importa, mas o vetor F (LEDs verdes) continua mostrando o que o `mux_saida` escolher: com o `decodificador_saida`, em `011` aparece o C2 de B e em `100`/`101` aparece A AND B. Opções: deixar assim, ou zerar F nessas três operações (6 portas AND com um sinal `F_EN`).
