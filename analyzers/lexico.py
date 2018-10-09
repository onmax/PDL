
import sys
sys.path.append('./test')
import test_lexico

import ply.lex as lex
import ply.yacc as yacc

class Lexico:
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
        'COMMENT': r"^\/\*.*\*\/$",
        "OP_PLUS": r"^\+$",
        'OP_DOUBLEPLUS': r"^\+\+$",
        'OP_DOUBLEQUAL': r"^==$",
        'OP_ANDAND': r"^\&\&$",
        'OP_OPENBRACKETS': r"^\{$",
        'OP_CLOSEBRACKETS': r"^\}$",
        'OP_OPENPARENTHESES': r"^\($",
        'OP_CLOSEPARENTHESES': r"^\)$"
    }
    #test_lexico.test_regex(tokens_regex)


    def __init__(self, path):
        self.transitions_from_0 = [
            {'key':'(', 'value':1},
            {'key':')', 'value':2},
            {'key':'{', 'value':3},
            {'key':'}', 'value':4},
            {'key':'+', 'value':5},
            {'key':'&', 'value':6},
            {'key':'=', 'value':7},
            {'key':'/', 'value':8}
        ]     
        # Contains the string of the token
        self.current = ''

        # Contains the status of the analyzer
        self.status = 0

        # list of status where it can exists blank
        self.can_have_blanks = ['COMMENT', 'STRING']

        with open(path) as f:
            while True:
                if self.read_char(f.read(1)) == 0:
                    break
            f.close()


    # Returns boolean if c is a delimiter
    def is_delimiter(self, c):
        delimiters = [ord(' '), ord('\n')]
        return ord(c) in delimiters


    def read_char(self, c):
        if not c:
            return 0
        if self.is_delimiter(c) and False:
            self.status = 0
        else:
            if self.status == 0:
                self.status0(c)
            elif self.status == 5:
                self.status5(c)
            elif self.status == 6:
                self.status6(c)
            elif self.status == 7:
                self.status7(c)
            elif self.status == 8:
                self.status8(c)
            elif self.status == 9:
                self.status9(c)
            elif self.status == 15:
                self.status15(c)
            elif self.status == 16:
                self.status16(c)

        self.current = self.current + c

      
    def status0(self, c):
        if c.isalpha():
            self.status = 9
        elif c.isdigit():
            self.status = 10
        else:
            for transition in self.transitions_from_0:
                if transition['key'] == c:
                    self.status = transition['value']

    def status5(self, c):
        if c == '+':
            print('doble mas')
            self.current = ''
            print('DOBLE MAS, GENERA TOKEN')
        else:
            print('ERROR HAY + CON ALGUN OTRO CARACTER Y ESO NO NOS GUSTA')
    
    def status6(self, c):
        if c == '&':
            self.current = ''
            print('&&, GENERA TOKEN')
        #No se que hay que hacer si recibimos otro caracter, supongo que error
    
    def status7(self, c):
        if c == '=':
            self.current = ''
            print('&&, GENERA TOKEN')
        #No se que hay que hacer si recibimos otro caracter, supongo que error

    
    # En este estado see debería leer el * perteneciente al comentario
    def status8(self, c):
        if c == '*':
            self.status = 15
        #No se que hay que hacer si recibimos otro caracter, supongo que error

    def status9(self, c):
        if not c.isalpha() and not c.isdigit() and ord(c) != ord('_'):
            print(self.current, ': PALABRA GENERA TOKEN')
            self.current = ''

    def status15(self, c):
        if c == '*':
            self.status = 16
    
    def status16(self, c):
        if c == '/':
            # Fin del comentario
            self.status = 0

        
    