# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/plotkin-bound/. The authors are listed in prov/PY83ZY.jsonl.

"""The Plotkin bound, binary and q-ary, and Hadamard codes that meet it.

Binary words are tuples of 0 and 1. Fractions keep the q-ary bound exact.
"""

from fractions import Fraction
from itertools import combinations


def plotkin_binary(n: int, d: int) -> int | None:
    """2 floor(d / (2d - n)) when 2d > n; None when the bound does not apply.

    An upper bound on A_2(n, d) for every binary code, linear or not.
    """
    if 2 * d <= n:
        return None
    return 2 * (d // (2 * d - n))


def plotkin_binary_refined(n: int, d: int) -> int | None:
    """The form of MacWilliams and Sloane, Chapter 2: separate cases for even and odd d.

    d even: 2 floor(d / (2d - n)) if n < 2d, and 4d if n = 2d.
    d odd: 2 floor((d + 1) / (2d + 1 - n)) if n < 2d + 1, and 4d + 4 if n = 2d + 1.
    """
    if d % 2 == 0:
        if n < 2 * d:
            return 2 * (d // (2 * d - n))
        if n == 2 * d:
            return 4 * d
        return None
    if n < 2 * d + 1:
        return 2 * ((d + 1) // (2 * d + 1 - n))
    if n == 2 * d + 1:
        return 4 * d + 4
    return None


def plotkin_q(q: int, n: int, d: int) -> int | None:
    """floor(d / (d - theta n)) with theta = 1 - 1/q, when d > theta n; else None."""
    theta = Fraction(q - 1, q)
    if d <= theta * n:
        return None
    return int(Fraction(d) / (d - theta * n))


def plotkin_rate(delta: float, q: int = 2) -> float:
    """Asymptotic Plotkin bound: R <= 1 - delta / theta for delta <= theta, else 0."""
    theta = 1 - 1 / q
    return max(0.0, 1 - delta / theta)


def plotkin_shortened(q: int, n: int, d: int) -> int:
    """The bound used for the asymptotic form: q^(n - m) * floor(d / (d - theta m)),
    with m = the largest length below d / theta (so the q-ary bound applies at length m).
    Valid for 1 <= d <= n.
    """
    theta = Fraction(q - 1, q)
    m = min(n, (d * q - 1) // (q - 1))  # largest m with theta m < d
    return q ** (n - m) * int(Fraction(d) / (d - theta * m))


def sylvester(r: int) -> list[list[int]]:
    """The Sylvester Hadamard matrix of order 2^r, entries +1 and -1."""
    h = [[1]]
    for _ in range(r):
        h = [row + row for row in h] + [row + [-x for x in row] for row in h]
    return h


def paley(q: int) -> list[list[int]]:
    """The Paley Hadamard matrix of order q + 1 for a prime q with q = 3 mod 4."""
    squares = {(x * x) % q for x in range(1, q)}

    def chi(a: int) -> int:
        a %= q
        return 0 if a == 0 else (1 if a in squares else -1)

    n = q + 1
    h = [[0] * n for _ in range(n)]
    for j in range(n):
        h[0][j] = 1
    for i in range(1, n):
        h[i][0] = -1
        for j in range(1, n):
            h[i][j] = 1 if i == j else chi(j - i)
    return h


def is_hadamard(h: list[list[int]]) -> bool:
    """H H^T = n I and all entries are +1 or -1."""
    n = len(h)
    if any(len(row) != n or any(x not in (1, -1) for x in row) for row in h):
        return False
    return all(sum(a * b for a, b in zip(h[i], h[j])) == (n if i == j else 0)
               for i in range(n) for j in range(n))


def normalize(h: list[list[int]]) -> list[list[int]]:
    """Multiply rows and columns by -1 so that the first row and column are all +1."""
    h = [row[:] for row in h]
    for i, row in enumerate(h):
        if row[0] == -1:
            h[i] = [-x for x in row]
    for j in range(len(h)):
        if h[0][j] == -1:
            for row in h:
                row[j] = -row[j]
    return h


def hadamard_codes(h: list[list[int]]) -> dict[str, list[tuple[int, ...]]]:
    """The three Hadamard codes of a normalized Hadamard matrix of order n (+1 -> 0, -1 -> 1).

    A: the rows with the first column deleted, an (n - 1, n, n/2) code.
    B: A and the complements of its words, an (n - 1, 2n, n/2 - 1) code.
    C: the rows and their complements, an (n, 2n, n/2) code.
    """
    hn = normalize(h)
    rows = [tuple(0 if x == 1 else 1 for x in row) for row in hn]
    comp = [tuple(1 - x for x in r) for r in rows]
    a = [r[1:] for r in rows]
    b = a + [r[1:] for r in comp]
    c = rows + comp
    return {"A": a, "B": b, "C": c}


def min_distance(words: list[tuple[int, ...]]) -> int:
    """Least distance between two distinct words (works for nonlinear codes)."""
    return min(sum(x != y for x, y in zip(u, v)) for u, v in combinations(words, 2))
