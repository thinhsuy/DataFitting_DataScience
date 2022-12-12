from math import sqrt
#Xin phép thầy cô cho em được dùng kiểu dữ liệu float16 của numpy, đây là datatype, không phải function
#Kiểu dữ liệu này sẽ cho phép các số em làm ra được làm tròn trong khoảng 16bit
#Dẫn tới việc kết quả sẽ gọn hơn và dễ nhìn hơn
from numpy import float16
#Ngoài ra, em không dùng bất cứ hàm dựng sẵn nào khác của numpy

alist = [line.rstrip() for line in open('input.txt')]
a = list()
for i in range(len(alist)):
    values = alist[i].split(' ')
    a.append([float(value) for value in values])

class GramSchmidt:
    def AnalyzingA(self, a):
        for j in range(len(a[0])):
            self.u.append(list())
            for i in range(len(a)):
                self.u[j].append(a[i][j])

    def __init__(self, a):
        self.a = a
        self.u = list(list())
        self.v = list(list())
        self.q = list(list())
        self.r = list(list())
        self.Status = "None"
        self.AnalyzingA(a)

    def Scalar(self, a, b):
        result = 0
        for i in range(len(a)):
            result += a[i]*b[i]
        return result

    def MultiplyingMatrices(self, A, B):
        result = [[0 for _ in range(len(B))] for _ in range(len(A))]
        for i in range(len(A)):
            for j in range(len(B[0])):
                for k in range(len(B)):
                    result[i][j] += A[i][k] * B[k][j]
        return result

    def NStandard(self, a, b):
        return sqrt(self.Scalar(a, b))

    def MultiplyVector(self, x, vector):
        return [value*x for value in vector]
    
    def Conduct(self):
        for i in range(len(self.u)):
            self.v.append(list())
            self.v[i] = self.u[i]
            for j in range(i):
                numeric = self.Scalar(self.u[i], self.v[j])/self.NStandard(self.v[j], self.v[j])**2
                NewVj = self.MultiplyVector(numeric, self.v[j])
                self.v[i] = [self.v[i][k]-NewVj[k] for k in range(len(self.v[i]))]
            if (self.NStandard(self.v[i], self.v[i])==0):
                print(" => this V has standard is 0")
                self.Status = "Linear Dependence"
                print()
                return
        print()
        self.Status = "Linear Independece"

    def GetStatus(self):
        if (self.Status=="None"): self.Conduct()
        return self.Status

    def Orthonormalize(self):
        if (self.Status=="None"): self.Conduct()
        if (self.Status=="Linear Dependence"): 
            return self.Status
        for i in range(len(self.v)):
            self.q.append(list())
            numeric = 1/self.NStandard(self.v[i], self.v[i])
            self.q[i] = self.MultiplyVector(numeric, self.v[i])
        
        self.q = [[float16(value) for value in row] for row in self.q]

    def QRFactorization(self):
        if (len(self.q)==0): self.Orthonormalize()
        if (self.Status=="Linear Dependence"): return self.Status
        result = self.MultiplyingMatrices(self.q, self.a)
        self.r = [[float16(value) for value in row] for row in result]
        return self.r, self.q

def matrixTransform(matrix):
    temp = [[0 for _ in range(len(matrix))] for _ in range(len(matrix))]
    for j in range(len(matrix[0])):
        for i in range(len(matrix)):
            temp[j][i] = matrix[i][j]
    return temp

R, Q = GramSchmidt(a).QRFactorization()
if Q == "Linear Dependence": print(Q)
else:
    Q = matrixTransform(Q)
    print("Matrix Q:")
    for row in Q:
        print(row)
    print()
    print("Matrix R:")
    for row in R:
        print(row)