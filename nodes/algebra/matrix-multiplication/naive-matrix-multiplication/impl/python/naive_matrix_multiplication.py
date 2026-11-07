# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/naive-matrix-multiplication/. The authors are listed in prov/F9X6P7.jsonl.

Matrix = list[list[int]]


def naive_matrix_multiplication(a: Matrix, b: Matrix, p: int | None = None, mod: int | None = None) -> Matrix:
    """Return the product a * b by the triple loop.

    a is n x m and b is m x p, given as lists of rows. When m = 0, b is empty,
    so the caller passes the number of columns p. With mod set, the arithmetic
    is in Z/mod Z and each entry is in [0, mod). Cost: n*m*p multiplications
    and n*m*p additions; extra space O(1) beyond the output.
    """
    n = len(a)
    m = len(b)
    if p is None:
        p = len(b[0]) if m > 0 else 0
    if any(len(row) != m for row in a) or any(len(row) != p for row in b):
        raise ValueError("the shapes do not match")
    c = [[0] * p for _ in range(n)]  # @line L1
    for i in range(n):  # @line L2
        for j in range(p):  # @line L3
            s = 0  # @line L4
            for k in range(m):  # @line L5
                s = s + a[i][k] * b[k][j]  # @line L6
                if mod is not None:
                    s %= mod
            c[i][j] = s  # @line L7
    return c  # @line L8
