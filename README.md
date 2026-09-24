# Projeto ULA e Sistema de Visualização (DE2-115)

Projeto prático desenvolvido para a placa de desenvolvimento **Altera/Terasic DE2-115 (Cyclone IV EP4CE115F29C7)**. O sistema consiste numa **Unidade Lógica e Aritmética (ULA)** com operações aritméticas, lógicas e de comparação, acoplada a um sistema de descodificação para visualização em ecrãs de 7 segmentos e LEDs, projetado **exclusivamente com portas lógicas fundamentais**.

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
  * **$A$ e $B$:** Replicam continuamente a magnitude das entradas (0 a 15). O sinal é exibido no LED respetivo.
  * **$F$ (Dezena e Unidade):** Exibem o valor do cálculo (máximo de 30).
  * **Regra de Apagamento (*Blanking*):** Os ecrãs de $F$ devem funcionar **apenas** nas operações de soma (`000`) e subtração (`001`). Em todas as outras operações, os ecrãs de $F$ permanecem apagados.
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
| `feat/decod-displays` | Descodificador binário $\to$ BCD de 2 dígitos (0 a 30), lógica de 7 segmentos (ativo baixo) e circuito de enable/apagamento para $F$. | Nenhuma (Fase 1) |
| `feat/ula-mux-selecao` | Multiplexador com portas lógicas controlado por $S_2S_1S_0$ para selecionar o barramento de saída $F$. | Nenhuma (Fase 1) |
| `feat/ula-integracao` | Junção esquemática dos blocos lógicos, aritméticos, comparadores e multiplexador no símbolo unificado `ULA`. | Submódulos ULA prontos |
| `feat/toplevel-pinagem` | Circuito esquemático *Top-Level* interligando a ULA aos descodificadores e mapeamento de pinos da DE2-115 no *Pin Planner* (`.qsf`). | `feat/ula-integracao` e `feat/decod-displays` |
| `docs/relatorio-final` | Documentação técnica: diagramas de blocos, tabelas-verdade, mapas-K, capturas de esquemáticos e formas de onda (*waveforms*). | Simulações funcionais |

---

## 🛠️ Boas Práticas de Contribuição
1. Nunca submeter alterações diretamente na `develop` ou `main`.
2. Trabalhar sempre no ramo `feat/...` respetivo da sua tarefa.
3. Realizar testes funcionais através de simulação gráfica (*Waveform Vector File - .vwf*) antes de solicitar a integração.
4. Ao concluir um bloco funcional, abrir um Pull Request para a `develop`.