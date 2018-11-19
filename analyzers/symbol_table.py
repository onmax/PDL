from analyzers.lexico import Lexico as lex


class Symbol_Table:

    def get_displacement(self, typeid):
        if typeid == 'int':
            return 2
        elif typeid == 'bool':
            return 1
        elif typeid == 'string':
            return 16

    def add_var(self, id, typeid, value, displacement, current_table):
        row = {
            "id": id,
            "type": typeid,
            "lex": value,
            "displacement": displacement
        }
        self.tables[current_table].append(row)

    def add_fn(self, id, typeret, value, current_table):
        row = {
            "id": id,
            "type_ret": typeret,
            "nparam": 0,
            "type_param": [],
            "mode_param": [],
            "lex": value
        }
        self.tables[current_table].append(row)

    def separate_tokens(self):
        id = 1
        displacement = 0
        self.tables['global'] = []
        current_table = 'global'
        end_arg = False
        brackets_counter = 0
        for i,token in enumerate(lex.tokens):
            if current_table != 'global':
                if token[1] == ')':
                    end_arg = True
                    continue
                if token[1] == '{':
                    brackets_counter += 1
                if token[1] == '}':
                    brackets_counter -= 1
                if brackets_counter == 0 and end_arg:
                    current_table = 'global'
            if token[1] == 'var':
                self.add_var(id, lex.tokens[i + 1][1], lex.tokens[i + 2][1], displacement, current_table)
                displacement += self.get_displacement(lex.tokens[i + 1][1])
                id += 1
            if token[1] == 'function':
                self.add_fn(id, lex.tokens[i + 1][1], lex.tokens[i + 2][1], current_table)
                self.tables[lex.tokens[i + 2][1]] = []
                current_table = lex.tokens[i + 2][1]
                end_arg = False
                id += 1


    def __init__(self):
        self.tables = {}
        self.separate_tokens()
        print(self.tables)
