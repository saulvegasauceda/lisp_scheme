class Environment:
    def __init__(self, parent=None):
        self.env = {}
        self.parent = parent
    
    def get(self, name):
        data = self.env.get(name, False)
        if data:
            return data
        else:
            if self.parent:
                return self.parent.get(name)
            else:
                raise Exception(f"{name} not found in scope")
    
    def add(self, name, data):
        self.env[name] = data

class Number:
    def __init__(self, value):
        self.value = value
    
    def evaluate(self, local_frame):
        return self.value
    
    def __str__(self):
        return self.value

class Arithmetic:
    def __init__(self, args):
        self.args = args
        self.symbol = None

    def __str__(self):
        result = f"({self.symbol}"
        
        for arg in self.args:
            result += f" {str(arg.__str__())}"
        result += ")"
        return result

class Add(Arithmetic):
    def __init__(self, args):
        self.args = args
        self.symbol = "+" 
    def evaluate(self, local_frame):
        return sum(sub_expr.evaluate() for sub_expr in self.args)

class Minus(Arithmetic):
    def __init__(self, args):
        self.args = args
        self.symbol = "-"

    def evaluate(self, local_frame):
        result = self.args[0].evaluate()
        if len(self.args) == 1:
            return -result

        for sub_expr in self.args[1:]:
            result -= sub_expr.evaluate()
        return result

class Divide(Arithmetic):
    def __init__(self, args):
        self.args = args
        self.symbol = "/"

    def evaluate(self, local_frame):
        result = self.args[0].evaluate()
        for sub_expr in self.args[1:]:
            result = result / sub_expr.evaluate() # check if short hand is possible
        return result

class Multiply(Arithmetic):
    def __init__(self, args):
        self.args = args
        self.symbol = "*"
    
    def evaluate(self, local_frame):
        result = 1
        for sub_expr in self.args:
            result = result * sub_expr.evaluate()

class If:
    def __init__(self, predicate, consequent, alternative):
        self.predicate = predicate
        self.consequent = consequent
        self.alternative = alternative

    def evaluate(self, local_frame):
        if self.predicate.evaluate():
            return self.consequent.evaluate()
        return self.alternative.evaluate()

class Else:
    def evaluate(self, local_frame):
        return True

class Cond:
    def __init__(self, clauses):
        self.clauses = clauses

    def evaluate(self, local_frame):
        for predicate, expression in clauses:
            if predicate.expression.evaluate():
                return expression.evaluate()        

class And:
    def __init__(self, expressions):
        self.expressions = expressions

    def evaluate(self, local_frame):
        return all(expr.evaluate() for expr in self.expressions)

class Or:
    def __init__(self, expressions):
        self.expressions = expressions

    def evaluate(self, local_frame):
        return any(expr.evaluate() for expr in self.expressions)

class Define_Var:
    def __init__(self, name, value, local_frame):
        self.name = name
        self.value = value

        local_frame.add(name) = self.value.evaluate()

class Define_Lambda:
    def __init__(self, name, params, body, local_frame):
        self.name = name
        self.params = params
        self.body = body

        local_frame.add(name) = self

class Lambda:
    def __init__(self, name, args):
        self.name = name
        self.args = args

    def evaluate(self, local_frame):
        procedure = local_frame.get(self.name)
        
        n = len(self.args)
        m = len(procedure.params)
        if n != m: 
            raise Exception(f"mismatched number of arguments for {self.name} call")
        
        function_frame = Environment(local_frame)
        for i in range(n):
            Define_Var(params[i], self.args[i], function_frame)

        return procedure.body.evaluate(local_frame)
        
    
class Variable:
    def __init__(self, name, local_frame):
        self.name = name
        self.value = local_frame.get(name)

    def evaluate(self, local_frame):
        return self.value
    
    def __str__(self):
        return self.name

