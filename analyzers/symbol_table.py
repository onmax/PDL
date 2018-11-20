import pprint
from colorama import init
from termcolor import colored
init()

import csv

from analyzers.lexico import Lexico as lex


class Symbol_Table:
    pp = pprint.PrettyPrinter(indent=4)

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
            "displacement": displacement,
            "var": True
        }
        self.tables[current_table].append(row)

    def add_fn(self, id, typeret, value, current_table):
        row = {
            "id": id,
            "type_ret": typeret,
            "nparam": 0,
            "type_param": [],
            "mode_param": [],
            "lex": value,
            "var": False
        }
        self.tables[current_table].append(row)

    def separate_tokens(self):
        id = {'global':1}
        displacement = {'global':0}
        current_table = 'global'
        self.tables[current_table] = []
        end_arg = False
        start_arg = False
        type_param = []
        brackets_counter = 0
        for i,token in enumerate(lex.tokens):
            if current_table != 'global':
                if start_arg:
                    if token[1] in ['int', 'bool', 'string']:
                        type_param.append(lex.tokens[i][1])
                        self.add_var(id[current_table], lex.tokens[i][1], lex.tokens[i + 1][1], displacement[current_table], current_table)
                        id[current_table] += 1
                        displacement[current_table] += self.get_displacement(lex.tokens[i][1])
                if token[1] == '(':
                    start_arg = True
                if token[1] == ')':
                    self.tables['global'][-1]['type_param'] = type_param
                    self.tables['global'][-1]['nparam'] = len(type_param)
                    type_param = []
                    end_arg = True
                    start_arg = False
                if token[1] == '{':
                    brackets_counter += 1
                if token[1] == '}':
                    brackets_counter -= 1
                if brackets_counter == 0 and end_arg:
                    current_table = 'global'
            if token[1] == 'var':
                self.add_var(id[current_table], lex.tokens[i + 1][1], lex.tokens[i + 2][1], displacement[current_table], current_table)
                displacement[current_table] += self.get_displacement(lex.tokens[i + 1][1])
                id[current_table] += 1
            if token[1] == 'function':
                self.add_fn(id[current_table], lex.tokens[i + 1][1], lex.tokens[i + 2][1], current_table)
                id[current_table] += 1
                self.tables[lex.tokens[i + 2][1]] = []
                current_table = lex.tokens[i + 2][1]
                displacement[current_table] = 0
                end_arg = False
                id[current_table] = 1


    def __init__(self):
        self.tables = {}
        self.separate_tokens()
        print('Generated ' + colored('{0} tables of symbols',
                                    'grey', 'on_blue').format(len(self.tables)))
        for table in self.tables:
            with open("./res/symbol_tables/" + table + ".txt" , "w+") as fout:
                fout.write(pprint.pformat(self.tables[table]))

            with open("./res/symbol_tables/" + table + ".csv" , "w+") as csvfile:
                filewriter = csv.writer(csvfile, delimiter=',', quotechar=',',
                            quoting=csv.QUOTE_MINIMAL)
                filewriter.writerow(['id','tipo','lexema','desplazamiento','tipo retorno','nparam','tipos parametros','modo parametros'])
                for row in self.tables[table]:
                    if row["var"]:
                        filewriter.writerow([row["id"],row["type"],row["lex"],row["displacement"], '-', '-', '-', '-'])
                    else:
                        filewriter.writerow([row["id"],'-', row["lex"], '-',row["type_ret"],row["nparam"],','.join(row["type_param"]), ','.join(row["mode_param"])])


