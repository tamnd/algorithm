# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/learning-with-rounding/. The authors are listed in prov/DNQHCE.jsonl.
"""Learning with rounding (LWR) samples and the toy direct PRF of Banerjee,
Peikert and Rosen (EUROCRYPT 2012).

round_p(x, q, p) maps x in Z_q to the nearest integer of (p/q) x, mod p.
sample_lwr() returns m samples (a_i, round_p(<a_i, s>)).
lwe_then_round() rounds LWE samples, the step in the proof that LWR is
as hard as LWE when q/p is large.
BPRDirectPRF is F(x) = round_p(a^T S_1^x_1 ... S_k^x_k) for k-bit inputs x,
with a uniform vector a and short square matrices S_i.

For study only. The parameters are far too small for any security, the code
is not constant time and uses the random module. For a real PRF use HMAC or
KMAC from a FIPS 140 validated module or the standard library.
"""

import random
from typing import List, Sequence, Tuple

Matrix = List[List[int]]
Vector = List[int]


def round_p(x: int, q: int, p: int) -> int:
    """The nearest integer to (p/q) x, reduced mod p (ties round up).

    Exact integer arithmetic: floor((p x + q/2) / q) for x in [0, q).
    """
    x %= q
    return ((p * x + q // 2) // q) % p


def sample_lwr(
    n: int, m: int, q: int, p: int, rng: random.Random, s: Sequence[int] = None
) -> Tuple[Matrix, Vector, Vector]:
    """m LWR samples: A uniform in Z_q^(m x n), b_i = round_p(<a_i, s>). Returns (A, b, s)."""
    if s is None:
        s = [rng.randrange(q) for _ in range(n)]
    A = [[rng.randrange(q) for _ in range(n)] for _ in range(m)]
    b = [round_p(sum(x * y for x, y in zip(row, s)), q, p) for row in A]
    return A, b, list(s)


def lwe_then_round(A: Matrix, s: Sequence[int], e: Sequence[int], q: int, p: int) -> Vector:
    """round_p(<a_i, s> + e_i) for each row: rounded LWE samples."""
    return [round_p(sum(x * y for x, y in zip(row, s)) + ei, q, p) for row, ei in zip(A, e)]


def mat_vec_left(v: Sequence[int], M: Matrix, q: int) -> Vector:
    """The row vector v^T M mod q."""
    n = len(M[0])
    return [sum(v[i] * M[i][j] for i in range(len(v))) % q for j in range(n)]


class BPRDirectPRF:
    """F(x) = round_p(a^T prod_{i: x_i = 1} S_i) for x in {0,1}^k.

    a is uniform in Z_q^n and each S_i is an n x n matrix with entries in
    [-bound, bound]. The output lies in Z_p^n. Cost per input: at most k
    vector-matrix products, k n^2 multiplications mod q.
    """

    def __init__(self, n: int, k: int, q: int, p: int, rng: random.Random, bound: int = 1):
        self.n, self.k, self.q, self.p = n, k, q, p
        self.a = [rng.randrange(q) for _ in range(n)]
        self.S = [
            [[rng.randint(-bound, bound) % q for _ in range(n)] for _ in range(n)] for _ in range(k)
        ]

    def unrounded(self, x: Sequence[int]) -> Vector:
        v = list(self.a)
        for bit, S in zip(x, self.S):
            if bit:
                v = mat_vec_left(v, S, self.q)
        return v

    def __call__(self, x: Sequence[int]) -> Vector:
        if len(x) != self.k or any(b not in (0, 1) for b in x):
            raise ValueError("input must be a 0/1 vector of length k")
        return [round_p(y, self.q, self.p) for y in self.unrounded(x)]
