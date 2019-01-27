"""
Run the tests by executing:
$ python -m unittest -v test_dictionary
"""

import unittest
from dictionary import Dictionary

class Test_Dictionary(unittest.TestCase):

    def test_GIVEN_an_empty_dictionary_WHEN_calling_xyz_THEN_result_must_be_equal_to_xyz(self):
        DICTIONARY = Dictionary()
        self.assertEqual(2, 1)

if __name__ == '__main__':
    unittest.main()
