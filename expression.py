class Environment:
    def __init__(self, env={}, parent=None):
        self.env = env
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
    def __init__(self, name, args):
        self.args = args
        self.name = name
    
    def __str__(self):
        result = f"({self.name}"
        
        for arg in self.args:
            result += f" {str(arg.__str__())}"
        result += ")"
        return result

class Add(Arithmetic):
    def evaluate(self, local_frame):
        return sum(sub_expr.evaluate(local_frame) for sub_expr in self.args)

class Minus(Arithmetic):
    def evaluate(self, local_frame):
        result = self.args[0].evaluate(local_frame)
        if len(self.args) == 1:
            return -result

        for sub_expr in self.args[1:]:
            result -= sub_expr.evaluate(local_frame)
        return result

class Divide(Arithmetic):
    def evaluate(self, local_frame):
        result = self.args[0].evaluate(local_frame)
        for sub_expr in self.args[1:]:
            result = result / sub_expr.evaluate(local_frame) # check if short hand is possible
        return result

class Multiply(Arithmetic):
    def evaluate(self, local_frame):
        result = 1
        for sub_expr in self.args:
            result = result * sub_expr.evaluate(local_frame) 
        return result

class And(Arithmetic):
    def evaluate(self, local_frame):
        return all(expr.evaluate(local_frame) for expr in self.args)

class Or(Arithmetic):
    def evaluate(self, local_frame):
        return any(expr.evaluate(local_frame) for expr in self.args)

class If:
    def __init__(self, predicate, consequent, alternative):
        self.predicate = predicate
        self.consequent = consequent
        self.alternative = alternative

    def evaluate(self, local_frame):
        if self.predicate.evaluate(local_frame):
            return self.consequent.evaluate(local_frame)
        return self.alternative.evaluate(local_frame)

class Else:
    def evaluate(self, local_frame):
        return True

class Cond:
    def __init__(self, clauses):
        self.clauses = clauses

    def evaluate(self, local_frame):
        for predicate, expression in clauses:
            if predicate.expression.evaluate(local_frame):
                return expression.evaluate(local_frame)        

class Define_Var:
    def __init__(self, name, value, local_frame):
        self.name = name
        self.value = value

    def evaluate(self, local_frame):
        local_frame.add(self.name, self.value.evaluate(local_frame))

class Define_Lambda:
    def __init__(self, name, params, body, local_frame):
        self.name = name
        self.params = params
        self.body = body
    
    def create_lambda(self, name, args):
        return Lambda(name, args, self.params, self.body)

    def evaluate(self, local_frame):
        local_frame.add(self.name, self.create_lambda)

class Lambda:
    def __init__(self, name, args, params, body):
        self.name = name
        self.args = args
        self.params = params
        self.body = body

    def evaluate(self, local_frame):
        n = len(self.args)
        m = len(self.params)
        if n != m: 
            raise Exception(f"mismatched number of arguments for {self.name} call")
        
        function_frame = Environment({}, local_frame)
        for i in range(n):
            Define_Var(self.params[i], self.args[i], function_frame).evaluate(function_frame)
        return self.body.evaluate(function_frame)
        
    
class Variable:
    def __init__(self, name, local_frame):
        self.name = name

    def evaluate(self, local_frame):
        return local_frame.get(self.name)
    
    def __str__(self):
        return self.name

