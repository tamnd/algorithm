# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/schoolbook-multiplication/. The authors are listed in prov/7VTRV2.jsonl.


def schoolbook_multiply(a: list[int], b: list[int], w: int = 8) -> list[int]:
    """Product of two limb arrays in base 2^w, least significant limb first.

    Precondition: each limb is in [0, 2^w). The result has len(a) + len(b) limbs
    (the top limb can be 0). Cost: exactly len(a) * len(b) limb products and
    Theta(len(a) * len(b)) limb operations.
    """
    base = 1 << w
    m, n = len(a), len(b)
    c = [0] * (m + n)  # @line L1
    for i in range(m):  # @line L2
        carry = 0  # @line L3
        for j in range(n):  # @line L4
            t = c[i + j] + a[i] * b[j] + carry  # @line L5: t <= base^2 - 1
            c[i + j] = t & (base - 1)  # @line L6
            carry = t >> w  # @line L7
        c[i + n] = carry  # @line L8
    return c  # @line L9


def schoolbook_square(a: list[int], w: int = 8) -> list[int]:
    """The square of a limb array with n (n - 1) / 2 cross products and n squares.

    Each cross product a[i] a[j] with i < j is computed once, the sum of the cross
    products is doubled by a shift, and the squares a[i]^2 are added. Cost Theta(n^2).
    """
    n = len(a)
    cross = [0] * (2 * n)
    for i in range(n):
        carry = 0
        for j in range(i + 1, n):
            t = cross[i + j] + a[i] * a[j] + carry
            cross[i + j] = t & ((1 << w) - 1)
            carry = t >> w
        if n:
            cross[i + n] = carry
    # double the cross products, then add the squares on the diagonal
    out = [0] * (2 * n)
    carry = 0
    for k in range(2 * n):
        t = 2 * cross[k] + carry
        if k % 2 == 0:
            t += a[k // 2] ** 2 % (1 << w)
        else:
            t += a[k // 2] ** 2 >> w
        out[k] = t & ((1 << w) - 1)
        carry = t >> w
    return out


def multiply_signed(x: tuple[int, list[int]], y: tuple[int, list[int]], w: int = 8) -> tuple[int, list[int]]:
    """Product of (sign, limbs) pairs with sign in {1, -1}, normalized; zero gets sign 1."""
    c = schoolbook_multiply(x[1], y[1], w)
    while c and c[-1] == 0:
        c.pop()
    return (x[0] * y[0] if c else 1), c
