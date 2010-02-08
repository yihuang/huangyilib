import sys
import urllib
class OutputStream(object):
    def __init__(self):
        self.buffer = []
    def write(self, content):
        self.buffer.append(content)

class InputStream(object):
    def __init__(self, environ):
        self._input = environ['wsgi.input']

    def readline(self):
        return self._input.readline()

def app(environ, start_response):
    old_stdout = sys.stdout
    old_stdin = sys.stdin

    ostream = OutputStream()
    istream = InputStream(environ)

    sys.stdout = ostream
    sys.stdin = istream

    import temp
    temp.main(urllib.unquote(environ['QUERY_STRING']))

    start_response('200 OK', [])
    return ostream.buffer

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    make_server('', 8000, app).serve_forever()
