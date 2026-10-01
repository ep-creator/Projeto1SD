# Fundamentos e decisões de projeto

## Sinal-magnitude e complemento a 2

Em **sinal-magnitude (SM)**, o bit mais alto é o sinal e os outros são o valor absoluto: `10101` = −5. É o formato pedido para as entradas e para F, porque é fácil de ler, mas é ruim para fazer contas: somar −5 com +3 exige comparar as magnitudes e subtrair a menor da maior.

Em **complemento a 2 (C2)**, um único somador binário faz soma e subtração de números com sinal. O C2 de um número é obtido invertendo todos os bits e somando 1. Um atalho equivalente, usado nos blocos `inversor` e `inversor5`, é copiar os bits da direita até o primeiro 1 (inclusive) e inverter todos os outros; por isso cada bit de saída é o bit de entrada XOR "existe algum 1 abaixo dele".

Por isso a ULA trabalha assim nas contas: **SM → C2 → soma → C2 → SM**. A entrada e a saída ficam em sinal-magnitude, como pede o enunciado, e a conta é feita em complemento a 2.

## Soma e subtração

1. **A subtração vira soma:** A − B = A + (−B). Trocar o sinal de B em sinal-magnitude é só inverter o bit de sinal: `sinal_B' = sinal_B ⊕ S0`. Na soma (S0 = 0) o sinal fica; na subtração (S0 = 1), inverte.
2. **SM → C2 (`comp2`):** se o número é positivo, a magnitude passa direto; se é negativo, sai o C2 da magnitude. O resultado é um número em C2 de 5 bits (−15 a +15). O −0 (`10000`) sai como `00000`; caso contrário, viraria −16.
3. **Soma em 6 bits (`somador6`):** a soma de dois números de −15 a +15 vai de −30 a +30, que não cabe em 5 bits. Os operandos são estendidos para 6 bits repetindo o bit de sinal e somados por seis somadores completos em cascata. Em 6 bits não há overflow.
4. **C2 → SM (`c2_para_sm`):** se o resultado é positivo, já está em sinal-magnitude. Se é negativo, a magnitude é o C2 dos 5 bits de baixo; o sinal continua no bit 5.

Exemplo, (−9) − (+12):

| Passo | A | B | Comentário |
|:---|:---:|:---:|:---|
| Entrada (SM) | 11001 | 01100 | −9 e +12 |
| Inverte o sinal de B | 11001 | 11100 | −9 e −12 |
| `comp2` (C2, 5 bits) | 10111 | 10100 | −9 e −12 em C2 |
| Estende para 6 bits | 110111 | 110100 | repete o bit de sinal |
| `somador6` | 101011 | | −21 em C2 |
| `c2_para_sm` | 110101 | | sinal 1, magnitude 10101 = 21 → −21 |

## Complemento a 2 de B

A operação 010 usa o próprio `comp2` aplicado a B: B positivo sai igual; B negativo sai em C2. A saída de 5 bits é estendida para 6 bits repetindo o sinal: F = {OS, OS, O3, O2, O1, O0}. Exemplo: B = −3 (`10011`) → C2 = `11101` → F = `111101`.

## Comparações em sinal-magnitude

Comparar em sinal-magnitude é comparar os sinais primeiro e as magnitudes depois:

| Sinal de A | Sinal de B | A > B quando… |
|:---:|:---:|:---|
| + | + | \|A\| > \|B\| |
| − | − | \|A\| < \|B\| (o de menor magnitude é o maior) |
| + | − | sempre, exceto se os dois forem zero (+0 = −0) |
| − | + | nunca |

Como A < B é o mesmo que B > A, a ULA usa uma segunda instância do `comp_maior` com A e B trocados, sem precisar de um "comparador menor".

## Displays de 7 segmentos

Os displays da DE2-115 são de anodo comum: cada segmento **acende com nível lógico 0**. Os segmentos são indexados de 0 a 6 na ordem a, b, c, d, e, f, g (a no topo, g no meio).

| Dígito | a b c d e f g | Dígito | a b c d e f g |
|:---:|:---:|:---:|:---:|
| 0 | 0000001 | 5 | 0100100 |
| 1 | 1001111 | 6 | 0100000 |
| 2 | 0010010 | 7 | 0001111 |
| 3 | 0000110 | 8 | 0000000 |
| 4 | 1001100 | 9 | 0000100 |

Em vez de converter o número para BCD e usar um decodificador BCD → 7 segmentos, o projeto usa **decodificadores diretos do binário para cada dígito**: um bloco gera os segmentos da dezena e outro os da unidade, a partir dos 4 bits (|A|, |B|) ou 5 bits (|F|) da magnitude. Cada segmento é uma soma de produtos tirada da tabela verdade e simplificada por mapa de Karnaugh. A dezena mostra 0 abaixo de 10.

## Decisões de projeto

* **Zero negativo:** +0 (`00000`) e −0 (`10000`) são iguais. O `comp2` converte −0 em +0; nas comparações, `comparador_igual` dá 1 e `comp_maior` dá 0 nos dois sentidos.
* **Soma e subtração em C2 de 6 bits:** evita overflow (−30 a +30) e usa um único somador para as duas operações.
* **Operação 010:** F = C2 de B em 5 bits, estendido para 6 bits repetindo o sinal.
* **Comparações:** F = `000000`; só o STATUS vale.
* **AND e XOR:** bit a bit sobre os 5 bits, incluindo o sinal (`F5 = SA op SB`); F4 = 0.
* **Displays de F:** acesos só na soma e na subtração; o sinal de F aparece como "−" (segmento g) no HEX2 e no LED LEDG5.
