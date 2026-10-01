# Verificação dos blocos

Confere todos os blocos de `lib/` no Quartus e simula cada um com **todas** as combinações de entrada, comparando com a especificação do projeto.

1. **Quartus** (*View > Utility Windows > Tcl Console*):
   ```tcl
   source C:/caminho/do/Projeto1SD/ferramentas/verificacao/converter.tcl
   ```
   * converte cada `lib/<bloco>.bdf` em Verilog (`saida/<bloco>.v`) com `quartus_map --convert_bdf_to_verilog`;
   * roda *Analysis & Synthesis* em cada `testes/<bloco>` e grava o resumo em `saida/log_map.txt`.
   Para só alguns blocos: `set only {ula comp_maior}` antes do `source`.
2. **Simulação** (precisa do [Icarus Verilog](https://bleyer.org/icarus/) no PATH):
   ```
   python3 ferramentas/verificacao/testa_blocos.py
   ```
   Cada linha mostra `OK`/`FALHA`, quantos casos passaram e, nos displays, os dígitos que aparecem para 0, 1, 2…

A pasta `saida/` é gerada e fica fora do Git.
