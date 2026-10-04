import argparse
import csv
from decimal import Decimal, InvalidOperation
from html import escape
from pathlib import Path

def summarize(stream):
    reader = csv.DictReader(stream)
    if reader.fieldnames != ['product', 'quantity', 'price']:
        raise ValueError('Expected CSV columns: product,quantity,price')
    totals = {}
    for row in reader:
        try:
            name = row['product'].strip()
            quantity = int(row['quantity'])
            price = Decimal(row['price'])
            if not name or quantity < 0 or not price.is_finite() or price < 0:
                raise ValueError()
        except (ValueError, TypeError, AttributeError, InvalidOperation):
            raise ValueError(f'Invalid CSV row {reader.line_num}') from None
        totals[name] = totals.get(name, Decimal('0')) + quantity * price
    return totals

def render(totals):
    rows = ''.join(f'<tr><td>{escape(name)}</td><td>{value:.2f}</td></tr>' for name, value in sorted(totals.items()))
    total = sum(totals.values(), Decimal('0'))
    return f'<!doctype html><html lang="en"><meta charset="utf-8"><title>Sales report</title><h1>Sales report</h1><table><tr><th>Product</th><th>Revenue</th></tr>{rows}</table><p>Total: {total:.2f}</p></html>'

def main():
    p = argparse.ArgumentParser(description='Create HTML sales report from CSV')
    p.add_argument('input')
    p.add_argument('--output', default='report.html')
    args = p.parse_args()
    try:
        with open(args.input, encoding='utf-8', newline='') as stream:
            totals = summarize(stream)
        Path(args.output).write_text(render(totals), encoding='utf-8')
    except (OSError, ValueError, UnicodeError) as exc:
        p.exit(2, f'Report failed: {exc}\n')
    print(f'Report saved: {args.output}')
if __name__ == '__main__':
    main()
