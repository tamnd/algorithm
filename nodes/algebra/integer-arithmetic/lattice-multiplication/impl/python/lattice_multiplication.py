# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lattice-multiplication/. The authors are listed in prov/HGRER8.jsonl.


def lattice_multiply(a: list[int], b: list[int], base: int = 10) -> list[int]:
    """Product of two digit arrays (least significant digit first) in a radix base >= 2.

    Fill the grid of the digit products, each split into a high and a low digit,
    add the digits along each diagonal, then make one carry pass over the
    diagonal sums. Returns len(a) + len(b) digits. Cost: len(a) * len(b) digit
    products and Theta(len(a) * len(b)) digit additions.
    """
    m, n = len(a), len(b)
    hi = [[0] * n for _ in range(m)]
    lo = [[0] * n for _ in range(m)]
    for i in range(m):  # @line L1
        for j in range(n):
            hi[i][j], lo[i][j] = divmod(a[i] * b[j], base)  # @line L2
    s = [0] * (m + n)  # @line L3
    for i in range(m):  # @line L4
        for j in range(n):
            s[i + j] += lo[i][j]  # @line L5
            s[i + j + 1] += hi[i][j]
    c = [0] * (m + n)
    carry = 0  # @line L6
    for k in range(m + n):  # @line L7
        t = s[k] + carry  # @line L8
        c[k] = t % base  # @line L9
        carry = t // base
    return c  # @line L10: the last carry is 0
