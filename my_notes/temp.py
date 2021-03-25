# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np
import pylab as pl
import math

def t(n):
    if(n>1):
        return n**2 + 8*t(n//2)
    
    return 1

x = [2**i for i in range(11)]
y = [t(i) for i in x]
print([yi/(xi**2*(2*xi-1)) for xi, yi in zip(x, y)])

pl.plot(x, y)
pl.show()


def get_quadrants(A):
    n = A.shape[0]
    return A[:n//2, :n//2], A[:n//2, n//2:], A[n//2:, :n//2], A[n//2:, n//2:]

def strassen_mult(A: np.ndarray, B: np.ndarray) -> np.ndarray :
    A11, A12, A21, A22 = get_quadrants(A)
    B11, B12, B21, B22 = get_quadrants(B)
    
    P1 = (A11 + A22).dot(B11 + B22)
    P2 = (A21 + A22).dot(B11)
    P3 = A11.dot(B12 - B22)
    P4 = A22.dot(B21 - B11)
    P5 = (A11 + A12).dot(B22)
    
    n = A.shape[0]
    C = np.empty((n, n))
    C[:n//2, :n//2] = P1 + P4 - P5 + (A12 - A22).dot(B21 + B22)
    C[:n//2, n//2:] = P3 + P5
    C[n//2:, :n//2] = P2 + P4
    C[n//2:, n//2:] = P1 + P3 - P2 + (A21 - A11).dot(B11 + B12)
    
    return C


from functools import lru_cache

@lru_cache(10000)
def p(n):
    if(n==1):
        return 1
    
    return sum([p(k)*p(n-k) for k in range(1, n)])


def m(eps, delta, n=100, k=32):
    return math.ceil( 2*( n*k + math.log(2/delta) )  / eps**2)


def plot2d(x, y, f):
    XX, YY = np.meshgrid(x, y)
    Z = f(XX, YY)
    pl.contourf(XX, YY, Z, 50)
    pl.show()
    
def f(x, y):
    if (x < -1 or x > 1):
        return 0.
    if(y>=0 and y <= 1-x**2):
        return 15/4 * x**2
    
    return 0.

fvect = np.vectorize(f)
