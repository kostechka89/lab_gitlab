import unittest
import app
class Tests(unittest.TestCase):
    def test_lifecycle(self):
        tasks = app.Tasks()
        item = tasks.add(' Learn Git ')
        self.assertEqual(item['title'], 'Learn Git')
        self.assertFalse(item['done'])
        self.assertTrue(tasks.complete(item['id'])['done'])
        tasks.delete(item['id'])
        self.assertEqual(tasks.items, {})
    def test_validation(self):
        for title in ('', '   ', None, 12):
            with self.assertRaises(ValueError): app.Tasks().add(title)
    def test_unique_ids(self):
        t = app.Tasks()
        self.assertNotEqual(t.add('a')['id'], t.add('b')['id'])
    def test_missing(self):
        with self.assertRaises(KeyError): app.Tasks().complete(999)
