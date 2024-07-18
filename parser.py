from constants import *

def parse(s, env):
    tokens = tokenify(s)
    expression, _ = parse_iter(tokens, env)
    return expression

def parse_iter(tokens, env):
    if tokens[0] != "(":
        raise Exception("expected open parantheses for expression")
    
    operator = tokens[1]
    if operator == "define":
        return parse_define(tokens, env)
    operands = tokens[2:]
    
    operator_class = env.get(operator)
    
    operands_expressions = []
    i = 0
    n = len(operands)
    while (i < n):
        token = operands[i]
        if token.isnumeric():
            sub_expr = Number(int(token))
            operands_expressions.append(sub_expr)
        elif token == "(":
            sub_expr, i = parse_iter(operands[i:], env)
            operands_expressions.append(sub_expr)
        elif token == ")":
            return operator_class(operator, operands_expressions), i
        else:
            sub_expr = Variable(token, env)
            operands_expressions.append(sub_expr)
        i += 1

def parse_define(tokens, env):
    if tokens[-1] != ")":
        raise Exception("missing closing parantheses")
    last_index = len(tokens)
    
    definition = tokens[2:-1]
    n = len(definition)
    if definition[0] == "(":
        name = definition[1]
        i = 2
        while (i < n):
            if definition[i] == ")":
                break
            i += 1

        params = definition[2: i]
        
        body, _ = parse_iter(definition[i+1:], env)
        return Define_Lambda(name, params, body, env), last_index
    else:
        remaining = definition[1:]
        if len(remaining) > 1:
            value = parse_iter(remaining, env)
        else: 
            value = Number(int(remaining[0])) 

        return Define_Var(definition[0], value, env), last_index

def tokenify(s):
    tokens = []
    current_token = ""

    for char in s:
        if char == "(" or char == ")":
            if current_token:
                tokens.append(current_token)
            tokens.append(char)
            current_token = ""   
        elif char.isspace():
            if current_token:
                tokens.append(current_token)
            current_token = ""
        else:
            current_token += char
    
    return tokens
        

