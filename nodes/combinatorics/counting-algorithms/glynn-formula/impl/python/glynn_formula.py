# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/glynn-formula/. The authors are listed in prov/X4CC5C.jsonl.


def glynn_permanent(a):
    """Return the permanent of the square matrix a (a list of rows).

    The entries may be int, fractions.Fraction, float or complex. For int
    entries the final division by 2**(n-1) is exact, so the result is an int.
    The sign vectors (delta_1 = +1, delta_2..delta_n free) are visited in
    binary reflected Gray code order, so each step flips one sign.
    """
    n = len(a)
    for row in a:
        if len(row) != n:
            raise ValueError("the matrix must be square")
    if n == 0:  # @line L1
        return 1
    delta = [1] * n  # @line L2
    sigma = 1
    c = [sum(a[i][j] for i in range(n)) for j in range(n)]
    total = 1  # @line L3
    for x in c:
        total *= x
    for k in range(1, 1 << (n - 1)):  # @line L4
        i = (k & -k).bit_length()  # @line L5: rho(k) + 1, the 0-based row index
        delta[i] = -delta[i]  # @line L6
        sigma = -sigma
        two_d = 2 * delta[i]
        row = a[i]
        for j in range(n):  # @line L7
            c[j] += two_d * row[j]
        prod = sigma  # @line L8
        for x in c:
            prod *= x
        total += prod
    div = 1 << (n - 1)  # @line L9
    if isinstance(total, int):
        q, r = divmod(total, div)
        if r != 0:
            raise ArithmeticError("the total is not divisible by 2**(n-1)")
        return q
    return total / div
