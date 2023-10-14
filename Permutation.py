from logging import root
from Matrix import *
from Root_Of_Unity import *
from fractions import Fraction
import numpy as np
from typing import Tuple, List

class Permutation:
    def __init__(self, cycle, length=None):
        # make sure the parameters are valid
        if (
            not isinstance(cycle, List) or
            not (length == None or isinstance(length, int))
        ): raise TypeError('Permutaion must be initialized in cycle notation with tuples')

        if length and length < 0: raise ValueError('The length must be set to a positive integer.')

        for run in cycle:
            if (
                not isinstance(run, Tuple) or 
                not all(isinstance(num, int) for num in run)
            ): raise TypeError('Permutaion must be initialized in cycle notation with tuples')

        m = max(sum(cycle, ()))

        if not length:
            length = m

        if length < m:
            raise ValueError('The largest integer in the cycle must be less than or equal to the length')

        # add in single cycles of missing ints from 1 to length
        for i in range(1, length + 1):
            if not i in [item for sublist in cycle for item in sublist]:
                cycle.append(tuple([i]))
        

        # initialize a square np zero array of size length
        array = np.zeros((length, length), dtype=object)
        for run in cycle:
            for i in range(len(run)):
                row = run[i] - 1
                column = run[(i + 1) % len(run)] - 1
                array[row][column] = RootOfUnity(Fraction())
        
        self.cycle = cycle
        self.matrix = Matrix(array).transpose()

    def __str__(self):
        str = ''
        for run in self.cycle:
            str += '('
            # we can skip the space if all values in the cycle or single digits
            if max(sum(self.cycle, ())) > 9:
                str += ' '.join(f'{x}' for x in run)
            else:
                str += ''.join(f'{x}' for x in run)
            str += ')'
        return str
    
    def __repr__(self):
        return f'Permutation with matrix\n{str(self.matrix)}'
