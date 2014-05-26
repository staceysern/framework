import os
import webob


class Framework(object):
    BLOCK_SIZE = 4096

    def __init__(self, static_folder='static'):
        self.static_folder = static_folder
        self.rules = {}

    def add_url_rule(self, rule, func):
        if rule[0] != '/':
            raise ValueError('urls must start with a leading slash')

        self.rules[rule] = func

    def run(self, host='127.0.0.1', port=5000):
        from waitress import serve
        serve(self, host=host, port=port)

    def _send_file(self, file_path, size):
        with open(file_path) as f:
            block = f.read(self.BLOCK_SIZE)
            while block:
                yield block
                block = f.read(self.BLOCK_SIZE)

    def __call__(self, environ, start_response):
        request = webob.Request(environ)

        func = None
        if request.path in self.rules:
            func = self.rules[request.path]
        elif request.path[-1] != '/':
            trailing_slash_path = request.path + '/'
            if trailing_slash_path in self.rules:
                func = self.rules[trailing_slash_path]

        if func:
            start_response('OK 200', [('Content-type', 'text/plain')])
            return func()
        else:
            if request.path == '/':
                file_path = self.static_folder + '/index.html'
            else:
                file_path = self.static_folder + request.path

            if os.path.exists(file_path):
                size = os.path.getsize(file_path)
                headers = [('Content-type', 'text/html'),
                           ('Content-length', str(size))]

                start_response('200 OK', headers)
                return self._send_file(file_path, size)
            else:
                start_response('404 Not found', [('Content-type', 'text/plain')])
                return ['Page not found']

if __name__ == '__main__':
    def hello_world():
        return 'Hello World!'

    framework = Framework()
    framework.add_url_rule('/helloworld/', hello_world)
    framework.run()
