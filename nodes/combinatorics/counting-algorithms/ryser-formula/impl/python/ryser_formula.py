# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ryser-formula/. The authors are listed in prov/11ZBTR.jsonl.


def ryser_permanent(a):
    """Return the permanent of the square matrix a (a list of rows).

    The entries may be any numbers that support +, - and * exactly, such as
    int or fractions.Fraction. The column subsets are visited in binary
    reflected Gray code order, so each step changes one column.
    """
    n = len(a)
    for row in a:
        if len(row) != n:
            raise ValueError("the matrix must be square")
    if n == 0:  # @line L1
        return 1
    r = [0] * n  # @line L2
    in_s = 0  # bit mask of the columns in S
    size = 0
    total = 0
    for k in range(1, 1 << n):  # @line L3
        j = (k & -k).bit_length() - 1  # @line L4: rho(k), 0-based column
        bit = 1 << j
        if in_s & bit:  # @line L5
            in_s ^= bit
            size -= 1
            for i in range(n):  # @line L6
                r[i] -= a[i][j]
        else:
            in_s |= bit
            size += 1
            for i in range(n):  # @line L6
                r[i] += a[i][j]
        prod = 1
        for x in r:  # @line L7
            prod *= x
        total += -prod if size & 1 else prod
    return -total if n & 1 else total  # @line L8
