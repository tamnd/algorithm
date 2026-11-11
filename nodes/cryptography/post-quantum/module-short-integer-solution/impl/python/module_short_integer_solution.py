# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/module-short-integer-solution/. The authors are listed in prov/2Y9DFJ.jsonl.
"""Module-SIS over R_q = Z_q[x]/(x^n + 1): instance generator, checker and
a toy collision solver.

An instance is a k x l matrix A of polynomials in R_q. A solution is a
nonzero z in R^l with A z = 0 in R_q^k and every coefficient of z at most
beta in absolute value (the infinity norm, as in ML-DSA).

generate_instance() draws A uniformly. is_solution() checks a candidate.
as_sis_matrix() writes A as an ordinary (k n) x (l n) SIS matrix with
negacyclic blocks. birthday_solver() hashes random binary z until two
collide and returns their difference, a solution with beta = 1. Its cost
is about q^(k n / 2) tries, so it only works on toy sizes.

For study only. The parameters are toy sizes, the code is not constant time
and uses the random module. For ML-DSA use a FIPS 140 validated module or a
maintained library such as liboqs or PQClean.
"""

import random
from typing import Dict, List, Sequence, Tuple

Poly = List[int]
PolyVec = List[Poly]
PolyMat = List[List[Poly]]


def poly_mul(a: Sequence[int], b: Sequence[int], q: int) -> Poly:
    """a b in Z_q[x]/(x^n + 1), schoolbook."""
    n = len(a)
    c = [0] * n
    for i in range(n):
        if a[i] == 0:
            continue
        for j in range(n):
            k = i + j
            if k < n:
                c[k] += a[i] * b[j]
            else:
                c[k - n] -= a[i] * b[j]
    return [x % q for x in c]


def mat_vec(A: PolyMat, z: PolyVec, q: int) -> PolyVec:
    """A z in R_q^k."""
    n = len(z[0])
    out = []
    for row in A:
        acc = [0] * n
        for a, zi in zip(row, z):
            acc = [(s + t) % q for s, t in zip(acc, poly_mul(a, zi, q))]
        out.append(acc)
    return out


def generate_instance(n: int, k: int, l: int, q: int, rng: random.Random) -> PolyMat:
    """A uniform k x l matrix over R_q."""
    return [[[rng.randrange(q) for _ in range(n)] for _ in range(l)] for _ in range(k)]


def centered(x: int, q: int) -> int:
    x %= q
    return x - q if x > q // 2 else x


def inf_norm(z: PolyVec) -> int:
    return max((abs(c) for p in z for c in p), default=0)


def is_solution(A: PolyMat, z: PolyVec, q: int, beta: int) -> bool:
    """z != 0, ||z||_inf <= beta (integer coefficients) and A z = 0 in R_q^k."""
    if len(z) != len(A[0]) or any(len(p) != len(A[0][0]) for p in z):
        return False
    if not any(c for p in z for c in p) or inf_norm(z) > beta:
        return False
    return all(c == 0 for p in mat_vec(A, [[c % q for c in p] for p in z], q) for c in p)


def negacyclic_block(a: Sequence[int], q: int) -> List[List[int]]:
    """The n x n matrix of z -> a z in R_q; column j holds x^j a."""
    n = len(a)
    cols, col = [], list(a)
    for _ in range(n):
        cols.append([c % q for c in col])
        col = [(-col[-1]) % q] + col[:-1]
    return [[cols[j][i] for j in range(n)] for i in range(n)]


def as_sis_matrix(A: PolyMat, q: int) -> List[List[int]]:
    """The (k n) x (l n) integer matrix of A."""
    n = len(A[0][0])
    rows = []
    for row in A:
        blocks = [negacyclic_block(a, q) for a in row]
        for i in range(n):
            rows.append(sum((blk[i] for blk in blocks), []))
    return rows


def birthday_solver(A: PolyMat, q: int, rng: random.Random, tries: int = 1 << 18) -> PolyVec:
    """A Module-SIS solution with beta = 1 from a collision of z -> A z on binary z."""
    k, l, n = len(A), len(A[0]), len(A[0][0])
    seen: Dict[Tuple[int, ...], PolyVec] = {}
    for _ in range(tries):
        z = [[rng.randrange(2) for _ in range(n)] for _ in range(l)]
        key = tuple(c for p in mat_vec(A, z, q) for c in p)
        old = seen.get(key)
        if old is not None and old != z:
            return [[x - y for x, y in zip(p, r)] for p, r in zip(z, old)]
        seen[key] = z
    raise ValueError("no collision found")


def ml_dsa_shape(name: str) -> Tuple[int, int, int, int]:
    """(n, k, l, q) of the ML-DSA matrix A for each FIPS 204 parameter set."""
    q = 8380417
    return {"ML-DSA-44": (256, 4, 4, q), "ML-DSA-65": (256, 6, 5, q), "ML-DSA-87": (256, 8, 7, q)}[name]
