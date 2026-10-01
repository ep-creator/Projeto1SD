# Ferramentas do relatório

* `gera_tabelas.py` — gerou os `testes/<bloco>/tabela_verdade.md` a partir da especificação de cada bloco (comportamento esperado, não simulação) e confere se as equações escritas batem com as tabelas. Rodar de novo **sobrescreve** os `.md`; se eles foram editados à mão, edite-os direto em vez de rodar o script.
* `monta_relatorio.py` — junta `docs/relatorio/partes/*.md`, os `tabela_verdade.md` e as figuras num `.docx` formatado (A4, margens 3/2 cm, sumário, legendas numeradas) e exporta o `.pdf` pelo LibreOffice.

Uso, na raiz do repositório:

```
python3 ferramentas/relatorio/monta_relatorio.py
```

Os diagramas em blocos são gerados com Graphviz: `dot -Tpng -Gdpi=180 docs/relatorio/figuras/visao_geral.dot -o docs/relatorio/figuras/visao_geral.png`.
