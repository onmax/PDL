
import sys
sys.path.append('./test')
import test_lexico

import ply.lex as lex
import ply.yacc as yacc


# initialize tokens
tokens = ["RESERVED_WORD", "STRING", "INTEGER", "OP_PLUS", "OP_DOUBLEPLUS", "OP_DOUBLEQUAL", "OP_ANDAND", 
    "OP_OPENBRACKETS","OP_CLOSEBRACKETS", "OP_OPENPARENTHESES","OP_CLOSEPARENTHESES"]

tokens_regex = {
    # Starts with a letter, then it can have 0 or more letters, digit or _
    'RESERVED_WORD': r"^[a-zA-Z][a-zA-Z0-9_]*$",
    #Any character between ""
    'STRING': r"^\"(.[^(\")]|(\\\")|(?:\s*))*\"$",
    # Must have at least one digit
    'INTEGER': r"^[0-9]+$",
    "OP_PLUS": r"^\+$",
    'OP_DOUBLEPLUS': r"^\+\+$",
    'OP_DOUBLEQUAL': r"^==$",
    'OP_ANDAND': r"^\&\&$",
    'OP_OPENBRACKETS': r"^\{$",
    'OP_CLOSEBRACKETS': r"^\}$",
    'OP_OPENPARENTHESES': r"^\($",
    'OP_CLOSEPARENTHESES': r"^\)$"
}

test_lexico.test_regex(tokens_regex)