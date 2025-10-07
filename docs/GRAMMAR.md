# Gramática (EBNF)

PROGRAM        = { LINE } ;
LINE           = LPAREN STMT RPAREN ;

STMT           = IF_STMT
               | WHILE_STMT
               | REPEAT_STMT
               | RESREF
               | LOAD
               | STORE_STMT
               | RPN_EXPR ;

RPN_EXPR       = TERM TERM OP_ARITH ;

TERM           = INT | REAL | ID | RES | LOAD | SUBEXPR ;
SUBEXPR        = LPAREN STMT RPAREN ;

RESREF         = RES ;
STORE_STMT     = VALUE ID STORE ;
VALUE          = INT | REAL | ID | RES | LOAD | SUBEXPR ;

IF_STMT        = COND BLOCK BLOCK IF ;
WHILE_STMT     = COND BLOCK WHILE ;
REPEAT_STMT    = BLOCK COND UNTIL ;

BLOCK          = LPAREN STMT RPAREN { LPAREN STMT RPAREN } ;

COND           = TERM TERM OP_REL | TERM ;

OP_ARITH       = OP_ADD | OP_SUB | OP_MUL | OP_DIVR | OP_DIVI | OP_MOD | OP_POW ;
OP_REL         = OP_EQ | OP_NE | OP_LT | OP_GT | OP_LE | OP_GE ;

## Tokens esperados (tipo, lexema)
LPAREN "(" | RPAREN ")"
INT "42" | REAL "3.14" | ID "X"
OP_ADD "+" | OP_SUB "-" | OP_MUL "*" | OP_DIVR "|" | OP_DIVI "/" | OP_MOD "%" | OP_POW "^"
OP_EQ "==" | OP_NE "!=" | OP_LT "<" | OP_GT ">" | OP_LE "<=" | OP_GE ">="
RES "N" (único token com lex = N)
STORE "STORE"
LOAD "MEM" (único token com lex = nome da memória)
IF "IF" | WHILE "WHILE" | UNTIL "UNTIL"

## FIRST/FOLLOW e Tabela LL(1)
A gramática foi desenhada para ser LL(1) usando marcadores únicos (LOAD, STORE, RES) e sufixos-chave (IF/WHILE/UNTIL).