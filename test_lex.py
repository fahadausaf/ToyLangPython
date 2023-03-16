import unittest
from lex import *
from tokenList import *

file_test_01 = 'input\\test_lex\\test_01_int_01.d'
# tokenList = lex(fileName)

class TestVerifyLexer(unittest.TestCase):
    def test_01_int(self):
        expected = [(1,1, KeywordTokens.INT)]
        actual = lex(file_test_01)
        self.assertEqual(actual, expected)

if __name__ == '__main--':
    unittest.main()