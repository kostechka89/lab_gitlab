import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

def analyze(text):
    words = re.findall(r"[^\W_]+(?:['’-][^\W_]+)*", text.lower(), re.UNICODE)
    return dict(characters=len(text), lines=len(text.splitlines()), words=len(words),
                unique_words=len(set(words)), top_words=Counter(words).most_common(5))

def main():
    p = argparse.ArgumentParser(description='Analyze UTF-8 text; omit file to read stdin')
    p.add_argument('file', nargs='?')
    args = p.parse_args()
    try:
        text = Path(args.file).read_text(encoding='utf-8') if args.file else sys.stdin.read()
    except (OSError, UnicodeError) as exc:
        p.exit(2, f'Cannot read input: {exc}\n')
    print(json.dumps(analyze(text), ensure_ascii=False, indent=2))
if __name__ == '__main__':
    main()
