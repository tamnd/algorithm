# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/private-information-retrieval/. The authors are listed in prov/Q7ZEPD.jsonl.
"""Private information retrieval: three schemes on a database of n bits.

1. Cube schemes of Chor, Goldreich, Kushilevitz and Sudan (1995) with 2^d
   servers: d = 1 is the basic 2-server XOR scheme (n bits up per server,
   1 bit down), d = 2 is the square scheme with 4 servers (2 sqrt(n) bits
   up per server, 1 bit down).
2. The balanced 2-server scheme: the database is a sqrt(n) x sqrt(n)
   matrix, the query is a subset of columns, and each server answers one
   bit per row, so 4 sqrt(n) bits in total.
3. The single-server scheme of Kushilevitz and Ostrovsky (1997) with
   Goldwasser-Micali on a toy modulus (a small local copy): k (s + t) bits
   for an s x t matrix, where k is the size of the modulus.

Each function returns the bit and the number of bits sent in each direction.

For study only. The code is not constant time, uses Python's random module,
and the 62-bit modulus gives no security. Use a maintained library (for
example SealPIR, or the SimplePIR code) for real data.
"""

import math
import random
from dataclasses import dataclass
from typing import Sequence


@dataclass
class Cost:
    up: int = 0          # bits from the client to the servers
    down: int = 0        # bits from the servers to the client


# ---------------------------------------------------------------- the trivial scheme


def trivial(db: Sequence[int], i: int) -> tuple[int, Cost]:
    """The server sends the whole database: n bits, and nothing is revealed."""
    return db[i], Cost(0, len(db))


# ---------------------------------------------------------------- cube schemes


def cube_pir(db: Sequence[int], i: int, d: int, rng: random.Random) -> tuple[int, Cost, list]:
    """CGKS with 2^d servers. The n = l^d bits are a d-dimensional cube.

    The client picks random subsets S_1..S_d of [l]. Server sigma, for
    sigma in {0,1}^d, gets the subsets S_k xor (sigma_k ? {i_k} : {}) and
    returns the XOR of the bits at all points of their product. Each point
    other than i is counted an even number of times over all servers, so
    the XOR of the 2^d answers is x_i. Returns also the queries."""
    n = len(db)
    side = round(n ** (1 / d))
    assert side ** d == n, "n must be a perfect d-th power"
    coords = []
    rest = i
    for _ in range(d):
        coords.append(rest % side)
        rest //= side
    subsets = [rng.getrandbits(side) for _ in range(d)]       # bit j set: j in S_k
    cost = Cost()
    total = 0
    queries = []
    for sigma in range(1 << d):
        query = [subsets[k] ^ (((sigma >> k) & 1) << coords[k]) for k in range(d)]
        queries.append(query)
        cost.up += d * side
        total ^= _cube_answer(db, query, side, d)
        cost.down += 1
    return total, cost, queries


def _cube_answer(db: Sequence[int], query: list[int], side: int, d: int) -> int:
    """XOR of x at all points (j_1..j_d) with j_k in the k-th subset."""
    ans = 0
    for idx, bit in enumerate(db):
        if not bit:
            continue
        rest, inside = idx, True
        for k in range(d):
            if not (query[k] >> (rest % side)) & 1:
                inside = False
                break
            rest //= side
        if inside:
            ans ^= 1
    return ans


def balanced_two_server(db: Sequence[int], i: int, rng: random.Random) -> tuple[int, Cost]:
    """Two servers, database as an s x s matrix (row r, column c at r*s + c).

    The client sends a random column subset S to server 1 and S xor {c} to
    server 2. Each server returns, for every row, the XOR of the bits of that
    row in its subset: s bits. Row r of the two answers XORs to x[r][c]."""
    s = math.isqrt(len(db))
    assert s * s == len(db)
    r, c = divmod(i, s)
    q1 = rng.getrandbits(s)
    q2 = q1 ^ (1 << c)

    def answer(q: int) -> list[int]:
        out = []
        for row in range(s):
            acc = 0
            for col in range(s):
                if (q >> col) & 1:
                    acc ^= db[row * s + col]
            out.append(acc)
        return out

    a1, a2 = answer(q1), answer(q2)
    return a1[r] ^ a2[r], Cost(2 * s, 2 * s)


# ---------------------------------------------------------------- Goldwasser-Micali


def is_probable_prime(n: int, rng: random.Random, rounds: int = 30) -> bool:
    if n < 2:
        return False
    for sp in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29):
        if n % sp == 0:
            return n == sp
    d, r = n - 1, 0
    while d % 2 == 0:
        d //= 2
        r += 1
    for _ in range(rounds):
        a = rng.randrange(2, n - 1)
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(r - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def blum_prime(bits: int, rng: random.Random) -> int:
    """A random prime p = 3 mod 4 of the given size."""
    while True:
        p = rng.getrandbits(bits) | (1 << (bits - 1)) | 3
        if is_probable_prime(p, rng):
            return p


@dataclass(frozen=True)
class GMKey:
    p: int
    q: int

    @property
    def n(self) -> int:
        return self.p * self.q

    def is_qr(self, z: int) -> bool:
        """Quadratic residue mod N: a square mod p and mod q (Euler's criterion)."""
        return pow(z, (self.p - 1) // 2, self.p) == 1 and pow(z, (self.q - 1) // 2, self.q) == 1


def gm_keygen(bits: int, rng: random.Random) -> GMKey:
    p = blum_prime(bits, rng)
    while True:
        q = blum_prime(bits, rng)
        if q != p:
            return GMKey(p, q)


def jacobi(a: int, n: int) -> int:
    """The Jacobi symbol (a/n) for odd n > 0."""
    a %= n
    result = 1
    while a:
        while a % 2 == 0:
            a //= 2
            if n % 8 in (3, 5):
                result = -result
        a, n = n, a
        if a % 4 == 3 and n % 4 == 3:
            result = -result
        a %= n
    return result if n == 1 else 0


def random_unit(n: int, rng: random.Random) -> int:
    while True:
        r = rng.randrange(2, n)
        if math.gcd(r, n) == 1:
            return r


def ko_query(key: GMKey, t: int, col: int, rng: random.Random) -> list[int]:
    """t numbers mod N, all with Jacobi symbol +1: a non-residue in column
    col and residues elsewhere. With p, q = 3 mod 4, -1 is a non-residue
    mod both, so -r^2 is a non-residue with Jacobi symbol +1."""
    out = []
    for j in range(t):
        r2 = pow(random_unit(key.n, rng), 2, key.n)
        out.append((key.n - r2) % key.n if j == col else r2)
    return out


def ko_answer(db: Sequence[int], s: int, t: int, ys: Sequence[int], modulus: int) -> list[int]:
    """For each row r: z_r = product over j of (y_j if x[r][j] = 1 else y_j^2).
    z_r is a residue exactly when the row has a 0 in the hidden column."""
    out = []
    for r in range(s):
        z = 1
        for j in range(t):
            y = ys[j]
            z = z * (y if db[r * t + j] else y * y) % modulus
        out.append(z)
    return out


def kushilevitz_ostrovsky(db: Sequence[int], i: int, s: int, t: int, key: GMKey,
                          rng: random.Random) -> tuple[int, Cost, list[int]]:
    """Single-server PIR for bit i of an s x t matrix (row i // t, column i % t)."""
    assert len(db) == s * t
    row, col = divmod(i, t)
    ys = ko_query(key, t, col, rng)
    zs = ko_answer(db, s, t, ys, key.n)
    k = key.n.bit_length()
    bit = 0 if key.is_qr(zs[row]) else 1
    return bit, Cost(k * t, k * s), ys
