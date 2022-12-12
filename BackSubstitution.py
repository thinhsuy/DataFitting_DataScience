class BackSubstitution:
    def is_zero(self, e):
        if ( e == 0 ):
            return True
        return False

    def isStair(self, Matrix):
        for i in range(len(Matrix)):
            for j in range(i):
                if (Matrix[i][j]!=0): 
                    return False
        return True

    def __init__(self, Matrix):
        m=len(Matrix) 
        n=len(Matrix[0]) 
        row = m-1
        col = n -1
        self.typeRoot = "Unknown"
        self.root = list()
        if (len(Matrix)>=len(Matrix[0])):
            raise Exception("The matrix is not right format!")
        elif (not self.isStair(Matrix)):
            raise Exception("The matrix is not on stairs state!")
        while(row >= 0):
            if all(self.is_zero(Matrix[row][i]) for i in range(col)) and Matrix[row][col] != 0: 
                self.typeRoot = "Impossible Equation"
                return 
            elif all(self.is_zero(Matrix[row][i]) for i in range(col)) and Matrix[row][col] == 0:
                row = row - 1
            else:
                break
        #Nghiem duy nhat    
        if row == col-1: 
            root = [] 
            co = col -1
            for i in range(col):
                root.append(0)
            self.typeRoot = "Single Equation"  
            while row >= 0:
                n0 = Matrix[row][col]
                for i in range(col):   
                    n0 -= Matrix[row][i]*root[i] 
                root[co] = n0
                co = co -1
                row = row -1
            self.root = root
            return 
        else:
            # Vo so nghiem
            self.typeRoot = "Innumerable Equation"
            root = []
            xn = []
            co = col - 1 
            xn_row = col + 1 
            temp = col
            for i in range(n):
                for j in range(col): 
                    xn.append(0) 
                root.append(xn)
                xn=[]
            while(row >= 0):
                first_zero_position = [self.is_zero(Matrix[row][i]) for i in range(col)].index(False)
                for i in range (first_zero_position + 1, temp,1):
                    root[i+1][i] = 1 
                root[0][first_zero_position] = Matrix[row][col]
                for i in range(first_zero_position+1,col,1):
                    for j in range(xn_row):
                        root[j][first_zero_position] -= root[j][i]*Matrix[row][i]
                row = row -1
                temp = first_zero_position 
            self.root = root
            return