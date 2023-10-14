import numpy as np
from Root_Of_Unity import RootOfUnity
from fractions import Fraction

class Matrix:
    def __init__(self, arr: np.ndarray) -> None:
        if arr is None or not isinstance(arr, np.ndarray):
            raise TypeError('A matrix must be initialized with a numpy ndarray.')
        if arr.ndim != 2 or not all(len(i) == len(arr[0]) for i in arr):
            raise ValueError('A matrix must be 2 dimensional and rectangular.')

        self.array = arr
    
    def __str__(self):
        m = len(self.array)
        mtxStr = ''
        centerLen = len(max(map(lambda x: str(x), self.array.flatten()), key=len)) + 2
        for i in range(m):
            # mtxStr += ('|' + ', '.join( map(lambda x:'{0:8.3f}'.format(x), self.arr[i])) + '| \n')
            mtxStr += ('|' + ' '.join(map(lambda x: str(x).center(centerLen, ' '), self.array[i])) + '|')
            if i < m - 1:
                mtxStr += '\n'
        return mtxStr

    def __eq__(self, other):
        if isinstance(other, Matrix):
            return np.array_equal(self.array, other.array)
        return False
    
    def __add__(self, other):
        # check if other is a matrix
        if not isinstance(other, Matrix):
            raise TypeError('A matrix can only be added to another matrix.')
        # check if the matrices have the same shape.
        # matrices have to be rectangular so shape should work properly
        if self.array.shape != other.array.shape:
            raise ValueError('A matrix can only be added to another matrix of the same size.')
        
        return Matrix(self.array + other.array)
    
    def __mul__(self, other):
        # check if other is a matrix
        if isinstance(other, Matrix):
            # check if the columns of self is equal to the rows of other
            if self.array.shape[1] != other.array.shape[0]:
                raise ValueError('A matrix can only be multiplied to another matrix where the number columns of the first equal the number of rows of the second.')
            
            return Matrix(self.array @ other.array)
        
        # check if other is a float or int
        if isinstance(other, (float, int)):
            return Matrix(other * self.array)
        
        raise TypeError('A matrix can only be multipled by another matrix, a float, or an int.')

    def __rmul__(self, other):
        # matrix multiplication is handled by __mul__

        # check if other is a float or int
        if isinstance(other, (float, int)):
            return self * other
        
        raise TypeError('A matrix can only be multipled by another matrix, a float, or an int.')

    def __pow__(self, other):
        # check if other is a float or int
        if isinstance(other, (float, int)):
            A = self.copy()
            for _ in range(other - 1):
                A = A * self
            return A
            
        raise TypeError('A matrix can only be raised to a power by a float or an int.')

    def transpose(self):
        return Matrix(self.array.transpose())

    def inverse(self):
        return Matrix(np.linalg.inv(self.array))

    def determinant(self):
        return np.linalg.det(self.array)

    def intInverse(self):
        adj = self.intAdjoint()
        det = self.intDeterminant()

        nrows, ncols = adj.array.shape

        inv = np.zeros([nrows, ncols], dtype=object)
        for row in range(nrows):
            for col in range(ncols):
                inv[row,col] = Fraction(int(adj.array[row,col]), int(det))
        return Matrix(inv)
    
    def intDeterminant(self):
        M = self.array.copy()
        M = [row[:] for row in M] # make a copy to keep original array unmodified
        N, sign, prev = len(M), 1, 1
        for i in range(N-1):
            if M[i][i] == 0: # swap with another row having nonzero i's elem
                swapto = next( (j for j in range(i+1,N) if M[j][i] != 0), None )
                if swapto is None:
                    return 0 # all M[*][i] are zero => zero determinant
                M[i], M[swapto], sign = M[swapto], M[i], -sign
            for j in range(i+1,N):
                for k in range(i+1,N):
                    assert ( M[j][k] * M[i][i] - M[j][i] * M[i][k] ) % prev == 0
                    M[j][k] = ( M[j][k] * M[i][i] - M[j][i] * M[i][k] ) // prev
            prev = M[i][i]
        return int(sign * M[-1][-1])
                
    def intCofactor(self):
        C = np.zeros(self.array.shape)
        nrows, ncols = C.shape
        minor = np.zeros([nrows-1, ncols-1])
        for row in range(nrows):
            for col in range(ncols):
                minor[:row,:col] = self.array[:row,:col]
                minor[row:,:col] = self.array[row+1:,:col]
                minor[:row,col:] = self.array[:row,col+1:]
                minor[row:,col:] = self.array[row+1:,col+1:]
                C[row, col] = (-1)**(row+col) * Matrix(minor).intDeterminant()
        return Matrix(C)


    def intAdjoint(self):
        # transpose of the cofactor matrix
        return self.intCofactor().transpose()

    def verySlow_rootOfUnityInverse(self):
        # this is used when all of the elements in the matrix are zeros or roots of unity
        # since we know that we are working with finite groups elsewhere in the code
        # we can assume that a power of the matrix will be its inverse (Lagrange's Theorem)
        # so will slowly go through all of it's powers until will find the one that is its inverse
        a = np.empty(len(self.array), dtype=object)
        a.fill(RootOfUnity(Fraction()))
        identity = Matrix.diagonal(a)
        found = False
        power = self.copy()
        while (not found):
            power = power * self
            if (power * self == identity):
                found = True
        return power





    def norm(self):
        return np.linalg.norm(self.array)

    def copy(self):
        return Matrix(self.array.copy())

    @classmethod
    def identity(cls, n:int):
        return cls(np.identity(n))
    
    @classmethod
    def diagonal(cls, diag:np.ndarray):
        return cls(np.diag(diag))

    @staticmethod
    # solves ax = b
    def solve(a, b):
        return Matrix(np.linalg.solve(a.arr, b.arr))

