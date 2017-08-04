# calpy
calpy is a simple, light weight math expression parser and calculator module which takes a string representation of a math expression via the solve function as input, and returns a float representation of the solution. 

## Usage:
```
import calpy


calpy.solve("(1+2)^2+16/4") # returns 13.0


calpy.solve("sin(pi/2)+cos(pi)+pi") # returns 3.14159...


calpy.solve("e^(ln(e))") # returns 2.71828...


calpy.solve("6^2/2(3)+4") # returns 58.0


calpy.solve("-1(-1)-1-1") # returns -1.0
```


## Supported Features:
Nested parentheses, negative numbers, and implied multiplication are all corectly parsed. The below operators, functions and constants are all supported.

|Operators|Functions|Specials|
|---------|:-----------|:-----|
|(+) Addition|sin(x)|pi (3.141592...)|
|(-) Subtraction|cos(x)|e (2.71828...)|
|(*) Multiplication|tan(x)|ans (Previous answer)|
|(/) Division|asin(x)|
|(%) Modulo|acos(x)|
|(^) Exponent|atan(x)|
|            |sinh(x)|
|            |cosh(x)|
|            |tanh(x)|
|            |asinh(x)|
|            |acosh(x)|
|            |atanh(x)|
|            |log(x)|
|            |ln(x)|
|            |pow(x, y)|
|            |deg(x)|
|            |rad(x)|
|            |sqrt(x)|
|            |tog(x)|
|            |mode(x)|
  
  ## Installation:
  calpy is not not registered in the Python Packaging Index, but the entire module is only a single file. Download the calpy.py source file, import it into your project, and it will be ready for use. Refer to the test.py file to see how to properly implement and errorcheck.
