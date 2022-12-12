import copy
from InverseMatrix import *

alist = [line.rstrip() for line in open('input.txt')]
a = list()
for i in range(len(alist)):
    values = alist[i].split(' ')
    a.append([float(value) for value in values])


#Class Gauss(A) would pass a Matrix as a reference
#Gauss(A).Elimination() would return A matrix after being eliminated
#Gauss(A).Jordan() would return A matrix afted being converted
# example: return {"Matrix"}

# if Gauss(A).setIdentityMatrix(I) is called 
# => all above funtions would return 2 matrixes instead
# example: return {"Matrix", "Identity"}



class Gaussian:
    def __init__(self, A):
        self.maze = A
        self.IdentityMatrix = list(list())
    
    def GetIdentityMatrix(self, Matrix):
        R = list(list())
        for i in range(len(Matrix)):
            R.append(list())
            for j in range(len(Matrix[0])):
                if (j==i):R[i].append(1.0)
                else: R[i].append(0.0)
        return R
    
    def isStair(self, Matrix):
        for i in range(len(Matrix)):
            for j in range(i):
                if (Matrix[i][j]!=0): 
                    return False
        return True

    def row_switch(self, Matrix,i,j):
        for k in range(len(Matrix[0])):
            tmp=Matrix[i][k]
            Matrix[i][k]=Matrix[j][k]
            Matrix[j][k]=tmp
        return Matrix

    def mul_scaler(self, Matrix,i,alpha):
        for k in range(len(Matrix[0])):
            Matrix[i][k]=Matrix[i][k]*alpha
        return Matrix

    def add_row(self, Matrix,i,j,alpha):
        for k in range(len(Matrix[0])):
            Matrix[i][k] = Matrix[i][k] + Matrix[j][k]*alpha
        return Matrix

    def is_zero(self, e):
        if ( e == 0 ):
            return True
        return False

    def calc_rows(self, Matrix, rowTarget, rowReference, extraValue):
        for j in range(len(Matrix[0])):
            Matrix[rowTarget][j] += extraValue * Matrix[rowReference][j]
        return Matrix
    
    def setIdentityMatrix(self, I):
        self.IdentityMatrix = I

    def Elimination(self):
        if (len(self.IdentityMatrix)!=0): isAI = True
        else: isAI = False
        R=copy.deepcopy(self.maze)
        if (isAI): I = copy.deepcopy(self.IdentityMatrix)
        else: I = list()
        m=len(R)
        n=len(R[0])
        row=0
        col=0
        while (row<m):
            while (col<n) and (all(self.is_zero(R[i][col]) for i in range(row,m))):
                col=col+1
            if col==n: 
                break
                
            pivot_row = row + [not self.is_zero(R[i][col]) for i in range(row,m)].index(True)

            R = self.row_switch(R,row,pivot_row)
            if (isAI): 
                I = self.row_switch(I,row,pivot_row)

            alphaValue = 1/R[row][col]
            R = self.mul_scaler(R,row,alphaValue)
            if (isAI): 
                I = self.mul_scaler(I,row,alphaValue)

            for k in range(row+1,m):
                if (R[k][col] != 0):
                    alphaValue = -(R[k][col])
                    R = self.add_row(R,k,row, alphaValue)
                    if (isAI): I = self.add_row(I,k,row, alphaValue)
            row=row+1

        return {"Matrix": R, "Identity": I}
    
    def checkIsConverseSuccessfully(self, Matrix):
        for i in range(len(Matrix)):
            for j in range(len(Matrix)):
                if (i==j and Matrix[i][j]!=1): return False
                elif (i!=j and Matrix[i][j]!=0): return False
        return True


    def Jordan(self):
        if (len(self.maze)!=len(self.maze[0])):
            raise Exception("Matrix is not square matrix")
        if (len(self.IdentityMatrix)!=0): isAI = True
        R=copy.deepcopy(self.maze)
        if (isAI): I=copy.deepcopy(self.IdentityMatrix)
        else: I = list()
        if (not self.isStair(R)): 
            X = self.Elimination()
            R = X["Matrix"]
            I = X["Identity"]
        n = len(R)
        m = len(R[0])
        for i in range(n-1):
            for j in range(i+1, n):   
                if (R[i][j]==0): continue
                div = -(R[i][j]/R[j][j])
                R = self.calc_rows(R, i, j, div)
                if (isAI): I = self.calc_rows(I, i ,j, div)
                continue
        if (not self.checkIsConverseSuccessfully(R)):
            print("This matrix is irreversible")
            R.clear()
            I.clear() 
        return {"Matrix": R, "Identity": I}