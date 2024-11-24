# test_script.py

# Blatant issue 1: SyntaxError - Missing closing parenthesis
def greet(name):
    print("Hello, " + name  # Missing closing parenthesis

# Blatant issue 2: NameError - Undefined variable
def add_numbers(a, b):
    result = a + b
    print("Result: ", resut)  # Misspelled variable 'result'

# Subtle issue 1: Unused import
import os  # This import is never used

# Subtle issue 2: Unnecessary semicolon
def calculate_area(radius):
    area = 3.14 * radius * radius;
    return area

# Subtle issue 3: Function defined but never used
def unused_function():
    pass  # This function is never called

# Subtle issue 4: Variable reassignment (less readable code)
def process_data(data):
    result = data
    result = result.strip()  # Reassigning 'result' without any need
    return result

# Subtle issue 5: Too many local variables in function
def process_file(filename):
    with open(filename, 'r') as file:
        data = file.read()
        words = data.split()
        word_count = len(words)
        line_count = len(data.splitlines())
        char_count = len(data)
        return line_count, word_count, char_count

# Subtle issue 6: Too many lines in function
def long_function():
    x = 1
    y = 2
    z = x + y
    a = x * y
    b = a - z
    c = b + x
    d = c * 2
    e = d - x
    f = e * y
    g = f - a
    h = g + b
    i = h - c
    j = i + d
    k = j - e
    l = k + f
    m = l - g
    n = m + h
    o = n - i
    p = o + j
    q = p - k
    r = q + l
    s = r - m
    t = s + n
    u = t - o
    v = u + p
    w = v - q
    return w

# Blatant issue 3: IndentationError (incorrect indentation)
def say_hello():
    if True:
        print("Hello")
         print("Indented wrong")  # Indentation error here

