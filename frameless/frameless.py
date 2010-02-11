import sys
import functools
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

def app(module_name, environ, start_response):
    old_stdout = sys.stdout
    old_stdin = sys.stdin

    ostream = OutputStream()
    istream = InputStream(environ)

    start_response('200 OK', [])
    print environ['wsgi.input'].read()
    return 'xxx'
    #print environ['wsgi.input'].read()

    sys.stdout = ostream
    sys.stdin = istream

    try:
        module = __import__(module_name)
        module.main(urllib.unquote(environ['QUERY_STRING']))
    except:
        sys.stdout = old_stdout
        sys.stdin = old_stdin
        raise
    else:
        sys.stdout = old_stdout
        sys.stdin = old_stdin

    return ostream.buffer

def main():
    import wsgiref
    from wsgiref.simple_server import make_server
    from StringIO import StringIO

    if len(sys.argv)<2:
        print 'usage: frameless.py module_name [ip port]'
        return
    module_name = sys.argv[1]
    if len(sys.argv)>=4:
        ip = sys.argv[2]
        port = int(sys.argv[3])
    else:
        ip = 'localhost'
        port = 8000

    wsgi_app = functools.partial(app, module_name)

    '''
    test_env = {}
    wsgiref.util.setup_testing_defaults(test_env)
    test_env['QUERY_STRING'] = 'helloworld'
    test_env['wsgi.input'] = StringIO('xxx\nddd\nyyy\n')
    print wsgi_app(test_env, lambda a,b:None)
    '''

    print 'listening on %s:%d'%(ip, port)
    make_server(ip, port, wsgi_app).serve_forever()

if __name__ == '__main__':
    main()
