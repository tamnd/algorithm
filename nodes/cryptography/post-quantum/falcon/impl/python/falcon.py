# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/falcon/. The authors are listed in prov/PSM659.jsonl.
"""Falcon: verification as in the round 3 specification, and a toy signer.

Part 1 is the verifier of the Falcon specification v1.2 (2020) for n = 512 and
n = 1024: HashToPoint with SHAKE256, the public key decoding (14 binary digits
for each coefficient), the decompression of the signature, and the check of
the squared norm of (s1, s2) against the bound floor(beta^2).

Part 2 is a toy signer for a small degree n. It keeps the structure of Falcon:
f and g with small coefficients, NTRUSolve for F and G with f G - g F = q, the
basis [[g, -f], [G, -F]] of the NTRU lattice, a randomized nearest plane
sampler, and the same verification equation. It is simplified in two ways. The
sampler is Klein's sampler on the 2n by 2n integer basis with an O(n^2) Gram-
Schmidt step for each coordinate, not the fast Fourier sampler (ffSampling) of
the specification, and the integer Gaussian is a plain rejection sampler with
floating point, not the constant-time SamplerZ of the specification. The key
reduction inside NTRUSolve uses exact rational numbers, which only works for
small n.

For study only. This code is not constant time, it uses floating point in the
signer, and it must not be used to protect real data. Use a reviewed library
such as liboqs, or the reference code of the Falcon team, and a FIPS 140
validated module once FN-DSA (FIPS 206) is final.
"""

import hashlib
import math
import random
from fractions import Fraction

Q = 12289

# n: (floor(beta^2), sigma of the signer, sigma_min)
OFFICIAL = {
    512: (34034726, 165.7366171829776, 1.2778336969128337),
    1024: (70265242, 168.38857144654395, 1.298280334344292),
}


# ------------------------------------------------------------ ring helpers
def poly_mul(a, b, mod=None):
    """Product in Z[x]/(x^n + 1), reduced mod `mod` when it is given."""
    n = len(a)
    out = [0] * n
    for i, ai in enumerate(a):
        if ai == 0:
            continue
        for j in range(n - i):
            out[i + j] += ai * b[j]
        for j in range(n - i, n):
            out[i + j - n] -= ai * b[j]
    if mod is not None:
        out = [x % mod for x in out]
    return out


def center(x, m=Q):
    x %= m
    return x - m if x > m // 2 else x


# ---------------------------------------------------------- Part 1: verify
def hash_to_point(salted_msg, n):
    """HashToPoint: SHAKE256, 16-bit big-endian values, keep those below 5q = 61445."""
    length = 4 * n
    while True:
        buf = hashlib.shake_256(salted_msg).digest(length)
        c = []
        for i in range(0, length - 1, 2):
            t = (buf[i] << 8) | buf[i + 1]
            if t < 5 * Q:
                c.append(t % Q)
                if len(c) == n:
                    return c
        length *= 2


def decode_public_key(pk):
    """Header byte 0x00 + log2(n), then n coefficients of 14 binary digits, big-endian."""
    logn = pk[0] & 0x0F
    n = 1 << logn
    if pk[0] != logn or len(pk) != 1 + 14 * n // 8:
        raise ValueError("bad public key encoding")
    acc = int.from_bytes(pk[1:], "big")
    total = 14 * n
    h = [(acc >> (total - 14 * (i + 1))) & 0x3FFF for i in range(n)]
    if any(x >= Q for x in h):
        raise ValueError("coefficient out of range")
    return h


# @line L13
def compress(s, slen):
    """The compressed encoding: sign, 7 low binary digits, then the high part in unary."""
    bits = []
    for x in s:
        a = abs(x)
        if a > 2047:
            return None
        bits.append(1 if x < 0 else 0)
        bits.extend((a >> (6 - j)) & 1 for j in range(7))
        bits.extend([0] * (a >> 7))
        bits.append(1)
    if len(bits) > 8 * slen:
        return None
    bits.extend([0] * (8 * slen - len(bits)))
    return bytes(int("".join(map(str, bits[i:i + 8])), 2) for i in range(0, len(bits), 8))


def decompress(data, n):
    """The inverse of compress. Returns None for a bad encoding ("minus zero", padding)."""
    bits = []
    for byte in data:
        bits.extend((byte >> (7 - j)) & 1 for j in range(8))
    pos = 0
    s = []
    for _ in range(n):
        if pos + 8 > len(bits):
            return None
        sign = bits[pos]
        low = 0
        for j in range(7):
            low = (low << 1) | bits[pos + 1 + j]
        pos += 8
        high = 0
        while True:
            if pos >= len(bits):
                return None
            b = bits[pos]
            pos += 1
            if b == 1:
                break
            high += 1
            if high > 15:
                return None
        a = (high << 7) | low
        if sign == 1 and a == 0:
            return None
        s.append(-a if sign else a)
    if any(bits[pos:]):
        return None
    return s


def norm_check(c, s2, h, bound):
    """s1 = c - s2 h mod q, centered; accept when |s1|^2 + |s2|^2 <= bound."""
    # @line L17
    s2h = poly_mul([x % Q for x in s2], h, Q)
    s1 = [center(ci - t) for ci, t in zip(c, s2h)]
    # @line L18
    return sum(x * x for x in s1) + sum(x * x for x in s2) <= bound


def verify(pk, msg, sig):
    """Verify a detached signature: header 0x30 + log2(n) | 40-byte nonce | compressed s2."""
    h = decode_public_key(pk)
    n = len(h)
    logn = n.bit_length() - 1
    if len(sig) < 41 or sig[0] != 0x30 + logn:
        return False
    nonce, comp = sig[1:41], sig[41:]
    # @line L16
    s2 = decompress(comp, n)
    if s2 is None:
        return False
    # @line L15
    c = hash_to_point(nonce + msg, n)
    return norm_check(c, s2, h, OFFICIAL[n][0])


def verify_kat_sm(pk, sm):
    """Verify the 'sm' field of the round 3 KAT files.

    sm = sig_len (2 bytes) | nonce (40) | message | 0x20 + log2(n) | compressed s2.
    Returns the message when the signature is valid, else None.
    """
    h = decode_public_key(pk)
    n = len(h)
    logn = n.bit_length() - 1
    sig_len = (sm[0] << 8) | sm[1]
    nonce = sm[2:42]
    msg = sm[42:len(sm) - sig_len]
    esig = sm[len(sm) - sig_len:]
    if esig[0] != 0x20 + logn:
        return None
    s2 = decompress(esig[1:], n)
    if s2 is None:
        return None
    if not norm_check(hash_to_point(nonce + msg, n), s2, h, OFFICIAL[n][0]):
        return None
    return msg


# ------------------------------------------------------- Part 2: toy signer
def adjoint(f):
    """f*(x) = f(1/x) in Z[x]/(x^n + 1)."""
    return [f[0]] + [-x for x in reversed(f[1:])]


def field_norm(f):
    """N(f)(y) = f0(y)^2 - y f1(y)^2 for f(x) = f0(x^2) + x f1(x^2)."""
    f0, f1 = f[0::2], f[1::2]
    a = poly_mul(f0, f0)
    b = poly_mul(f1, f1)
    b = [-b[-1]] + b[:-1]  # multiply by y in Z[y]/(y^(n/2) + 1)
    return [x - y for x, y in zip(a, b)]


def lift(fp):
    """F'(x^2): put the coefficients at the even positions."""
    out = [0] * (2 * len(fp))
    out[0::2] = fp
    return out


def galois_conj(f):
    """f(-x)."""
    return [x if i % 2 == 0 else -x for i, x in enumerate(f)]


def _solve_rational(dpoly, npoly):
    """Solve d k = num in Q[x]/(x^n + 1) exactly, with the anticirculant matrix of d."""
    n = len(dpoly)
    cols = []
    for j in range(n):
        e = [0] * n
        e[j] = 1
        cols.append(poly_mul(dpoly, e))
    m = [[Fraction(cols[j][i]) for j in range(n)] + [Fraction(npoly[i])] for i in range(n)]
    for col in range(n):
        piv = next(r for r in range(col, n) if m[r][col] != 0)
        m[col], m[piv] = m[piv], m[col]
        inv = 1 / m[col][col]
        m[col] = [x * inv for x in m[col]]
        for r in range(n):
            if r != col and m[r][col] != 0:
                fac = m[r][col]
                m[r] = [x - fac * y for x, y in zip(m[r], m[col])]
    return [m[i][n] for i in range(n)]


def reduce_fg(f, g, F, G):
    """Babai reduction of (F, G) against (f, g): k = round((F f* + G g*) / (f f* + g g*))."""
    num = [a + b for a, b in zip(poly_mul(F, adjoint(f)), poly_mul(G, adjoint(g)))]
    den = [a + b for a, b in zip(poly_mul(f, adjoint(f)), poly_mul(g, adjoint(g)))]
    k = [round(x) for x in _solve_rational(den, num)]
    kf, kg = poly_mul(k, f), poly_mul(k, g)
    return [a - b for a, b in zip(F, kf)], [a - b for a, b in zip(G, kg)]


def _xgcd(a, b):
    x0, y0, x1, y1 = 1, 0, 0, 1
    while b:
        qt, a, b = a // b, b, a % b
        x0, x1 = x1, x0 - qt * x1
        y0, y1 = y1, y0 - qt * y1
    return a, x0, y0


def ntru_solve(f, g, q=Q):
    """Find F, G with f G - g F = q in Z[x]/(x^n + 1), or None. Iterative over the tower."""
    tower = [(f, g)]
    while len(tower[-1][0]) > 1:
        a, b = tower[-1]
        tower.append((field_norm(a), field_norm(b)))
    f1, g1 = tower[-1][0][0], tower[-1][1][0]
    d, u, v = _xgcd(f1, g1)
    if abs(d) != 1:
        return None
    if d == -1:
        u, v = -u, -v
    F, G = [-v * q], [u * q]
    for a, b in reversed(tower[:-1]):
        F = poly_mul(lift(F), galois_conj(b))
        G = poly_mul(lift(G), galois_conj(a))
        F, G = reduce_fg(a, b, F, G)
    return F, G


def inverse_mod_q(f, q=Q):
    """f^(-1) in Z_q[x]/(x^n + 1) by Gaussian elimination mod q, or None."""
    n = len(f)
    cols = []
    for j in range(n):
        e = [0] * n
        e[j] = 1
        cols.append(poly_mul(f, e, q))
    m = [[cols[j][i] for j in range(n)] + [1 if i == 0 else 0] for i in range(n)]
    for col in range(n):
        piv = next((r for r in range(col, n) if m[r][col] % q), None)
        if piv is None:
            return None
        m[col], m[piv] = m[piv], m[col]
        inv = pow(m[col][col], -1, q)
        m[col] = [x * inv % q for x in m[col]]
        for r in range(n):
            if r != col and m[r][col]:
                fac = m[r][col]
                m[r] = [(x - fac * y) % q for x, y in zip(m[r], m[col])]
    return [m[i][n] for i in range(n)]


def sample_z(mu, sigma, rng):
    """Integer Gaussian with center mu and standard deviation sigma, by rejection."""
    lo = math.floor(mu - 10 * sigma)
    hi = math.ceil(mu + 10 * sigma)
    while True:
        x = rng.randint(lo, hi)
        if rng.random() < math.exp(-((x - mu) ** 2) / (2 * sigma * sigma)):
            return x


def basis_rows(f, g, F, G):
    """The 2n rows x^i (g, -f) and x^i (G, -F) of the NTRU lattice basis."""
    n = len(f)
    rows = []
    for a, b in ((g, [-x for x in f]), (G, [-x for x in F])):
        for i in range(n):
            e = [0] * n
            e[i] = 1
            rows.append(poly_mul(a, e) + poly_mul(b, e))
    return rows


def gram_schmidt(rows):
    out = []
    for r in rows:
        v = [float(x) for x in r]
        for u in out:
            uu = sum(x * x for x in u)
            mu = sum(x * y for x, y in zip(v, u)) / uu
            v = [x - mu * y for x, y in zip(v, u)]
        out.append(v)
    return out


class ToyFalcon:
    """A Falcon-like signer for a small power of two n, with q = 12289."""

    def __init__(self, n=16, rng=None):
        self.n = n
        self.rng = rng or random.SystemRandom()
        self.sigma = 1.17 * math.sqrt(Q) * 1.28  # GS norms are at most 1.17 sqrt(q)
        self.bound = math.floor((1.1 * self.sigma) ** 2 * 2 * n)
        self._keygen()

    def _keygen(self):
        n = self.n
        s_fg = 1.17 * math.sqrt(Q / (2 * n))
        while True:
            # @line L1
            f = [sample_z(0, s_fg, self.rng) for _ in range(n)]
            g = [sample_z(0, s_fg, self.rng) for _ in range(n)]
            # @line L2
            finv = inverse_mod_q(f)
            if finv is None:
                continue
            # @line L3
            sol = ntru_solve(f, g)
            if sol is None:
                continue
            F, G = sol
            # @line L5
            rows = basis_rows(f, g, F, G)
            gs = gram_schmidt(rows)
            # @line L2
            if max(math.sqrt(sum(x * x for x in v)) for v in gs) > 1.17 * math.sqrt(Q):
                continue
            self.f, self.g, self.F, self.G = f, g, F, G
            # @line L4
            self.h = poly_mul(g, finv, Q)
            self.rows, self.gs = rows, gs
            self.gs_sq = [sum(x * x for x in v) for v in gs]
            # @line L6
            return

    def _klein(self, target):
        """Randomized nearest plane: a lattice vector near target."""
        t = [float(x) for x in target]
        v = [0] * (2 * self.n)
        for i in reversed(range(2 * self.n)):
            c = sum(x * y for x, y in zip(t, self.gs[i])) / self.gs_sq[i]
            z = sample_z(c, self.sigma / math.sqrt(self.gs_sq[i]), self.rng)
            if z:
                b = self.rows[i]
                t = [x - z * y for x, y in zip(t, b)]
                v = [x + z * y for x, y in zip(v, b)]
        return v

    def sign(self, msg):
        n = self.n
        while True:
            # @line L7
            nonce = bytes(self.rng.getrandbits(8) for _ in range(40))
            # @line L8
            c = hash_to_point(nonce + msg, n)
            # @line L9
            # @line L10
            v = self._klein(c + [0] * n)
            # @line L11
            s1 = [ci - vi for ci, vi in zip(c, v[:n])]
            s2 = [-x for x in v[n:]]
            # @line L12
            if sum(x * x for x in s1) + sum(x * x for x in s2) <= self.bound:
                # @line L14
                return nonce, s2

    def verify(self, msg, sig):
        nonce, s2 = sig
        return norm_check(hash_to_point(nonce + msg, self.n), s2, self.h, self.bound)
