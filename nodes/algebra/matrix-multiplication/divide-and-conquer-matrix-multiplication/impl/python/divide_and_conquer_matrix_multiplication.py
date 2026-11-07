# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/divide-and-conquer-matrix-multiplication/. The authors are listed in prov/4CTYKM.jsonl.

Matrix = list[list[int]]


def divide_and_conquer_matrix_multiplication(a: Matrix, b: Matrix, p: int | None = None, mod: int | None = None) -> Matrix:
    """Return a * b by the recursive eight-product method.

    a is n x m and b is m x p, as lists of rows; pass p when m = 0. With mod
    set, the arithmetic is in Z/mod Z. The recursion splits each side at its
    ceiling half, so any shape works without padding. Cost: n*m*p
    multiplications and additions; recursion depth O(log max(n, m, p)).
    """
    n, m = len(a), len(b)
    if p is None:
        p = len(b[0]) if m > 0 else 0
    if any(len(row) != m for row in a) or any(len(row) != p for row in b):
        raise ValueError("the shapes do not match")
    c = [[0] * p for _ in range(n)]
    dc_multiply_add(a, b, c, 0, 0, 0, 0, 0, 0, n, m, p, mod)
    return c


def dc_multiply_add(a: Matrix, b: Matrix, c: Matrix, ai: int, ak: int, bk: int, bj: int,
                    ci: int, cj: int, n: int, m: int, p: int, mod: int | None) -> None:
    """C view += A view * B view. The A view starts at (ai, ak), the B view at (bk, bj), the C view at (ci, cj)."""
    if n == 0 or m == 0 or p == 0:  # @line L1
        return
    if n == 1 and m == 1 and p == 1:  # @line L2
        v = c[ci][cj] + a[ai][ak] * b[bk][bj]  # @line L3
        c[ci][cj] = v % mod if mod is not None else v
        return  # @line L4
    n1, m1, p1 = (n + 1) // 2, (m + 1) // 2, (p + 1) // 2  # @line L5
    rows = ((0, n1), (n1, n - n1))
    inner = ((0, m1), (m1, m - m1))
    cols = ((0, p1), (p1, p - p1))
    for r0, rn in rows:  # @line L6
        for s0, sn in cols:  # @line L7
            k0, kn = inner[0]
            dc_multiply_add(a, b, c, ai + r0, ak + k0, bk + k0, bj + s0, ci + r0, cj + s0, rn, kn, sn, mod)  # @line L8
            k0, kn = inner[1]
            dc_multiply_add(a, b, c, ai + r0, ak + k0, bk + k0, bj + s0, ci + r0, cj + s0, rn, kn, sn, mod)  # @line L9
