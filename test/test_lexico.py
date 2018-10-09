import re

def test_regex(tokens):
    print('Comenzando test de expresiones regulares\n')

    tests = [
        #1-5
        test_regex_simple(tokens["RESERVED_WORD"], 'variable', True),                       
        test_regex_simple(tokens["RESERVED_WORD"], '2variable', False),                     
        test_regex_simple(tokens["RESERVED_WORD"], '2_variable', False),                    
        test_regex_simple(tokens["RESERVED_WORD"], '2', False),                             
        test_regex_simple(tokens["RESERVED_WORD"], '_variable', False),                     
        #6-10
        test_regex_simple(tokens["RESERVED_WORD"], 'VAR1', True),                           
        test_regex_simple(tokens["RESERVED_WORD"], 'VAR_1', True),                          
        test_regex_simple(tokens["RESERVED_WORD"], '&variable', False),                     
        test_regex_simple(tokens["RESERVED_WORD"], '', False),                              
        test_regex_simple(tokens["STRING"], '"Hola, esto es un string"', True),
        #11-15          
        test_regex_simple(tokens["STRING"], '"    Esto es un string    "', True),
        test_regex_simple(tokens["STRING"], 'No es un string"', False),                     
        test_regex_simple(tokens["STRING"], '"No es un string', False),                     
        test_regex_simple(tokens["STRING"], 'Tampoco es un string', False),                 
        test_regex_simple(tokens["STRING"], '"Esto deberia ser un error""', False),         
        test_regex_simple(tokens["STRING"], '"Esto deberia "ser un error"', False),         
        #16-20                  
        test_regex_simple(tokens["STRING"], '"Esto deberia " ser un error"', False),         
        test_regex_simple(tokens["STRING"], '"Y esto " tambien', False),                    
        test_regex_simple(tokens["STRING"], '"Y esto " tambien"', False),                    
        test_regex_simple(tokens["STRING"], '"Esto \\" esta bien"', True),                    
        test_regex_simple(tokens["STRING"], '', False),
        test_regex_simple(tokens["COMMENT"], '/*Esto es un comentario*/', True),
        test_regex_simple(tokens["COMMENT"], '/*Esto es * un comentario*/', True),
        test_regex_simple(tokens["COMMENT"], '/*No es un comentario*', False),
        #21-25                  
        test_regex_simple(tokens["OP_PLUS"], '+', True),                                    
        test_regex_simple(tokens["OP_PLUS"], '1+', False),                                  
        test_regex_simple(tokens["OP_PLUS"], '-', False),                                   
        test_regex_simple(tokens["OP_PLUS"], '12', False),    
        #26-30                  
    ]                             
   

    for i, test in enumerate(tests):
        print('Pasado test {0}: {1}'.format(i + 1, test))

# Check if regex is in the test_str and then checks if it should or not.
def test_regex_simple(regex, test_str, should_be):
    match = re.findall(regex, test_str, re.MULTILINE)
    if((len(match) != 0) != should_be):
        match = [i[0] for i in match]
        if '' not in match:  
            print('\tTest: {0}'.format(test_str))
            print('\tMatch: {0}\n'.format(match))
        else:
            return True
    return (len(match) != 0) == should_be