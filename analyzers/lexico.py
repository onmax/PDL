
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
            {"target":"0","char":"DELIMITER","tot": None, "is_final": False},
            {"target":"1","char":"(","tot":"op_openparentheses"},
            {"target":"2","char":")","tot":"op_closeparentheses"},
            {"target":"3","char":"{","tot":"op_openbracket"},
            {"target":"4","char":"}","tot":"op_closebracket"},
            {"target":"5","char":"+","tot": None, "is_final": False},
            {"target":"6","char":"&","tot": None, "is_final": False},
            {"target":"7","char":"=","tot":"op_doubleequal", "is_final": False},
            {"target":"8","char":"/","tot":"comment", "is_final": False},
            {"target":"9","char": "LETTER", "tot":"identifying", "is_final": False},
            {"target":"10","char":"DIGIT","tot":"integer", "is_final": False},
        ],
        "STATUS_5": [
            {"target":"11","char":"+","tot":"op_doubleplus"},
            {"target":"12","char":"DELIMITER","tot":"op_plus"} 
        ],
        "STATUS_6": [
            {"target":"13","char":"&","tot":"op_andand"},
        ],
        "STATUS_7": [
            {"target":"14","char":"=","tot":"op_doubleequal"},
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
            {"target":"17","char":"/","tot":"comment"},
            {"target":"15","char":"O.C.","tot": None},
        ],
        # End of comment



        # identifying
        "STATUS_9": [
            {"target":"15","char":"LETTER","tot":"identifying", "is_final": False},
            {"target":"15","char":"DIGIT","tot":"identifying", "is_final": False},
            {"target":"15","char":"_","tot":"identifying", "is_final": False},
            {"target":"17","char":"O.C.","tot":"identifying", "is_final": True},
        ],

        # number
        "STATUS_10": [
            {"target":"10","char":"DIGIT","tot":"integer", "is_final": False},
            {"target":"15","char":"O.C.","tot":"integer", "is_final": True}
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
        
        if transition["is_final"]:
            self.generate_token()
        
        

    def __init__(self, path):
        with open(path) as f:
            while True:
                if self.handle_char(f.read(1)) == 0:
                    break
            f.close()

