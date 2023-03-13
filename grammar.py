from abc import ABC
from enum import Enum

class Statement(ABC):
    pass

class Expression(ABC):
    pass

class ArithmaticOperands(Enum):
    Add = '+'
    Sub = '-'
    Mul = '*'
    Div = '/'

ArithmaticOperands = Enum('ArithmaticOperands', ['Add', 'Sub', 'Mul', 'Div'])

class Terminator(Expression):
    pass

class DeclareVariable(Statement):
    identifier = None
    expression = Expression()
    terminator = Terminator()

class Assignment(Statement):
    identifier = None
    expression = Expression()

class StatementSequence(Statement):
    left = Statement()
    right = Statement()

class NumericValue(Expression):
    value = None

class ArithmaticExpression(Expression):
    left = Expression()
    operand = ArithmaticOperands
    right = Expression()
