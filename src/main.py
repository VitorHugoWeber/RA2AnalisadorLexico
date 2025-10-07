import os, sys, json
from .tokens import lerTokens
from .grammar import construirGramatica
from .parser_ll1 import Parser

def pp(node, indent=0):
    pad = "  " * indent
    s = f"{pad}{node.kind}"
    if node.value is not None:
        s += f"({node.value})"
    print(s)
    for ch in node.children:
        pp(ch, indent + 1)

def main():
    if len(sys.argv) < 2:
        print("uso: python -m src.main tests/tokens_demo.jsonl")
        sys.exit(1)
    path = sys.argv[1]
    linhas = lerTokens(path)
    _g = construirGramatica()
    ast_program = []
    ok = True
    for idx, linha in enumerate(linhas, start=1):
        try:
            p = Parser(linha)
            ast = p.parse_line()
            ast_program.append(ast)
        except Exception as e:
            ok = False
            print(f"erro sintático na linha {idx}: {e}")
    if not os.path.isdir("out"):
        os.makedirs("out", exist_ok=True)
    with open("out/ast.json", "w", encoding="utf-8") as f:
        json.dump([n.to_dict() for n in ast_program], f, ensure_ascii=False, indent=2)
    for n in ast_program:
        pp(n)
    sys.exit(0 if ok else 2)

if __name__ == "__main__":
    main()