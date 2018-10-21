
import pprint

# import ply.lex as lex


class Lexico:
    pp = pprint.PrettyPrinter(indent=4)

    line = 1
    column = ''

    delimiters = [ord(' '), ord('\n'), ord('\t')]

    tokens = []

    status = 0
    content = ""

    afd_ranges = []

    #
    #   RANGE AFD
    #       undefined: > 1000:
    afd_ranges.append(('undefined', ({"start": 1000, "end": 99999})))
    #           1001: Starts with / and it can be division or comment
    #
    #       single-character: 1-50
    #       double-character: 51-100
    afd_ranges.append(('character', ({"start": 1, "end": 100})))
    #
    #       Number: 101-200
    #           Integer: 101-105
    afd_ranges.append(('integer', ({"start": 101, "end": 105})))
    #
    #       Identyfying: 201-300
    afd_ranges.append(('identyfying', ({"start": 201, "end": 300})))
    #
    #       String: 301-400
    #           With ": 301-310
    #           With ': 311-320
    afd_ranges.append(('string with "', ({"start": 301, "end": 310})))
    #
    #       Comments: 401-500
    #          Line: 401-410
    #          Block: 411-420
    afd_ranges.append(('line comment', ({"start": 401, "end": 410})))
    afd_ranges.append(('block comment', ({"start": 411, "end": 420})))
    #
    afd = {
        "STATUS_0": [
            {"target": 0, "char": "DELIMITER", "tot": None},
            {"target": 1, "char": "(", "tot": "OP_OPENPARENTHESIS"},
            {"target": 2, "char": ")", "tot": "OP_CLOSEPARENTHESIS"},
            {"target": 3, "char": "{", "tot": "OP_OPENBRACKET"},
            {"target": 4, "char": "}", "tot": "OP_CLOSEBRACKET"},
            {"target": 51, "char": "+", "tot": None},
            {"target": 52, "char": "&", "tot": None},
            {"target": 53, "char": "=", "tot": None},
            {"target": 1001, "char": "/", "tot": None},
            {"target": 201, "char": "LETTER", "tot": None},
            {"target": 101, "char": "DIGIT", "tot": None},
        ],
        "STATUS_51": [
            {"target": 54, "char": "+", "tot": "OP_DOUBLEPLUS"},
            {"target": 55, "char": "DELIMITER", "tot": "OP_PLUS"}
        ],
        "STATUS_52": [
            {"target": 56, "char": "&", "tot": "OP_ANDAND"},
        ],
        "STATUS_53": [
            {"target": 57, "char": "=", "tot": "OP_DOUBLEEQUAL"},
        ],



        # identifying
        "STATUS_201": [
            {"target": 201, "char": "LETTER", "tot": None},
            {"target": 201, "char": "DIGIT", "tot": None},
            {"target": 201, "char": "_", "tot": None},
            {"target": 202, "char": "DELIMITER", "tot": "IDENTIFYING"},
        ],

        # number
        "STATUS_101": [
            {"target": 101, "char": "DIGIT", "tot": None},
            {"target": 102, "char": "DELIMITER", "tot": "INTEGER"}
        ],



        # /
        "STATUS_1001": [
            {"target": 5, "char": "DELIMITER", "tot": "OP_DIVISION"},
            {"target": 401, "char": "/", "tot": None},  # Single line comment
            {"target": 411, "char": "*", "tot": None},  # Block comment
        ],


        # Line comment
        "STATUS_401": [
            {"target": 401, "char": "\n", "tot": "LINE COMMENT"},
            {"target": 401, "char": "O.C.", "tot": None},
        ],
        # End of line comment



        # Block comment
        "STATUS_411": [
            {"target": 412, "char": "*", "tot": None},
            {"target": 411, "char": "O.C.", "tot": None},
        ],
        "STATUS_412": [
            {"target": 413, "char": "/", "tot": "BLOCK COMMENT"},
            {"target": 411, "char": "DELIMITER", "tot": None},
        ],
        # End of block comment
    }

    def is_char(self, c):
        if c in ["DELIMITER", "DIGIT", "LETTER"]:
            return c
        else:
            return "CHARACTER"

    def get_range_name(self, status):
        for afd_range in self.afd_ranges:
            if status in range(afd_range[1]["start"], afd_range[1]["end"]):
                return afd_range[0]

    def init_transition_matrix(self):
        matrix = {}
        options = set()
        for status in self.afd:
            for transition in self.afd[status]:
                if status not in matrix:
                    matrix[status] = []
                if "STATUS_" + str(transition["target"]) not in matrix:
                    matrix["STATUS_" + str(transition["target"])] = []
                if [transition["char"]] not in matrix[status]:
                    matrix[status].append(
                        (transition["char"], transition["target"]))
                options.add(transition["char"])

        error_code = 1
        for option in options:
            for status in matrix:
                is_error = [item for item in matrix[status]
                            if option in item] == []
                if is_error:
                    matrix[status].append(
                        ('ERR', option, error_code))
                    error_code = error_code + 1
        with open("./res/transition_matrix.txt", "w") as fout:
            fout.write(pprint.pformat(matrix))

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
            if self.status > 300 and self.status <= 500:
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
        elif transition["tot"] in ["LINE COMMENT", "BLOCK COMMENT"]:
            if transition["tot"] == "LINE COMMENT":
                # Remove \n in line comment
                self.content = self.content[:-1]
            # print("Comment: No way. I can't generate a token with \n{0}\n".format(self.content))
        else:
            self.generate_token(transition)

        self.content = ''
        self.status = 0
        return 1

    def __init__(self, path):
        self.init_transition_matrix()
        with open("./res/afd.txt", "w") as fout:
            fout.write(pprint.pformat(self.afd))
        with open(path) as f:
            while True:
                c = f.read(1)
                if len(c) == 0 or self.handle_char(c) == 0:
                    break
        with open("./res/tokens_generated.txt", "w") as fout:
            fout.write(pprint.pformat(self.tokens))
