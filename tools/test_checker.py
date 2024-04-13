"""
Run the tests by executing:
$ pwd
AmE-dictionary/tools
$ python -m unittest -v test_checker
"""

import unittest
from checker import Checker
from typing import Final


class TestChecker(unittest.TestCase):

    def test_GivenAnEmptyDictionary_When_Checker_ThenExceptionIsRaised(self):
        dictionary: Final = ''
        self.assertRaises(ValueError, Checker, dictionary)

    def test_GivenANonexistentDictionaryForChecker_When_Checker_ThenExceptionIsRaised(self):
        dictionary = 'this-file-does-not-exist'
        self.assertRaises(IOError, Checker, dictionary)

    def test_GivenTheRealDictionaryForChecker_When_check_entries_ThenReturnTrue(self):
        dictionary = '../data/dictionary.md'
        checker = Checker(dictionary)
        self.assertTrue(checker.check_entries())

    def test_GivenTheRealDictionaryForChecker_When_check_duplicated_headwords_ThenReturnTrue(self):
        dictionary = '../data/dictionary.md'
        checker = Checker(dictionary)
        self.assertTrue(checker.check_duplicated_headwords())

    def test_GivenTheRealDictionaryForChecker_When_check_undef_high_freq_keywords_ThenReturnTrue(self):
        dictionary = '../data/dictionary.md'
        checker = Checker(dictionary)
        self.assertTrue(checker.check_undef_high_freq_keywords())


if __name__ == '__main__':
    unittest.main()
