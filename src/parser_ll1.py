from typing import List
from .tokens import Token
from .astnodes import ASTNode

ARITH = {"OP_ADD", "OP_SUB", "OP_MUL", "OP_DIVR", "OP_DIVI", "OP_MOD", "OP_POW"}
REL = {"OP_EQ", "OP_NE", "OP_LT", "OP_GT", "OP_LE", "OP_GE"}

class Parser:
    def __init__(self, linha_tokens: List[Token]):
        self.toks = linha_tokens
        self.i = 0

    def la(self, k=0):
        j = self.i + k
        if j < 0 or j >= len(self.toks):
            return None
        return self.toks[j]

    def consume(self, expected_type=None):
        t = self.la(0)
        if t is None:
            raise SyntaxError("fim inesperado")
        if expected_type and t.type != expected_type:
            raise SyntaxError(f"esperado {expected_type}, encontrado {t.type}")
        self.i += 1
        return t

    def expect(self, ttype):
        return self.consume(ttype)

    def parse_line(self) -> ASTNode:
        self.expect("LPAREN")
        node = self.parse_stmt()
        self.expect("RPAREN")
        if self.i != len(self.toks):
            raise SyntaxError("tokens extras após RPAREN")
        return ASTNode("Line", None, [node])

    def last_token_type_before_final_rparen(self):
        if not self.toks or self.toks[-1].type != "RPAREN":
            return None
        for j in range(len(self.toks) - 2, -1, -1):
            if self.toks[j].type == "RPAREN":
                break
            return self.toks[j].type
        return None

    def parse_stmt(self) -> ASTNode:
        t = self.la(0)
        if t is None:
            raise SyntaxError("linha vazia")
        suf = self.last_token_type_before_final_rparen()
        if suf == "IF":
            return self.parse_if_stmt()
        if suf == "WHILE":
            return self.parse_while_stmt()
        if suf == "UNTIL":
            return self.parse_repeat_stmt()
        if t.type == "RES":
            return self.parse_resref()
        if t.type == "LOAD":
            return self.parse_load()
        if self.is_store_ahead():
            return self.parse_store()
        return self.parse_rpn_expr()

    def parse_rpn_expr(self) -> ASTNode:
        left = self.parse_term()
        right = self.parse_term()
        op = self.la(0)
        if op is None or op.type not in ARITH:
            raise SyntaxError("operador aritmético esperado")
        self.consume()
        return ASTNode("Binary", op.lex, [left, right])

    def parse_term(self) -> ASTNode:
        t = self.la(0)
        if t is None:
            raise SyntaxError("termo esperado")
        if t.type in ("INT", "REAL", "ID"):
            self.consume()
            return ASTNode("Atom", t.lex)
        if t.type == "RES":
            return self.parse_resref()
        if t.type == "LOAD":
            return self.parse_load()
        if t.type == "LPAREN":
            return self.parse_subexpr()
        raise SyntaxError("termo inválido")

    def parse_subexpr(self) -> ASTNode:
        self.expect("LPAREN")
        inner = self.parse_stmt()
        self.expect("RPAREN")
        return ASTNode("Subexpr", None, [inner])

    def parse_resref(self) -> ASTNode:
        n = self.consume("RES")
        return ASTNode("ResRef", n.lex)

    def parse_load(self) -> ASTNode:
        m = self.consume("LOAD")
        return ASTNode("Load", m.lex)

    def is_store_ahead(self) -> bool:
        a = self.la(0)
        b = self.la(1)
        c = self.la(2)
        return a is not None and b is not None and c is not None and b.type == "ID" and c.type == "STORE"

    def parse_store(self) -> ASTNode:
        val = self.parse_value()
        mem = self.consume("ID")
        self.expect("STORE")
        return ASTNode("Store", None, [val, ASTNode("Mem", mem.lex)])

    def parse_value(self) -> ASTNode:
        t = self.la(0)
        if t is None:
            raise SyntaxError("valor esperado")
        if t.type in ("INT", "REAL", "ID"):
            self.consume()
            return ASTNode("Atom", t.lex)
        if t.type == "RES":
            return self.parse_resref()
        if t.type == "LOAD":
            return self.parse_load()
        if t.type == "LPAREN":
            return self.parse_subexpr()
        raise SyntaxError("valor inválido")

    def parse_if_stmt(self) -> ASTNode:
        cond = self.parse_cond()
        blk_t = self.parse_block()
        blk_f = self.parse_block()
        self.expect("IF")
        return ASTNode("If", None, [cond, blk_t, blk_f])

    def parse_while_stmt(self) -> ASTNode:
        cond = self.parse_cond()
        blk = self.parse_block()
        self.expect("WHILE")
        return ASTNode("While", None, [cond, blk])

    def parse_repeat_stmt(self) -> ASTNode:
        blk = self.parse_block()
        cond = self.parse_cond()
        self.expect("UNTIL")
        return ASTNode("RepeatUntil", None, [blk, cond])

    def parse_block(self) -> ASTNode:
        items = []
        if self.la(0) is None or self.la(0).type != "LPAREN":
            raise SyntaxError("bloco esperado")
        self.expect("LPAREN")
        items.append(self.parse_stmt())
        self.expect("RPAREN")
        while True:
            if self.la(0) is None or self.la(0).type != "LPAREN":
                break
            self.expect("LPAREN")
            items.append(self.parse_stmt())
            self.expect("RPAREN")
        return ASTNode("Block", None, items)

    def parse_cond(self) -> ASTNode:
        a = self.parse_term()
        b = self.la(0)
        if b is None:
            return ASTNode("Cond", None, [a])
        if b.type in ("INT", "REAL", "ID", "RES", "LOAD", "LPAREN"):
            right = self.parse_term()
            op = self.la(0)
            if op is None or op.type not in REL:
                raise SyntaxError("operador relacional esperado")
            self.consume()
            return ASTNode("Rel", op.lex, [a, right])
        return ASTNode("Cond", None, [a])