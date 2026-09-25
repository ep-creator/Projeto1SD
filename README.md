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

Regras centrais: **cada bloco tem sua própria pasta, e cada pasta de bloco é também um projeto Quartus de teste**. Os blocos ficam agrupados por categoria para facilitar a localização. Qualquer bloco pode ser alterado, compilado e simulado sozinho, e os projetos de integração (`ula` e o top-level) usam exatamente os mesmos arquivos `.bdf`, sem cópias.

```text
Projeto1SD/
├── README.md
├── .gitignore
│
├── src/
│   ├── Projeto1SD.qpf / .qsf     <-- integração final + pinagem da DE2-115
│   ├── toplevel.bdf              <-- ULA + decodificadores + LEDs
│   ├── sim/toplevel.vwf          <-- waveform do sistema completo (relatório, item e)
│   │
│   └── modules/
│       ├── comum/                <-- blocos genéricos, reutilizados por várias categorias
│       │   └── mux2x1/
│       │       ├── mux2x1.bdf        <-- esquemático
│       │       ├── mux2x1.bsf        <-- símbolo
│       │       ├── mux2x1.qpf/.qsf   <-- projeto de teste do bloco
│       │       └── sim/mux2x1.vwf    <-- waveform do bloco (relatório, item d)
│       ├── c2/                   <-- complemento a 2
│       │   ├── inversor/         <-- C2 de 4 bits (inverte e soma 1)
│       │   └── comp2/            <-- sinal/magnitude -> C2 condicional
│       ├── logica/               <-- AND e XOR bit a bit
│       ├── comparadores/         <-- A = B, A > B, A < B
│       │   └── comparador_igual/
│       ├── aritmetica/           <-- somador/subtrator e conversões
│       ├── selecao/              <-- MUX de saída controlado por S[2..0]
│       ├── display/              <-- binário -> BCD, 7 segmentos, blanking
│       └── integracao/
│           └── ula/              <-- junta os blocos da ULA; testa a ULA sem a placa
│
└── docs/relatorio/               <-- base do relatório impresso (itens a–f)
```

| Categoria | Branch responsável |
| :--- | :--- |
| `comum/` | quem precisar do bloco genérico (avisar o grupo) |
| `c2/`, `logica/` | `feat/ula-logica-c2` |
| `comparadores/` | `feat/ula-comparadores` |
| `aritmetica/` | `feat/ula-aritmetica` |
| `selecao/` | `feat/ula-mux-selecao` |
| `display/` | `feat/decod-displays` |
| `integracao/` | `feat/ula-integracao` |
| `src/` (top-level e pinagem) | `feat/toplevel-pinagem` |

---

## 🧩 Convenções

* **Nomes:** `snake_case` minúsculo. Pasta do bloco, `.bdf`, `.bsf`, `.qpf` e entidade têm **o mesmo nome** (no Quartus o nome da entidade de um `.bdf` é o nome do arquivo). Não use nomes de primitivas do Quartus (`and`, `xor`, `not`...): por isso `op_and`, `op_xor`.
* **Onde fica cada bloco:** na categoria da operação a que pertence. Se é genérico e usado por mais de uma categoria, vai para `comum/`.
* **Interfaces em barramento:** vetores como `NOME[n..0]`, bit mais significativo à esquerda. Nos operandos e no resultado, **o bit de sinal é o MSB**: `A[4..0]`, `B[4..0]` (`A[4]` = sinal) e `F[5..0]` (`F[5]` = sinal). Seletor: `S[2..0]`. Sinais de 1 bit têm nome próprio em maiúsculas (`EQ`, `GT`, `LT`, `STATUS`).
* **Extração de bits:** fio fino nomeado com o índice (`A[3]`) derivado do barramento, como em `comparador_igual.bdf`.
* **Dependências:** um bloco que usa outros declara as pastas deles como bibliotecas do próprio projeto (`SEARCH_PATH` no `.qsf`), incluindo as dependências das dependências. Nunca copie um `.bdf` para dentro de outra pasta.
* **Simulações:** sempre em `<bloco>/sim/<bloco>.vwf`. A pasta `simulation/` é gerada pelo Quartus e fica fora do Git.
* **Pinagem:** o `src/Projeto1SD.qsf` só é editado na branch `feat/toplevel-pinagem`.

---

## 🧪 Como Trabalhar e Testar

**Criar um bloco novo:**

1. Crie a pasta `src/modules/<categoria>/<bloco>/` e, dentro dela, a pasta `sim/`.
2. No Quartus: *File > New Project Wizard*. Diretório `src/modules/<categoria>/<bloco>`, nome do projeto e da entidade top-level `<bloco>`, família *Cyclone IV E*, dispositivo **EP4CE115F29C7**.
3. Desenhe o esquemático e salve como `<bloco>.bdf` na mesma pasta. Adicione-o ao projeto (*Project > Add/Remove Files in Project*).
4. Se o bloco usa outros: *Assignments > Settings > Libraries* e adicione em *Project libraries* as pastas `../../<categoria>/<dependência>` (e as dependências delas). Isso grava linhas `SEARCH_PATH` no `.qsf`. Exemplo do `comp2.qsf`:

```tcl
set_global_assignment -name TOP_LEVEL_ENTITY comp2
set_global_assignment -name BDF_FILE comp2.bdf
set_global_assignment -name SEARCH_PATH ../../c2/inversor
set_global_assignment -name SEARCH_PATH ../../comum/mux2x1
```

5. Gere o símbolo: *File > Create/Update > Create Symbol Files for Current File*.

**Testar um bloco isolado:**

1. Abra `src/modules/<categoria>/<bloco>/<bloco>.qpf`.
2. Compile (`Ctrl+L`) ou analise (`Ctrl+K`).
3. *File > New > University Program VWF*, adicione os pinos (*Edit > Insert > Node Finder*), monte os estímulos e salve como `sim/<bloco>.vwf`.
4. *Simulation > Run Functional Simulation*.

**Testar em conjunto:** abra o projeto que integra (`ula` ou `src/Projeto1SD.qpf`). Ele enxerga as versões atuais dos blocos pelas bibliotecas (`SEARCH_PATH`).

**Mudou a interface de um bloco** (pinos adicionados, renomeados ou removidos):

1. No projeto do bloco: *File > Create/Update > Create Symbol Files for Current File*.
2. Nos esquemáticos que usam o bloco: botão direito na instância > *Update Symbol or Block*.

---

## ❓ Decisões em Aberto

* **Zero negativo:** em sinal/magnitude, `+0` (`00000`) e `−0` (`10000`) são o mesmo número. O `comparador_igual` atual trata os dois como diferentes, e o `comp2` converte `−0` em `10000`, que em C2 vale −16. Definir a regra e ajustar os blocos.
* **Operação `010` (C2 de B):** o enunciado pede F "binário e não complementado a dois", mas também diz que os LEDs mostram o complemento 2. Confirmar com o monitor se F deve mostrar o padrão de bits do C2 de B ou o valor −B em sinal/magnitude.

---

## 📦 Instruções para Avaliação na Bancada

1. Abra o Quartus Prime e carregue o projeto `src/Projeto1SD.qpf`.
2. Confirme que o dispositivo selecionado é o FPGA **Cyclone IV EP4CE115F29C7**.
3. As atribuições de pinos das chaves (`SW`), displays (`HEX0`–`HEX7`) e LEDs (`LEDR`, `LEDG`) já estão definidas em `src/Projeto1SD.qsf`.
4. Compile o projeto e grave na placa DE2-115 via USB-Blaster.
5. Cada bloco pode ser inspecionado isoladamente abrindo `src/modules/<categoria>/<bloco>/<bloco>.qpf`.
