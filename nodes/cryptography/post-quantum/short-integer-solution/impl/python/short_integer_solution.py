# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/short-integer-solution/. The authors are listed in prov/JRMD0G.jsonl.
"""The short integer solution (SIS) problem and Ajtai's hash function.

ajtai_hash() computes f_A(x) = A x mod q for a 0/1 vector x.
is_sis_solution() checks a candidate z: nonzero, A z = 0 mod q, and short.
birthday_collision() finds x != x' with f_A(x) = f_A(x'); then z = x - x'
is a SIS solution with entries in {-1, 0, 1}.
kernel_vector() finds a nonzero z with A z = 0 mod q by elimination, with no
bound on its length: it shows that the shortness is the hard part.

For study only. The code is not constant time, uses the random module, and
runs only on toy parameters. For a real hash function use SHA-256 or SHA-3
from the standard library, and for lattice signatures a FIPS 140 validated
ML-DSA module.
"""

import math
import random
from typing import Dict, List, Optional, Sequence, Tuple

Matrix = List[List[int]]
Vector = List[int]


def random_matrix(n: int, m: int, q: int, rng: random.Random) -> Matrix:
    """A uniform n x m matrix over Z_q (n rows, m columns)."""
    return [[rng.randrange(q) for _ in range(m)] for _ in range(n)]


def ajtai_hash(A: Matrix, x: Sequence[int], q: int) -> Tuple[int, ...]:
    """f_A(x) = A x mod q. Cost: n m additions and multiplications mod q."""
    return tuple(sum(a * b for a, b in zip(row, x)) % q for row in A)


def output_bits(n: int, q: int) -> float:
    """log2 of the number of possible outputs, n log2 q."""
    return n * math.log2(q)


def is_sis_solution(A: Matrix, z: Sequence[int], q: int, beta: float) -> bool:
    """True when z is nonzero, A z = 0 mod q and the Euclidean norm of z is at most beta."""
    if not any(z):
        return False
    if any(v % q for v in ajtai_hash(A, z, q)):
        return False
    return math.sqrt(sum(v * v for v in z)) <= beta


def birthday_collision(
    A: Matrix, q: int, rng: random.Random, max_tries: int = 1 << 20
) -> Tuple[Vector, Vector, int]:
    """Hash random 0/1 vectors until two different ones give the same output.

    Returns (x, x2, tries). When m > n log2 q a collision must exist; with
    N = q^n outputs a collision is expected after about sqrt(pi N / 2) tries.
    """
    m = len(A[0])
    seen: Dict[Tuple[int, ...], Vector] = {}
    for t in range(1, max_tries + 1):
        x = [rng.randrange(2) for _ in range(m)]
        h = ajtai_hash(A, x, q)
        old = seen.get(h)
        if old is not None and old != x:
            return old, x, t
        seen[h] = x
    raise ValueError("no collision found")


def collision_to_sis(x: Sequence[int], x2: Sequence[int]) -> Vector:
    """z = x - x2 lies in {-1, 0, 1}^m, is nonzero, and A z = 0 mod q."""
    return [a - b for a, b in zip(x, x2)]


def kernel_vector(A: Matrix, q: int) -> Optional[Vector]:
    """A nonzero z with A z = 0 mod a prime q, by Gaussian elimination.

    The entries of z are arbitrary in [0, q), so z is long: this solves the
    linear algebra part of SIS but not the length condition.
    Cost: O(n^2 m) operations mod q.
    """
    n, m = len(A), len(A[0])
    rows = [[x % q for x in r] for r in A]
    pivots: List[int] = []
    r = 0
    for col in range(m):
        piv = next((i for i in range(r, n) if rows[i][col]), None)
        if piv is None:
            continue
        rows[r], rows[piv] = rows[piv], rows[r]
        inv = pow(rows[r][col], -1, q)
        rows[r] = [x * inv % q for x in rows[r]]
        for i in range(n):
            if i != r and rows[i][col]:
                f = rows[i][col]
                rows[i] = [(x - f * y) % q for x, y in zip(rows[i], rows[r])]
        pivots.append(col)
        r += 1
        if r == n:
            break
    free = next((c for c in range(m) if c not in pivots), None)
    if free is None:
        return None
    z = [0] * m
    z[free] = 1
    for i, c in enumerate(pivots):
        z[c] = (-rows[i][free]) % q
    return z
