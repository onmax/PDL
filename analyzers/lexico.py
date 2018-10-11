
import sys
sys.path.append("./test")

import ply.lex as lex
import ply.yacc as yacc

class Lexico:
    line = 1
    column = ''

    delimiters = [ord(' '), ord('\n')]

    status = "0"
    content = ""

    afd = {
        "STATUS_0": [
            {"target":"0","char":"DELIMITER","tot": None},
            {"target":"1","char":"(","tot":"OP_OPENPARENTHESIS"},
            {"target":"2","char":")","tot":"OP_CLOSEPARENTHESIS"},
            {"target":"3","char":"{","tot":"OP_OPENBRACKET"},
            {"target":"4","char":"}","tot":"OP_CLOSEBRACKET"},
            {"target":"5","char":"+","tot": None},
            {"target":"6","char":"&","tot": None},
            {"target":"7","char":"=","tot": None},
            {"target":"8","char":"/","tot": None},
            {"target":"9","char": "LETTER", "tot": None},
            {"target":"10","char":"DIGIT","tot":None},
        ],
        "STATUS_5": [
            {"target":"11","char":"+","tot":"OP_DOUBLEPLUS"},
            {"target":"12","char":"DELIMITER","tot":"OP_PLUS"} 
        ],
        "STATUS_6": [
            {"target":"13","char":"&","tot":"OP_ANDAND"},
        ],
        "STATUS_7": [
            {"target":"14","char":"=","tot":"OP_DOUBLEEQUAL"},
        ],


        
        # Comment
        "STATUS_8": [
            {"target":"15","char":"*","tot": None},
        ],
        "STATUS_15": [
            {"target":"16","char":"*","tot": None},
            {"target":"15","char":"O.C.","tot": None},
        ],
        "STATUS_16": [
            {"target":"17","char":"/","tot":"COMMENT"},
            {"target":"15","char":"O.C.","tot": None},
        ],
        # End of comment



        # identifying
        "STATUS_9": [
            {"target":"15","char":"LETTER","tot":None},
            {"target":"15","char":"DIGIT","tot":None},
            {"target":"15","char":"_","tot": None},
            {"target":"17","char":"O.C.","tot":"IDENTIFYING"},
        ],

        # number
        "STATUS_10": [
            {"target":"10","char":"DIGIT","tot": None},
            {"target":"15","char":"O.C.","tot":"INTEGER", "is_final": True}
        ]
    }

    def handle_column(self, c):
        if ord(c) == ord('\n'):
            self.line = self.line + 1    
            self.column = ''
        else:
            self.column = self.column + c

    def is_delimiter(self, c):
        return ord(c) in self.delimiters

    def get_transition(self, c):
        transitions = self.afd["STATUS_" + self.status]
        transition = None
        for _transition in transitions:
            char = _transition["char"]
            if (char == "DELIMITER" and ord(c) in self.delimiters
            or char == "DIGIT" and c.isdigit()
            or char == "LETTER" and c.isalpha()
            or char == "O.C."
            or char == c):
                transition = _transition
                break
        return transition

    def print_error(self):
        print(self.column)
        print((len(self.column) - 1) * ' ' + '^')
        print('Error in line ' + str(self.line) + " and column " + str(len(self.column)))

    def generate_token(self):
        print("GENERAR TOKEN")

    def handle_char(self, c):
        self.handle_column(c)
        transition = self.get_transition(c)
        if transition == None:
            self.print_error()
            return 0
        if transition["char"] != "O.C.":
            self.content = self.content + c
        
        if transition["tot"] != None:
            if transition["tot"] == ''
            self.generate_token()
        
        

    def __init__(self, path):
        with open(path) as f:
            while True:
                if self.handle_char(f.read(1)) == 0:
                    break
            f.close()

