from abc import ABC

class Statement(ABC):
    pass

class Expression(ABC):
    pass

class DeclareVariable(Statement):
    identifier = None
    expression = Expression()

class Assignment(Statement):
    identifier = None
    expression = Expression()

class NumericValue(Expression):
    value = None