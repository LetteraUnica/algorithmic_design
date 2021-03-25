from __future__ import annotations

from numbers import Number
from typing import List


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

    if(A.num_of_cols != B.num_of_rows):
        raise ValueError("The two matrices can't be multiplied")
    
    C = [[0 for j in range(B.num_of_cols)] for i in range(A.num_of_rows)]

    for i in range(A.num_of_rows):
        for j in range(B.num_of_cols):
            value = 0.
            for k in range(A.num_of_cols):
                value += A[i][k] * B[k][j]
            
            C[i][j] = value 
                
    return Matrix(C, clone_matrix=False)


def get_matrix_quadrants(A: Matrix) -> Tuple[Matrix, Matrix, Matrix, Matrix]:
    ''' Return the matrix quadrants

    Parameters
    ----------
    A: Matrix
        The matrix of which the quadrants are requested

    Returns
    -------
    Tuple(Matrix, Matrix, Matrix, Matrix)
        Tuple made of the quadrants of the passed matrix
    '''

    A11 = A.submatrix(0, A.num_of_rows//2, 0, A.num_of_cols//2)
    A12 = A.submatrix(0, A.num_of_rows//2, A.num_of_cols//2, A.num_of_cols//2)
    A21 = A.submatrix(A.num_of_rows//2, A.num_of_rows//2, 0, A.num_of_cols//2)
    A22 = A.submatrix(A.num_of_rows//2, A.num_of_rows//2, A.num_of_cols//2, A.num_of_cols//2)

    return A11, A12, A21, A22

def zero_matrix(rows: int, cols: int) -> Matrix:
    """
    Returns a matrix filled with zeros

    Parameters
    ----------
    rows: int
        Number of rows
    cols: int
        Number of columns

    Returns
    -------
    Matrix
        Matrix filled with zeros
    """

    return Matrix([[0 for j in range(cols)] for i in range(rows)], clone_matrix=False)

def pad_matrix(A: Matrix, rows_to_add: int, cols_to_add: int) -> Matrix:
    """ Returns a padded matrix

    Parameters
    ----------
    A: Matrix
        The matrix to pad
    rows_to_add: int
        Number of rows to add, they will be filled with zeros
    cols_to_add: int
        Number of columns to add, they will be filled with zeros

    Returns
    -------
    Matrix
        Padded matrix
    """

    new_A = zero_matrix(A.num_of_rows + rows_to_add, A.num_of_cols + cols_to_add)
    new_A.assign_submatrix(0, 0, A)
    return new_A

def strassen_matrix_mult(A: Matrix, B: Matrix, min_size: int = 64) -> Matrix:
    ''' Multiply two matrices by using Strassen's algorithm

    Parameters
    ----------
    A: Matrix
        The first matrix to be multiplied
    B: Matrix
        The second matrix to be multiplied
    min_size: int
        Size below which the standard gauss multiplication is used

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

    if(A.num_of_cols != B.num_of_rows):
        raise ValueError("The two matrices can't be multiplied")

    # Base case
    if max(A.num_of_rows, B.num_of_cols, A.num_of_cols) < min_size:
        return gauss_matrix_mult(A, B)

    # A uneven
    padded_rows = A.num_of_rows % 2
    A = pad_matrix(A, padded_rows, A.num_of_cols%2)
    
    # B uneven
    padded_cols = B.num_of_cols % 2
    B = pad_matrix(B, B.num_of_rows%2, padded_cols)
        
    A11, A12, A21, A22 = get_matrix_quadrants(A)
    B11, B12, B21, B22 = get_matrix_quadrants(B)
    
    S1 = B12 - B22
    S2 = A11 + A12
    S3 = A21 + A22
    S4 = B21 - B11
    S5 = A11 + A22
    S6 = B11 + B22
    S7 = A12 - A22
    S8 = B21 + B22
    S9 = A11 - A21
    S10 = B11 + B12
    
    P1 = strassen_matrix_mult(A11, S1)
    P2 = strassen_matrix_mult(S2, B22)
    P3 = strassen_matrix_mult(S3, B11)
    P4 = strassen_matrix_mult(A22, S4)
    P5 = strassen_matrix_mult(S5, S6)
    P6 = strassen_matrix_mult(S7, S8)
    P7 = strassen_matrix_mult(S9, S10)
    
    C11 = P5 + P4 - P2 + P6
    C12 = P1 + P2 
    C21 = P3 + P4
    C22 = P5 + P1 - P3 - P7
    
    C = zero_matrix(A.num_of_rows, B.num_of_cols)
    C.assign_submatrix(0, 0, C11)
    C.assign_submatrix(0, C.num_of_cols//2, C12)
    C.assign_submatrix(C.num_of_rows//2, 0, C21)
    C.assign_submatrix(C.num_of_rows//2, C.num_of_cols//2, C22)
    
    return C.submatrix(0, C.num_of_rows - padded_rows, 0, C.num_of_cols - padded_cols)


def better_strassen_matrix_mult(A: Matrix, B: Matrix, min_size: int = 64) -> Matrix:
    ''' Multiply two matrices by using Strassen's algorithm

    Parameters
    ----------
    A: Matrix
        The first matrix to be multiplied
    B: Matrix
        The second matrix to be multiplied
    min_size: int
        Size below which the standard gauss multiplication is used

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

    if(A.num_of_cols != B.num_of_rows):
        raise ValueError("The two matrices can't be multiplied")

    # Base case
    if max(A.num_of_rows, B.num_of_cols, A.num_of_cols) < min_size:
        return gauss_matrix_mult(A, B)

    # A uneven
    padded_rows = A.num_of_rows % 2
    A = pad_matrix(A, padded_rows, A.num_of_cols%2)
    
    # B uneven
    padded_cols = B.num_of_cols % 2
    B = pad_matrix(B, B.num_of_rows%2, padded_cols)
    
    A11, A12, A21, A22 = get_matrix_quadrants(A)
    B11, B12, B21, B22 = get_matrix_quadrants(B)

    P = better_strassen_matrix_mult(A11 + A22, B11 + B22)
    C11 = P
    C22 = P

    P = better_strassen_matrix_mult(A11 + A12, B22.copy())
    C12 = P
    C11 = C11 - P

    P = better_strassen_matrix_mult(A11.copy(), B12 - B22)
    C12 = C12 + P
    C22 = C22 + P

    P = better_strassen_matrix_mult(A21 + A22, B11.copy())
    C21 = P
    C22 = C22 - P

    P = better_strassen_matrix_mult(A22.copy(), B21 - B11)
    C11 = C11 + P
    C21 = C21 + P

    C22 = C22 - better_strassen_matrix_mult(A11 - A21, B11 + B12)

    C11 = C11 + better_strassen_matrix_mult(A12 - A22, B21 + B22)

    C = zero_matrix(A.num_of_rows, B.num_of_cols)
    C.assign_submatrix(0, 0, C11)
    C.assign_submatrix(0, C.num_of_cols//2, C12)
    C.assign_submatrix(C.num_of_rows//2, 0, C21)
    C.assign_submatrix(C.num_of_rows//2, C.num_of_cols//2, C22)
    
    C = C.submatrix(0, C.num_of_rows - padded_rows, 0, C.num_of_cols - padded_cols)
    return C

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
        A = [row[from_col:from_col+num_of_cols]
             for row in self._A[from_row:from_row+num_of_rows]]

        return Matrix(A, clone_matrix=False)

    def assign_submatrix(self, from_row: int, from_col: int, A: Matrix):
        for y, row in enumerate(A):
            self_row = self[y + from_row]
            for x, value in enumerate(row):
                self_row[x + from_col] = value

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


if(__name__=="main"):

    from random import random
    import time
    from IPython.display import clear_output
    import pylab as pl

    # Sizes to consider
    all_n = [2**i for i in range(1, 10)]
    time_gauss = []
    time_strassen_naive = []
    time_strassen_better = []

    f = open("matrix-times.txt", "w")
    f.write("# Gauss_matmul/strassen_matmul/memory_efficient_strassen_matmul")
    for n in all_n:
        # Generates two uniform random matrix
        A = Matrix([[random() for j in range(n)] for i in range(n)], clone_matrix=False)
        B = Matrix([[random() for j in range(n)] for i in range(n)], clone_matrix=False)
        
        # Time of the gauss matmul
        start = time.time()
        gauss_matrix_mult(A, B)
        time_gauss.append(time.time() - start)
        f.write(f"{time_gauss[-1]} ")
        
        # Time of the naive strassen matmul
        start = time.time()
        strassen_matrix_mult(A, B)
        time_strassen_naive.append(time.time() - start)
        f.write(f"{time_strassen_naive[-1]} ")
        
        # Time of the better strassen matmul
        start = time.time()
        better_strassen_matrix_mult(A, B)
        time_strassen_better.append(time.time() - start)
        f.write(f"{time_strassen_better[-1]}\n")
        
        # To track progress
        print("done:", n)

    f.close()

    # Plot the curves
    pl.loglog(all_n, time_gauss, label="Gauss matmul")
    pl.loglog(all_n, time_strassen_naive, label="Strassen matmul")
    pl.loglog(all_n, time_strassen_better, label="Strassen efficient matmul")
    pl.legend()
    pl.ylabel("Time [s]")
    pl.xlabel("Size of the matrix [n]")
    pl.title("Time vs size for matrix multiplication")
    pl.savefig("Time-comparison.png", dpi=300)