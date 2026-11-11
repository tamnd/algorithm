# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/niederreiter-cryptosystem/. The authors are listed in prov/3XG2CE.jsonl.
"""Toy Niederreiter encryption with a binary Goppa code.

The message is encoded as an error vector e of weight t (constant weight
encoding with the combinatorial number system), and the ciphertext is the
syndrome s = H' e of e under the public parity check matrix H' = M H P. The
owner removes M, decodes the syndrome with Patterson's algorithm, removes P,
and decodes the message from e.

The Goppa code and Patterson's algorithm are a local copy of the code on the
McEliece page. This is NOT Classic McEliece: there is no KEM, no hashing, no
systematic key, and the parameters (m = 6, n = 64, t = 5) give no security.

For study only. The code is not constant time and uses the random module.
Use a vetted library, for example a FIPS 140 validated module, to protect
real data.

Binary vectors and matrix rows are Python ints (bit j is position j).
Polynomials over GF(2^m) are lists of field elements, lowest degree first,
with no trailing zeros.
"""

import random
from math import comb
from typing import List, Optional, Sequence, Tuple

Poly = List[int]


class Field:
    """GF(2^m) given by a primitive polynomial `modulus` of degree m."""

    def __init__(self, m: int, modulus: int):
        self.m = m
        self.q = 1 << m
        self.exp = [0] * (2 * self.q)
        self.log = [0] * self.q
        x = 1
        for i in range(self.q - 1):
            self.exp[i] = x
            self.log[x] = i
            x <<= 1
            if x & self.q:
                x ^= modulus
        if x != 1:
            raise ValueError("modulus is not primitive")
        for i in range(self.q - 1, 2 * self.q):
            self.exp[i] = self.exp[i - (self.q - 1)]

    def mul(self, a: int, b: int) -> int:
        if a == 0 or b == 0:
            return 0
        return self.exp[self.log[a] + self.log[b]]

    def inv(self, a: int) -> int:
        if a == 0:
            raise ZeroDivisionError("0 has no inverse")
        return self.exp[(self.q - 1 - self.log[a]) % (self.q - 1)]


def trim(a: Poly) -> Poly:
    while a and a[-1] == 0:
        a.pop()
    return a


def deg(a: Poly) -> int:
    return len(a) - 1


def padd(a: Poly, b: Poly) -> Poly:
    n = max(len(a), len(b))
    return trim([(a[i] if i < len(a) else 0) ^ (b[i] if i < len(b) else 0) for i in range(n)])


def pmul(f: Field, a: Poly, b: Poly) -> Poly:
    if not a or not b:
        return []
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                out[i + j] ^= f.mul(x, y)
    return trim(out)


def pdivmod(f: Field, a: Poly, b: Poly) -> Tuple[Poly, Poly]:
    a = list(a)
    q = [0] * max(0, len(a) - len(b) + 1)
    inv_lead = f.inv(b[-1])
    while len(a) >= len(b) and a:
        c = f.mul(a[-1], inv_lead)
        shift = len(a) - len(b)
        q[shift] = c
        for i, y in enumerate(b):
            a[shift + i] ^= f.mul(c, y)
        trim(a)
    return trim(q), a


def pmod(f: Field, a: Poly, b: Poly) -> Poly:
    return pdivmod(f, a, b)[1]


def peval(f: Field, a: Poly, x: int) -> int:
    y = 0
    for c in reversed(a):
        y = f.mul(y, x) ^ c
    return y


def pinv_mod(f: Field, a: Poly, g: Poly) -> Poly:
    r0, r1 = list(g), pmod(f, a, g)
    v0, v1 = [], [1]
    while deg(r1) > 0:
        q, r = pdivmod(f, r0, r1)
        r0, r1 = r1, r
        v0, v1 = v1, padd(v0, pmul(f, q, v1))
    if not r1:
        raise ZeroDivisionError("not invertible modulo g")
    return pmul(f, v1, [f.inv(r1[0])])


def psqrt_mod(f: Field, a: Poly, g: Poly) -> Poly:
    for _ in range(f.m * deg(g) - 1):
        a = pmod(f, pmul(f, a, a), g)
    return a


def is_irreducible(f: Field, g: Poly) -> bool:
    t = deg(g)
    xp = [0, 1]
    for _ in range(1, t // 2 + 1):
        for _ in range(f.m):
            xp = pmod(f, pmul(f, xp, xp), g)
        a, b = list(g), padd(xp, [0, 1])
        while b:
            a, b = b, pmod(f, a, b)
        if deg(a) > 0:
            return False
    return True


def random_irreducible(f: Field, t: int, rng: random.Random) -> Poly:
    while True:
        g = [rng.randrange(f.q) for _ in range(t)] + [1]
        if g[0] and is_irreducible(f, trim(g)):
            return g


def rank(rows: Sequence[int]) -> int:
    basis: List[int] = []
    for row in rows:
        for b in basis:
            row = min(row, row ^ b)
        if row:
            basis.append(row)
            basis.sort(reverse=True)
    return len(basis)


def parity(x: int) -> int:
    return bin(x).count("1") & 1


def mat_vec(rows: Sequence[int], x: int) -> int:
    """The column vector M x: bit i is the parity of row i AND x."""
    return sum(parity(row & x) << i for i, row in enumerate(rows))


def mat_mul(a: Sequence[int], b: Sequence[int]) -> List[int]:
    """A B for binary matrices given by rows."""
    out = []
    for row in a:
        acc = 0
        for i, brow in enumerate(b):
            if (row >> i) & 1:
                acc ^= brow
        out.append(acc)
    return out


def invert(a: Sequence[int]) -> List[int]:
    """The inverse of an invertible r x r binary matrix, by Gauss-Jordan elimination."""
    r = len(a)
    rows = [(a[i], 1 << i) for i in range(r)]
    for c in range(r):
        piv = next(i for i in range(c, r) if (rows[i][0] >> c) & 1)
        rows[c], rows[piv] = rows[piv], rows[c]
        for i in range(r):
            if i != c and (rows[i][0] >> c) & 1:
                rows[i] = (rows[i][0] ^ rows[c][0], rows[i][1] ^ rows[c][1])
    return [rows[i][1] for i in range(r)]


class Goppa:
    """The binary Goppa code Gamma(L, g), with its mt x n parity check matrix."""

    def __init__(self, f: Field, g: Poly, support: Sequence[int]):
        self.f, self.g, self.support = f, g, list(support)
        self.t, self.n = deg(g), len(support)
        cols = [pinv_mod(f, [a, 1], g) for a in support]
        m, t = f.m, self.t
        self.h = [0] * (m * t)                   # row d m + b: bit b of coefficient d
        for i, col in enumerate(cols):
            for d, c in enumerate(col):
                for b in range(m):
                    if (c >> b) & 1:
                        self.h[d * m + b] |= 1 << i

    def poly_from_syndrome(self, s: int) -> Poly:
        m = self.f.m
        return trim([(s >> (d * m)) & ((1 << m) - 1) for d in range(self.t)])

    def patterson(self, s: int) -> Optional[int]:
        """The e with wt(e) <= t and H e = s, or None."""
        f, g, t = self.f, self.g, self.t
        sp = self.poly_from_syndrome(s)
        if not sp:
            return 0
        tt = pinv_mod(f, sp, g)
        if tt == [0, 1]:
            sigma: Poly = [0, 1]
        else:
            tau = psqrt_mod(f, padd(tt, [0, 1]), g)
            r0, r1, v0, v1 = list(g), tau, [], [1]
            while deg(r1) > t // 2:
                q, r = pdivmod(f, r0, r1)
                r0, r1 = r1, r
                v0, v1 = v1, padd(v0, pmul(f, q, v1))
            sigma = padd(pmul(f, r1, r1), pmul(f, [0, 1], pmul(f, v1, v1)))
        e = 0
        for i, alpha in enumerate(self.support):
            if peval(f, sigma, alpha) == 0:
                e |= 1 << i
        if bin(e).count("1") != deg(sigma):
            return None
        return e


# ---------------------------------------------------------------- constant weight encoding

def cw_encode(x: int, n: int, t: int) -> int:
    """The weight t vector whose positions c_1 > ... > c_t satisfy
    x = C(c_1, t) + C(c_2, t - 1) + ... + C(c_t, 1) (combinatorial number system)."""
    if not 0 <= x < comb(n, t):
        raise ValueError("message out of range")
    e = 0
    c = n
    for i in range(t, 0, -1):
        c -= 1
        while comb(c, i) > x:
            c -= 1
        x -= comb(c, i)
        e |= 1 << c
    return e


def cw_decode(e: int, t: int) -> int:
    positions = [c for c in range(e.bit_length()) if (e >> c) & 1]
    if len(positions) != t:
        raise ValueError("wrong weight")
    return sum(comb(c, i + 1) for i, c in enumerate(positions))


# ---------------------------------------------------------------- Niederreiter

def keygen(f: Field, n: int, t: int, rng: random.Random):
    """Returns (pk, sk) with pk = (H', n, t) and sk = (M^-1, code, permutation)."""
    g = random_irreducible(f, t, rng)                         # @line L1
    code = Goppa(f, g, rng.sample(range(f.q), n))
    h = code.h                                                # @line L2
    r = len(h)
    while True:                                               # @line L3
        mm = [rng.getrandbits(r) for _ in range(r)]
        if rank(mm) == r:
            break
    perm = list(range(n))
    rng.shuffle(perm)
    mh = mat_mul(mm, h)
    pub = []
    for row in mh:                                            # column j of H' is column perm[j] of M H
        out = 0
        for j in range(n):
            if (row >> perm[j]) & 1:
                out |= 1 << j
        pub.append(out)
    return (pub, n, t), (invert(mm), code, perm)              # @line L4


def encrypt(pk, x: int) -> int:
    """The syndrome of the constant weight encoding of x, 0 <= x < C(n, t)."""
    pub, n, t = pk
    e = cw_encode(x, n, t)                                    # @line L5
    return mat_vec(pub, e)                                    # @line L6


def decrypt(sk, s: int) -> Optional[int]:
    m_inv, code, perm = sk
    s1 = mat_vec(m_inv, s)                                    # @line L7
    e1 = code.patterson(s1)                                   # @line L8
    if e1 is None or bin(e1).count("1") != code.t:
        return None
    e = 0
    for j, pj in enumerate(perm):                             # @line L9
        if (e1 >> pj) & 1:
            e |= 1 << j
    return cw_decode(e, code.t)                               # @line L10


FIELD64 = Field(6, 0b1000011)   # x^6 + x + 1
FIELD16 = Field(4, 0b10011)     # x^4 + x + 1
