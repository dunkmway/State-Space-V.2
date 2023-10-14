from fractions import Fraction

ADDITIVE = 0
MULTIPLICATIVE = 1
_printMode = ADDITIVE

def setPrintMode(mode):
    if mode != ADDITIVE and mode != MULTIPLICATIVE:
        raise ValueError('Print mode must be set to "ADDITIVE" or "MULTIPLICATIVE".')
    global _printMode
    _printMode = mode

# Simple class for representing roots of unity
# the root is stored as a fraction only and string coercion returns the Euler formula form (multiplicative)
# the only valid operation is multiplication with other roots of unity
class RootOfUnity:
    def __init__(self, frac):
        # check if frac is a Fraction
        if not isinstance(frac, Fraction):
            raise TypeError('A root of unity must be initialized with a fraction.')
        self.frac = frac % 1

    def __add__(self, other):
        if other == 0:
            return RootOfUnity(self.frac)

        raise TypeError('A root of unity can only be added by 0')

    def __radd__(self, other):
        return self + other

    def __mul__(self, other):
        # check if other is a matrix
        if isinstance(other, RootOfUnity):
            return RootOfUnity((self.frac + other.frac) % 1)
        
        if other == 0:
            return 0
        
        if other == 1:
            return RootOfUnity(self.frac)

        raise TypeError('A root of unity can only be multipled by another root of unity, 0, or 1')

    def __rmul__(self, other):
        return self * other

    def __eq__(self, other):
        if isinstance(other, RootOfUnity):
            return self.frac == other.frac

        return False

    def __str__(self):
        global _printMode
        if _printMode == ADDITIVE:
            if self.frac == 0:
                return str(1)
            return str(self.frac)
        elif _printMode == MULTIPLICATIVE:
            return f'e^(2πi*{self.frac})'
        else:
            raise ValueError('print mode set to invalid value')

    def toString_additive(self):
        return str(self.frac)
    
    def toString_multiplicative(self):
        return self.__str__()