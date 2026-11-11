# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mceliece-cryptosystem/. The authors are listed in prov/060YA3.jsonl.
"""Toy McEliece encryption with a binary Goppa code and Patterson decoding.

The code works over GF(2^m) for a small m (the tests use m = 6, n = 64 and
t = 5). It follows McEliece's 1978 scheme: the public key is G' = S G P for a
generator matrix G of a binary Goppa code, a ciphertext is c = m G' + e with
an error e of weight t, and the owner removes e with Patterson's algorithm.

This is NOT Classic McEliece. Classic McEliece uses the Niederreiter form, a
KEM with SHAKE256, n = 3488 and more, a systematic public key, and exact
encodings; none of that is here, and there are no KAT tests.

For study only. The code is not constant time, uses the random module, and
the parameters are far too small for any security. Use a vetted library, for
example a FIPS 140 validated module, to protect real data.

Binary vectors and matrix rows are Python ints (bit j is position j).
Polynomials over GF(2^m) are lists of field elements, lowest degree first,
with no trailing zeros (the zero polynomial is []).
"""

import random
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


# ---------------------------------------------------------------- polynomials

def trim(a: Poly) -> Poly:
    while a and a[-1] == 0:
        a.pop()
    return a


def deg(a: Poly) -> int:
    return len(a) - 1  # -1 for the zero polynomial


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
    if not b:
        raise ZeroDivisionError("division by the zero polynomial")
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
    """a^-1 mod g by the extended Euclidean algorithm (g irreducible, a != 0 mod g)."""
    r0, r1 = list(g), pmod(f, a, g)
    v0, v1 = [], [1]
    while deg(r1) > 0:
        q, r = pdivmod(f, r0, r1)
        r0, r1 = r1, r
        v0, v1 = v1, padd(v0, pmul(f, q, v1))
    if not r1:
        raise ZeroDivisionError("not invertible modulo g")
    return pmul(f, v1, [f.inv(r1[0])])


def psquare_mod(f: Field, a: Poly, g: Poly) -> Poly:
    return pmod(f, pmul(f, a, a), g)


def psqrt_mod(f: Field, a: Poly, g: Poly) -> Poly:
    """The square root of a in GF(2^m)[x]/(g), a field with 2^(m t) elements:
    sqrt(a) = a^(2^(m t - 1)), that is, m t - 1 squarings."""
    for _ in range(f.m * deg(g) - 1):
        a = psquare_mod(f, a, g)
    return a


def pgcd(f: Field, a: Poly, b: Poly) -> Poly:
    while b:
        a, b = b, pmod(f, a, b)
    return a


def is_irreducible(f: Field, g: Poly) -> bool:
    """Ben-Or's test: g of degree t is irreducible over GF(q) if and only if
    gcd(g, x^(q^i) - x) = 1 for i = 1 .. t // 2."""
    t = deg(g)
    xp = [0, 1]
    for _ in range(1, t // 2 + 1):
        for _ in range(f.m):          # x^(q^i) = (x^(q^(i-1)))^q, q = 2^m
            xp = psquare_mod(f, xp, g)
        if deg(pgcd(f, g, padd(xp, [0, 1]))) > 0:
            return False
    return True


def random_irreducible(f: Field, t: int, rng: random.Random) -> Poly:
    while True:
        g = [rng.randrange(f.q) for _ in range(t)] + [1]
        if g[0] and is_irreducible(f, trim(g)):
            return g


# ---------------------------------------------------------------- binary matrices

def rank(rows: Sequence[int]) -> int:
    basis: List[int] = []
    for row in rows:
        for b in basis:
            row = min(row, row ^ b)
        if row:
            basis.append(row)
            basis.sort(reverse=True)
    return len(basis)


def nullspace(rows: Sequence[int], n: int) -> List[int]:
    """A basis of {x : rows . x = 0} over GF(2), for vectors of n bits."""
    piv: List[Tuple[int, int]] = []           # (pivot column, reduced row)
    for row in rows:
        for c, b in piv:
            if (row >> c) & 1:
                row ^= b
        if row:
            c = row.bit_length() - 1
            piv = [(c2, b ^ row if (b >> c) & 1 else b) for c2, b in piv]
            piv.append((c, row))
    pivots = {c for c, _ in piv}
    basis = []
    for free in range(n):
        if free in pivots:
            continue
        x = 1 << free
        for c, b in piv:
            if (b >> free) & 1:
                x |= 1 << c
        basis.append(x)
    return basis


def solve_left(rows: Sequence[int], y: int) -> Optional[int]:
    """Some u (bit i for row i) with XOR of rows[i] over u_i = 1 equal to y, or None."""
    basis: List[Tuple[int, int]] = []         # (vector, combination), distinct leading bits
    for i, row in enumerate(rows):
        comb = 1 << i
        for v, cmb in basis:
            if row ^ v < row:
                row ^= v
                comb ^= cmb
        if row:
            basis.append((row, comb))
            basis.sort(key=lambda p: -p[0])
    u = 0
    for v, cmb in basis:
        if y ^ v < y:
            y ^= v
            u ^= cmb
    return u if y == 0 else None


def vec_mat(u: int, rows: Sequence[int]) -> int:
    out = 0
    for i, row in enumerate(rows):
        if (u >> i) & 1:
            out ^= row
    return out


def random_invertible(k: int, rng: random.Random) -> List[int]:
    while True:
        s = [rng.getrandbits(k) for _ in range(k)]
        if rank(s) == k:
            return s


def invert(s: Sequence[int]) -> List[int]:
    """The inverse of an invertible k x k binary matrix (rows as ints)."""
    k = len(s)
    return [solve_left(s, 1 << j) for j in range(k)]


# ---------------------------------------------------------------- the Goppa code

class Goppa:
    """The binary Goppa code Gamma(L, g) with support L = (a_0, ..., a_{n-1})."""

    def __init__(self, f: Field, g: Poly, support: Sequence[int]):
        self.f, self.g, self.support = f, g, list(support)
        self.t = deg(g)
        self.n = len(support)
        # Column i: the coefficients of 1 / (x - a_i) mod g, as m t bits.
        self.cols = [pinv_mod(f, [a, 1], g) for a in support]
        m, t = f.m, self.t
        self.h = [0] * (m * t)
        for i, col in enumerate(self.cols):
            for d in range(t):
                c = col[d] if d < len(col) else 0
                for b in range(m):
                    if (c >> b) & 1:
                        self.h[d * m + b] |= 1 << i

    def syndrome_poly(self, y: int) -> Poly:
        """S(x) = sum over the ones y_i of 1 / (x - a_i) mod g."""
        s: Poly = []
        for i in range(self.n):
            if (y >> i) & 1:
                s = padd(s, self.cols[i])
        return s

    def patterson(self, y: int) -> Optional[int]:
        """The error e with wt(e) <= t and y + e in the code, or None."""
        f, g, t = self.f, self.g, self.t
        s = self.syndrome_poly(y)
        if not s:
            return 0
        tt = pinv_mod(f, s, g)                       # T = S^-1 mod g
        if tt == [0, 1]:
            sigma: Poly = [0, 1]                     # T = x: one error at a = 0
        else:
            tau = psqrt_mod(f, padd(tt, [0, 1]), g)  # tau^2 = T + x mod g
            r0, r1, v0, v1 = list(g), tau, [], [1]
            while deg(r1) > t // 2:                  # a = b tau mod g with small degrees
                q, r = pdivmod(f, r0, r1)
                r0, r1 = r1, r
                v0, v1 = v1, padd(v0, pmul(f, q, v1))
            a, b = r1, v1
            sigma = padd(pmul(f, a, a), pmul(f, [0, 1], pmul(f, b, b)))
        e = 0
        for i, alpha in enumerate(self.support):
            if peval(f, sigma, alpha) == 0:
                e |= 1 << i
        if bin(e).count("1") != deg(sigma):
            return None
        return e


# ---------------------------------------------------------------- McEliece

def keygen(f: Field, n: int, t: int, rng: random.Random):
    """Returns (pk, sk) with pk = (G', t) and sk = (S^-1, Goppa code, permutation)."""
    g = random_irreducible(f, t, rng)                         # @line L1
    support = rng.sample(range(f.q), n)
    code = Goppa(f, g, support)
    gen = nullspace(code.h, n)                                # @line L2
    k = len(gen)
    s = random_invertible(k, rng)                             # @line L3
    perm = list(range(n))
    rng.shuffle(perm)
    sg = [vec_mat(row, gen) for row in s]
    pub = []
    for row in sg:                                            # G' = S G P: column j of G' is column perm[j] of S G
        out = 0
        for j in range(n):
            if (row >> perm[j]) & 1:
                out |= 1 << j
        pub.append(out)
    return (pub, n, t), (invert(s), code, gen, perm)          # @line L4


def encrypt(pk, msg: int, rng: random.Random) -> int:
    """c = msg G' + e with a random e of weight t. msg has k bits."""
    pub, n, t = pk
    e = 0
    for i in rng.sample(range(n), t):                        # @line L5
        e |= 1 << i
    return vec_mat(msg, pub) ^ e                              # @line L6


def decrypt(sk, c: int) -> Optional[int]:
    s_inv, code, gen, perm = sk
    y = 0
    for j, pj in enumerate(perm):                             # @line L7
        if (c >> j) & 1:
            y |= 1 << pj
    e = code.patterson(y)                                     # @line L8
    if e is None:
        return None
    u = solve_left(gen, y ^ e)                                # @line L9
    if u is None:
        return None
    return vec_mat(u, s_inv)                                  # @line L10


FIELD64 = Field(6, 0b1000011)   # x^6 + x + 1
FIELD16 = Field(4, 0b10011)     # x^4 + x + 1
