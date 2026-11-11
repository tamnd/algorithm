# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/shamir-secret-sharing/. The authors are listed in prov/95YWP2.jsonl.
"""Shamir's t-of-n secret sharing over GF(p) and over GF(2^8).

The dealer hides the secret s as the constant term of a random polynomial
f of degree t - 1 and gives party i the point (i, f(i)). Any t points fix f,
and Lagrange interpolation at 0 gives s. Any t - 1 points fit every secret
equally well.

Over GF(2^8) (the AES field, reduction polynomial x^8 + x^4 + x^3 + x + 1,
0x11b) a byte string is shared byte by byte with the same x values.

For study only. The code is not constant time and must not be used to protect
real data. Use a reviewed implementation built on libsodium or a FIPS 140
validated module.
"""

import secrets


# ------------------------------------------------------------ GF(p)
def share(s, t, n, p, rand=None):
    """Shares (i, f(i)) for i = 1..n of a random f of degree < t with f(0) = s."""
    assert 1 <= t <= n < p
    rand = rand or (lambda: secrets.randbelow(p))
    coeffs = [s % p] + [rand() for _ in range(t - 1)]          # @line L1
    out = []
    for i in range(1, n + 1):                                  # @line L2
        y = 0
        for c in reversed(coeffs):                             # Horner
            y = (y * i + c) % p
        out.append((i, y))                                     # @line L3
    return out


def lagrange_at_zero(xs, p):
    """The coefficients lambda_j with f(0) = sum_j lambda_j f(x_j) for deg f < len(xs)."""
    lams = []
    for j, xj in enumerate(xs):
        num, den = 1, 1
        for m, xm in enumerate(xs):
            if m != j:
                num = num * xm % p
                den = den * (xm - xj) % p
        lams.append(num * pow(den, -1, p) % p)                 # @line L4
    return lams


def reconstruct(shares, p):
    """f(0) from t shares (x_j, y_j) with distinct nonzero x_j."""
    xs = [x for x, _ in shares]
    assert len(set(xs)) == len(xs) and all(x % p for x in xs)
    lams = lagrange_at_zero(xs, p)
    return sum(l * y for l, (_, y) in zip(lams, shares)) % p   # @line L5


def interpolate_at(shares, x, p):
    """f(x) from t shares, by Lagrange interpolation at any point x."""
    total = 0
    for j, (xj, yj) in enumerate(shares):
        num, den = 1, 1
        for m, (xm, _) in enumerate(shares):
            if m != j:
                num = num * (x - xm) % p
                den = den * (xj - xm) % p
        total += yj * num * pow(den, -1, p)
    return total % p


def consistent(shares, t, p):
    """True if all the given shares (more than t) lie on one polynomial of degree < t."""
    base = shares[:t]
    return all(interpolate_at(base, x, p) == y for x, y in shares[t:])


def add_shares(a, b, p):
    """Linearity: shares of s and s' with the same x values give shares of s + s'."""
    return [(x, (y + z) % p) for (x, y), (x2, z) in zip(a, b) if x == x2]


def refresh(shares, t, p, rand=None):
    """Proactive refresh: add a fresh sharing of 0. The secret stays the same."""
    zero = share(0, t, len(shares), p, rand)
    return add_shares(shares, zero, p)


# ------------------------------------------------------------ GF(2^8)
def gf_mul(a, b):
    """Product in GF(2^8) = GF(2)[x] / (x^8 + x^4 + x^3 + x + 1)."""
    out = 0
    while b:
        if b & 1:
            out ^= a
        a <<= 1
        if a & 0x100:
            a ^= 0x11B
        b >>= 1
    return out


def gf_inv(a):
    assert a != 0
    out, base, e = 1, a, 254          # a^254 = a^-1, since a^255 = 1
    while e:
        if e & 1:
            out = gf_mul(out, base)
        base = gf_mul(base, base)
        e >>= 1
    return out


def gf_share_byte(s, t, n, rand=None):
    assert 1 <= t <= n <= 255
    rand = rand or (lambda: secrets.randbelow(256))
    coeffs = [s] + [rand() for _ in range(t - 1)]
    out = []
    for i in range(1, n + 1):
        y = 0
        for c in reversed(coeffs):
            y = gf_mul(y, i) ^ c
        out.append((i, y))
    return out


def gf_reconstruct_byte(shares):
    xs = [x for x, _ in shares]
    assert len(set(xs)) == len(xs) and 0 not in xs
    total = 0
    for j, (xj, yj) in enumerate(shares):
        num, den = 1, 1
        for m, xm in enumerate(xs):
            if m != j:
                num = gf_mul(num, xm)
                den = gf_mul(den, xm ^ xj)      # subtraction is XOR
        total ^= gf_mul(yj, gf_mul(num, gf_inv(den)))
    return total


def gf_share_bytes(secret, t, n):
    """Share each byte with a fresh polynomial; party i gets (i, bytes)."""
    columns = [gf_share_byte(b, t, n) for b in secret]
    return [(i, bytes(col[i - 1][1] for col in columns)) for i in range(1, n + 1)]


def gf_reconstruct_bytes(shares):
    length = len(shares[0][1])
    return bytes(gf_reconstruct_byte([(x, ys[k]) for x, ys in shares]) for k in range(length))
