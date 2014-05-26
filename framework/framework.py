import os
import webob


class Framework(object):
    BLOCK_SIZE = 4096

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

        file_path = request.path[1:]
        if file_path == '':
            file_path = 'index.html'

        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            headers = [('Content-type', 'text/html'),
                       ('Content-length', str(size))]

            start_response('200 OK', headers)
            return self._send_file(file_path, size)
        else:
            start_response('404 Not found', [('Content-type', 'text/plain')])
            return [file_path + ' not found']


if __name__ == '__main__':
    framework = Framework()
    framework.run()
