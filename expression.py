class Arithmetic:
    def __init__(args):
        self.args = args

class Add(Arithmetic):
    def evaluate(self):
        return sum(sub_expr.evalute() for sub_expr in self.args)

class Minus(Arithmetic):
    def evaluate(self):
        result = self.args[0].evaluate()
        if len(self.args) == 1:
            return -result

        for sub_expr in self.args[1:]:
            result -= sub_expr.evalute()
        return result

class Divide(Arithmetic):
    def evaluate(self):
        result = self.args[0].evalute()
        for sub_expr in self.args[1:]:
            result = result / sub_expr.evaluate() # check if short hand is possible
        return result

class Multiply(Arithmetic):
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

class If:
    def __init__(self, predicate, consequent, alternative):
        self.predicate = predicate
        self.consequent = consequent
        self.alternative = alternative

    def evaluate(self):
        if self.predicate.evaluate():
            return self.consequent.evaluate()
        return self.alternative.evaluate()
