import unittest
import app
class Tests(unittest.TestCase):
    def test_lifecycle(self):
        p = app.Planner()
        p.add('Lab 2', 'DevOps')
        self.assertIn('Lab 2', p.render())
        self.assertIn('Pending', p.render())
        p.complete(1)
        self.assertIn('Completed', p.render())
        p.delete(1)
        self.assertEqual(p.tasks, {})
    def test_validation(self):
        with self.assertRaises(ValueError): app.Planner().add(' ', 'Math')
        with self.assertRaises(ValueError): app.Planner().add('Lab', '')
    def test_escape(self):
        p = app.Planner()
        p.add('<script>', 'A&B')
        self.assertIn('&lt;script&gt;', p.render())
        self.assertIn('A&amp;B', p.render())
        self.assertNotIn('<script>', p.render())
