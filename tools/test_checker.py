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

"""
        self.assertTrue(CHECKER.check_entries())
        self.assertTrue(CHECKER.check_duplicated_headwords())
        self.assertTrue(CHECKER.check_undef_high_freq_keywords())
"""

if __name__ == '__main__':
    unittest.main()
