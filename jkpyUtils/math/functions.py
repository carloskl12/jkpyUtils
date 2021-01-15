'''
Diferentes funciones que aceptan números, listas o tuplas
'''

import math 
from .vector import Vector

def linspace(xinit,xend,npoints):
    delta = (xend - xinit)/(npoints-1)
    xi = xinit
    r = []
    for i in range(npoints):
        r.append(xi)
        xi+=delta
    r[-1] = xend
    return Vector( *r )

def sin(x):
    if isinstance(x, (list,tuple, Vector)):
        r = [math.sin(xi) for xi in x]
        return Vector(*r)
    return math.sin(x)

def cos(x):
    if isinstance(x, (list,tuple,Vector)):
        r = [math.cos(xi) for xi in x]
        return Vector(*r)
    return math.cos(x)


