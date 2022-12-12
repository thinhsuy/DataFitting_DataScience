from numpy import *
from Gaussian import *
from Polynominal import *
from BackSubstitution import *

#numpy.poly1d() would help to define Polynominal with the format [a,b,c] => ax^2 + bx + c
#incase the rule not allow to use library, just define a class that contains the above formula

alist = [line.rstrip() for line in open('input.txt')]
A = list()
for i in range(len(alist)):
    values = alist[i].split(' ')
    A.append([float16(value) for value in values])

class Diagonalize:
    def __init__(self, A):
        self.matrix = A
        self.size = len(self.matrix)
        self.enigentVector = list()
        self.enigentVariable = list()
        
    def ConvertEigentMatrix(self):
        R = list(list())
        for i in range(self.size):
            R.append(list())
            for j in range(self.size):
                if (i==j): 
                    R[i].append(poly1d([1, -self.matrix[i][j]]))
                else: 
                    R[i].append(poly1d([-self.matrix[i][j]]))
        return R
    
    def SplitMatrix(self, maze, position):
        #split the matrix that excluding the row and col of position
        B=list(list())
        x=-1
        for i in range(self.size):
            if i==position[0]: continue
            B.append(list())
            x+=1
            for j in range(self.size):
                if (j==position[1]): continue
                B[x].append(maze[i][j])
        return B

    def Determinant(self, maze):
        if len(maze)==2:
            return maze[0][0]*maze[1][1] - maze[0][1]*maze[1][0]
        else:
            result = poly1d([0])
            #recursively calculating value of det
            for i in range(self.size):
                result += maze[0][i]*((-1)**(i+2))*self.Determinant(self.SplitMatrix(maze, (0, i)))
            return result

    def getRoots_of_polynomial(self, polynominal):
        #convert all results into float16 to avoid complex numbers
        afterConverse = [float16(value) for value in roots(poly1d(polynominal.coef))]
        #remove duplicate roots
        return list(dict.fromkeys(afterConverse))

    def ApplyEquationToPolyn(self, coef, equation):
        value = 0
        for i in range(len(coef)):
            if (i==len(coef)-1): value+=coef[i]
            else:
                value += coef[i]*(equation**(len(coef)-1-i))
        return value

    def ApplyEquationBackAI(self, maze, equation):
        M = list(list())
        for i in range(self.size):
            M.append(list())
            for j in range(self.size):
                M[i].append(self.ApplyEquationToPolyn(maze[i][j].coef, equation))
        return M

    def LinearPolySolving(self, matrix):
        for row in matrix: row.append(0)
        gauss = Gaussian(matrix).Elimination()["Matrix"]
        bs = BackSubstitution(gauss).root
        for P_list in bs:
            if (any(P_list)):
                self.enigentVector.append(P_list)

    def FullyOperatingAlgorithm(self):
        #step 1: convert matrix A to [YI-A]
        self.matrixIA = self.ConvertEigentMatrix()
        #step 2: calculate Det[YI-A]
        AI_polynominal = self.Determinant(self.matrixIA)
        #step 3: get roots of polymonial of Det[YI-A]=0
        self.enigentVariable = self.getRoots_of_polynomial(AI_polynominal)
        #step 4: foreach root, get the matrix after applying to [YI-A]
        for root in self.enigentVariable:
            matrix = self.ApplyEquationBackAI(self.matrixIA, root)
            #step 5: foreach matrix after applying Lambda, calculate the roots which would be engientVector
            self.LinearPolySolving(matrix)
        return self.enigentVector

D = Diagonalize(A)
matrix = D.FullyOperatingAlgorithm()
print(matrix)
