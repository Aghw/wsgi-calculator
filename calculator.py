import sys
import re
import numpy

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


def add(*args):
    """ Returns a STRING with the sum of the arguments """

    # TODO: Fill sum with the correct value, based on the
    # args provided.
    result = sum(map(int, list(args)))
    return "The total is: {}".format(str(result))


def subtract(*args):
    """ Returns a STRING with the sum of the arguments """

    operands = list(map(int, list(args)))
    result = [first - second for first, second in zip(operands, operands[1:])]
    return "The result is: {}".format(str(result[0]))


def multiple(*args):
    """ Returns a STRING with the sum of the arguments """

    operands = list(map(int, list(args)))
    return "The result is: {}".format(str(numpy.prod(operands)))


def divide(*args):
    """ Returns a STRING with the sum of the arguments """

    operands = list(map(int, list(args)))
    return "The result is: {}".format(str(operands[0]/operands[1]))


def operations(*args):
    """ Returns a STRING with the sum of the arguments """
    operations = ['add', 'subtract', 'multiply', 'divide']
    body = ['<body style="text-align: center;margin: 0 25%; border-left: .1rem dotted gray; border-right: .1rem dotted gray;">',
            '<nav style="font-size: 3rem; height: 5rem; background-color: #e3f2fd; align:center; margin: 0 auto; border-radius: .7rem;">']
    item_template = '<a id="{}" href="/{}">{}</a>'

    for operation in operations:
        body.append(item_template.format(operation, operation, operation))
    body.append('</nav>')
    body.append('<br>')

    body.append('<h3>Math Operations </h3>')
    body.append('</body>')
    # <a id="donation_list" href="{{ url_for("all") }}">Donations</a>
    # </nav>
    # body = ['<h3>Math Operations </h3>']
    # item_template = '<li><a href="/{}">{}</a></li>'
    
    # operations = ['add', 'subtract', 'multiply', 'divide']

    # body.append('<ul>')
    # for operation in operations:
    #     body.append(item_template.format(operation, operation))
    # body.append('</ul>')
    # # <form>
    # # <table>
    # #     <tr><td>Operand1</td><td>{author}</td></tr>
    # #     <tr><td>Operand2</td><td>{publisher}</td></tr>
    # #     <tr><td></td><td>{isbn}</td></tr>
    # # </table>
    # # </form>

    return '\n'.join(body)

    # return "Math Operations {}".format(str(args))


# TODO: Add functions for handling more arithmetic operations.

def resolve_path(path):
    """
    Should return two values: a callable and an iterable of
    arguments.
    """

    # TODO: Provide correct values for func and args. The
    # examples provide the correct *syntax*, but you should
    # determine the actual values of func and args using the
    # path.
    func = add
    args = ['25', '32']

    funcs = {
        '':operations,
        'add': add,
        'subtract': subtract,
        'multiply': multiple,
        'divide': divide,
    }

    path = path.strip('/').split('/')

    func_name = path[0].lower()
    args = path[1:]

    try:
        func = funcs[func_name]
    except KeyError:
        raise NameError

    return func, args

def application(environ, start_response):
    # TODO: Your application code from the book database
    # work here as well! Remember that your application must
    # invoke start_response(status, headers) and also return
    # the body of the response in BYTE encoding.
    #
    # TODO (bonus): Add error handling for a user attempting
    # to divide by zero.
    headers = [("Content-type", "text/html")]
    try:
        path = environ.get('PATH_INFO', None)
        if path is None:
            raise NameError
        func, args = resolve_path(path)
        body = func(*args)
        status = "200 OK"
    except NameError:
        status = "404 Not Found"
        body = "<h1>Not Found</h1>"
    except Exception:
        status = "500 Internal Server Error"
        body = "<h1>Internal Server Error</h1>"
        print(traceback.format_exc())
    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body.encode('utf8')]

if __name__ == '__main__':
    # TODO: Insert the same boilerplate wsgiref simple
    # server creation that you used in the book database.
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
