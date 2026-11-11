# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hidden-field-equations/. The authors are listed in prov/N046XB.jsonl.
"""Hidden field equations (HFE) encryption at toy size, the Matsumoto-Imai
scheme C*, and Patarin's linearization attack on C*.

For study only. The code is not constant time, uses the random module, and the
toy field sizes (n = 7 to 16 bits) give no security. HFE and C* are broken as
proposed; do not use them. For real public-key encryption use a vetted
library, for example libsodium or a FIPS 140 validated module with ML-KEM.

An element of GF(2^n) is an int below 2^n, and the map phi between GF(2^n)
and GF(2)^n is the identity on ints: bit i is the coefficient of t^i.
"""

import hashlib
import random
from typing import Callable, Dict, List, Optional, Sequence, Tuple

# ---------------------------------------------------------------- GF(2^n)

class Field:
    def __init__(self, n: int, modulus: int):
        self.n, self.modulus, self.order = n, modulus, (1 << n) - 1

    def mul(self, a: int, b: int) -> int:
        r = 0
        while b:
            if b & 1:
                r ^= a
            b >>= 1
            a <<= 1
            if (a >> self.n) & 1:
                a ^= self.modulus
        return r

    def pow(self, a: int, e: int) -> int:
        r = 1
        while e:
            if e & 1:
                r = self.mul(r, a)
            a = self.mul(a, a)
            e >>= 1
        return r

    def inv(self, a: int) -> int:
        return self.pow(a, self.order - 1)


MODULI = {7: 0b10000011, 9: 0b1000010001, 11: 0b100000000101, 16: 0b10000000000101101}
# t^7 + t + 1, t^9 + t^4 + 1, t^11 + t^2 + 1, t^16 + t^5 + t^3 + t^2 + 1


# ---------------------------------------------------------------- GF(2) linear algebra

def parity(v: int) -> int:
    return bin(v).count("1") & 1


def mat_vec(rows: Sequence[int], x: int) -> int:
    return sum(parity(r & x) << i for i, r in enumerate(rows))


def invert(rows: Sequence[int], n: int) -> Optional[List[int]]:
    """The inverse of an n x n matrix over GF(2) (row i is an int), or None."""
    a = [(rows[i], 1 << i) for i in range(n)]
    for c in range(n):
        p = next((i for i in range(c, n) if (a[i][0] >> c) & 1), None)
        if p is None:
            return None
        a[c], a[p] = a[p], a[c]
        for i in range(n):
            if i != c and (a[i][0] >> c) & 1:
                a[i] = (a[i][0] ^ a[c][0], a[i][1] ^ a[c][1])
    return [r for _, r in a]


class Affine:
    """x -> M x + c over GF(2)^n, with its inverse."""

    def __init__(self, n: int, rng: random.Random):
        while True:
            self.m = [rng.getrandbits(n) for _ in range(n)]
            self.minv = invert(self.m, n)
            if self.minv is not None:
                break
        self.c = rng.getrandbits(n)

    def __call__(self, x: int) -> int:
        return mat_vec(self.m, x) ^ self.c

    def inverse(self, y: int) -> int:
        return mat_vec(self.minv, y ^ self.c)


def rref(rows: Sequence[int]) -> List[Tuple[int, int]]:
    """Reduced row echelon form over GF(2): a list of (pivot column, row),
    with the pivot at the lowest set bit and cleared from all other rows."""
    out: List[Tuple[int, int]] = []
    for r in rows:
        for c, pr in out:
            if (r >> c) & 1:
                r ^= pr
        if r == 0:
            continue
        c = (r & -r).bit_length() - 1
        out = [(c2, pr ^ r) if (pr >> c) & 1 else (c2, pr) for c2, pr in out]
        out.append((c, r))
    return out


def kernel(rows: Sequence[int], ncols: int) -> List[int]:
    """A basis of {v : <r, v> = 0 for every row r}."""
    red = rref(rows)
    piv = {c for c, _ in red}
    basis = []
    for f in range(ncols):
        if f in piv:
            continue
        v = 1 << f
        for c, r in red:
            if (r >> f) & 1:
                v |= 1 << c
        basis.append(v)
    return basis


def solve_affine(eqs: Sequence[Tuple[int, int]], n: int) -> Optional[Tuple[int, List[int]]]:
    """All x with <a, x> = b for every (a, b): a particular solution and a
    basis of the kernel, or None if there is no solution."""
    red = rref([a | (b << n) for a, b in eqs])
    if any(c == n for c, _ in red):
        return None
    x0 = 0
    for c, r in red:
        if (r >> n) & 1:
            x0 |= 1 << c
    return x0, kernel([a for a, _ in eqs], n)


# ---------------------------------------------------------------- quadratic maps over GF(2)

class QuadraticMap:
    """n_out quadratic polynomials over GF(2) in n variables, packed: quad,
    lin and const hold the coefficients of all polynomials as bits."""

    def __init__(self, n: int, quad: Dict[Tuple[int, int], int], lin: List[int], const: int):
        self.n, self.quad, self.lin, self.const = n, quad, lin, const

    @classmethod
    def interpolate(cls, f: Callable[[int], int], n: int) -> "QuadraticMap":
        """The quadratic polynomials of a map that is quadratic over GF(2):
        c = f(0), l_j = f(e_j) - c, q_jk = f(e_j + e_k) - f(e_j) - f(e_k) + c."""
        c = f(0)
        single = [f(1 << j) for j in range(n)]
        lin = [s ^ c for s in single]
        quad = {(j, k): f((1 << j) | (1 << k)) ^ single[j] ^ single[k] ^ c
                for j in range(n) for k in range(j + 1, n)}
        return cls(n, quad, lin, c)

    def __call__(self, x: int) -> int:
        v = self.const
        for j in range(self.n):
            if (x >> j) & 1:
                v ^= self.lin[j]
                for k in range(j + 1, self.n):
                    if (x >> k) & 1:
                        v ^= self.quad[(j, k)]
        return v


# ---------------------------------------------------------------- polynomials over GF(2^n)

Poly = List[int]   # coefficients, lowest degree first, no trailing zeros


def trim(a: Poly) -> Poly:
    while a and a[-1] == 0:
        a.pop()
    return a


def padd(a: Poly, b: Poly) -> Poly:
    out = [0] * max(len(a), len(b))
    for i, v in enumerate(a):
        out[i] ^= v
    for i, v in enumerate(b):
        out[i] ^= v
    return trim(out)


def pmul(F: Field, a: Poly, b: Poly) -> Poly:
    if not a or not b:
        return []
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                if y:
                    out[i + j] ^= F.mul(x, y)
    return trim(out)


def pdivmod(F: Field, a: Poly, b: Poly) -> Tuple[Poly, Poly]:
    a = list(a)
    q = [0] * max(len(a) - len(b) + 1, 0)
    inv = F.inv(b[-1])
    while len(a) >= len(b):
        c = F.mul(a[-1], inv)
        s = len(a) - len(b)
        q[s] = c
        for i, v in enumerate(b):
            a[s + i] ^= F.mul(c, v)
        trim(a)
    return trim(q), a


def pgcd(F: Field, a: Poly, b: Poly) -> Poly:
    while b:
        a, b = b, pdivmod(F, a, b)[1]
    inv = F.inv(a[-1])
    return [F.mul(v, inv) for v in a]


def frobenius_mod(F: Field, u: Poly, g: Poly, k: int) -> Poly:
    """u^(2^k) mod g, by k squarings."""
    for _ in range(k):
        u = pdivmod(F, pmul(F, u, u), g)[1]
    return u


def roots(F: Field, f: Poly) -> List[int]:
    """All roots of f in GF(2^n). First h = gcd(f, X^(2^n) - X), the product
    of the distinct linear factors; then split h with the trace map
    Tr(beta X) = sum (beta X)^(2^i), which takes only the values 0 and 1 on
    the roots (the Berlekamp trace algorithm)."""
    f = trim(list(f))
    if len(f) <= 1:
        raise ValueError("constant polynomial")
    xq = frobenius_mod(F, [0, 1], f, F.n)
    h = pgcd(F, f, padd(xq, [0, 1]))
    out: List[int] = []

    def split(h: Poly) -> None:
        if len(h) == 2:
            out.append(h[0])           # monic X + h0 has root h0 in characteristic 2
            return
        for i in range(F.n):           # beta runs over the basis 1, t, t^2, ...
            u = pdivmod(F, [0, 1 << i], h)[1]
            tr = list(u)
            for _ in range(F.n - 1):
                u = frobenius_mod(F, u, h, 1)
                tr = padd(tr, u)
            g = pgcd(F, h, tr) if tr else h
            if 1 < len(g) < len(h):
                split(g)
                split(pdivmod(F, h, g)[0])
                return
        raise AssertionError("trace splitting failed")

    if len(h) > 1:
        split(h)
    return sorted(out)


# ---------------------------------------------------------------- HFE

def random_central(F: Field, d: int, rng: random.Random) -> Dict[int, int]:
    """F(X) = sum a_ij X^(2^i + 2^j) + sum b_i X^(2^i) + c with every
    exponent at most d. Each term is quadratic over GF(2)."""
    exps = {0}
    for i in range(F.n):
        if (1 << i) <= d:
            exps.add(1 << i)
        for j in range(i, F.n):
            if (1 << i) + (1 << j) <= d:
                exps.add((1 << i) + (1 << j))
    coeffs = {e: rng.randrange(1 << F.n) for e in exps}
    coeffs[max(exps)] = 1 + rng.randrange((1 << F.n) - 1)
    return coeffs


def central_eval(F: Field, coeffs: Dict[int, int], X: int) -> int:
    v = 0
    for e, a in coeffs.items():
        v ^= F.mul(a, F.pow(X, e))
    return v


def check_bits(m: int, r: int) -> int:
    return int.from_bytes(hashlib.sha256(m.to_bytes(8, "big")).digest()[:4], "big") & ((1 << r) - 1)


class HFEKey:
    def __init__(self, F: Field, central: Dict[int, int], S: Affine, T: Affine, r: int):
        self.F, self.central, self.S, self.T, self.r = F, central, S, T, r


def keygen(n: int, d: int, r: int, rng: random.Random) -> Tuple[QuadraticMap, HFEKey]:
    F = Field(n, MODULI[n])
    central = random_central(F, d, rng)                       # @line L1
    S, T = Affine(n, rng), Affine(n, rng)                     # @line L2
    P = QuadraticMap.interpolate(                             # @line L3
        lambda x: T(central_eval(F, central, S(x))), n)
    return P, HFEKey(F, central, S, T, r)                     # @line L4


def encrypt(P: QuadraticMap, m: int, r: int) -> int:
    x = m | (check_bits(m, r) << (P.n - r))                   # @line L5
    return P(x)                                               # @line L6


def decrypt(sk: HFEKey, y: int) -> Optional[int]:
    F, k = sk.F, sk.F.n - sk.r
    Y = sk.T.inverse(y)                                       # @line L7
    poly = [0] * (max(sk.central) + 1)
    for e, a in sk.central.items():
        poly[e] ^= a
    poly[0] ^= Y
    for X in roots(F, poly):                                  # @line L8
        x = sk.S.inverse(X)                                   # @line L9
        m = x & ((1 << k) - 1)
        if x >> k == check_bits(m, sk.r):
            return m
    return None                                               # @line L10


# ---------------------------------------------------------------- C* (Matsumoto-Imai)

class CStarKey:
    def __init__(self, F: Field, theta: int, S: Affine, T: Affine):
        self.F, self.theta, self.S, self.T = F, theta, S, T
        e = (1 << theta) + 1
        self.h = pow(e, -1, F.order)            # needs gcd(2^theta + 1, 2^n - 1) = 1


def cstar_keygen(n: int, theta: int, rng: random.Random) -> Tuple[QuadraticMap, CStarKey]:
    F = Field(n, MODULI[n])
    S, T = Affine(n, rng), Affine(n, rng)
    e = (1 << theta) + 1
    P = QuadraticMap.interpolate(lambda x: T(F.pow(S(x), e)), n)
    return P, CStarKey(F, theta, S, T)


def cstar_decrypt(sk: CStarKey, y: int) -> int:
    return sk.S.inverse(sk.F.pow(sk.T.inverse(y), sk.h))


# ---------------------------------------------------------------- Patarin's linearization attack

def bilinear_monomials(x: int, y: int, n: int) -> int:
    """The (n + 1)^2 products x_i y_j with x_n = y_n = 1, as bits."""
    xs = [(x >> i) & 1 for i in range(n)] + [1]
    ys = [(y >> j) & 1 for j in range(n)] + [1]
    v = 0
    for i in range(n + 1):
        if xs[i]:
            for j in range(n + 1):
                if ys[j]:
                    v |= 1 << (i * (n + 1) + j)
    return v


def linearization_relations(P: QuadraticMap, n: int, rng: random.Random, extra: int = 40) -> List[int]:
    """Patarin (1995): for C*, B = A^(2^theta + 1) implies
    A * B^(2^theta) = A^(2^(2 theta)) * B, which is bilinear in the plaintext
    x and the ciphertext y. Find all such relations from (n + 1)^2 + extra
    pairs (x, P(x)), using only the public key."""
    rows = []
    for _ in range((n + 1) ** 2 + extra):
        x = rng.getrandbits(n)
        rows.append(bilinear_monomials(x, P(x), n))
    return kernel(rows, (n + 1) ** 2)


def patarin_attack(P: QuadraticMap, n: int, relations: Sequence[int], y: int) -> Optional[int]:
    """Put the ciphertext y into each relation, which leaves a linear
    equation in x; solve and test the few candidates with the public key."""
    ys = [(y >> j) & 1 for j in range(n)] + [1]
    eqs = []
    for rel in relations:
        a, b = 0, 0
        for i in range(n + 1):
            s = 0
            for j in range(n + 1):
                if ys[j] and (rel >> (i * (n + 1) + j)) & 1:
                    s ^= 1
            if i < n:
                a |= s << i
            else:
                b = s
        eqs.append((a, b))
    sol = solve_affine(eqs, n)
    if sol is None:
        return None
    x0, basis = sol
    if len(basis) > 16:
        return None
    for mask in range(1 << len(basis)):
        x = x0
        for i, v in enumerate(basis):
            if (mask >> i) & 1:
                x ^= v
        if P(x) == y:
            return x
    return None
