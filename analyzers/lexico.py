
import sys
sys.path.append("./test")

# import ply.lex as lex


class Lexico:
    line = 1
    column = ''

    delimiters = [ord(' '), ord('\n')]

    comment_status = [8, 15, 16]

    # TO DO: Add states of string like comment
    string_status = []

    tokens = []

    status = 0
    content = ""


    #
    #   RANGE AFD
    #       single-character: 1-50
    #       double-character: 51-100
    #       Number: 101-200
    #           Integer: 101-110
    #       Identyfying: 201-300
    #       String: 301-400
    #           With ": 301-310
    #           With ': 311-320
    #       Comments: 401-500
    #          Line: 401-410
    #          Block: 411-520
    #
    afd = {
        "STATUS_0": [
            {"target": 0, "char": "DELIMITER", "tot": None},
            {"target": 1, "char": "(", "tot": "OP_OPENPARENTHESIS"},
            {"target": 2, "char": ")", "tot": "OP_CLOSEPARENTHESIS"},
            {"target": 3, "char": "{", "tot": "OP_OPENBRACKET"},
            {"target": 4, "char": "}", "tot": "OP_CLOSEBRACKET"},
            {"target": 31, "char": "+", "tot": None},
            {"target": 32, "char": "&", "tot": None},
            {"target": 33, "char": "=", "tot": None},
            {"target": 8, "char": "/", "tot": None},
            {"target": 9, "char": "LETTER", "tot": None},
            {"target": 10, "char": "DIGIT", "tot": None},
        ],
        "STATUS_31": [
            {"target": 11, "char": "+", "tot": "OP_DOUBLEPLUS"},
            {"target": 12, "char": "DELIMITER", "tot": "OP_PLUS"}
        ],
        "STATUS_32": [
            {"target": 13, "char": "&", "tot": "OP_ANDAND"},
        ],
        "STATUS_33": [
            {"target": 14, "char": "=", "tot": "OP_DOUBLEEQUAL"},
        ],



        # Comment
        "STATUS_8": [
            {"target": 15, "char": "*", "tot": None},
        ],
        "STATUS_15": [
            {"target": 16, "char": "*", "tot": None},
            {"target": 15, "char": "O.C.", "tot": None},
        ],
        "STATUS_16": [
            {"target": 17, "char": "/", "tot": "COMMENT"},
            {"target": 15, "char": "DELIMITER", "tot": None},
        ],
        # End of comment



        # identifying
        "STATUS_9": [
            {"target": 9, "char": "LETTER", "tot": None},
            {"target": 9, "char": "DIGIT", "tot": None},
            {"target": 9, "char": "_", "tot": None},
            {"target": 17, "char": "DELIMITER", "tot": "IDENTIFYING"},
        ],

        # number
        "STATUS_10": [
            {"target": 10, "char": "DIGIT", "tot": None},
            {"target": 15, "char": "DELIMITER", "tot": "INTEGER"}
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
        transitions = self.afd["STATUS_" + str(self.status)]
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
        print('Error in line ' + str(self.line) +
              " and column " + str(len(self.column)))

    def already_in_symbol_table(self, id):
        return False

    def generate_token(self, transition):
        self.tokens.append((transition["tot"], self.content))

    def handle_char(self, c):
        self.handle_column(c)

        # Store the transition given c
        transition = self.get_transition(c)

        # If the transition doesn't exist then error and return 0 in order to stop the program
        if transition == None:
            self.print_error()
            return 0

        # If the afd must to read O.C or DELIMITER then we don't concatenate delimiters with exception of comment and string
        if (transition["char"] != "O.C." or transition["char"] != "DELIMITER") and ord(c) in self.delimiters:
            if self.status in self.comment_status or self.status in self.string_status:
                self.content = self.content + c
        else:
            self.content = self.content + c

        # if tot is None, then we go to the next status
        if transition["tot"] == None:
            self.status = transition["target"]
            return 1

        # We generate token with the exception of identifying
        if transition["tot"] == 'IDENTIFYING' and self.already_in_symbol_table(self.content):
            print("variable o PR ya existe")
        elif transition["tot"] == "COMMENT":
            print("Comment: No way. I can't generate a token with " + self.content)
        else:
            self.generate_token(transition)

        self.content = ''
        self.status = 0
        return 1

    def __init__(self, path):
        with open(path) as f:
            while True:
                c = f.read(1)
                if len(c) == 0 or self.handle_char(c) == 0:
                    break
            print(self.tokens)
            f.close()
