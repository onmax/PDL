
import sys
sys.path.append('./test')
import test_lexico

import ply.lex as lex
import ply.yacc as yacc

class Lexico:

    afd = [
        {
            'STATUS_0': [
                {'target':'1','char':'(','tot':'op_openparentheses', 'must_generate_token': True},
                {'target':'1','char':')','tot':'op_closeparentheses', 'must_generate_token': True},
                {'target':'1','char':'(','tot':'op_openparentheses', 'must_generate_token': True},
                {'target':'1','char':'(','tot':'op_openparentheses', 'must_generate_token': True},
                {'target':'1','char':'(','tot':'op_openparentheses', 'must_generate_token': True},
            ]
        }
    ]

    def __init__(self, path):
        with open(path) as f:
            while True:
                if self.read_char(f.read(1)) == 0:
                    break
            f.close()

