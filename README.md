# Analisador Sintático RPN (Fase 2)

PONTIFÍCIA UNIVERSIDADE CATÓLICA DO PARANÁ - ESCOLA POLITÉCNICA  
ENGENHARIA DE COMPUTAÇÃO - LINGUAGENS FORMAIS E COMPILADORES  
RA2 - ANALISADOR LÉXICO  
PROFESSOR: Frank Coelho de Alcantara  
ALUNOS:  
- Gabriel Hess
- João Victor Roth Tozzo Alfredo
- Mariana Trentiny Barbosa
- Vitor Hugo Behlau Weber  
LINGUAGEM: Python


## Como executar

1. Python 3.10+
2. `pip install -r requirements.txt` (não há dependências externas; passo opcional)
3. Execute com arquivo de tokens JSONL:
python -m src.main tests/tokens_demo.jsonl

O programa lê um JSON Lines onde cada linha representa uma linha do programa já tokenizada pela Fase 1.


## Saídas

- AST completa do programa em `out/ast.json`
- Impressão textual da AST no console
- Gramática em `docs/GRAMMAR.md`
(Sem requirements.txt mesmo; é só para manter padrão.)


## Entrega
- Código-fonte em Python
- 3 arquivos de teste JSONL com 10+ linhas cada (válidos, controles e erros)
- AST em `out/ast.json`
- Gramática em `docs/GRAMMAR.md`
- Árvore de uma execução em `docs/AST_SAMPLE.md`


## Execução
./AnalisadorSintatico tests/tokens_ok_1.jsonl
./AnalisadorSintatico tests/tokens_ok_2_controls.jsonl
./AnalisadorSintatico tests/tokens_errados.jsonl


## Erros
Erros sintáticos são reportados com número da linha.
