#!/usr/bin/env python3
"""
For your homework this week, you'll be creating a wsgi application of
your own.

You'll create an online calculator that can perform several operations.

You'll need to support:

  * Addition
  * Subtractions
  * Multiplication
  * Division

Your users should be able to send appropriate requests and get back
proper responses. For example, if I open a browser to your wsgi
application at `http://localhost:8080/multiple/3/5' then the response
body in my browser should be `15`.

Consider the following URL/Response body pairs as tests:

```
  http://localhost:8080/multiply/3/5   => 15
  http://localhost:8080/add/23/42      => 65
  http://localhost:8080/subtract/23/42 => -19
  http://localhost:8080/divide/22/11   => 2
  http://localhost:8080/               => <html>Here's how to use this page...</html>
```

To submit your homework:

  * Fork this repository (Session03).
  * Edit this file to meet the homework requirements.
  * Your script should be runnable using `$ python calculator.py`
  * When the script is running, I should be able to view your
    application in my browser.
  * I should also be able to see a home page (http://localhost:8080/)
    that explains how to perform calculations.
  * Commit and push your changes to your fork.
  * Submit a link to your Session03 fork repository!


"""


def resolve_path(path):
    """
    Should return two values: a callable and an iterable of
    arguments.
    """

    funcs = {
        '' : show_help,
        'add' : add,
        'subtract' : subtract,
        'multiply' : multiply,
        'divide' : divide,
    }

    path = path.strip('/').split('/')
    args = path[1:]
    
    try:
        func = funcs[path[0]]
    except KeyError:
        raise NameError

    return func, args


def show_help(*args):
    page = """
Usage: Construct slash-separated URI with operation and arguments.  E.g.,<br />
<a href='multiply/3/5'>multiply/3/5</a><br />
<a href='add/23/42'>add/23/42</a><br />
<a href='subtract/23/42'>subtract/23/42</a><br />
<a href='divide/22/11'>divide/22/11/a><br />
"""
    return page.format()


def add(*args):
    page = """{}"""

    sum = int(args[0])
    for arg in args[1:]:
        sum += int(arg)

    return page.format(sum)


def subtract(*args):
    page = """{}"""

    difference = int(args[0])
    for arg in args[1:]:
        difference -= int(arg)

    return page.format(difference)


def multiply(*args):
    page = """{}"""

    product = int(args[0])
    for arg in args[1:]:
        product *= int(arg)

    return page.format(product)


def divide(*args):
    page = """{}"""

    quotient = int(args[0])
    for arg in args[1:]:
        quotient /= int(arg)

    return page.format(quotient)


def application(environ, start_response):
    headers = [("Content-type", "text/html")]
    status = "500 Internal Server Error"
    body = "<h1>Internal Server Error</h1>"
    try:
        path = environ.get('PATH_INFO', None)
        if path is None:
            raise NameError
        func, args = resolve_path(path)
        body = func(*args)
        status = "200 OK"
    except NameError as e:
        print(e)
        print(traceback.format_exc())
        status = "404 Not Found"
        body = "<h1>Not Found</h1>"
    except ZeroDivisionError as e:
        status = "400 Bad Request"
        body = "<h1>Attempted to divide by zero</h1>"
    except Exception as e:
        print(e)
        print(traceback.format_exc())
    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body.encode('utf8')]


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
