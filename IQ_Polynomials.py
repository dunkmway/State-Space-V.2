############ INVERTIBLE QUASIHOMOGENEOUS POLYNOMIALS ############


from functools import reduce
from typing import Tuple
import numpy as np

from Matrix import Matrix
from Root_Of_Unity import RootOfUnity

FERMAT = 0
CHAIN = 1
LOOP = 2

class IQPoly:
    def __init__(self, *args):
        # verify the correct args for input
        for tuple in args:
            type = tuple[0]
            exponents = tuple[1]

            if (
                not isinstance(tuple, Tuple) or 
                not len(tuple) == 2 or 
                not isinstance(type, int) or 
                not isinstance(exponents, list) or
                not all(isinstance(exponent, int) for exponent in exponents)
            ): raise TypeError('IQPoly must be initialized with tuple of the form (atomic form code, list of integer exponents)')

            # check if the exponents are all greater than 1
            if not all(exponent >= 2 for exponent in exponents):
                raise ValueError('All exponents must be greater than or equal to 2')
            if type == FERMAT:
                # check if the exponents list contains only 1 value
                if not len(exponents) == 1:
                    raise ValueError('Fermat type polynomials can only be created with 1 exponent.')
            elif type == CHAIN:
                # check if the exponents list contains 1 or more values
                if not len(exponents) >= 1:
                    raise ValueError('Chain type polynomials can only be created with 1 or more exponents.')
            elif type == LOOP:
                # check if the exponents list contains 2 or more values
                if not len(exponents) >= 2:
                    raise ValueError('Loop type polynomials can only be created with 2 or more exponents.')
        
        # create the exponent matrix
        currentMonomial = 0 # keep track of which monomial we are populating
        totalMonomials = reduce(lambda x, y: x + len(y[1]), args, 0) # use the total number of monomials to initialize the array
        array = np.zeros((totalMonomials, totalMonomials)) # initialze an array with 0's

        # run through the args and add in the correct exponents
        for tuple in args:
            type = tuple[0]
            exponents = tuple[1]
        
            if type == FERMAT:
                # fermat type polynomials are in the form W = x_(1)^(a_1)
                array[currentMonomial][currentMonomial] = exponents[0]
                currentMonomial += 1
            elif type == CHAIN:
                # chain type polynomials are in the form W = x_(1)^(a_1) * x_(2) + x_(2)^(a_2) * x_(3) + ... + x_(n)^(a_n) 
                for idx,exp in enumerate(exponents):
                    array[currentMonomial][currentMonomial] = exp
                    if idx < len(exponents) - 1:
                        array[currentMonomial][currentMonomial + 1] = 1
                    currentMonomial += 1
            elif type == LOOP:
                # loop type polynomials are in the form W = x_(1)^(a_1) * x_(2) + x_(2)^(a_2) * x_(3) + ... + x_(n)^(a_n) * x_(1)
                for idx,exp in enumerate(exponents):
                    array[currentMonomial][currentMonomial] = exp
                    if idx < len(exponents) - 1:
                        array[currentMonomial][currentMonomial + 1] = 1
                    else:
                        array[currentMonomial][currentMonomial - (len(exponents) - 1)] = 1
                    currentMonomial += 1
        
        # exponents will stay as ints
        self.exponent_matrix = Matrix(array)
        self.transpose_exponent_matrix = self.exponent_matrix.transpose()

        # calculate the weights
        self.weights = self.exponent_matrix.intInverse() * Matrix(np.full((len(array), 1), 1))

        # inverse exponents will be cast to roots of unity
        inverse = self.exponent_matrix.intInverse()
        nrows, ncols = inverse.array.shape
        for row in range(nrows):
            for col in range(ncols):
                inverse.array[row,col] = RootOfUnity(inverse.array[row, col])

        self.inverse_exponent_matrix = Matrix(inverse.array)
        self.inverse_transpose_exponent_matrix = self.inverse_exponent_matrix.transpose()

    def __repr__(self):
        return (
            'Invertible Quasihomogeneous Polynomial\n'
            f'{self.toString_W()}\n'
        )

    def __str__(self):
        expM = self.exponent_matrix

        str = 'W = ('
        for i, row in enumerate(expM.array):
            isFirst = True
            for j, element in enumerate(row):
                if element != 0:
                    if not isFirst:
                        str += ' * '
                    if i == j:
                        str += f'x_{j + 1}^{int(element)}'
                    else:
                        str += f'x_{j + 1}'
                    if isFirst:
                        isFirst = False

            str += ') + ('
        return str[0:len(str) - 4]

    def toString_W(self):
        return self.__str__()

    def toString_WT(self):
        expM = self.transpose_exponent_matrix

        str = 'W^T = ('
        for i, row in enumerate(expM.array):
            isFirst = True
            for j, element in enumerate(row):
                if element != 0:
                    if i == j:
                        str += f'x_{j + 1}^{int(element)}'
                    else:
                        str += f'x_{j + 1}'
                    if isFirst:
                        str += ' * '
                        isFirst = False
            str += ') + ('
        return str[0:len(str) - 4]



            
