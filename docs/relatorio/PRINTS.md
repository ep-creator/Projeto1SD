# Prints e simulações para o relatório

O relatório (`Relatorio_Projeto1SD.docx` / `.pdf`) é gerado a partir dos `testes/<bloco>/tabela_verdade.md`, de `docs/relatorio/partes/` e das figuras abaixo. Onde a figura ainda não existe, o documento mostra um quadro amarelo **[inserir figura: …]**. Basta salvar cada print com o nome indicado e gerar o relatório de novo.

## Como tirar os prints

**Circuito (`<bloco>_circuito.png`)**

1. Abra `testes/<bloco>/<bloco>.qpf` no Quartus; o esquemático é o `lib/<bloco>.bdf`.
2. *View > Fit in Window* (Ctrl+W) para caber tudo na tela.
3. Recorte **só o esquemático** com a Ferramenta de Captura (Win+Shift+S) e salve como `testes/<bloco>/<bloco>_circuito.png`.

**Simulação (`<bloco>_simulacao.png`)**

1. Abra (ou crie em *File > New > University Program VWF*) o `testes/<bloco>/<bloco>.vwf`, com todas as entradas e saídas do bloco.
2. Para cobrir todas as combinações, agrupe as entradas num barramento e use *Edit > Value > Count Value* (ou dê um padrão de clock diferente para cada entrada, dobrando o período a cada uma).
3. *Simulation > Run Functional Simulation*. Na janela do resultado, *View > Fit in Window*.
4. Recorte **só a área dos sinais** (nomes + formas de onda, sem barras de ferramentas e sem o espaço vazio embaixo) e salve como `testes/<bloco>/<bloco>_simulacao.png`.
5. Se a simulação estiver em hexadecimal, mude os barramentos para binário ou decimal com sinal (botão direito no sinal > *Radix*), conforme ficar mais fácil de conferir com a tabela verdade.

Depois de cada simulação, confira a waveform com a tabela verdade do `tabela_verdade.md` do bloco. Se alguma linha não bater, anote em **Observações** no próprio `.md`.

## Lista

Situação em 01/10: **todos os prints de circuito estão prontos** (tirados no Quartus 25.1 do PC de casa). Todos os blocos já têm `.vwf`: as do grupo foram mantidas e as que faltavam (ou estavam desatualizadas) foram geradas por `ferramentas/relatorio/gera_vwf.py`, com os vetores de teste já preenchidos. Falta **rodar as simulações e tirar os prints**.

> No PC de casa a simulação não roda: o Questa do Quartus 25.1 recusa a licença (`License issue: Invalid host`, arquivo `C:/Users/enzop/questa_lic.dat`). Ou se gera uma licença nova para este PC no portal de licenças da Intel, ou as simulações são rodadas no PC do laboratório (Quartus 21.1 com ModelSim, que não pede licença).

| Bloco | Circuito | Simulação | `.vwf` |
| :--- | :---: | :---: | :--- |
| `mux2x1` | ☑ | ☐ | gerada (vetores prontos) |
| `mux4x1` | ☑ | ☐ | gerada (vetores prontos) |
| `inversor` | ☑ | ☐ | gerada (vetores prontos) |
| `inversor5` | ☑ | ☐ | gerada (vetores prontos) |
| `comp2` | ☑ | ☑ | do grupo, simulação pronta |
| `somador_completo` | ☑ | ☐ | gerada (vetores prontos) |
| `somador6` | ☑ | ☑ | do grupo, simulação pronta |
| `c2_para_sm` | ☑ | ☐ | gerada (vetores prontos) |
| `somador_subtrator` | ☑ | ☐ | gerada (vetores prontos) |
| `op_and` | ☑ | ☐ | gerada (vetores prontos) |
| `op_xor` | ☑ | ☐ | gerada (vetores prontos) |
| `comp_mag` | ☑ | ☐ | do grupo (conferir se cobre os casos) |
| `comp_maior` | ☑ | ☐ | gerada (vetores prontos) |
| `comparador_igual` | ☑ | ☐ | do grupo (conferir se cobre os casos) |
| `decodificador_comparadores` | ☑ | ☐ | do grupo (conferir se cobre os casos) |
| `mux_comparadores` | ☑ | ☐ | do grupo (conferir se cobre os casos) |
| `decodificador_saida` | ☑ | ☐ | do grupo (conferir se cobre os casos) |
| `mux_saida` | ☑ | ☐ | gerada (vetores prontos) |
| `decod7seg_ab_dezena` | ☑ | ☐ | gerada (vetores prontos) |
| `decod7seg_ab_unidade` | ☑ | ☐ | gerada (vetores prontos) |
| `decod7seg_f_dezena` | ☑ | ☐ | do grupo (conferir se cobre os casos) |
| `decod7seg_f_unidade` | ☑ | ☐ | gerada (vetores prontos) |
| `decod7seg_f` | ☑ | ☐ | gerada (vetores prontos) |
| `apaga_display` | ☑ | ☐ | gerada (vetores prontos) |
| `ula` | ☑ | ☐ | gerada (vetores prontos) |

**Outras figuras** (em `docs/relatorio/figuras/`)

| Arquivo | O que é |
| :--- | :--- |
| `toplevel_circuito.png` | print do `src/toplevel.bdf` inteiro (pronto) |
| `placa.jpg` | foto da DE2-115 funcionando (por exemplo, uma subtração com resultado negativo) |
| `visao_geral.png`, `ula_interna.png` | diagramas em blocos (já gerados a partir dos `.dot` desta pasta) |

## Gerar o relatório

Na raiz do repositório (precisa de Python com `python-docx`, `pandoc` e LibreOffice):

```
python3 ferramentas/relatorio/monta_relatorio.py
```

Gera `docs/relatorio/Relatorio_Projeto1SD.docx` e `.pdf` e lista as figuras que ainda faltam.
