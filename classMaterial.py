import math

import astropy

print('Me when the impostor is sus')
result = 13 // 4
print('The result is', result, sep=':')
result2 = 13 % 4
print('The result is', result2, sep=':')

value = math.sqrt(30)
print(value)
from sympy import *
x = Symbol('x')
value2 = diff(x**2/42*x)
print(value2)
from astropy import constants as const

print(const.e)
from tabulate import tabulate

table1 = [['one','two','three','four'], ['wat','da','dog','doin']]
print(tabulate(table1))