from constants import *

def parse(s):
    tokens = tokenify(s)
    expression, _ = parse_iter(tokens)
    return expression

def parse_iter(tokens):
    if tokens[0] != "(":
        raise Exception("expected open parantheses for expression")
    
    operator = tokens[1]
    operands = tokens[2:]
    
    operator_class = special[operator]
    
    operands_expressions = []
    i = 0
    n = len(operands)
    while (i < n):
        token = operands[i]
        if token.isnumeric():
            sub_expr = Number(int(token))
            operands_expressions.append(sub_expr)
        elif token == "(":
            sub_expr, i = parse_iter(operands[i:])
            operands_expressions.append(sub_expr)
        elif token == ")":
            return operator_class(operands_expressions), i
        else:
            sub_expr = Variable(token, 0)
            operands_expressions.append(sub_expr)
        i += 1


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
        

