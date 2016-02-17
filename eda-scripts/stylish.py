# handy little functions to display consistent, coloured code in the terminal
from termcolor import colored

# decorator for most functions
def spaceAfter(inputFunction):
    # concatenate
    def concatSpace(x):

        return inputFunction(x) + ' '

    return concatSpace

def tab(x=1):

    return '\t'*x

@spaceAfter
def title(x):

    return colored(x, 'yellow', attrs=['bold', 'underline'])

@spaceAfter
def highlight(x, colour='cyan'):

    return colored(x, colour)

@spaceAfter
def subheader(x):

    return colored(x, 'white', attrs=['underline'])

@spaceAfter
def important(x):

    return colored(x, 'white', attrs=['bold'])

@spaceAfter
def positive(x):

    return colored(x, 'green')

@spaceAfter
def negative(x):

    return colored(x, 'red')

@spaceAfter
def success(x):

    return colored(x, 'green', attrs=['bold'])

@spaceAfter
def warning(x):

    return colored(x, 'red', attrs=['bold'])

@spaceAfter
def debugHeader(x):

    return colored(x, 'magenta', attrs=['bold', 'underline'])

@spaceAfter
def debugValue(x):

    return colored(x, 'magenta')

def done():

    return '\t...done'
