import sys
import os
import unittest

# Add the parent directory (src) to the sys.path to import your_script
current_dir = os.path.dirname(__file__)
parent_dir = os.path.join(current_dir, '../src')
sys.path.insert(0, os.path.abspath(parent_dir))

from letterBoxedSolver import createNextPossibleLetterMap, isWordValid, findPossibleWords, bruteForceAlgorithm

class TestLetterPuzzleSolver(unittest.TestCase):

    def test_createNextPossibleLetterMap(self):
        letterSets = ["abc", "def", "ghi"]
        expected_map = {
            'a': ['d', 'e', 'f', 'g', 'h', 'i'], 
            'b': ['d', 'e', 'f', 'g', 'h', 'i'], 
            'c': ['d', 'e', 'f', 'g', 'h', 'i'],
            'd': ['a', 'b', 'c', 'g', 'h', 'i'],
            'e': ['a', 'b', 'c', 'g', 'h', 'i'],
            'f': ['a', 'b', 'c', 'g', 'h', 'i'],
            'g': ['a', 'b', 'c', 'd', 'e', 'f'],
            'h': ['a', 'b', 'c', 'd', 'e', 'f'],
            'i': ['a', 'b', 'c', 'd', 'e', 'f']
        }
        result_map = createNextPossibleLetterMap(letterSets)
        self.assertEqual(result_map, expected_map)

    def test_isWordValid(self):
        letterSets = ["rud", "nmg", "fio", "apl"]
        nextPossibilities = createNextPossibleLetterMap(letterSets)
        letters = set(a for s in letterSets for a in s)
        # Test with valid and invalid words
        self.assertTrue(isWordValid("program", letters, nextPossibilities))
        self.assertFalse(isWordValid("invalid", letters, nextPossibilities))

    def test_findPossibleWords(self):
        letterSets = ["rud", "nmg", "fio", "apl"]
        words = findPossibleWords(letterSets, filename="test_filtered_words.txt")

        # Ensure 'p' is a key in the dictionary
        self.assertIn('p', words)

        # Check if 'program' is in the list for 'p'
        self.assertIn("program", words.get('p', []))
        
        # Similarly, check for 'mindful'
        self.assertIn('m', words)
        self.assertIn("mindful", words.get('m', []))

        # Optionally, check that 'invalid' is not in the list for 'i'
        self.assertNotIn("invalid", words.get('i', []))

    # Additional tests for bruteForceAlgorithm and overall functionality can be added

if __name__ == "__main__":
    unittest.main()
