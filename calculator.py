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

    total = sum(map(int, list(args)))
    result = "The total is: {}".format(str(total))

    body = ['<body style="text-align: center;margin: 0 25%; border-left: .1rem dotted gray; border-right: .1rem dotted gray;">']
    body.append('<hr>')
    body.append('<h3>Result of Addition Operation </h3>')
    body.append('<br>')

    parag = '<p style="text-align: left;padding: 0 2%;">{}</p>'.format(str(result))
    body.append(parag)
    body.append('<br>')
    body.append('<a href="/">Back to the main page.</a>')
    body.append('<hr>')
    body.append('</body>')
    return '\n'.join(body)

def subtract(*args):
    """ Returns a STRING with the sum of the arguments """

    operands = list(map(int, list(args)))
    subtract = [first - second for first, second in zip(operands, operands[1:])]
    result = "The result is: {}".format(str(subtract[0]))

    body = ['<body style="text-align: center;margin: 0 25%; border-left: .1rem dotted gray; border-right: .1rem dotted gray;">']
    body.append('<hr>')
    body.append('<h3>Result of Subtraction Operation </h3>')
    body.append('<br>')

    parag = '<p style="text-align: left;padding: 0 2%;">{}</p>'.format(str(result))
    body.append(parag)
    body.append('<br>')
    body.append('<a href="/">Back to the main page.</a>')
    body.append('<hr>')
    body.append('</body>')
    return '\n'.join(body)


def multiple(*args):
    """ Returns a STRING with the sum of the arguments """

    operands = list(map(int, list(args)))
    result = "The result is: {}".format(str(numpy.prod(operands)))
    
    body = ['<body style="text-align: center;margin: 0 25%; border-left: .1rem dotted gray; border-right: .1rem dotted gray;">']
    body.append('<hr>')
    body.append('<h3>Result of Multiplication Operation </h3>')
    body.append('<br>')

    parag = '<p style="text-align: left;padding: 0 2%;">{}</p>'.format(str(result))
    body.append(parag)
    body.append('<br>')
    body.append('<a href="/">Back to the main page.</a>')
    body.append('<hr>')
    body.append('</body>')
    return '\n'.join(body)


def divide(*args):
    """ Returns a STRING with the sum of the arguments """

    operands = list(map(int, list(args)))
    result = "The result is: {}".format(str(operands[0]/operands[1]))

    body = ['<body style="text-align: center;margin: 0 25%; border-left: .1rem dotted gray; border-right: .1rem dotted gray;">']
    body.append('<hr>')
    body.append('<h3>Result of Division Operation </h3>')
    body.append('<br>')

    parag = '<p style="text-align: left;padding: 0 2%;">{}</p>'.format(str(result))
    body.append(parag)
    body.append('<br>')
    body.append('<a href="/">Back to the main page.</a>')
    body.append('<hr>')
    body.append('</body>')
    return '\n'.join(body)

def index(*args):
    """ Returns a STRING with the sum of the arguments """
    args = ['25', '32']
    operations = ['Add', 'Subtract', 'Multiply', 'Divide']
    body = ['<body style="text-align: center;margin: 0 25%; border-left: .1rem dotted gray; border-right: .1rem dotted gray;">',
            '<nav style="font-size: 2rem; height: 5rem; background-color: #e3f2fd; align:center; margin: 0 auto; font-family: Courier, Ariel;">']
    item_template = '<a id="{}" href="/{}/{}/{}">{}</a>'
    body.append('<hr>')
    for operation in operations:
        body.append(item_template.format(operation, operation.lower(), args[0], args[1], operation))
    body.append('</nav>')
    
    body.append('<br>')

    body.append('<h3>Math Operations </h3>')
    body.append('<br>')

    parag = '<p style="text-align: left;padding: 0 2%;">1) To use this site, click on the menu items, '
    parag += 'which will direct you to a new page.</p>'
    parag += '<p style="text-align: left;padding: 0 2%;">2) On the address bar of the new page, '
    parag += 'after the Math operator, enter two numbers separated by "/", and hit enter.</p>'
    parag += '<p style="text-align: left;padding: 0 2%;">3) '
    parag += 'You should see the result of the math operation on the operands in the page.</p>'

    body.append(parag)
    body.append('<br>')
    body.append('<hr>')
    body.append('</body>')

    return '\n'.join(body)


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
        '':index,
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
    except ZeroDivisionError:
        status = "404 Dvision by Zero"
        body = "<h1>Division by Zero</h1>"
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
