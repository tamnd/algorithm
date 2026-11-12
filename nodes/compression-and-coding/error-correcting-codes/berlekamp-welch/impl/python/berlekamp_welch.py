# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/berlekamp-welch/. The authors are listed in prov/7100GD.jsonl.
"""The Berlekamp-Welch decoder for Reed-Solomon codes in the evaluation view.

The code is {(f(a_1), ..., f(a_n)) : deg f < k} for distinct points a_i of a
field F. Given a received word y, the decoder finds a monic error locator E of
degree e = floor((n - k) / 2) and a polynomial Q of degree < e + k with
Q(a_i) = y_i E(a_i) for every i, by one linear system, and returns f = Q / E.

Polynomials are lists of field elements, lowest degree first. The field is any
object with add, sub, mul and inv (see gf.py).
"""

from typing import Protocol


class Field(Protocol):
    def add(self, a: int, b: int) -> int: ...
    def sub(self, a: int, b: int) -> int: ...
    def mul(self, a: int, b: int) -> int: ...
    def inv(self, a: int) -> int: ...


def poly_eval(f: Field, p: list[int], x: int) -> int:
    """Horner's rule."""
    y = 0
    for c in reversed(p):
        y = f.add(f.mul(y, x), c)
    return y


def poly_divmod(f: Field, num: list[int], den: list[int]) -> tuple[list[int], list[int]]:
    """Quotient and remainder; den must have a nonzero leading coefficient."""
    rem = list(num)
    if len(rem) < len(den):
        return [], rem
    quo = [0] * (len(rem) - len(den) + 1)
    lead = f.inv(den[-1])
    for i in range(len(quo) - 1, -1, -1):
        c = f.mul(rem[i + len(den) - 1], lead)
        quo[i] = c
        for j, d in enumerate(den):
            rem[i + j] = f.sub(rem[i + j], f.mul(c, d))
    return quo, rem[: len(den) - 1]


def solve_any(f: Field, rows: list[list[int]], rhs: list[int]) -> list[int] | None:
    """One solution of rows * x = rhs (free unknowns set to 0), or None if there is none.

    Gauss-Jordan elimination: O(r c min(r, c)) operations for r rows and c unknowns.
    """
    ncols = len(rows[0]) if rows else 0
    m = [list(r) + [b] for r, b in zip(rows, rhs)]
    pivots: list[int] = []
    rk = 0
    for col in range(ncols):
        piv = next((i for i in range(rk, len(m)) if m[i][col]), None)
        if piv is None:
            continue
        m[rk], m[piv] = m[piv], m[rk]
        inv = f.inv(m[rk][col])
        m[rk] = [f.mul(v, inv) for v in m[rk]]
        for i in range(len(m)):
            if i != rk and m[i][col]:
                c = m[i][col]
                m[i] = [f.sub(v, f.mul(c, w)) for v, w in zip(m[i], m[rk])]
        pivots.append(col)
        rk += 1
    if any(m[i][ncols] for i in range(rk, len(m))):
        return None  # a row 0 = nonzero: no solution
    x = [0] * ncols
    for i, col in enumerate(pivots):
        x[col] = m[i][ncols]
    return x


def berlekamp_welch(f: Field, xs: list[int], ys: list[int], k: int) -> list[int] | None:
    """Return the k coefficients of the f with deg f < k and f(x_i) != y_i at most e times, or None.

    Precondition: the xs are distinct, len(xs) = len(ys) = n, and 1 <= k <= n.
    Here e = floor((n - k) / 2). If such an f exists it is unique and is returned;
    otherwise the result is None (a detected failure).
    Cost: one linear system with n equations and 2e + k <= n unknowns, O(n^3) field operations.
    """
    n = len(xs)
    e = (n - k) // 2  # @line L1
    rows, rhs = [], []
    for a, y in zip(xs, ys):  # @line L2: Q(a) - y E(a) = 0 with E monic of degree e
        powers = [1]
        for _ in range(e + k):
            powers.append(f.mul(powers[-1], a))
        row = powers[: e + k] + [f.sub(0, f.mul(y, powers[j])) for j in range(e)]
        rows.append(row)
        rhs.append(f.mul(y, powers[e]))  # the known term y a^e moved to the right side
    sol = solve_any(f, rows, rhs)  # @line L3
    if sol is None:
        return None
    q, e_poly = sol[: e + k], sol[e + k:] + [1]
    msg, rem = poly_divmod(f, q, e_poly)  # @line L4: deg Q < e + k, so deg msg < k
    if any(rem):  # @line L5
        return None
    # Where E(a_i) != 0, msg(a_i) = Q(a_i) / E(a_i) = y_i, and E has at most e roots,
    # so msg is within distance e of y.
    return (msg + [0] * k)[:k]  # @line L6
