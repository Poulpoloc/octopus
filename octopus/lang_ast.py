class Expression:
    pass

class Var(Expression):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

class Int(Expression):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Plus(Expression):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return f"{self.left} + {self.right}"

class LetIn(Expression):
    def __init__(self, variable, expression, body):
        self.variable = variable
        self.expression = expression
        self.body = body

    def __str__(self):
        return f"let {self.variable} = {self.expression} in {self.body}"
