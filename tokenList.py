from enum import Enum


class Token():
    token = None
    lineNo = None
    charNo = None

class LiteralTokens():
    pass

# End of File token
class EOF(LiteralTokens):
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
    

class LogicTokens(Enum):
    NOT = '!'
    EQUAL_TO = '=='
    NOT_EQUAL_TO = '!='
    LESS_THAN = '<'
    LESS_THAN_EQUAL_TO = '<='
    GREATER_THAN = '>'
    GREATER_THAN_EQUAL_TO = '>='

class ExpressionTokens(Enum):
    TERMINATOR = ';'
    ASSIGNMENT = '='
    COMMA = ','
    OPEN_PAREN = '('
    CLOSE_PAREN = ')'
    OPEN_BRAC = '['
    CLOSE_BRAC = ']'
    OPEN_CURLY_BRAC = '{'
    CLOSE_CURLY_BRAC = '}'

class KeywordTokens(Enum):
    INT = 'int'
    CHAR = 'char'
    PRINTF = 'printf'
    IF = 'if'
    THEN = 'then'
    ELSE = 'else'
    ENDIF = 'endif'
    FUNCTION = 'function'