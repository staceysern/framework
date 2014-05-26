import os
import re
import webob


class Router(object):
    BLOCK_SIZE = 4096
    re_variable = re.compile(r'<(?P<t_word>[a-zA-Z0-9_]+)>')

    def __init__(self, static_folder):
        self.static_folder = static_folder
        self.rules = []

    def _send_file(self, file_path, size):
        with open(file_path) as f:
            block = f.read(self.BLOCK_SIZE)
            while block:
                yield block
                block = f.read(self.BLOCK_SIZE)

    def add_rule(self, rule, func):
        if rule[0] != '/':
            raise ValueError('urls must start with a leading slash')

        variables = set()
        groups = []
        for match in re.finditer(self.re_variable, rule):
            name = match.groups()[0]
            if name in variables:
                raise ValueError("variable name '" + name + "' used twice")
            else:
                variables.add(name)

            group = list('(?P<' + name + '>[a-zA-Z0-9-._~]+)')
            groups.append((match.start(), match.end(),group))

        regex = list(rule)
        for start, end, group in groups[::-1]:
            regex[start:end] = group
        regex.append('$')
        self.rules.append((re.compile("".join(regex)), func))

    def route(self, path, start_response):
        for regex, func in self.rules:
             match = re.match(regex, path)
             if match:
                 start_response('OK 200', [('Content-type', 'text/plain')])
                 return func(**match.groupdict())

        if path[-1] != '/':
            trailing_slash_path = path + '/'
            for regex, func in self.rules:
                match = re.match(regex, trailing_slash_path)
                if match:
                    start_response('301 Redirect',
                                   [('Location', trailing_slash_path)])
                    return []

        if path == '/':
            file_path = self.static_folder + '/index.html'
        else:
            file_path = self.static_folder + path

        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            headers = [('Content-type', 'text/html'),
                       ('Content-length', str(size))]

            start_response('200 OK', headers)
            return self._send_file(file_path, size)
        else:
            start_response('404 Not found', [('Content-type', 'text/plain')])
            return ['Page not found']


class Framework(object):
    def __init__(self, static_folder='static'):
        self.router = Router(static_folder)

    def add_url_rule(self, rule, func):
        self.router.add_rule(rule, func)

    def run(self, host='127.0.0.1', port=5000):
        from waitress import serve
        serve(self, host=host, port=port)

    def __call__(self, environ, start_response):
        request = webob.Request(environ)
        return self.router.route(request.path, start_response)
