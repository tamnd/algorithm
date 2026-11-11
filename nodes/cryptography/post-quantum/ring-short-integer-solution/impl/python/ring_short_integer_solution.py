# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ring-short-integer-solution/. The authors are listed in prov/NX628Q.jsonl.
"""Ring-SIS hashing over Z_q[x]/(f) and the collision attack for f = x^n - 1.

ring_hash() computes h(z_1, ..., z_m) = a_1 z_1 + ... + a_m z_m in
Z_q[x]/(f) for the key (a_1, ..., a_m); f is x^n + 1 (sign = -1) or x^n - 1
(sign = +1). With 0/1 inputs this is the SWIFFT-style compression function
(SWIFFT uses n = 64, m = 16, q = 257 and computes the products by an FFT).
cyclic_collision() finds a collision for f = x^n - 1 by working in the
factor x - 1: inputs c_i (1 + x + ... + x^(n-1)) hash to (sum c_i a_i(1)) u.
birthday_collision() finds collisions by brute force for tiny parameters.

For study only. The parameters are toy sizes, the code is not constant time
and uses the random module. For hashing use SHA-2 or SHA-3 from a standard
library or a FIPS 140 validated module.
"""

import random
from typing import Dict, List, Sequence, Tuple

Poly = List[int]


def mul(a: Sequence[int], b: Sequence[int], q: int, sign: int) -> Poly:
    """a b in Z_q[x]/(x^n - sign). sign = -1 gives x^n + 1, sign = +1 gives x^n - 1."""
    n = len(a)
    c = [0] * n
    for i in range(n):
        if a[i] == 0:
            continue
        for j in range(n):
            if b[j] == 0:
                continue
            k = i + j
            if k < n:
                c[k] += a[i] * b[j]
            else:
                c[k - n] += sign * a[i] * b[j]
    return [x % q for x in c]


def ring_hash(key: Sequence[Sequence[int]], z: Sequence[Sequence[int]], q: int, sign: int = -1) -> Tuple[int, ...]:
    """sum_i a_i z_i in Z_q[x]/(x^n - sign). Cost: m n^2 multiplications (m n log n with an FFT)."""
    n = len(key[0])
    acc = [0] * n
    for a, x in zip(key, z):
        acc = [(u + v) % q for u, v in zip(acc, mul(a, x, q, sign))]
    return tuple(acc)


def random_key(n: int, m: int, q: int, rng: random.Random) -> List[Poly]:
    return [[rng.randrange(q) for _ in range(n)] for _ in range(m)]


def random_input(n: int, m: int, rng: random.Random) -> List[Poly]:
    return [[rng.randrange(2) for _ in range(n)] for _ in range(m)]


def is_ring_sis_solution(key, z, q: int, sign: int, bound: int = 1) -> bool:
    """z nonzero, every coefficient in [-bound, bound], and sum a_i z_i = 0."""
    if not any(c for p in z for c in p):
        return False
    if any(abs(c) > bound for p in z for c in p):
        return False
    return all(v == 0 for v in ring_hash(key, [[c % q for c in p] for p in z], q, sign))


def cyclic_collision(key: Sequence[Sequence[int]], q: int, rng: random.Random, tries: int = 100000) -> Tuple[List[Poly], List[Poly]]:
    """A collision of the hash over Z_q[x]/(x^n - 1).

    u = 1 + x + ... + x^(n-1) satisfies a u = a(1) u, because x u = u.
    So an input with z_i = c_i u (c_i in {0, 1}) hashes to (sum c_i a_i(1)) u,
    and two bit vectors c != c' with the same sum c . a(1) mod q collide.
    That is a subset sum mod q in m values: about q^(1/2) tries.
    """
    n, m = len(key[0]), len(key)
    vals = [sum(a) % q for a in key]  # a_i(1)
    seen: Dict[int, Tuple[int, ...]] = {}
    for _ in range(tries):
        c = tuple(rng.randrange(2) for _ in range(m))
        s = sum(ci * v for ci, v in zip(c, vals)) % q
        old = seen.get(s)
        if old is not None and old != c:
            return [[ci] * n for ci in old], [[ci] * n for ci in c]
        seen[s] = c
    raise ValueError("no collision found")


def birthday_collision(key, q: int, sign: int, rng: random.Random, tries: int = 1 << 18) -> Tuple[List[Poly], List[Poly]]:
    """Generic birthday search on 0/1 inputs, for tiny parameters only."""
    n, m = len(key[0]), len(key)
    seen: Dict[Tuple[int, ...], List[Poly]] = {}
    for _ in range(tries):
        z = random_input(n, m, rng)
        h = ring_hash(key, z, q, sign)
        old = seen.get(h)
        if old is not None and old != z:
            return old, z
        seen[h] = z
    raise ValueError("no collision found")


def rotation_block(a: Sequence[int], q: int, sign: int) -> List[List[int]]:
    """The n x n matrix of z -> a z in Z_q[x]/(x^n - sign); column j is x^j a."""
    n = len(a)
    cols, col = [], list(a)
    for _ in range(n):
        cols.append([x % q for x in col])
        col = [(sign * col[-1]) % q] + col[:-1]
    return [[cols[j][i] for j in range(n)] for i in range(n)]


def as_sis_matrix(key, q: int, sign: int) -> List[List[int]]:
    """The n x (m n) SIS matrix [Rot(a_1) | ... | Rot(a_m)]."""
    blocks = [rotation_block(a, q, sign) for a in key]
    n = len(key[0])
    return [sum((blk[i] for blk in blocks), []) for i in range(n)]


def difference(z: Sequence[Sequence[int]], w: Sequence[Sequence[int]]) -> List[Poly]:
    return [[x - y for x, y in zip(p, r)] for p, r in zip(z, w)]
