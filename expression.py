class Number:
    def __init__(self, value):
        self.value = value
    
    def evaluate(self):
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
    def evaluate(self):
        return sum(sub_expr.evaluate() for sub_expr in self.args)

class Minus(Arithmetic):
    def __init__(self, args):
        self.args = args
        self.symbol = "-"

    def evaluate(self):
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

    def evaluate(self):
        result = self.args[0].evaluate()
        for sub_expr in self.args[1:]:
            result = result / sub_expr.evaluate() # check if short hand is possible
        return result

class Multiply(Arithmetic):
    def __init__(self, args):
        self.args = args
        self.symbol = "*"
    
    def evaluate(self):
        result = 1
        for sub_expr in self.args:
            result = result * sub_expr.evaluate()

class Variable:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def evaluate(self):
        return value.evaluate()
    
    def __str__(self):
        return self.name

class If:
    def __init__(self, predicate, consequent, alternative):
        self.predicate = predicate
        self.consequent = consequent
        self.alternative = alternative

    def evaluate(self):
        if self.predicate.evaluate():
            return self.consequent.evaluate()
        return self.alternative.evaluate()
