from typing import List

def MCM_aux(P,m,s,i,j):
    m[i][j] = None

    for k in range(i, j):
        q = m[i][k] + m[k+1][j] + P[i]*P[k+1]*P[j+1]
        if m[i][j] is None or q < m[i][j]:
            m[i][j] = q
            s[i][j] = k + 1 # python starts counting from zero not 1, that makes us add it by hand

def matrix_chain_mult(P: List[int]):
    n = len(P)
    m = [[0 for j in range(n-1)] for i in range(n-1)]
    s = [[0 for j in range(n-1)] for i in range(n-1)]

    for diag in range(1,n): 
        for i in range(n-diag-1):
            j = i + diag    # until now we have selected the cell of the diagonal

            # select minumum sum

            MCM_aux(P,m,s,i,j)
    
    return m, s

