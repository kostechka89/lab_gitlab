import io
import unittest
from decimal import Decimal
import app
class Tests(unittest.TestCase):
    def test_aggregation(self):
        r = app.summarize(io.StringIO('product,quantity,price\nBook,2,10.10\nBook,1,2.00\nPen,3,1.50\n'))
        self.assertEqual(r['Book'], Decimal('22.20'))
        self.assertIn('Total: 26.70', app.render(r))
    def test_invalid(self):
        for row in ('Book,-1,2', 'Book,1,NaN', 'Book,1,-2', 'Book,x,2', ',1,2'):
            with self.assertRaises(ValueError): app.summarize(io.StringIO('product,quantity,price\n' + row))
    def test_header(self):
        with self.assertRaises(ValueError): app.summarize(io.StringIO('wrong,header\n'))
    def test_empty_and_escape(self):
        self.assertEqual(app.summarize(io.StringIO('product,quantity,price\n')), {})
        self.assertIn('&lt;b&gt;', app.render({'<b>': Decimal('1')}))
