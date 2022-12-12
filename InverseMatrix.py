class InverseMatrix:
    def __init__(self, A):
        self.Matrix = A
        if (len(self.Matrix)!=len(self.Matrix[0])):
            raise Exception("This is not square matrix")
        self.Matrix = self.Converse(self.Matrix)

    def Converse(self, Matrix):
        R = list(list())
        for i in range(len(Matrix)):
            R.append(list())
            for j in range(len(Matrix[0])):
                if (j==i):R[i].append(1)
                else: R[i].append(0)
        return R