# Projeto ULA e Sistema de Visualização (DE2-115)

Projeto prático desenvolvido para a placa de desenvolvimento **Altera/Terasic DE2-115 (Cyclone IV EP4CE115F29C7)**. O sistema consiste numa **Unidade Lógica e Aritmética (ULA)** com operações aritméticas, lógicas e de comparação, acoplada a um sistema de decodificação para visualização em displays de 7 segmentos e LEDs, projetado **exclusivamente com portas lógicas fundamentais**.

---

## 📌 Especificação Técnica

### Entradas e Seleção
* **Operandos $A$ e $B$:** Vetores de 5 bits cada, no formato **Sinal e Magnitude** (`[S, M3, M2, M1, M0]`). Se o número for negativo, $S = 1$; caso contrário, $S = 0$.
* **Seletor de Operações ($S_2 S_1 S_0$):** Vetor de 3 bits responsável por selecionar a função da ULA:

| $S_2$ | $S_1$ | $S_0$ | Operação | Tipo de Saída |
| :---: | :---: | :---: | :--- | :--- |
| `0` | `0` | `0` | $F = A + B$ | Vetor $F$ (6 bits) + Displays |
| `0` | `0` | `1` | $F = A - B$ | Vetor $F$ (6 bits) + Displays |
| `0` | `1` | `0` | $F = \text{Complemento a 2 de } B$ | Vetor $F$ (6 bits) + LEDs |
| `0` | `1` | `1` | $F = (A == B)$ | LED de Status (1 bit) |
| `1` | `0` | `0` | $F = (A > B)$ | LED de Status (1 bit) |
| `1` | `0` | `1` | $F = (A < B)$ | LED de Status (1 bit) |
| `1` | `1` | `0` | $F = A \text{ AND } B$ | Vetor $F$ (6 bits) + LEDs |
| `1` | `1` | `1` | $F = A \text{ XOR } B$ | Vetor $F$ (6 bits) + LEDs |

### Saídas e Periféricos
* **Vetor $F$ (6 bits):** Resultado da operação em **Sinal e Magnitude** (`[S_F, F4, F3, F2, F1, F0]`). Não sai em complemento a 2.
* **LED de Status (1 bit):** Ativado quando a condição booleana das operações de comparação ($=$, $>$, $<$) for verdadeira.
* **Displays de 7 Segmentos:**
  * **$A$ e $B$:** Replicam continuamente a magnitude das entradas (0 a 15). O sinal é exibido no LED respectivo.
  * **$F$ (Dezena e Unidade):** Exibem o valor do cálculo (máximo de 30).
  * **Regra de Apagamento (*Blanking*):** Os displays de $F$ devem funcionar **apenas** nas operações de soma (`000`) e subtração (`001`). Em todas as outras operações, os displays de $F$ permanecem apagados.
  * Lógica dos segmentos ativa em **nível lógico baixo (0)**.
* **LEDs Vermelhos/Verdes:** Replicam as chaves de entrada ($A$, $B$, $S$), o vetor de saída $F$ e o bit de Status.

---

## 🗂️ Divisão do Projeto e Mapeamento de Branches

O fluxo de trabalho adota o modelo **Git Flow**, onde cada funcionalidade é desenvolvida e validada de forma modular antes de ser integrada na branch `develop`. A branch `main` é reservada exclusivamente para versões estáveis validadas na placa.

```text
main (código final estável)
  └── develop (integração contínua)
        ├── feat/ula-logica-c2
        ├── feat/ula-comparadores
        ├── feat/ula-aritmetica
        ├── feat/decod-displays
        ├── feat/ula-mux-selecao
        ├── feat/ula-integracao
        ├── feat/toplevel-pinagem
        └── docs/relatorio-final
```

### Detalhe das Branches

| Branch | Responsabilidade / Tarefa | Dependências |
| :--- | :--- | :--- |
| `feat/ula-logica-c2` | Portas lógicas para as operações bit a bit AND, XOR e o circuito de Complemento a 2 de $B$. | Nenhuma (Fase 1) |
| `feat/ula-comparadores` | Comparadores de magnitude/sinal para 5 bits ($A=B$, $A>B$, $A<B$) e condução do bit de Status. | Nenhuma (Fase 1) |
| `feat/ula-aritmetica` | Conversão interna de sinal/magnitude para Complemento a 2, somador/subtrator de 5/6 bits e reconversão para sinal/magnitude em $F$. | Nenhuma (Fase 1) |
| `feat/decod-displays` | Decodificador binário $\to$ BCD de 2 dígitos (0 a 30), lógica de 7 segmentos (ativo baixo) e circuito de enable/apagamento para $F$. | Nenhuma (Fase 1) |
| `feat/ula-mux-selecao` | Multiplexador com portas lógicas controlado por $S_2S_1S_0$ para selecionar o barramento de saída $F$. | Nenhuma (Fase 1) |
| `feat/ula-integracao` | Junção esquemática dos blocos lógicos, aritméticos, comparadores e multiplexador no símbolo unificado `ULA`. | Submódulos ULA prontos |
| `feat/toplevel-pinagem` | Circuito esquemático *Top-Level* interligando a ULA aos decodificadores e mapeamento de pinos da DE2-115 no *Pin Planner* (`.qsf`). | `feat/ula-integracao` e `feat/decod-displays` |
| `docs/relatorio-final` | Documentação técnica: diagramas de blocos, tabelas-verdade, mapas-K, capturas de esquemáticos e formas de onda (*waveforms*). | Simulações funcionais |

---

## 📁 Estrutura do Diretório

Regra central: **cada bloco existe uma única vez, na biblioteca `lib/`**. Todo projeto Quartus (teste de um bloco, ULA, top-level ou um projeto novo de qualquer pessoa) aponta para `lib/` e usa esses mesmos arquivos. Nada é copiado. Por isso, alterar um bloco na biblioteca vale para todos os projetos que o usam.

```text
Projeto1SD/
├── README.md
├── CHECKLIST.md                  <-- andamento do projeto, bloco a bloco
├── .gitignore
│
├── lib/                          <-- A BIBLIOTECA: todos os blocos, numa pasta só
│   ├── mux2x1.bdf                <-- circuito do bloco (a entidade)
│   ├── mux2x1.bsf                <-- símbolo, usado para inserir o bloco em outros esquemáticos
│   ├── comp2.bdf / comp2.bsf
│   └── ...                       <-- só .bdf e .bsf aqui (nenhum projeto .qpf)
│
├── testes/                       <-- tabela verdade e simulação, uma pasta por bloco
│   ├── mux2x1/
│   │   ├── mux2x1.qpf / .qsf     <-- projeto de teste do bloco (usa ../../lib)
│   │   ├── tabela_verdade.md     <-- tabela verdade (relatório)
│   │   └── mux2x1.vwf            <-- simulação (relatório, item d)
│   └── ...
│
├── src/                          <-- montagem final
│   ├── Projeto1SD.qpf / .qsf     <-- top-level + pinagem da DE2-115 (usa ../lib)
│   ├── toplevel.bdf              <-- ULA + decodificadores + LEDs (a fazer)
│   └── toplevel.vwf              <-- simulação do sistema completo (relatório, item e)
│
└── docs/relatorio/               <-- base do relatório impresso (itens a–f)
```

**Por que `lib/` não tem subpastas:** o Quartus não procura blocos dentro de subpastas de uma biblioteca. Com uma pasta só, qualquer projeto precisa de **uma única linha** (`SEARCH_PATH`) para enxergar todos os blocos, e um bloco novo fica disponível para todos assim que o `.bdf` e o `.bsf` são salvos em `lib/`. As categorias ficam no catálogo abaixo.

### 📚 Catálogo da biblioteca

| Bloco | Categoria | Função | Usa | Pendência |
| :--- | :--- | :--- | :--- | :--- |
| `mux2x1` | comum | MUX 2:1 de 1 bit | — | — |
| `mux4x1` | comum | MUX 4:1 de 1 bit | — | — |
| `inversor` | c2 | C2 de 4 bits (inverte e soma 1) | — | — |
| `comp2` | c2 | Sinal/magnitude → C2 condicional (`I[3..0]`, `IS` → `O[3..0]`, `OS`) | `inversor`, `mux2x1` | — |
| `op_and` | lógica | AND bit a bit | — | `F[4]`/`F[5]` trocados |
| `op_xor` | lógica | XOR bit a bit | — | `F[4]`/`F[5]` trocados |
| `comparador_igual` | comparadores | $A = B$ | — | — |
| `mux_comparadores` | comparadores | Escolhe EQ/GT/LT para o `STATUS` | — | — |
| `decodificador_comparadores` | decodificadores | `S` → bits de seleção dos comparadores (`F1`, `F2`) | — | — |
| `mux_saida` | seleção | MUX 4:1 de 6 bits | `mux4x1` | entradas de 1 bit; falta `.bsf` |
| `somador_completo` | aritmética | Somador completo de 1 bit | — | — |
| `somador6` | aritmética | Soma em C2: 5 + 5 bits → 6 bits (`A[4..0]`, `B[4..0]` → `O[5..0]`) | `somador_completo` | — |
| `decodificador_saida` | decodificadores | `S` → seletor do `mux_saida` (`F1`, `F2`) | — | — |
| `decod7seg_ab_dezena` | display | Magnitude 0–15 → dezena em 7 segmentos | — | — |
| `decod7seg_ab_unidade` | display | Magnitude 0–15 → unidade em 7 segmentos | — | valor 9 |
| `decod7seg_f_dezena` | display | Magnitude 0–30 → dezena em 7 segmentos | — | — |
| `decod7seg_f_unidade` | display | Magnitude 0–30 → unidade em 7 segmentos | — | simulação só com `gUNI` |
| `decod7seg_f` | display | \|F\| nos dois displays (`S[4..0]`, `sinal_S` → segmentos DEZ/UNI, `led_negativo`) | `decod7seg_f_dezena`, `decod7seg_f_unidade` | falta `.bsf` |

Detalhes das pendências em [⏳ Pendências](#-pendências-depois-dos-testes). O andamento bloco a bloco está no [CHECKLIST.md](CHECKLIST.md).

| Categoria | Branch responsável |
| :--- | :--- |
| comum | quem precisar do bloco genérico (avisar o grupo) |
| c2, lógica | `feat/ula-logica-c2` |
| comparadores, decodificadores | `feat/ula-comparadores` |
| aritmética | `feat/ula-aritmetica` |
| seleção | `feat/ula-mux-selecao` |
| display | `feat/decod-displays` |
| integração (`ula`) | `feat/ula-integracao` |
| `src/` (top-level e pinagem) | `feat/toplevel-pinagem` |

---

## 🧩 Convenções

* **Nomes:** `snake_case` minúsculo, **únicos na biblioteca**. O `.bdf`, o `.bsf`, a entidade e a pasta de teste têm **o mesmo nome** (no Quartus o nome da entidade de um `.bdf` é o nome do arquivo). Não use nomes de primitivas do Quartus (`and`, `xor`, `not`...): por isso `op_and`, `op_xor`.
* **Interfaces em barramento:** vetores como `NOME[n..0]`, bit mais significativo à esquerda. Nos operandos e no resultado, **o bit de sinal é o MSB**: `A[4..0]`, `B[4..0]` (`A[4]` = sinal) e `F[5..0]` (`F[5]` = sinal). Seletor: `S[2..0]`. Sinais de 1 bit têm nome próprio em maiúsculas (`EQ`, `GT`, `LT`, `STATUS`).
* **Extração de bits:** fio fino nomeado com o índice (`A[3]`) derivado do barramento, como em `comparador_igual.bdf`.
* **Biblioteca:** `lib/` guarda só `.bdf` e `.bsf`. Nunca copie um bloco para dentro de outra pasta nem crie um projeto `.qpf` em `lib/`.
* **Caminhos sempre relativos:** `../lib` (em `src/`) ou `../../lib` (em `testes/<bloco>/`). Um caminho absoluto (`C:\...`) só funciona no computador de quem o criou.
* **Testes:** `testes/<bloco>/` guarda o projeto de teste, a `tabela_verdade.md` e a simulação `<bloco>.vwf`. A pasta `simulation/` é gerada pelo Quartus e fica fora do Git.
* **Pinagem:** o `src/Projeto1SD.qsf` só recebe pinagem na branch `feat/toplevel-pinagem`.

---

## 🧪 Como Usar a Biblioteca

### Usar os blocos num projeto (qualquer computador)

1. Clone o repositório. A biblioteca vem junto, em `lib/`; não há nada para instalar.
2. Crie ou abra o projeto **dentro do repositório** (por exemplo, em `src/` ou em `testes/<bloco>/`).
3. *Assignments > Settings > Libraries*, em **Project libraries**, adicione o caminho relativo até `lib` (`../lib` ou `../../lib`) e clique em *Add*. Isso grava uma linha no `.qsf`:

```tcl
set_global_assignment -name SEARCH_PATH ../lib
```

4. No esquemático, abra a *Symbol Tool* (duplo clique na área vazia). A pasta `lib` aparece na lista de bibliotecas, junto das nativas do Quartus. Escolha o bloco e insira.
5. Para ver o funcionamento interno de um bloco, dê duplo clique na instância, ou veja a árvore em *Project Navigator > Hierarchy*.

Se aparecer *"entity ... is undefined"*, o projeto não está enxergando `lib/`: confira o caminho no passo 3 e se o `.bdf` do bloco está em `lib/`.

### Alterar um bloco da biblioteca

Os blocos não ficam travados: o arquivo em `lib/` é o próprio circuito.

1. Abra `testes/<bloco>/<bloco>.qpf`. O esquemático aberto é `lib/<bloco>.bdf`.
2. Faça a alteração e salve (`Ctrl+S`). O arquivo de `lib/` é atualizado, e todos os projetos passam a usar a versão nova na próxima compilação.
3. Compile e rode a simulação `testes/<bloco>/<bloco>.vwf` de novo; atualize a `tabela_verdade.md` se o comportamento mudou.
4. **Se mudou algum pino** (adicionou, removeu ou renomeou):
   1. *File > Create/Update > Create Symbol Files for Current File*, salvando por cima de `lib/<bloco>.bsf`.
   2. Em cada esquemático que usa o bloco: botão direito na instância > *Update Symbol or Block*.
5. Faça o commit na branch da categoria. Avise o grupo quando alterar bloco de outra pessoa, porque a mudança vale para todos.

### Adicionar um bloco novo à biblioteca

1. Crie a pasta `testes/<bloco>/`.
2. *File > New Project Wizard*: diretório `testes/<bloco>`, nome do projeto e entidade top-level `<bloco>`, família *Cyclone IV E*, dispositivo **EP4CE115F29C7**.
3. *Assignments > Settings > Libraries* e adicione `../../lib` em *Project libraries*. Assim o bloco novo já pode usar os outros blocos da biblioteca. **Confira o `.qsf`** depois (passo 8): o Wizard pode não gravar a linha.
4. *File > New > Block Diagram/Schematic File*, desenhe e salve com *File > Save As* **dentro de `lib/`**, como `<bloco>.bdf`, com *Add file to current project* marcado.
5. Gere o símbolo: *File > Create/Update > Create Symbol Files for Current File*. Confira que `<bloco>.bsf` ficou em `lib/`.
6. Copie `tabela_verdade.md` de outro bloco para `testes/<bloco>/` e adapte; salve a simulação como `testes/<bloco>/<bloco>.vwf`.
7. Acrescente o bloco no [catálogo](#-catálogo-da-biblioteca).
8. Confira que o `.qsf` tem a linha `SEARCH_PATH ../../lib`. Se não tiver, acrescente com o projeto **fechado** no Quartus (o `.qsf` pode não terminar com quebra de linha, por isso o `` `n `` antes):

```powershell
Add-Content -Path testes/<bloco>/<bloco>.qsf -Value "`nset_global_assignment -name SEARCH_PATH ../../lib" -Encoding ascii
```

O `.qsf` do teste fica assim (exemplo do `comp2`):

```tcl
set_global_assignment -name TOP_LEVEL_ENTITY comp2
set_global_assignment -name BDF_FILE ../../lib/comp2.bdf
set_global_assignment -name SEARCH_PATH ../../lib
```

### Testar um bloco isolado

1. Abra `testes/<bloco>/<bloco>.qpf`.
2. Compile (`Ctrl+L`) ou analise (`Ctrl+K`).
3. Abra `<bloco>.vwf` da mesma pasta, ou crie com *File > New > University Program VWF*, adicione os pinos (*Edit > Insert > Node Finder*) e salve em `testes/<bloco>/`.
4. *Simulation > Run Functional Simulation*.

---

## ✅ Decisões Tomadas

* **Zero negativo:** `+0` (`00000`) e `−0` (`10000`) são **iguais**. Blocos a conferir: `comparador_igual` (deve dar `1` para `00000` × `10000`), comparadores `>`/`<` (nenhum dos dois ativa nesse caso) e `comp2` (antes convertia `−0` em `10000`, que em C2 vale −16).
* **Operação `010` (C2 de B):** F mostra o resultado obtido pelo bloco `comp2`: se B é positivo, sai igual a B; se B é negativo, sai o complemento a 2.

## ⏳ Pendências (depois dos testes)

* **Interfaces fora da convenção:** ficam como estão até a integração funcionar; depois são padronizadas. Casos atuais: `op_and`/`op_xor` (`A[3..0]` + `SA`, saídas `F[0]`…`F[5]` soltas), `decodificador_comparadores` (`S3, S2, S1` → `F1, F2`), `comparador_igual` (saída `F`, convenção seria `EQ`) e `inversor` (`I0..I3` → `F0..F3`).
* **Defeitos conhecidos (lógica dos autores, a revisar na integração):**
  * `op_and` e `op_xor`: `F[4]` e `F[5]` trocados (o sinal sai em `F[4]` e o GND em `F[5]`).
  * `decod7seg_ab_unidade`: o 9 (`1001`) aparece como 5 — a AND4 de entradas A, B', C', D ainda está na OR4 de `bu_seg` (o commit `9b892ca` só redesenhou os fios).
  * `mux_saida`: as entradas `SOMA_OU_SUB`, `Comp2B`, `AND` e `XOR` são de 1 bit e ligadas aos 6 MUX, então as 6 saídas ficam iguais; precisam ser barramentos `[5..0]`.
* **Blocos que faltam:** `inversor5`, `c2_para_sm`, `somador_subtrator`, `comparador_maior`, `apaga_display`, `ula`; top-level e pinagem. Lista completa em [CHECKLIST.md](CHECKLIST.md).
* **Arquivos a gerar no Quartus:** waveforms de `mux2x1`, `inversor`, `mux4x1`, `mux_saida` e `decod7seg_f`; `.bsf` do `decod7seg_f` (abrir `testes/<bloco>/<bloco>.qpf` e gerar em `lib/`).

---

## 📦 Instruções para Avaliação na Bancada

1. Abra o Quartus Prime e carregue o projeto `src/Projeto1SD.qpf`.
2. Confirme que o dispositivo selecionado é o FPGA **Cyclone IV EP4CE115F29C7**.
3. As atribuições de pinos das chaves (`SW`), displays (`HEX0`–`HEX7`) e LEDs (`LEDR`, `LEDG`) já estão definidas em `src/Projeto1SD.qsf`.
4. Compile o projeto e grave na placa DE2-115 via USB-Blaster.
5. Cada bloco pode ser inspecionado isoladamente abrindo `testes/<bloco>/<bloco>.qpf`.
