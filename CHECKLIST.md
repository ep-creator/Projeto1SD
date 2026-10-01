# ✅ Checklist do Projeto1SD

Lista de tudo que a ULA precisa, bloco por bloco. Marque `[x]` quando o item estiver pronto (no VS Code ou direto no GitHub).
Um bloco está **concluído** quando todos os subitens dele estão marcados.

> **Situação (01/10/2026):** versão final. Toplevel montado, pinagem aplicada e sistema **testado na DE2-115, funcionando**. Integrado na `main`. Relatório quase pronto: faltam os prints das simulações e a foto da placa.

**Etiquetas:** 🟢 pronto (compilado e simulado com todas as entradas) · 🟡 existe, mas precisa alterar · 🔴 falta criar · 🔌 só ligação

## 📋 O que falta

**Placa**
- [x] `src/toplevel.bdf`: `ula` + displays + LEDs + sinal de F no HEX2
- [x] Pinagem da DE2-115 em `src/Projeto1SD.qsf` (92 pinos)
- [x] Compilação completa e gravação na placa
- [x] Teste na placa

**Relatório** (documento: `docs/relatorio/Relatorio_Projeto1SD.docx` / `.pdf`)
- [x] Texto: capa, introdução, visão geral em blocos, fundamentos, módulos, sistema completo e conclusão (`docs/relatorio/partes/`)
- [x] Capa: equipe (ala8, dbm5, ep, pabpa) e professor Abel Guilhermino
- [x] Tabelas verdade, equações e mapas-K de todos os blocos (`testes/<bloco>/tabela_verdade.md`), geradas pela especificação
- [x] Prints dos circuitos dos 25 blocos e do toplevel
- [x] `.vwf` de todos os blocos (as que faltavam geradas por `ferramentas/relatorio/gera_vwf.py`)
- [ ] Rodar as simulações e tirar os prints (lista em [`docs/relatorio/PRINTS.md`](docs/relatorio/PRINTS.md)); no PC de casa o Questa recusa a licença (*Invalid host*): usar o PC do lab ou gerar licença nova
- [ ] Conferir as tabelas verdade com as simulações
- [ ] Foto da placa funcionando (`docs/relatorio/figuras/placa.jpg`)
- [ ] Gerar a versão final (`python3 ferramentas/relatorio/monta_relatorio.py`) e imprimir

**Git**
- [x] Merge da `feat/biblioteca` na `develop`
- [x] Merge da `feat/toplevel` na `develop` e da `develop` na `main`

## Visão geral

```text
toplevel ─────────────────── chaves, LEDs e displays da DE2-115 (src/toplevel.bdf)
├── ula ──────────────────── A[4..0], B[4..0], S[2..0] → F[5..0], STATUS, DISP_EN
│   ├── somador_subtrator ── 000 / 001  (comp2 ×2 → somador6 → c2_para_sm)
│   ├── comp2 ────────────── 010
│   ├── op_and, op_xor ───── 110 / 111
│   ├── comparadores ─────── 011 / 100 / 101 → STATUS
│   └── seleção ──────────── decodificador_saida + mux_saida, F = 0 nas comparações
└── displays ─────────────── |A|, |B| e |F| em dezena e unidade; F apagado fora de 000/001
```

Todos os blocos abaixo da `ula` e dos displays estão em `lib/`, compilados no Quartus e simulados com todas as combinações de entrada (ver [Verificação](README.md#-verificação)).

---

## 0. Estrutura do repositório

- [x] Biblioteca `lib/` e testes em `testes/<bloco>/` (branch `feat/biblioteca`)
- [x] Validar no Quartus: projeto de teste acha os blocos em `lib/`
- [x] Validar no Quartus: montagem em `src/` e edição de um bloco valendo para todos
- [x] Validar no Quartus: criar um bloco novo pelo *New Project Wizard* (ponto 4, feito com o `somador6`; o Wizard não grava o `SEARCH_PATH`, conferir o `.qsf`)
- [x] Merge da `feat/biblioteca` na `develop` (01/10)
- [x] Branches antigas removidas (ficam só `main` e `develop`)

---

## 1. Aritmética: soma e subtração (`000`, `001`)

Caminho: A e B em sinal-magnitude → `comp2` → soma em C2 de 6 bits → volta para sinal-magnitude.

- [x] 🟢 **`somador_subtrator`**: `sinal_a`, `W[3..0]`, `sinal_b`, `X[3..0]`, `sinal_op` → `R[5..0]` em sinal-magnitude (`sinal_op = S[0]`)
  - [x] 🟢 **`comp2`** ×2 (A e B), sinal-magnitude → C2 (`−0` sai `+0`)
  - [x] 🔌 inverte o sinal de B na subtração: `sinal_b XOR sinal_op`
  - [x] 🟢 **`somador6`** (6× **`somador_completo`**), extensão de sinal interna
  - [x] 🟢 **`c2_para_sm`** (**`inversor5`** + `mux2x1` ×5), ligado na saída em 01/10
  - [x] simulado com as 2048 combinações (A, B, operação)
  - [ ] tabela verdade + `.vwf` para o relatório

---

## 2. Complemento a 2 de B (`010`)

- [x] 🟢 **`comp2`**
- [x] 🔌 saída em 6 bits na `ula`: `F = {OS, OS, O[3..0]}`

---

## 3. Lógica: AND e XOR (`110`, `111`)

- [x] 🟢 **`op_and`**: `F[5] = SA AND SB`, `F[4] = 0`, `F[3..0] = A AND B`
- [x] 🟢 **`op_xor`**: `F[5] = SA XOR SB`, `F[4] = 0`, `F[3..0] = A XOR B`
- [ ] refazer `op_and.vwf` e `op_xor.vwf` + tabelas verdade

---

## 4. Comparadores → `STATUS` (`011`, `100`, `101`)

- [x] 🟢 **`comparador_igual`** (+0 = −0 já tratado no bloco)
- [x] 🟢 **`comp_maior`**: A > B em sinal-magnitude, +0 = −0 (`comp_mag` ×2; lógica do sinal corrigida em 01/10)
  - [x] 🟢 **`comp_mag`**: \|A\| > \|B\| em 4 bits
  - [x] 🔌 na `ula`: `GT = comp_maior(A, B)` e `LT = comp_maior(B, A)`
- [x] 🟢 **`decodificador_comparadores`** + **`mux_comparadores`** → `STATUS` (0 fora das comparações)

---

## 5. Seleção da saída F

- [x] 🟢 **`decodificador_saida`**: `S` → seletor do `mux_saida`
- [x] 🟢 **`mux_saida`**: MUX 4:1 de 6 bits (entradas viraram barramentos `[5..0]` em 01/10)
- [x] 🟢 **`mux4x1`**
- [x] 🔌 `F_EN = (S[2] XNOR S[1]) + S[2]'·S[0]'`: F = `000000` nas comparações (decisão de 01/10)
- [x] 🔌 `DISP_EN = S[2]' · S[1]'` (displays de F só em `000`/`001`)

---

## 6. ULA

- [x] 🟢 **`ula`**: `A[4..0]`, `B[4..0]`, `S[2..0]` → `F[5..0]`, `STATUS`, `DISP_EN`
  - [x] criar na biblioteca
  - [x] simulada nas 8192 combinações de A, B e S
  - [ ] `.vwf` para o relatório com os casos de `testes/ula/tabela_verdade.md`

---

## 7. Displays (7 segmentos, ativo em nível baixo)

- [x] 🟢 **`decod7seg_ab_dezena`** ×2 (A e B): magnitude 0–15 → `0`/`1`
- [x] 🟢 **`decod7seg_ab_unidade`** ×2 (A e B): magnitude 0–15 → `0`–`9` (dígito 9 corrigido em 01/10)
- [x] 🟢 **`decod7seg_f`**: \|F\| → dezena (`decod7seg_f_dezena`) e unidade (`decod7seg_f_unidade`), mais `led_negativo`
- [x] 🟢 **`apaga_display`** ×2: apaga os displays de F quando `DISP_EN = 0`

---

## 8. Top-level e placa

- [x] 🟢 **`src/toplevel.bdf`** com as ligações abaixo
- [x] 🟢 Pinagem em `src/Projeto1SD.qsf` (`src/pinagem_de2_115.tcl` + HEX2)
- [x] Compilação completa sem erros
- [ ] Simulação do sistema completo (`src/toplevel.vwf`) para o relatório
- [x] Teste na placa → merge na `main`

**Ligações do toplevel** (todos os blocos vêm de `lib/`; no `src/Projeto1SD.qsf` já tem `SEARCH_PATH ../lib`):

| De | Para | Observação |
| :--- | :--- | :--- |
| `SW[17..13]` | `ula.A[4..0]` | `SW17` = sinal de A |
| `SW[12..8]` | `ula.B[4..0]` | `SW12` = sinal de B |
| `SW[2..0]` | `ula.S[2..0]` | |
| `SW[17..0]` | `LEDR[17..0]` | LEDs vermelhos repetem as chaves (inclui o sinal de A e de B) |
| `ula.F[5..0]` | `LEDG[5..0]` | `LEDG5` = sinal de F |
| `ula.STATUS` | `LEDG[8]` | |
| `A[3], A[2], A[1], A[0]` | `decod7seg_ab_dezena` e `_unidade`: entradas `A, B, C, D` | nos decodificadores de A e B, `A` = bit mais significativo |
| dezena / unidade de \|A\| | `HEX7` / `HEX6` | `seg_a`/`au_seg` → `HEX7[0]` … `seg_g`/`gu_seg` → `HEX7[6]` |
| dezena / unidade de \|B\| | `HEX5` / `HEX4` | idem |
| `ula.F[4..0]`, `ula.F[5]` | `decod7seg_f.S[4..0]`, `sinal_S` | |
| `decod7seg_f` `aDEZ..gDEZ` | `apaga_display.I[0..6]` → `HEX1[0..6]` | `EN = ula.DISP_EN` |
| `decod7seg_f` `aUNI..gUNI` | `apaga_display.I[0..6]` → `HEX0[0..6]` | `EN = ula.DISP_EN` |
| `NAND(F[5], DISP_EN)` | `HEX2[6]` | "−" quando F é negativo (só em 000/001); `HEX2[5..0]` em VCC |
| — | `HEX3` | não usado (fica apagado) |

---

## Decisões

- **Zero negativo:** +0 e −0 são iguais.
- **Soma/subtração:** via `comp2` (sinal-magnitude → C2 → soma → volta para sinal-magnitude com `c2_para_sm`).
- **Operação `010`:** F em 6 bits = `{OS, OS, O[3..0]}` (saídas do `comp2`).
- **Comparações (`011`, `100`, `101`):** F = `000000`; só o `STATUS` vale (decidido em 01/10).
- **`A < B`:** segunda instância do `comp_maior` com A e B trocados.
- **Displays:** decodificadores binário → 7 segmentos do grupo, sem BCD; a dezena mostra `0` abaixo de 10.
