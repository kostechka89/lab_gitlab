import unittest
import app
class Tests(unittest.TestCase):
    def test_counts(self):
        result = app.analyze('Hello hello!\nWorld')
        self.assertEqual(result['words'], 3)
        self.assertEqual(result['unique_words'], 2)
        self.assertEqual(result['lines'], 2)
        self.assertEqual(result['top_words'][0], ('hello', 2))
        self.assertEqual(result['characters'], 18)
    def test_empty(self):
        r = app.analyze('')
        self.assertEqual(r['words'], 0)
        self.assertEqual(r['lines'], 0)
    def test_unicode(self):
        self.assertEqual(app.analyze('Привет, ПРИВЕТ!')['unique_words'], 1)
    def test_punctuation(self):
        self.assertEqual(app.analyze('one-two ... three')['words'], 2)
