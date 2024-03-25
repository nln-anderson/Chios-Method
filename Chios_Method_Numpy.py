# Chio's Method for Solving an n x n Matrix
# Code is modeled from: Heffernon, J. (2022). Linear Algebra, 4th Edition

    # DOESN"T HANDLE CASE WHERE THE FIRST ENTRY a_11 IS 0

import numpy as np

def two_by_two_determinant(a: float,b: float,c: float,d: float) -> float:
    """
    Calculates the determinant of a 2x2 matrix. 

    PARAMETERS:
    a,b,c,d (type: float) - the entries of a 2x2 matrix

    OUTPUT:
    determinant (type: float) - the determinant of the 2x2 matrix
    
    DOCTESTS:
    >>> two_by_two_determinant(2,3,4,5)
    -2
    """

    determinant = a * d - c * b

    return determinant

def Chios_Matrix(matrix: np.ndarray) -> np.ndarray:
    """
    Creates Chio's Matrix of a given matrix input.

    PARAMETERS:
    matrix (type: array) - an nxn matrix

    OUTPUT:
    c_matrix (type: array) - Chio's matrix, an (n-1) x (n-1) matrix 

    DOCTESTS:
    >>> mat = Chios_Matrix(np.array([[2,1,1], [3,4,-1], [1,5,1]]))
    >>> print(mat)
    [[ 5. -5.]
     [ 9.  1.]]
    """
    # Establish matrix dimensions
    n = len(matrix)

    # Create an empty matrix that will be filled with Chio determinants
    c_matrix = np.zeros((n-1, n-1))

    # Filling the entries
    for i in range(n-1):
        # For each row
        for j in range(n-1):
            # For each entry in the row (aka column), compute the corresponding 2x2 determinant
            c_matrix[i, j] = two_by_two_determinant(matrix[0,0], matrix[0,j + 1], matrix[i + 1,0], matrix[i + 1,j+1])
        
    return c_matrix

def determinant_calculator_chio(matrix: np.ndarray) -> float:
    """
    Calculates the determinant of an n x n matrix using Chio's Method

    PARAMETERS:
    matrix (type: arrary) - an n x n matrix

    OUTPUT:
    determinant (type: float) - the determinant of the matrix

    DOCTESTS:
    >>> determinant_calculator_chio(np.array([[2,1,1], [3,4,-1], [1,5,1]]))
    25.0
    """
    n = len(matrix)

    # Base Case
    if n == 1:
        return matrix[0][0]
    
    # Chio's Method
    else:
        
        c_matrix = Chios_Matrix(matrix)
        
        return determinant_calculator_chio(c_matrix) / ((matrix[0][0])**(n-2))
    
# Example
print(determinant_calculator_chio(np.array([[3,1,2,-6],[1,5,2,1],[6,2,1,-7],[-6,-1,-2,5]])))