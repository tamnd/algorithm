# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ntru-problem/. The authors are listed in prov/C899GW.jsonl.
"""Toy NTRU (Hoffstein, Pipher and Silverman 1998) and the lattice attack on
the NTRU problem with a local LLL.

The ring is Z[x]/(x^n - 1) with n prime, p = 3 and q a power of 2.
keygen() draws ternary f and g, computes f^-1 mod q (inverse mod 2 by the
extended Euclidean algorithm, then Newton lifting to q) and f^-1 mod 3
(extended Euclid over F_3), and returns h = p f_q g mod q.
The NTRU problem: given h' = g / f mod q (here h' = p^-1 h), find short
(f, g). lattice_attack() reduces the basis [[I, H], [0, q I]] with LLL and
then searches the reduced rows and their pairwise sums and differences for
a vector of the public key shape. On these toy sizes it almost always
returns (f, g) times a signed power of x; rarely it finds another key of
the same shape, or nothing.

For study only. The sizes are toy sizes (n about 11 to 17), far below any
secure parameter, the code is not constant time and uses the random module.
For NTRU-based cryptography use a maintained library, for example liboqs or
the sntrup761 code in OpenSSH, or ML-KEM from a FIPS 140 validated module.
"""

import random
from typing import List, Optional, Sequence, Tuple

Poly = List[int]


# ---------- ring arithmetic in Z[x]/(x^n - 1) ----------

def cmul(a: Sequence[int], b: Sequence[int], mod: Optional[int] = None) -> Poly:
    """Cyclic product a b mod x^n - 1, optionally reduced mod `mod`."""
    n = len(a)
    c = [0] * n
    for i in range(n):
        if a[i] == 0:
            continue
        for j in range(n):
            c[(i + j) % n] += a[i] * b[j]
    return [x % mod for x in c] if mod else c


def center(a: Sequence[int], m: int) -> Poly:
    """Representatives in (-m/2, m/2]."""
    out = []
    for x in a:
        x %= m
        out.append(x - m if x > m // 2 else x)
    return out


def rotate(a: Sequence[int], i: int) -> Poly:
    """x^i a mod x^n - 1."""
    n = len(a)
    i %= n
    return list(a[n - i:]) + list(a[:n - i])


# ---------- inverses ----------

def _trim(a: List[int]) -> List[int]:
    while a and a[-1] == 0:
        a.pop()
    return a


def _pdivmod(a: List[int], b: List[int], p: int) -> Tuple[List[int], List[int]]:
    """Polynomial division over F_p (coefficient lists, low degree first)."""
    a = _trim([x % p for x in a])
    b = _trim([x % p for x in b])
    inv = pow(b[-1], -1, p)
    qt = [0] * max(len(a) - len(b) + 1, 1)
    while len(a) >= len(b):
        c = a[-1] * inv % p
        s = len(a) - len(b)
        qt[s] = c
        for i, y in enumerate(b):
            a[s + i] = (a[s + i] - c * y) % p
        _trim(a)
    return qt, a


def _psub_mul(a: List[int], c: List[int], b: List[int], p: int) -> List[int]:
    """a - c b over F_p."""
    out = [0] * max(len(a), len(c) + len(b) - 1 if c and b else 0)
    for i, x in enumerate(a):
        out[i] = x
    for i, x in enumerate(c):
        for j, y in enumerate(b):
            out[i + j] -= x * y
    return _trim([x % p for x in out])


def inverse_mod_prime(f: Sequence[int], p: int) -> Optional[Poly]:
    """f^-1 in F_p[x]/(x^n - 1) by the extended Euclidean algorithm, or None."""
    n = len(f)
    r0, r1 = [p - 1] + [0] * (n - 1) + [1], _trim([x % p for x in f])  # x^n - 1, f
    s0, s1 = [], [1]  # invariant: r_i = s_i f mod (x^n - 1)
    while r1:
        qt, r = _pdivmod(r0, r1, p)
        r0, r1 = r1, r
        s0, s1 = s1, _psub_mul(s0, qt, s1, p)
    if len(r0) != 1:
        return None  # gcd is not a constant
    c = pow(r0[0], -1, p)
    out = [0] * n
    for i, x in enumerate(s0):
        out[i % n] = (out[i % n] + c * x) % p
    return out


def inverse_mod_power_of_two(f: Sequence[int], q: int) -> Optional[Poly]:
    """f^-1 mod (x^n - 1, q) for q = 2^k: invert mod 2, then Newton steps F <- F (2 - f F)."""
    F = inverse_mod_prime(f, 2)
    if F is None:
        return None
    m = 2
    while m < q:
        m = min(m * m, q)
        fF = cmul(f, F, m)
        two_minus = [(-x) % m for x in fF]
        two_minus[0] = (two_minus[0] + 2) % m
        F = cmul(F, two_minus, m)
    return F


# ---------- key generation, encryption, decryption ----------

def ternary(n: int, ones: int, minus: int, rng: random.Random) -> Poly:
    v = [1] * ones + [-1] * minus + [0] * (n - ones - minus)
    rng.shuffle(v)
    return v


def keygen(n: int, q: int, d: int, rng: random.Random, p: int = 3):
    """Returns (h, f, g, f_p). f has d+1 ones and d minus ones, g has d of each."""
    while True:
        f = ternary(n, d + 1, d, rng)
        fq = inverse_mod_power_of_two(f, q)
        fp = inverse_mod_prime(f, p)
        if fq is not None and fp is not None:
            break
    g = ternary(n, d, d, rng)
    h = [p * x % q for x in cmul(fq, g, q)]
    return h, f, g, fp


def encrypt(h: Sequence[int], m: Sequence[int], r: Sequence[int], q: int) -> Poly:
    """e = r h + m mod q, with m ternary and r ternary."""
    return [(x + y) % q for x, y in zip(cmul(r, h, q), m)]


def decrypt(e: Sequence[int], f: Sequence[int], fp: Sequence[int], q: int, p: int = 3) -> Poly:
    """a = f e mod q centered, then m = f_p a mod p centered."""
    a = center(cmul(f, e, q), q)
    return center(cmul(fp, a, p), p)


# ---------- LLL (local copy, floating-point Gram-Schmidt) ----------

def lll(basis: Sequence[Sequence[int]], delta: float = 0.99) -> List[List[int]]:
    """LLL reduction of the rows of an integer basis (Lenstra, Lenstra and Lovasz 1982).

    Integer basis vectors, Gram-Schmidt data in floating point, with the
    swap update formulas of Cohen's Algorithm 2.6.3. Fine for the small
    dimensions and entries used here; not for large inputs.
    """
    b = [list(r) for r in basis]
    m = len(b)
    mu = [[0.0] * m for _ in range(m)]
    B = [0.0] * m
    bstar: List[List[float]] = []
    for i in range(m):
        v = [float(x) for x in b[i]]
        for j in range(i):
            mu[i][j] = sum(x * y for x, y in zip(b[i], bstar[j])) / B[j]
            v = [x - mu[i][j] * y for x, y in zip(v, bstar[j])]
        bstar.append(v)
        B[i] = sum(x * x for x in v)
    k = 1
    while k < m:
        for j in range(k - 1, -1, -1):
            r = round(mu[k][j])
            if r:
                b[k] = [x - r * y for x, y in zip(b[k], b[j])]
                for i in range(j):
                    mu[k][i] -= r * mu[j][i]
                mu[k][j] -= r
        if B[k] >= (delta - mu[k][k - 1] ** 2) * B[k - 1]:
            k += 1
            continue
        b[k], b[k - 1] = b[k - 1], b[k]
        t = mu[k][k - 1]
        bn = B[k] + t * t * B[k - 1]
        mu[k][k - 1] = t * B[k - 1] / bn
        B[k] = B[k - 1] * B[k] / bn
        B[k - 1] = bn
        for j in range(k - 1):
            mu[k - 1][j], mu[k][j] = mu[k][j], mu[k - 1][j]
        for i in range(k + 1, m):
            s = mu[i][k]
            mu[i][k] = mu[i][k - 1] - t * s
            mu[i][k - 1] = s + mu[k][k - 1] * mu[i][k]
        k = max(k - 1, 1)
    return b


# ---------- the attack ----------

def ntru_lattice_basis(hp: Sequence[int], q: int) -> List[List[int]]:
    """Rows (x^i, x^i h' mod q) for i < n, then (0, q x^i). (f, g) is in the lattice."""
    n = len(hp)
    rows = [[1 if j == i else 0 for j in range(n)] + rotate(hp, i) for i in range(n)]
    rows += [[0] * n + [q if j == i else 0 for j in range(n)] for i in range(n)]
    return rows


def has_key_shape(F: Sequence[int], G: Sequence[int], d: int) -> bool:
    """F has d+1 ones and d minus ones, G has d of each: the public key space."""
    if any(x not in (-1, 0, 1) for x in list(F) + list(G)):
        return False
    return F.count(1) == d + 1 and F.count(-1) == d and G.count(1) == d and G.count(-1) == d


def lattice_attack(h: Sequence[int], q: int, d: int, p: int = 3) -> Optional[Tuple[Poly, Poly]]:
    """Recover a key (F, G) of the public shape with F h' = G mod q, h' = p^-1 h.

    Step 1: LLL on the NTRU lattice. Step 2: look for a vector of the key
    shape (up to sign) among the reduced rows, their pairwise sums and
    differences, and these plus or minus (u, 0), u = 1 + x + ... + x^(n-1).
    (u, 0) lies in the lattice because h'(1) = g(1) / f(1) = 0, and LLL
    often mixes it into the short vectors. Returns None if no candidate fits.
    """
    n = len(h)
    hp = [pow(p, -1, q) * x % q for x in h]
    reduced = lll(ntru_lattice_basis(hp, q))
    reduced.sort(key=lambda v: sum(x * x for x in v))
    cands = list(reduced)
    for i in range(len(reduced)):
        for j in range(i + 1, len(reduced)):
            cands.append([x + y for x, y in zip(reduced[i], reduced[j])])
            cands.append([x - y for x, y in zip(reduced[i], reduced[j])])
    for v in cands:
        for c in (0, 1, -1):
            w = [x + c for x in v[:n]] + v[n:]
            for s in (1, -1):
                F, G = [s * x for x in w[:n]], [s * x for x in w[n:]]
                if has_key_shape(F, G, d) and center(cmul(F, hp, q), q) == G:
                    return F, G
    return None


def is_rotation(F: Sequence[int], G: Sequence[int], f: Sequence[int], g: Sequence[int]) -> bool:
    """(F, G) = +- x^i (f, g) for some i."""
    n = len(f)
    for i in range(n):
        for s in (1, -1):
            if list(F) == [s * x for x in rotate(f, i)] and list(G) == [s * x for x in rotate(g, i)]:
                return True
    return False
