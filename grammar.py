from abc import ABC
from enum import Enum


class Statement(ABC):
    pass


class Expression(ABC):
    pass


class ArithmaticLogicOperands(Enum):
    Add = '+'
    Sub = '-'
    Mul = '*'
    Div = '/'


ArithmaticLogicOperands = Enum('ArithmaticLogicOperands', ['Add', 'Sub', 'Mul', 'Div'])

class LogicOperands(Enum):
    LessThan = '<'
    LessThanEqualTo = '<='
    GreaterThan = '>'
    GreaterThanEqualTo = '>='
    EqualTo = '=='

LogicOperands = Enum('LogicOperands', ['LessThan','LessThanEqualTo', 'GreaterThan', 'GreaterThanEqualTo', 'EqualTo'])

class Terminator(Expression):
    pass

class NumericValue(Expression):
    value = None


class StringValue(Expression):
    value = None

class AlphaNumericValue(Expression):
    value = None

class ArithmaticExpression(Expression):
    left = Expression()
    operand = ArithmaticLogicOperands
    right = Expression()

class LogicExpression(Expression):
    left = Expression()
    operand = ArithmaticLogicOperands
    right = Expression()

class DeclareIntVariable(Statement):
    identifier = None
    expression = Expression()
    terminator = Terminator()

class DeclareCharVariable(Statement):
    identifier = None
    expression = StringValue()
    terminator = Terminator()

class Assignment(Statement):
    identifier = None
    expression = Expression()

class Printf(Statement):
    expression = Expression()
    terminator = Terminator()

class StatementSequence(Statement):
    left = Statement()
    right = Statement()



