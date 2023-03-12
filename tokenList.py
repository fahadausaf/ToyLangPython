from enum import Enum

class Tokens(Enum):
    ADD = '+'
    SUBTRACT = '-'
    MULTIPLY = '*'
    DIVIDE = '/'
    TERMINATOR = ';'
    ASSIGNMENT = '='
    EQUAL_TO = '=='
    LESS_THAN = '<'
    GREATER_THAN = '>'
    COMMA = ','
    OPEN_PAREN = '('
    CLOSE_PAREN = ')'
    OPEN_BRAC = '['
    CLOSE_BRAC = ']'