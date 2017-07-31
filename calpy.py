# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright (c) 2016 nick-gits                                                #
#                                                                             #
# Permission is hereby granted, free of charge, to any person obtaining a copy#
# of this software and associated documentation files (the "Software"), to    #
# deal in the Software without restriction, including without limitation the  #
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or #
# sell copies of the Software, and to permit persons to whom the Software is  #
# furnished to do so, subject to the following conditions:                    #
#                                                                             #
# The above copyright notice and this permission notice shall be included in  #
# all copies or substantial portions of the Software.                         #
#                                                                             #
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR  #
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,    #
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE #
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER      #
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING     #
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS#
# IN THE SOFTWARE.                                                            #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


import math
RADIAN_MODE  = 0
DEGREE_MODE  = 1
DEBUG =  False       # Set to True to show debugging messages
_mode  = RADIAN_MODE # Set mode to radian by default


operators = {
    # Operator symbol: (Precedence, Operation)
    '+': (1, lambda a, b: a + b),
    '-': (1, lambda a, b: a - b),
    '*': (2, lambda a, b: a * b),
    '/': (2, lambda a, b: a / b),
    '%': (2, lambda a, b: a % b),
    '^': (3, lambda a, b: a ** b)
}


functions = {
    # Function symbol: (n of args, Function)
    'sqrt' : (1, lambda a:     math.sqrt(a)),
    'sin'  : (1, lambda a:          _sin(a)),
    'cos'  : (1, lambda a:          _cos(a)),
    'tan'  : (1, lambda a:          _tan(a)),
    'asin' : (1, lambda a:         _asin(a)),
    'acos' : (1, lambda a:         _acos(a)),
    'atan' : (1, lambda a:         _atan(a)),
    'sinh' : (1, lambda a:         _sinh(a)),
    'cosh' : (1, lambda a:         _cosh(a)),
    'tanh' : (1, lambda a:         _tanh(a)),
    'asinh': (1, lambda a:        _asinh(a)),
    'acosh': (1, lambda a:        _acosh(a)),
    'atanh': (1, lambda a:        _atanh(a)),
    'log'  : (1, lambda a:    math.log10(a)),
    'ln'   : (1, lambda a:      math.log(a)),
    'pow'  : (2, lambda a, b:        a ** b),
    'deg'  : (1, lambda a:  math.degrees(a)),
    'rad'  : (1, lambda a:  math.radians(a)),
    'tog'  : (0, lambda  :    toggle_mode()),
    'mode' : (0, lambda  :       get_mode())
}


specials = {
    # Special symbol: Value
    'pi' : math.pi,
    'e'  : math.e,
    'ans': math.nan, # Changes with every successful call to solve function
}


class CalcSyntaxError(Exception):
    """Raised when invalid input is supplied to the solve function"""
    pass


class CalcOverflowError(Exception):
    """Raised when input number or solution is too large"""
    pass


def solve(raw_exp):
    """
    Return the solution of the provided raw math expression.

    argument(s):
        raw_exp -- string representation of a raw math expression

    return value(s):
        solution -- float equal to the evaluated string expression, can also
                    raise CalcSyntaxError and CalcOverflowError
    """
    if DEBUG:
        print("Debug Info:\nInputted String Expression:\n" + raw_exp)

    raw_exp = raw_exp.lower()
    tokenized_exp = _tokenize_expression(raw_exp)

    for token in tokenized_exp:
        if not _is_valid_token(token):
            raise CalcSyntaxError("Syntax Error: Invalid token(s)")

    postfix_exp = _to_postfix(tokenized_exp)

    # Iterate through postfix_exp, push numbers on to number_stack, once
    # a non-number token is reached in postfix_exp, perform corresponding
    # operation and push the result back on to number_stack.
    number_stack = []
    for token in postfix_exp:
        if _is_number(token):
            number_stack.append(float(token))
        elif token in operators:
            if len(number_stack) >= 2:
                temp = number_stack.pop()
                try:
                    number_stack.append(operators[token][1](number_stack.pop(),
                                                            temp))
                except OverflowError:
                    raise CalcOverflowError("Overflow Error: "\
                                            "Operand too large")
            else:
                raise CalcSyntaxError("Syntax Error: Mismatched operands")
        elif token in functions:
            # TODO: Rewrite below block to allow any number of arguments in a
            #       function, currently only 0, 1 or 2 are allowed.
            if functions[token][0] == 0:
                number_stack.append(functions[token][1]())
            elif functions[token][0] == 1:
                number_stack.append(functions[token][1](number_stack.pop()))
            elif functions[token][0] == 2:
                temp = number_stack.pop()
                number_stack.append(functions[token][1](number_stack.pop(),
                                    temp))
        elif token in specials:
            number_stack.append(specials[token])

    # Solution will be last remaining number on stack.
    if len(number_stack) > 0:
        solution = round(number_stack.pop(), 15)
    else:
        raise CalcSyntaxError("Syntax Error: No operands given")

    # Stops round() from returning -0 under certain circumstances.
    if solution == -0:
        solution += 0

    specials["ans"] = solution
    return solution


def toggle_mode():
    global _mode
    if _mode == 1:
        _mode = 0
        return 0
    elif _mode == 0:
        _mode = 1
        return 1


def get_mode():
    global _mode
    return _mode


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# The functions below are helper or utility functions, not meant to           #
# be externally visible, they are not a part of the API and there             #
# should be no attempts to call any of the below functions from an            #
# outside file, and as such are prepended with an underscore.                 #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


# Recieves a string representing a math expression and returns the same
# expression in the form of a tokenized list.
def _tokenize_expression(raw_exp):
    tokenized_exp = []
    number_buffer = ''
    alpha_buffer  = ''

    for char in raw_exp:
        if _is_number(char) or char == '.':
            if len(alpha_buffer) > 0:
                tokenized_exp.append(alpha_buffer)
                alpha_buffer = ''
            number_buffer += char
        elif char.isalpha():
            if len(number_buffer) > 0:
                tokenized_exp.append(number_buffer)
                number_buffer = ''
            alpha_buffer += char
        elif char in operators or char == '(' or char == ')' or char == ',':
            if len(number_buffer) > 0:
                tokenized_exp.append(number_buffer)
                number_buffer = ''
            elif len(alpha_buffer) > 0:
                tokenized_exp.append(alpha_buffer)
                alpha_buffer = ''
            tokenized_exp.append(char)

    # Checks if there is a leading number or alphabetical token that
    # has not been pushed to tokenized_exp.
    if len(number_buffer) > 0:
        tokenized_exp.append(number_buffer)
    if len(alpha_buffer) > 0:
        tokenized_exp.append(alpha_buffer)

    if DEBUG:
        print('Tokenized Infix:\n' + str(tokenized_exp))

    # Insert implied multiplication operators
    for i in range(len(tokenized_exp) - 1):
        if ((tokenized_exp[i] not in operators and
             tokenized_exp[i+1] not in operators) and not
            (tokenized_exp[i] in functions and tokenized_exp[i+1] == '(') and
             tokenized_exp[i+1] != ')' and tokenized_exp[i] != '('):
            tokenized_exp.insert(i+1, '*')

    if DEBUG:
        print('Tokenized Infix After Handling Implied Multiplication:\n'
              + str(tokenized_exp))

    # Handle negative signs, start with negative numbers raised to a power
    i = 0
    while i < len(tokenized_exp) - 1:
        if tokenized_exp[i] == '^':
            if tokenized_exp[i - 1] == ')': # Left parenthesis
                k, n_parens = i - 2, 0
                while k >= 0:
                    if tokenized_exp[k] == '(':
                        if n_parens == 0:
                            tokenized_exp.insert(k, '(')
                            i += 1
                            break
                        else:
                            n_parens -= 1
                    elif tokenized_exp[k] == ')':
                        n_parens += 1
                    k -= 1
            else:
                tokenized_exp.insert(i - 1, '(')
                i += 1
            if tokenized_exp[i + 1] == '(': # Right parenthesis
                k, n_parens = i + 2, 0
                while k < len(tokenized_exp):
                    if tokenized_exp[k] == ')':
                        if n_parens == 0:
                            tokenized_exp.insert(k, ')')
                            break
                        else:
                            n_parens -= 1
                    elif tokenized_exp[k] == '(':
                        n_parens += 1
                    k += 1
            else:
                if tokenized_exp[i + 1] == '-':
                    tokenized_exp.insert(i + 3, ')')
                else:
                    tokenized_exp.insert(i + 2, ')')
            k, n_parens = i + 1, 0
        i += 1
    # Handle rest of negative signs
    i = 0
    while i < len(tokenized_exp) - 1:
        if tokenized_exp[i] == '-' and ((tokenized_exp[i-1] in operators or
                                        i == 0) or tokenized_exp[i-1] == '('):
            if _is_number(tokenized_exp[i+1]) or tokenized_exp[i+1] in specials:
                tokenized_exp.insert(i, '0')
                tokenized_exp.insert(i, '(')
                tokenized_exp.insert(i+4, ')')
            elif tokenized_exp[i+1] in functions or tokenized_exp[i+1] == '(':
                tokenized_exp.insert(i, 0)
                tokenized_exp.insert(i, '(')
                k = i
                while k < len(tokenized_exp):
                    if tokenized_exp[k] == ')':
                        tokenized_exp.insert(k, ')')
                        break
                    k += 1
        i += 1

    if DEBUG:
        print('Tokenized Infix After Handling Negatives:\n'
              + str(tokenized_exp))

    return tokenized_exp


# Recieves a tokenized list representing a math expression in infix form,
# and returns a tokenized list representing the exprssion in postfix form.
# Implementation of Shunting-yard algorithm.
# See: https://en.wikipedia.org/wiki/Shunting-yard_algorithm
def _to_postfix(infix_exp):
    postfix_exp = []
    op_stack    = []

    for token in infix_exp:
        if _is_number(token):
            postfix_exp.append(token)
        elif token in operators:
            while ((len(op_stack) > 0 and op_stack[-1] in operators) and
                    ((token != '^' and
                        operators[token][0] <= operators[op_stack[-1]][0]) or
                    (token == '^' and
                        operators[token][0] < operators[op_stack[-1]][0]))):
                postfix_exp.append(op_stack.pop())
            op_stack.append(token)
        elif token in functions:
            op_stack.append(token)
        elif token in specials:
            if token == 'ans' and math.isnan(specials['ans']):
                raise CalcSyntaxError("Syntax Error: Ans never defined")
            postfix_exp.append(token)
        elif token == '(':
            op_stack.append(token)
        elif token == ')':
            while len(op_stack) > 0 and op_stack[-1] != '(':
                postfix_exp.append(op_stack.pop())
            if len(op_stack) == 0:
                raise CalcSyntaxError("Syntax Error: "\
                                      "Mismatched parenthesis")
            op_stack.pop()
            if len(op_stack) > 0 and op_stack[-1] in functions:
                postfix_exp.append(op_stack.pop())
        elif token == ',':
            while len(op_stack) > 0 and op_stack[-1] != '(':
                postfix_exp.append(op_stack.pop())
            if len(op_stack) == 0:
                raise CalcSyntaxError("Syntax Error: "\
                                      "Mismatched or missing parenthesis")
    while len(op_stack) > 0:
        if op_stack[-1] == '(' or op_stack[-1] == ')':
            raise CalcSyntaxError("Syntax Error: Mismatched parenthesis")
        postfix_exp.append(op_stack.pop())

    if DEBUG:
        print('Tokenized Postfix:\n' + str(postfix_exp))

    return postfix_exp


# Recieves a string, returns true if it can be casted to a float.
def _is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


# Returns true if the provided string is a recognized operator, function,
# special, number or other character accepted in math expressions.
def _is_valid_token(token):
    if ((token in operators) or
       (token in functions)  or
       (token in specials)   or
       (_is_number(token))   or
       (token in ['(', ')', ','])):
       return True
    else:
       return False


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# The functions below are math functions, only for internal use. Do not call  #
# these functions from an external file. If you added your own function to    #
# the functions dictionary, define the actual function below (Unless it is    #
# simple enough to place in a lambda on its own).                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


def _sin(x):
    return math.sin(x) if _mode == RADIAN_MODE else math.sin(math.radians(x))


def _cos(x):
    return math.cos(x) if _mode == RADIAN_MODE else math.cos(math.radians(x))


def _tan(x):
    return math.tan(x) if _mode == RADIAN_MODE else math.tan(math.radians(x))


def _asin(x):
    try:
        if _mode == RADIAN_MODE:
            return math.asin(x)
        else:
            return math.asin(math.radians(x))
    except ValueError:
        raise CalcSyntaxError("Domain Error")


def _acos(x):
    try:
        if _mode == RADIAN_MODE:
            return math.acos(x)
        else:
            return math.acos(math.radians(x))
    except ValueError:
        raise CalcSyntaxError("Domain Error")


def _atan(x):
    return math.atan(x) if _mode == RADIAN_MODE else math.atan(math.radians(x))


def _sinh(x):
    return math.sinh(x) if _mode == RADIAN_MODE else math.sinh(math.radians(x))


def _cosh(x):
    return math.cosh(x) if _mode == RADIAN_MODE else math.cosh(math.radians(x))


def _tanh(x):
    return math.tanh(x) if _mode == RADIAN_MODE else math.tanh(math.radians(x))


def _asinh(x):
    return math.asinh(x) if _mode==RADIAN_MODE else math.asinh(math.radians(x))


def _acosh(x):
    try:
        if _mode == RADIAN_MODE:
            return math.acosh(x)
        else:
            return math.acosh(math.radians(x))
    except ValueError:
        raise CalcSyntaxError("Domain Error")


def _atanh(x):
    try:
        if _mode == RADIAN_MODE:
            return math.atanh(x)
        else:
            return math.atanh(math.radians(x))
    except ValueError:
        raise CalcSyntaxError("Domain Error")
