from cmath import *
from numpy import *

class Poly:
    def __init__(self, coef):
        self.coef = coef
        self.size = len(self.coef)
        self.level = self.size-1

    def __str__(self):
        str = ""
        for i in range(self.size):
            if (self.size-1-i==0): str+= f"[{self.coef[i]}] "
            elif (self.size-1-i==1): str+= f"[{self.coef[i]}x] "
            else: str += f"[{self.coef[i]}x^{self.size-1-i}] "
        return str
    
    def __add__(self, target):
        A, B = sorted([self.coef, target.coef], key=len)
        for i, x in enumerate(reversed(A), 1):
            B[-i]+=x
        return Poly(B)

    
    def __sub__(self, target):
        A, B = sorted([self.coef, target.coef], key=len)
        for i, x in enumerate(reversed(A), 1):
            B[-i]-=x
        return Poly(B)

    def __mul__(self, target):
        if type(target) == type(1):
            return Poly([float16(value)*float16(target) for value in self.coef])
        if type(target) == type(0.0):
            return Poly([float16(value)*target for value in self.coef])
        valueList = list(tuple())
        for i in range(self.size):
            for j in range(target.size):
                value = self.coef[i]*target.coef[j]
                level = (self.size-1-i)+(target.size-1-j)
                valueList.append((value, level))
        valueList = sorted(valueList, key=lambda x: x[1], reverse=True)
        newArr = [0 for _ in range(valueList[0][1]+1)]
        for value in valueList:
            newArr[value[1]] += value[0]
        newArr.reverse()
        return Poly(newArr)

#(x^2+2x+3)*(x+2) = (x^3 + 2x^2 + 2x^2 + 4x + 3x + 6)
                 # = (x^3 + 4x^2 + 7x + 6)


class EquationSolving:
    def __init__(self, arr):
        self.coef = arr
        self.size = len(self.coef)
    
    def getRoots(self):
        if (self.size == 1): 
            return self.coef[0]

        if (self.size == 2): 
            return self.SingleEquation(self.coef[1], self.coef[0])
        if (self.size == 3 and self.coef[0]==0):
            return self.SingleEquation(self.coef[2], self.coef[1])

        if (self.size == 3):
            return self.QuadraticEquation(self.coef[0], self.coef[1], self.coef[2])
        if (self.size == 4 and self.coef[0]==0):
            return self.QuadraticEquation(self.coef[1], self.coef[2], self.coef[3])

        else: roots(poly1d(self.coef))

    def SingleEquation(self, a, b):
        return (-b/a)

    def QuadraticEquation(self, a, b, c):
        d = (b**2) - (4*a*c)
        x1 = (-b-sqrt(d))/(2*a)
        x2 = (-b+sqrt(d))/(2*a)
        return [x1, x2]