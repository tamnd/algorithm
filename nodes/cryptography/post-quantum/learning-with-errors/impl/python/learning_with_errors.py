# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/learning-with-errors/. The authors are listed in prov/91A2EW.jsonl.
"""Learning with errors (LWE): a sampler and three solvers for toy sizes.

sample_lwe() draws m samples (a_i, b_i = <a_i, s> + e_i mod q).
solve_noiseless() recovers s by Gaussian elimination when every e_i = 0.
primal_attack() recovers s from noisy samples with Kannan's embedding and a
small floating point LLL (written here, so the page has no dependency).
search_from_decision() is Regev's search to decision reduction for a prime
modulus: it finds s with calls to any decision oracle.

For study only. The code is not constant time, uses the random module, and
runs only on toy parameters. Use a FIPS 140 validated ML-KEM module for real
data.
"""

import math
import random
from typing import Callable, List, Optional, Sequence, Tuple

Matrix = List[List[int]]
Vector = List[int]


def centered(x: int, q: int) -> int:
    """The representative of x mod q in (-q/2, q/2]."""
    x %= q
    return x - q if x > q // 2 else x


def sample_error(rng: random.Random, alpha_q: float) -> int:
    """Regev's discretized Gaussian: a normal value of standard deviation
    alpha_q / sqrt(2 pi), rounded to the nearest integer."""
    return round(rng.gauss(0.0, alpha_q / math.sqrt(2.0 * math.pi)))


def sample_lwe(
    n: int,
    m: int,
    q: int,
    alpha_q: float,
    rng: random.Random,
    secret: Optional[Sequence[int]] = None,
    bounded: Optional[int] = None,
) -> Tuple[Matrix, Vector, Vector, Vector]:
    """Return (A, b, s, e) with A uniform in Z_q^(m x n) and b = A s + e mod q.

    The secret is uniform unless given. The error is the discretized Gaussian
    of width alpha_q, or uniform in [-bounded, bounded] when bounded is set.
    Cost: O(m n) operations on integers below q^2.
    """
    s = list(secret) if secret is not None else [rng.randrange(q) for _ in range(n)]
    A = [[rng.randrange(q) for _ in range(n)] for _ in range(m)]
    if bounded is None:
        e = [sample_error(rng, alpha_q) for _ in range(m)]
    else:
        e = [rng.randint(-bounded, bounded) for _ in range(m)]
    b = [(sum(x * y for x, y in zip(row, s)) + ei) % q for row, ei in zip(A, e)]
    return A, b, s, e


def normal_form(A: Matrix, b: Vector, q: int) -> Tuple[Matrix, Vector, Vector]:
    """Applebaum, Cash, Peikert and Sahai: turn m samples into m - n samples
    whose secret is the error vector of the first n samples.

    The first n rows of A must be invertible mod the prime q. Returns
    (A', b', rows) where b' = A' e_1 + e_2 with e_1 the error of the chosen
    rows. Cost: O(n^3 + m n^2).
    """
    rows = independent_rows(A, q)
    A1 = [A[i] for i in rows]
    b1 = [b[i] for i in rows]
    inv = invert_mod(A1, q)
    assert inv is not None
    rest = [i for i in range(len(A)) if i not in set(rows)]
    A_new, b_new = [], []
    for i in rest:
        # a^T A1^-1 is the new row; b - a^T A1^-1 b1 = a^T A1^-1 (-e1) + e2.
        row = [sum(A[i][k] * inv[k][j] for k in range(len(A1))) % q for j in range(len(A1))]
        val = (b[i] - sum(r * y for r, y in zip(row, b1))) % q
        A_new.append([(-x) % q for x in row])
        b_new.append(val)
    return A_new, b_new, rows


def invert_mod(M: Matrix, q: int) -> Optional[Matrix]:
    """The inverse of a square matrix modulo a prime q, or None. Cost: O(n^3)."""
    n = len(M)
    aug = [list(map(lambda x: x % q, row)) + [int(i == j) for j in range(n)] for i, row in enumerate(M)]
    for col in range(n):
        piv = next((r for r in range(col, n) if aug[r][col]), None)
        if piv is None:
            return None
        aug[col], aug[piv] = aug[piv], aug[col]
        inv = pow(aug[col][col], -1, q)
        aug[col] = [x * inv % q for x in aug[col]]
        for r in range(n):
            if r != col and aug[r][col]:
                f = aug[r][col]
                aug[r] = [(x - f * y) % q for x, y in zip(aug[r], aug[col])]
    return [row[n:] for row in aug]


def independent_rows(A: Matrix, q: int) -> List[int]:
    """Indices of the first n rows of A that are linearly independent mod q."""
    n = len(A[0])
    basis: List[Tuple[int, Vector]] = []  # (pivot column, reduced row)
    chosen: List[int] = []
    for idx, row in enumerate(A):
        v = [x % q for x in row]
        for piv, br in basis:
            if v[piv]:
                f = v[piv]
                v = [(x - f * y) % q for x, y in zip(v, br)]
        piv = next((j for j in range(n) if v[j]), None)
        if piv is None:
            continue
        inv = pow(v[piv], -1, q)
        basis.append((piv, [x * inv % q for x in v]))
        chosen.append(idx)
        if len(chosen) == n:
            return chosen
    raise ValueError("A has rank below n")


def solve_noiseless(A: Matrix, b: Vector, q: int) -> Vector:
    """Solve A s = b mod a prime q when the system has rank n (no error).

    Gauss-Jordan elimination on the m x (n + 1) augmented matrix.
    Cost: O(m n^2) operations mod q.
    """
    n = len(A[0])
    rows = [[x % q for x in r] + [y % q] for r, y in zip(A, b)]
    r = 0
    for col in range(n):
        piv = next((i for i in range(r, len(rows)) if rows[i][col]), None)
        if piv is None:
            raise ValueError("rank below n")
        rows[r], rows[piv] = rows[piv], rows[r]
        inv = pow(rows[r][col], -1, q)
        rows[r] = [x * inv % q for x in rows[r]]
        for i in range(len(rows)):
            if i != r and rows[i][col]:
                f = rows[i][col]
                rows[i] = [(x - f * y) % q for x, y in zip(rows[i], rows[r])]
        r += 1
    for i in range(n, len(rows)):
        if rows[i][n]:
            raise ValueError("inconsistent system: the samples have errors")
    return [rows[i][n] for i in range(n)]


def lll(B: Matrix, delta: float = 0.99) -> Matrix:
    """LLL reduction of the rows of an integer basis (full row rank).

    Floating point Gram-Schmidt with the update formulas of Cohen,
    A Course in Computational Algebraic Number Theory, Algorithm 2.6.3.
    Good for the toy dimensions (up to about 40) and small entries used here.
    """
    b = [list(r) for r in B]
    d = len(b)
    mu = [[0.0] * d for _ in range(d)]
    bn = [0.0] * d
    star: List[List[float]] = []
    for i in range(d):
        v = [float(x) for x in b[i]]
        for j in range(i):
            mu[i][j] = sum(x * y for x, y in zip(b[i], star[j])) / bn[j]
            v = [x - mu[i][j] * y for x, y in zip(v, star[j])]
        star.append(v)
        bn[i] = sum(x * x for x in v)
    k = 1
    while k < d:
        for j in range(k - 1, -1, -1):  # size reduction of b_k
            r = round(mu[k][j])
            if r:
                b[k] = [x - r * y for x, y in zip(b[k], b[j])]
                mu[k][j] -= r
                for i in range(j):
                    mu[k][i] -= r * mu[j][i]
        if bn[k] >= (delta - mu[k][k - 1] ** 2) * bn[k - 1]:
            k += 1
            continue
        m_ = mu[k][k - 1]  # swap b_k and b_(k-1)
        big = bn[k] + m_ * m_ * bn[k - 1]
        mu[k][k - 1] = m_ * bn[k - 1] / big
        bn[k] = bn[k - 1] * bn[k] / big
        bn[k - 1] = big
        b[k], b[k - 1] = b[k - 1], b[k]
        for j in range(k - 1):
            mu[k][j], mu[k - 1][j] = mu[k - 1][j], mu[k][j]
        for i in range(k + 1, d):
            t = mu[i][k]
            mu[i][k] = mu[i][k - 1] - m_ * t
            mu[i][k - 1] = t + mu[k][k - 1] * mu[i][k]
        k = max(k - 1, 1)
    return b


def embedding_basis(A: Matrix, b: Vector, q: int, scale: int = 1) -> Tuple[Matrix, List[int]]:
    """Kannan's embedding: a basis of the q-ary lattice A Z^n + q Z^m, in
    Hermite normal form, with the target (b, scale) as one more row.

    Returns the (m + 1) x (m + 1) basis and the order of the samples used.
    """
    m, n = len(A), len(A[0])
    first = independent_rows(A, q)  # @line L1
    order = first + [i for i in range(m) if i not in set(first)]
    A1 = [A[i] for i in first]
    inv = invert_mod(A1, q)
    assert inv is not None
    # C = A2 A1^-1: the lattice is {(v1, C v1 mod q)}.
    C = [  # @line L2
        [sum(A[order[r]][t] * inv[t][j] for t in range(n)) % q for j in range(n)]
        for r in range(n, m)
    ]
    basis: Matrix = []
    for i in range(n):  # @line L3
        basis.append([int(i == j) for j in range(n)] + [C[r][i] for r in range(m - n)] + [0])
    for r in range(m - n):
        basis.append([0] * n + [q * int(r == j) for j in range(m - n)] + [0])
    basis.append([b[i] for i in order] + [scale])  # @line L4
    return basis, order


def primal_attack(A: Matrix, b: Vector, q: int, bound: int) -> Optional[Vector]:
    """Recover s from LWE samples by the primal (embedding) attack.

    Reduce the embedding basis with LLL. A row (+-e, +-1) gives the error of
    the samples, and then s by solving n of the equations. The result is
    checked: every residual b_i - <a_i, s> must lie in [-bound, bound].
    Returns None when LLL does not find the error vector.
    """
    n = len(A[0])
    basis, order = embedding_basis(A, b, q)
    reduced = lll(basis)  # @line L5
    for row in reduced:  # @line L6
        if abs(row[-1]) != 1:
            continue
        e = [row[-1] * x for x in row[:-1]]  # @line L7 (make the last entry +1)
        A1 = [A[order[i]] for i in range(n)]
        rhs = [(b[order[i]] - e[i]) % q for i in range(n)]
        s = solve_noiseless(A1, rhs, q)  # @line L8
        res = [centered(bi - sum(x * y for x, y in zip(ai, s)), q) for ai, bi in zip(A, b)]
        if all(abs(r) <= bound for r in res):  # @line L9
            return s
    return None  # @line L10


def brute_force_decide(samples: Sequence[Tuple[Vector, int]], n: int, q: int, bound: int) -> bool:
    """A toy decision oracle: True when some s fits every sample with an
    error in [-bound, bound]. Cost: q^n m, so only for tiny n and q."""
    cand = [[]]
    for _ in range(n):
        cand = [c + [x] for c in cand for x in range(q)]
    for s in cand:
        if all(abs(centered(bi - sum(x * y for x, y in zip(ai, s)), q)) <= bound for ai, bi in samples):
            return True
    return False


def search_from_decision(
    samples: Sequence[Tuple[Vector, int]],
    n: int,
    q: int,
    decide: Callable[[List[Tuple[Vector, int]]], bool],
    rng: random.Random,
) -> Vector:
    """Regev's search to decision reduction (prime q of polynomial size).

    For coordinate i and guess k, map each sample (a, b) to
    (a + l e_i, b + l k) with a fresh uniform l. If k = s_i the result is again
    LWE with secret s; else b gains l (k - s_i), which is uniform because q is
    prime. The decision oracle tells the two cases apart.
    Cost: at most n q oracle calls.
    """
    s: Vector = []
    for i in range(n):
        for k in range(q):
            moved = []
            for a, bb in samples:
                l = rng.randrange(q)
                a2 = list(a)
                a2[i] = (a2[i] + l) % q
                moved.append((a2, (bb + l * k) % q))
            if decide(moved):
                s.append(k)
                break
        else:
            raise ValueError("the oracle accepted no guess")
    return s
