
import sys
sys.path.append("./test")

import ply.lex as lex
import ply.yacc as yacc

class Lexico:
    line = 1
    column = ''

    delimiters = [ord(' '), ord('\n')]

    comment_status = [8, 15, 16]

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
            {"target":"9","char":"LETTER","tot":None},
            {"target":"9","char":"DIGIT","tot":None},
            {"target":"9","char":"_","tot": None},
            {"target":"17","char":"DELIMITER","tot":"IDENTIFYING"},
        ],

        # number
        "STATUS_10": [
            {"target":"10","char":"DIGIT","tot": None},
            {"target":"15","char":"DELIMITER","tot":"INTEGER"}
        ]
    }

    def handle_column(self, c):
        if len(c) == 0:
            return 0

        if ord(c) == ord('\n'):
            self.line = self.line + 1    
            self.column = ''
        else:
            self.column = self.column + c

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

    def already_in_symbol_table(self, id):
        return True

    def generate_token(self):
        print("GENERAR TOKEN: " + self.content)


    def handle_char(self, c):
        if len(c) == 0:
            return 0
        self.handle_column(c)
        transition = self.get_transition(c)
        if transition == None:
            self.print_error()
            return 0
        if transition["char"] != "O.C." or transition["char"] != "DELIMITER":
            if ord(c) != ord(' ') and ord(c) != ord('\n') or self.status in self.comment_status:
                self.content = self.content + c

        else:
            self.content = ''
        
        
        if transition["tot"] != None:
            if transition["tot"] == 'IDENTIFYING' and not self.already_in_symbol_table(self.content):
                print("variable o PR ya existe")
            else:
                self.generate_token()
            self.content = ''
            self.status = '0'
        else:
            self.status = transition["target"]
        return 1
        
        
        

    def __init__(self, path):
        with open(path) as f:
            while True:
                if self.handle_char(f.read(1)) == 0:
                    break
            f.close()

