"""
Run the tests by executing:
$ pwd
AmE-dictionary/tools
$ python -m unittest -v test_checker
"""

import unittest
from checker import Checker

class Test_Checker(unittest.TestCase):

    def test_GivenAnEmptyDictionary_When_Checker_ThenExceptionIsRaised(self):
        DICTIONARY = ''
        self.assertRaises(ValueError, Checker, DICTIONARY)

    def test_GivenANonexistentDictionaryForChecker_When_Checker_ThenExceptionIsRaised(self):
        DICTIONARY = 'this-file-does-not-exist'
        self.assertRaises(IOError, Checker, DICTIONARY)
        
    def test_GivenTheRealDictionaryForChecker_When_check_entries_ThenReturnTrue(self):
        DICTIONARY = '../data/dictionary.md'
        CHECKER = Checker(DICTIONARY)
        self.assertTrue(CHECKER.check_entries())

    def test_GivenTheRealDictionaryForChecker_When_check_duplicated_headwords_ThenReturnTrue(self):
        DICTIONARY = '../data/dictionary.md'
        CHECKER = Checker(DICTIONARY)
        self.assertTrue(CHECKER.check_duplicated_headwords())

    def test_GivenTheRealDictionaryForChecker_When_check_undef_high_freq_keywords_ThenReturnTrue(self):
        DICTIONARY = '../data/dictionary.md'
        CHECKER = Checker(DICTIONARY)
        self.assertTrue(CHECKER.check_undef_high_freq_keywords())

if __name__ == '__main__':
    unittest.main()
