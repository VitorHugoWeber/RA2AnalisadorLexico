import json

class Token:
    __slots__ = ("type", "lex")
    def __init__(self, t, lex):
        self.type = t
        self.lex = str(lex)

def lerTokens(path):
    linhas = []
    with open(path, "r", encoding="utf-8") as f:
        for raw in f:
            if not raw.strip():
                continue
            arr = json.loads(raw)
            linha = [Token(t["type"], t.get("lex", "")) for t in arr]
            linhas.append(linha)
    return linhas