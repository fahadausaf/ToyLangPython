from enum import Enum

class Tokens(Enum):
    pass

class LiteralTokens():
    pass

class VariableLiteralToken(LiteralTokens):
    value = None

class StringLiteralToken(LiteralTokens):
    value = None

class NumericLiteralToken(LiteralTokens):
    value = None

class ArithmaticTokens(Enum):
    ADD = '+'
    SUBTRACT = '-'
    MULTIPLY = '*'
    DIVIDE = '/'
    

class LogicTokens(Tokens):
    EQUAL_TO = '=='
    LESS_THAN = '<'
    LESS_THAN_EQUAL_TO = '<='
    GREATER_THAN = '>'
    GREATER_THAN_EQUAL_TO = '>='

class ExpressionTokens(Tokens):
    TERMINATOR = ';'
    ASSIGNMENT = '='
    COMMA = ','
    OPEN_PAREN = '('
    CLOSE_PAREN = ')'
    OPEN_BRAC = '['
    CLOSE_BRAC = ']'

class KeywordTokens(Tokens):
    INT = 'int'
    CHAR = 'char'
    PRINT = 'printf'