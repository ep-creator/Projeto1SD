# Introdução

Este relatório descreve o projeto de uma Unidade Lógica e Aritmética (ULA) de 5 bits, acoplada a decodificadores para displays de 7 segmentos, desenvolvida para a placa de prototipação Terasic DE2-115. A ULA recebe dois operandos em sinal-magnitude e executa oito operações: soma, subtração, complemento a 2, três comparações (igual, maior e menor), AND e XOR bit a bit.

Como pede o enunciado, todo o projeto foi feito **somente com portas lógicas**, em esquemáticos (`.bdf`) no Quartus Prime Lite, sem HDL e sem megafunções. O sistema foi dividido em blocos pequenos, cada um projetado a partir da sua tabela verdade, simulado isoladamente e reutilizado nos blocos maiores. Os blocos ficam numa biblioteca única (`lib/`) do repositório do grupo, e cada um tem um projeto de teste com tabela verdade e simulação em `testes/<bloco>/`.

O relatório segue os itens do enunciado: a seção 2 apresenta a visão geral do sistema em blocos; a seção 3 resume os conceitos usados (sinal-magnitude, complemento a 2, comparação e displays); a seção 4 traz, para cada módulo, a tabela verdade, as equações e mapas de Karnaugh, o circuito e a simulação; a seção 5 mostra o sistema completo conectado, a pinagem e os testes na placa; a seção 6 conclui.
