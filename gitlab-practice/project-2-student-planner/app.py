from html import escape
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs

class Planner:
    def __init__(self):
        self.tasks = {}
        self.next_id = 1
    def add(self, title, subject):
        if not title.strip() or not subject.strip():
            raise ValueError('Title and subject required')
        self.tasks[self.next_id] = dict(title=title.strip(), subject=subject.strip(), done=False)
        self.next_id += 1
    def complete(self, ident):
        self.tasks[ident]['done'] = True
    def delete(self, ident):
        del self.tasks[ident]
    def render(self):
        rows = ''
        for ident, task in self.tasks.items():
            state = 'Completed' if task['done'] else 'Pending'
            rows += f'<li>{escape(task["subject"])}: {escape(task["title"])} — {state}'
            for action in ('complete', 'delete'):
                rows += f'<form method="post" action="/{action}"><input type="hidden" name="id" value="{ident}"><button>{action}</button></form>'
            rows += '</li>'
        return ('<!doctype html><html lang="en"><meta charset="utf-8"><title>Student Planner</title>'
                '<h1>Student Planner</h1><form method="post" action="/add">'
                '<input name="subject" placeholder="Subject" required><input name="title" placeholder="Assignment" required>'
                '<button>Add assignment</button></form><ul>' + rows + '</ul></html>')

class Handler(BaseHTTPRequestHandler):
    planner = Planner()
    def do_GET(self):
        if self.path != '/':
            self.send_error(404)
            return
        body = self.planner.render().encode()
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)
    def do_POST(self):
        try:
            form = parse_qs(self.rfile.read(int(self.headers.get('Content-Length', 0))).decode())
            if self.path == '/add':
                self.planner.add(form['title'][0], form['subject'][0])
            elif self.path == '/complete':
                self.planner.complete(int(form['id'][0]))
            elif self.path == '/delete':
                self.planner.delete(int(form['id'][0]))
            else:
                self.send_error(404)
                return
        except (KeyError, ValueError, UnicodeError):
            self.send_error(400)
            return
        self.send_response(303)
        self.send_header('Location', '/')
        self.end_headers()

def main():
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('--port', type=int, default=8002)
    args = p.parse_args()
    ThreadingHTTPServer(('0.0.0.0', args.port), Handler).serve_forever()
if __name__ == '__main__':
    main()
