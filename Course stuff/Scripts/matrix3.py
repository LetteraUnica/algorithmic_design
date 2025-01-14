from __future__ import annotations

from numbers import Number
from typing import List
from typing import Tuple


def gauss_matrix_mult(A: Matrix, B: Matrix) -> Matrix:
    ''' Multiply two matrices by using Gauss's algorithm

    Parameters
    ----------
    A: Matrix
        The first matrix to be multiplied
    B: Matrix
        The second matrix to be multiplied

    Returns
    -------
    Matrix
        The row-column multiplication of the matrices passed as parameters

    Raises
    ------
    ValueError
        If the number of columns of `A` is different from the number of
        rows of `B`
    '''

    if A.num_of_cols != B.num_of_rows:
        raise ValueError('The two matrices cannot be multiplied')

    result = [[0 for col in range(B.num_of_cols)] for row in range(A.num_of_rows)]

    for row in range(A.num_of_rows):
        for col in range(B.num_of_cols):
            value = 0
            for k in range(A.num_of_cols):
                value += A[row][k] * B[k][col]

            result[row][col] = value

    return Matrix(result, clone_matrix=False)

# auxiliary function used to split the matrix in four quadrants: use 'submatrix' method of 'Matrix' class
def get_matrix_quadrants(A: Matrix) -> Tuple[Matrix, Matrix, Matrix, Matrix]:
    A11 = A.submatrix(0 , A.num_of_rows//2, 0, A.num_of_cols//2)
    A12 = A.submatrix(0 , A.num_of_rows//2, A.num_of_cols//2, A.num_of_cols//2)
    A21 = A.submatrix(A.num_of_rows//2, A.num_of_rows//2, 0, A.num_of_cols//2)
    A22 = A.submatrix(A.num_of_rows//2, A.num_of_rows//2, A.num_of_cols//2, A.num_of_cols//2)

    return A11, A12, A21, A22

def get_matrix_quadrant(A: Matrix, i: Int, j: Int) -> Matrix:
    ''' Return selected matrix quadrant

    Parameters
    ----------
    A: Matrix
        The first matrix to be multiplied
    i, j: Integers
        Coordinates of the desired quadrant 

    Returns
    -------
    Matrix
        The quadrant corresponding to the Aij sub-matrix of the matrix A

    Raises
    ------
    ValueError
        If the pair i,j does not correspond to one of the four matrix quadrants
    '''

    if i<1 or i>2 or j<1 or j>2:
        raise ValueError('unidentified quadrant')

    return A.submatrix((i-1)*A.num_of_rows//2,A.num_of_rows//2, (j-1)*A.num_of_cols//2, A.num_of_cols//2)

def S(A: Matrix, i: Int, j: Int, l: Int, m: Int) -> Matrix:

    if i==l or i==j and l==m:
        S_matrix = get_matrix_quadrant(A,i,j) + get_matrix_quadrant(A,l,m)
    else:
        S_matrix = get_matrix_quadrant(A,i,j) - get_matrix_quadrant(A,l,m)
    
    return S_matrix

def S(A: Matrix, i: Int, j: Int, l: Int, m: Int) -> Matrix:

    if i==l or i==j and l==m:
        return get_matrix_quadrant(A,i,j) + get_matrix_quadrant(A,l,m)
    else:
        return get_matrix_quadrant(A,i,j) - get_matrix_quadrant(A,l,m)

def strassen_matrix_mult(A: Matrix, B: Matrix) -> Matrix:

    original_nrows_A = A.num_of_rows
    original_ncols_B = B.num_of_cols

    # check dimension of matrices: if small dont bother with strassen algorithm and use divide-conquer algorithm
    # this is base case: during theory we decided as base case n=1, with no consequence on the complexity (remember final result didnt depend on base case, since changing the base case
    # would just mean reducing the height of the tree, not the behavior of the algorithm)
    # But why below this 32 gauss algorithm could be much better: recursive steps and calls require a very large amount of memory due to extensive use of sums (much more than the usage done in the
    # naive algorithm), other than 7 recursive calls, which require again to save spaces for other sums and so on.
    if max(A.num_of_rows, B.num_of_cols, A.num_of_cols) < 32:
        return gauss_matrix_mult(A,B)

    if A.num_of_rows%2 != 0:
        A.insert_row()

    if A.num_of_cols%2 != 0:
        A.insert_column()
        B.insert_row()

    if B.num_of_cols%2 != 0:
        B.insert_column()
    
    # recursive step
    # A11, A12, A21, A22 = get_matrix_quadrants(A)
    # B11, B12, B21, B22 = get_matrix_quadrants(B)

    # First batch of sums [Theta(n^2)]
    # S1 = B12 - B22
    # S2 = A11 + A12
    # S3 = A21 + A22
    # S4 = B21 - B11
    # S5 = A11 + A22
    # S6 = B11 + B22
    # S7 = A12 - A22
    # S8 = B21 + B22
    # S9 = A11 - A21
    # S10 = B11 + B12

    # recursive calls: needed, because if I perform the naive solution the complexity would not change
    # P1 = strassen_matrix_mult(get_matrix_quadrant(A,1,1), S(B,1,2,2,2))
    # P2 = strassen_matrix_mult(S(A,1,1,1,2), get_matrix_quadrant(B,2,2))
    # P3 = strassen_matrix_mult(S(A,2,1,2,2), get_matrix_quadrant(B,1,1))
    # P4 = strassen_matrix_mult(get_matrix_quadrant(A,2,2), S(B,2,1,1,1))
    # P5 = strassen_matrix_mult(S(A,1,1,2,2), S(B,1,1,2,2))

    # P1 = strassen_matrix_mult(A11, S_matrix(1,B12,B22))
    # P2 = strassen_matrix_mult(S_matrix(2,A11,A12), B22)
    # P3 = strassen_matrix_mult(S_matrix(3,A21,A22), B11)
    # P4 = strassen_matrix_mult(A22, S_matrix(4,B21,B11))
    # P5 = strassen_matrix_mult(S_matrix(5,A11,A22), S_matrix(6,B11,B22))

    # P6 = strassen_matrix_mult(S(A,1,2,2,2), S(B,2,1,2,2))
    # P7 = strassen_matrix_mult(S(A,1,1,2,1), S(B,1,1,1,2))

    # Second batch of sums [Thate(n^2)]
    # C11 = P5 + P4 - P2 + P6
    # C12 = P1 + P2 
    # C21 = P3 + P4
    # C22 = P5 + P1 - P3 - P7

    result = Matrix([[0 for x in range(B.num_of_cols)] for y in range(A.num_of_rows)], clone_matrix=False)

    # use 'assign_submatrix' method of 'Matrix' class to build resulting matrix
    result.assign_submatrix(0, 0, strassen_matrix_mult(S(A,1,1,2,2), S(B,1,1,2,2)) + strassen_matrix_mult(get_matrix_quadrant(A,2,2), S(B,2,1,1,1)) 
    - strassen_matrix_mult(S(A,1,1,1,2), get_matrix_quadrant(B,2,2)) + strassen_matrix_mult(S(A,1,2,2,2), S(B,2,1,2,2)))
    result.assign_submatrix(0, result.num_of_cols//2, strassen_matrix_mult(get_matrix_quadrant(A,1,1), S(B,1,2,2,2)) + strassen_matrix_mult(S(A,1,1,1,2), get_matrix_quadrant(B,2,2)))
    result.assign_submatrix(result.num_of_rows//2, 0, strassen_matrix_mult(S(A,2,1,2,2), get_matrix_quadrant(B,1,1)) + strassen_matrix_mult(get_matrix_quadrant(A,2,2), S(B,2,1,1,1)))
    result.assign_submatrix(result.num_of_rows//2, result.num_of_cols//2, strassen_matrix_mult(S(A,1,1,2,2), S(B,1,1,2,2)) + strassen_matrix_mult(get_matrix_quadrant(A,1,1), S(B,1,2,2,2))
     - strassen_matrix_mult(S(A,2,1,2,2), get_matrix_quadrant(B,1,1)) - strassen_matrix_mult(S(A,1,1,2,1), S(B,1,1,1,2)))

    # result.assign_submatrix(0, 0, P5 + P4 - P2 + strassen_matrix_mult(S_matrix(7,A12,A22), S_matrix(8,B21,B22)))
    # result.assign_submatrix(0, result.num_of_cols//2, P1 + P2)
    # result.assign_submatrix(result.num_of_rows//2, 0, P3 + P4)
    # result.assign_submatrix(result.num_of_rows//2, result.num_of_cols//2, P5 + P1 - P3 - strassen_matrix_mult(S_matrix(9,A11,A21), S_matrix(10,B11,B12)))


    result = result.submatrix(0, original_nrows_A, 0, original_ncols_B)

    return result

class Matrix(object):
    ''' A simple naive matrix class

    Members
    -------
    _A: List[List[Number]]
        The list of rows that store all the matrix values

    Parameters
    ----------
    A: List[List[Number]]
        The list of rows that store all the matrix values
    clone_matrix: Optional[bool]
        A flag to require a full copy of `A`'s data structure.

    Raises
    ------
    ValueError
        If there are two lists having a different number of values
    '''
    def __init__(self, A: List[List[Number]], clone_matrix: bool = True):
        num_of_cols = None

        for i, row in enumerate(A):
            if num_of_cols is not None:
                if num_of_cols != len(row):
                    raise ValueError('This is not a matrix')
            else:
                num_of_cols = len(row)

        if clone_matrix:
            self._A = [[value for value in row] for row in A]
        else:
            self._A = A

    @property
    def num_of_rows(self) -> int:
        return len(self._A)

    @property
    def num_of_cols(self) -> int:
        if len(self._A) == 0:
            return 0

        return len(self._A[0])

    def copy(self):
        A = [[value for value in row] for row in self._A]

        return Matrix(A, clone_matrix=False)

    def __getitem__(self, y: int):
        ''' Return one of the rows

        Parameters
        ----------
        y: int
            the index of the rows to be returned

        Returns
        -------
        List[Number]
            The `y`-th row of the matrix
        '''
        return self._A[y]

    def __iadd__(self, A: Matrix) -> Matrix:
        ''' Sum a matrix to this matrix and update it

        Parameters
        ----------
        A: Matrix
            The matrix to be summed up

        Returns
        -------
        Matrix
            The matrix corresponding to the sum between this matrix and
            that passed as parameter

        Raises
        ------
        ValueError
            If the two matrices have different sizes
        '''

        if (self.num_of_cols != A.num_of_cols or
                self.num_of_rows != A.num_of_rows):
            raise ValueError('The two matrices have different sizes')

        for y in range(self.num_of_rows):
            for x in range(self.num_of_cols):
                self[y][x] += A[y][x]

        return self

    def __add__(self, A: Matrix) -> Matrix:
        ''' Sum a matrix to this matrix

        Parameters
        ----------
        A: Matrix
            The matrix to be summed up

        Returns
        -------
        Matrix
            The matrix corresponding to the sum between this matrix and
            that passed as parameter

        Raises
        ------
        ValueError
            If the two matrices have different sizes
        '''
        res = self.copy()

        res += A

        return res

    def __isub__(self, A: Matrix) -> Matrix:
        ''' Subtract a matrix to this matrix and update it

        Parameters
        ----------
        A: Matrix
            The matrix to be subtracted up

        Returns
        -------
        Matrix
            The matrix corresponding to the subtraction between this matrix and
            that passed as parameter

        Raises
        ------
        ValueError
            If the two matrices have different sizes
        '''

        if (self.num_of_cols != A.num_of_cols or
                self.num_of_rows != A.num_of_rows):
            raise ValueError('The two matrices have different sizes')

        for y in range(self.num_of_rows):
            for x in range(self.num_of_cols):
                self[y][x] -= A[y][x]

        return self

    def __sub__(self, A: Matrix) -> Matrix:
        ''' Subtract a matrix to this matrix

        Parameters
        ----------
        A: Matrix
            The matrix to be subtracted up

        Returns
        -------
        Matrix
            The matrix corresponding to the subtraction between this matrix and
            that passed as parameter

        Raises
        ------
        ValueError
            If the two matrices have different sizes
        '''
        res = self.copy()

        res -= A

        return res

    def __mul__(self, A: Matrix) -> Matrix:
        ''' Multiply one matrix to this matrix

        Parameters
        ----------
        A: Matrix
            The matrix which multiplies this matrix

        Returns
        -------
        Matrix
            The row-column multiplication between this matrix and that passed
            as parameter

        Raises
        ------
        ValueError
            If the number of columns of this matrix is different from the
            number of rows of `A`
        '''
        return gauss_matrix_mult(self, A)

    def __rmul__(self, value: Number) -> Matrix:
        ''' Multiply one matrix by a numeric value

        Parameters
        ----------
        value: Number
            The numeric value which multiplies this matrix

        Returns
        -------
        Matrix
            The multiplication between `value` and this matrix

        Raises
        ------
        ValueError
            If `value` is not a number
        '''

        if not isinstance(value, Number):
            raise ValueError('{} is not a number'.format(value))

        return Matrix([[value*elem for elem in row] for row in self._A],
                      clone_matrix=False)

    def submatrix(self, from_row: int, num_of_rows: int,
                  from_col: int, num_of_cols: int) -> Matrix:
        ''' Return a submatrix of this matrix

        Parameters
        ----------
        from_row: int
            The first row to be included in the submatrix to be returned
        num_of_rows: int
            The number of rows to be included in the submatrix to be returned
        from_col: int
            The first col to be included in the submatrix to be returned
        num_of_cols: int
            The number of cols to be included in the submatrix to be returned

        Returns
        -------
        Matrix
            A submatrix of this matrix
        '''
        A = [row[from_col:from_col+num_of_cols] for row in self._A[from_row:from_row+num_of_rows]]

        return Matrix(A, clone_matrix=False)

    def assign_submatrix(self, from_row: int, from_col: int, A: Matrix):
        for y, row in enumerate(A):
            self_row = self[y + from_row]
            for x, value in enumerate(row):
                self_row[x + from_col] = value

    def insert_row(self):
        self._A.append([0 for x in range(self.num_of_cols)])

    def insert_column(self):
        for row in self._A:
            row.append(0)
    
    @property
    def max(self):
        max_el = self._A[0][0]

        for row in self._A:
            for j in row:
                if j > max_el:
                    max_el = j
        
        return max_el

    def __repr__(self):
        return '\n'.join('{}'.format(row) for row in self._A)


class IdentityMatrix(Matrix):
    ''' A class for identity matrices

    Parameters
    ----------
    size: int
        The size of the identity matrix
    '''
    def __init__(self, size: int):
        A = [[1 if x == y else 0 for x in range(size)]
             for y in range(size)]

        super().__init__(A)

# way to compare execution times of the two algorithms

# check if file is executed
if __name__ == '__main__':

    # in order to randomize matrices
    from random import random
    from random import seed

    # to use standard output
    from sys import stdout

    # function to measure the exec time
    from timeit import timeit

    # set the seed of the pesudo-random number generator
    seed(0)

    for i in range(13):
        size = 2**i
        stdout.write(f'{size}')
        A = Matrix([[random() for x in range(size)] for y in range(size)])
        B = Matrix([[random() for x in range(size)] for y in range(size)])

        for funct in ['gauss_matrix_mult', 'strassen_matrix_mult']:
            T = timeit(f'{funct}(A,B)', globals=locals(), number=1) # timeit requires as first par a string not a call, represinting the piece of code you want to execute
                                                                    # second par: local() we want to tell python that the two matrices A, B must be found in the current scope
                                                                    # evaluate execution time for 1 repetition for each size
            stdout.write('\t{:.3f}'.format(T)) # before printing the T I print a tab character, because I want the size on a column a before beginning the second (for time) I need to separate
                                              # the two with a tab character. Time will be printed with three chars after the dot
            stdout.flush() # print everything of the above and clean the buffer
        stdout.write('\n')