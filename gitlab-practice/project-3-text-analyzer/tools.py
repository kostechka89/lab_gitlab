import argparse
import hashlib
import json
import py_compile
import shutil
import subprocess
import sys
import tempfile
import time
import socket
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import URLError
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parent
KIND = 3

def smoke(directory):
    directory = Path(directory)
    if KIND in (1, 2):
        with socket.socket() as s:
            s.bind(('127.0.0.1', 0))
            port = s.getsockname()[1]
        proc = subprocess.Popen([sys.executable, 'app.py', '--port', str(port)], cwd=directory, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        base = f'http://127.0.0.1:{port}'
        try:
            path = '/tasks' if KIND == 1 else '/'
            for _ in range(100):
                try:
                    with urlopen(base + path, timeout=1) as r:
                        assert r.status == 200
                    break
                except URLError:
                    if proc.poll() is not None: raise RuntimeError('Server exited')
                    time.sleep(.05)
            else:
                raise RuntimeError('Server did not start')
            def request(path, method='GET', body=None, headers=None):
                with urlopen(Request(base + path, data=body, method=method, headers=headers or {}), timeout=2) as r:
                    return r.read().decode()
            if KIND == 1:
                item = json.loads(request('/tasks', 'POST', b'{"title":"Smoke task"}', {'Content-Type':'application/json'}))
                assert item['title'] == 'Smoke task'
                assert json.loads(request('/tasks'))[0]['id'] == item['id']
                assert json.loads(request('/tasks/' + str(item['id']), 'PATCH'))['done']
                request('/tasks/' + str(item['id']), 'DELETE')
                assert json.loads(request('/tasks')) == []
            else:
                html = request('/add', 'POST', b'title=Lab+2&subject=DevOps')
                assert 'Lab 2' in html and 'Pending' in html
                assert 'Completed' in request('/complete', 'POST', b'id=1')
                assert 'Lab 2' not in request('/delete', 'POST', b'id=1')
        finally:
            proc.terminate()
            try: proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                proc.kill(); proc.wait()
    elif KIND == 3:
        r = subprocess.run([sys.executable, 'app.py', 'sample.txt'], cwd=directory, check=True, capture_output=True, text=True)
        assert json.loads(r.stdout)['words'] == 3
        r = subprocess.run([sys.executable, 'app.py'], input='one two', cwd=directory, check=True, capture_output=True, text=True)
        assert json.loads(r.stdout)['words'] == 2
    else:
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp)/'report.html'
            subprocess.run([sys.executable, 'app.py', 'sample.csv', '--output', str(output)], cwd=directory, check=True)
            assert 'Total: 24.70' in output.read_text()
    print('Application smoke: PASS')

def main():
    p = argparse.ArgumentParser()
    p.add_argument('action', choices=['build', 'smoke', 'deploy'])
    p.add_argument('artifact', nargs='?', default='dist/application.zip')
    args = p.parse_args()
    artifact = ROOT / args.artifact
    if args.action == 'build':
        py_compile.compile(str(ROOT/'app.py'), doraise=True)
        artifact.parent.mkdir(parents=True, exist_ok=True)
        with ZipFile(artifact, 'w') as z:
            for name in ['app.py', 'README.md', 'requirements.txt', 'sample.txt', 'sample.csv']:
                file = ROOT/name
                if file.exists(): z.write(file, name)
        print('Build: PASS', artifact.name)
    elif args.action == 'smoke':
        with tempfile.TemporaryDirectory() as temp:
            with ZipFile(artifact) as z: z.extractall(temp)
            smoke(temp)
    else:
        dest = ROOT/'deploy'
        if dest.exists(): shutil.rmtree(dest)
        dest.mkdir()
        with ZipFile(artifact) as z: z.extractall(dest)
        smoke(dest)
        manifest = {f.name: hashlib.sha256(f.read_bytes()).hexdigest() for f in dest.iterdir() if f.is_file()}
        (dest/'manifest.json').write_text(json.dumps(manifest, indent=2))
        print('Educational deploy: PASS')
if __name__ == '__main__':
    main()
