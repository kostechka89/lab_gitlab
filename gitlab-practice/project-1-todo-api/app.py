import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

class Tasks:
    def __init__(self):
        self.items = {}
        self.next_id = 1
    def add(self, title):
        if not isinstance(title, str) or not title.strip():
            raise ValueError('Title is required')
        item = dict(id=self.next_id, title=title.strip(), done=False)
        self.items[self.next_id] = item
        self.next_id += 1
        return item
    def complete(self, ident):
        self.items[ident]['done'] = True
        return self.items[ident]
    def delete(self, ident):
        del self.items[ident]

class Handler(BaseHTTPRequestHandler):
    tasks = Tasks()
    def reply(self, status, value):
        body = json.dumps(value).encode()
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)
    def do_GET(self):
        if self.path != '/tasks':
            return self.reply(404, {'error': 'Not found'})
        self.reply(200, list(self.tasks.items.values()))
    def do_POST(self):
        if self.path != '/tasks':
            return self.reply(404, {'error': 'Not found'})
        try:
            data = json.loads(self.rfile.read(int(self.headers.get('Content-Length', 0))))
            if not isinstance(data, dict):
                raise ValueError('Expected object')
            self.reply(201, self.tasks.add(data.get('title')))
        except (ValueError, TypeError):
            self.reply(400, {'error': 'Valid JSON and nonempty title required'})
    def change(self, delete=False):
        try:
            parts = self.path.split('/')
            if len(parts) != 3 or parts[1] != 'tasks':
                raise KeyError()
            ident = int(parts[2])
            if delete:
                self.tasks.delete(ident)
                self.reply(200, {'deleted': ident})
            else:
                self.reply(200, self.tasks.complete(ident))
        except (KeyError, ValueError):
            self.reply(404, {'error': 'Not found'})
    def do_PATCH(self):
        self.change()
    def do_DELETE(self):
        self.change(True)

def main():
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('--port', type=int, default=8001)
    args = p.parse_args()
    ThreadingHTTPServer(('0.0.0.0', args.port), Handler).serve_forever()

if __name__ == '__main__':
    main()
