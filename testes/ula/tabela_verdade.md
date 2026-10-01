# ula — tabela verdade e simulação

* **Circuito:** [`lib/ula.bdf`](../../lib/ula.bdf)
* **Entradas:** `A[4..0]`, `B[4..0]` (sinal-magnitude, bit 4 = sinal), `S[2..0]`
* **Saídas:** `F[5..0]` (sinal-magnitude, `F[5]` = sinal), `STATUS`, `DISP_EN`
* **Simulação:** `ula.vwf` (a criar)

| S | Operação | F | STATUS | DISP_EN |
|:---:|:---|:---|:---:|:---:|
| `000` | A + B | `somador_subtrator` (sinal-magnitude) | 0 | 1 |
| `001` | A − B | `somador_subtrator` (sinal-magnitude) | 0 | 1 |
| `010` | C2 de B | `{OS, OS, O[3..0]}` do `comp2` | 0 | 0 |
| `011` | A = B | `000000` | `comparador_igual` | 0 |
| `100` | A > B | `000000` | `comp_maior(A, B)` | 0 |
| `101` | A < B | `000000` | `comp_maior(B, A)` | 0 |
| `110` | A AND B | `op_and` | 0 | 0 |
| `111` | A XOR B | `op_xor` | 0 | 0 |

## Casos de teste

| S | A | B | F esperado | STATUS |
|:---:|:---:|:---:|:---:|:---:|
| `000` | +5 (`00101`) | −3 (`10011`) | +2 (`000010`) | 0 |
| `001` | −9 (`11001`) | +12 (`01100`) | −21 (`110101`) | 0 |
| `000` | −8 (`11000`) | −8 (`11000`) | −16 (`110000`) | 0 |
| `000` | −15 (`11111`) | −15 (`11111`) | −30 (`111110`) | 0 |
| `001` | +7 (`00111`) | +7 (`00111`) | 0 (`000000`) | 0 |
| `000` | −0 (`10000`) | +0 (`00000`) | 0 (`000000`) | 0 |
| `011` | −0 (`10000`) | +0 (`00000`) | `000000` | 1 |
| `100` | +2 (`00010`) | −5 (`10101`) | `000000` | 1 |
| `101` | −3 (`10011`) | −3 (`10011`) | `000000` | 0 |

## Observações

