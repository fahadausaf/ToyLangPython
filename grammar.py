from abc import ABC
from enum import Enum


class Statement(ABC):
    pass

class Expression(ABC):
    pass


class ListOperand(Enum):
    Comma = ','

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
    NotEqualTo = '!='
    And = '&'

LogicOperands = Enum('LogicOperands', ['LessThan','LessThanEqualTo', 'GreaterThan', 'GreaterThanEqualTo', 'EqualTo', 'NotEqualTo', 'And'])

class UnaryOperands(Enum):
    Not = '!'
    Minus = '-'

UnaryOperands = Enum('UnaryOperands', ['Not', 'Minus'])

class EndFile(Expression):
    pass

class Terminator(Expression):
    pass

class NumericValue(Expression):
    value = None


class StringValue(Expression):
    value = None

class AlphaNumericValue(Expression):
    value = None

class VariableExpression(Expression):
    identifier = None

class ArithmaticExpression(Expression):
    left = Expression()
    operand = ArithmaticLogicOperands
    right = Expression()

class LogicExpression(Expression):
    left = Expression()
    operand = ArithmaticLogicOperands
    right = Expression()

class UnaryExpression(Expression):
    operand = UnaryOperands
    expression = Expression()

class DeclareIntVariable(Statement):
    identifier = None
    expression = Expression()

class DeclareCharVariable(Statement):
    identifier = None
    expression = StringValue()

class FunctionDefinition(Statement):
    identifier = None
    parameterList = None
    functionBody = Statement()

class FunDefinition(Statement):
    identifier = None
    parameterList = None
    functionBody = Statement()

class Assignment(Statement):
    identifier = None
    expression = Expression()
    terminator = Terminator()

class Printf(Statement):
    expression = Expression()
    terminator = Terminator()

class StatementSequence(Statement):
    left = Statement()
    right = Statement()

class IfThenElse(Statement):
    ifCondition = Expression()
    thenStatement = Statement()
    elseStatement = None

class ListTail(Statement):
    comma = ListOperand.Comma
    list = Expression()

class List(Statement):
    head = Expression()
    tail = ListTail()



