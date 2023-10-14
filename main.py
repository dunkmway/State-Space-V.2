from Matrix import *
import Root_Of_Unity as ROI
import IQ_Polynomials as IQP
from Permutation import *
import Symmetry_Groups as SG
from fractions import Fraction


def main():
    ROI.setPrintMode(ROI.ADDITIVE)

    # W = IQP.IQPoly(
    #     (IQP.LOOP, [3,3,3,3,3,3])
    # )
    # W = IQP.IQPoly(
    #     (IQP.CHAIN, [4,5,3,2])
    # )
    W = IQP.IQPoly(
        (IQP.FERMAT, [4]),
        (IQP.FERMAT, [4]),
        (IQP.FERMAT, [4]),
        (IQP.FERMAT, [4])
    )
    # print(W)
    # print(W.weights)
    # print(W.inverse_exponent_matrix)
    # print(W.exponent_matrix.intDeterminant())

    file = open('Output.txt', 'w')
    file.write(str(W) + '\n')
    file.write(str(W.weights) + '\n')
    file.write(str(W.inverse_exponent_matrix) + '\n')

    P = Permutation([(1,2,3)], 4)
    P_2 = Permutation([(1,3,2)], 4)
    # P = Permutation([(1,2,3)])

    G_MAX = SG.SymGroup(W, [P])
    # G_MAX = SG.SymGroup(W, [P, P_2])
    # G_MAX = SG.SymGroup(W)


    print(repr(G_MAX))
    gens = '\n'.join(f'{str(gen)}\n' for gen in G_MAX.generators)
    elems = '\n'.join(f'{elem}\n' for elem in G_MAX.elements)
    # # genRepr = '\n'.join(f'{elem}\n' for elem in G_MAX.element_generator_representation)
    # print('Generators:')
    # print(gens)
    # print('Elements:')
    # print(elems)
    # # print('Generator Representation:')
    # # print(genRepr)
    # print(f'Conjugacy Classes:')

    file.write('Generators:\n')
    file.write(gens + '\n')
    file.write('ELements:\n')
    file.write(elems + '\n')

    file.write('Conjugacy Classes:\n')
    for index, cc in enumerate(G_MAX.conjugacyClasses):
        # print(f'Conjugacy Class Number {index + 1} with size {len(cc)}.')
        # print('\n'.join(f'{elem}\n' for elem in cc))

        file.write(f'Conjugacy Class Number {index + 1} with size {len(cc)}.\n')
        file.write('\n'.join(f'{elem}\n' for elem in cc) + '\n')

    file.close()



    
if __name__ == "__main__":
    main()