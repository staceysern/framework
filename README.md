Framework
=========

Framework is a WSGI application which can be configured with routes for both static and dynamic content.

Here's an example of an application which

 * serves static content out of the `static_folder` directory
 * calls the `hello_world()` function to provide the content for the path `/hello_world`
 * calls the `user()` function for paths which match `/user/<name>` where the characters appearing after the second slash but before a possible third slash are passed as an argument named `name`

```
from framework import Framework

def hello_world():
    ...

def user(name):
    ...

app = Framework('static_folder')
app.add_url_rule('/hello_world', hello_world)
app.add_url_rule('/user/<name>', user)
app.run('www.example.com', 80)
```

Framework accepts an optional argument which specifies the directory containing static files.  It defaults to `static`.

The run command takes a hostname and port as arguments.  The default values are `'127.0.0.1'` and `5000`.

Variable names can contain letters, digits and underscores. URLs can contain letters, digits, underscores, hyphens, periods and tildes.

When a URL with a trailing slash has been configured and the URL is accessed without the trailing slash, a 301 redirect will be issued to the URL with the trailing slash.

Requirements
____________

The `waitress` and `WebOb` libraries are required to use Framework.  `pip install -r requirements.txt` will install them.

Example
_______

An example application has been included which demonstrates the different type of URLs supported by Framework.

`python example.py` runs the application.  The index page can be reached in a browser at `localhost:8080/`.

To Do
_____

 * Handle POST requests
 * Template support