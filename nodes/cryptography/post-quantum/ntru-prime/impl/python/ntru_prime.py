# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ntru-prime/. The authors are listed in prov/ECE9S6.jsonl.
"""The core of Streamlined NTRU Prime with the sntrup761 parameters.

Ring: R = Z[x]/(x^p - x - 1) with p = 761, q = 4591, weight w = 286.
KeyGen: a small g that is invertible mod 3, a short f (weight w),
h = g / (3 f) in R/q. Encrypt: c = Round(h r) for a short r, where Round
moves each centered coefficient to the nearest multiple of 3.
Decrypt: e = 3 f c in R/q (centered), then r = e / g in R/3; if r does not
have weight w, a fixed weight-w vector is returned instead.

This file stops at the core. It does not implement the byte encodings,
the hashes with their prefixes or the plaintext confirmation of the full
sntrup761 KEM, so it cannot reproduce the official known answer tests.

For study only. This code is not constant time and must not be used to
protect real data.
"""

import secrets

P, Q, W = 761, 4591, 286
MODULUS = [-1, -1] + [0] * (P - 2) + [1]  # x^p - x - 1, low degree first


def _mul_full(a, b, mod):
    """Plain product with Kronecker substitution, coefficients reduced mod `mod`."""
    w = 2 * mod.bit_length() + 12
    A = sum((x % mod) << (w * i) for i, x in enumerate(a))
    B = sum((x % mod) << (w * i) for i, x in enumerate(b))
    C, mask = A * B, (1 << w) - 1
    return [(C >> (w * k)) & mask for k in range(len(a) + len(b) - 1)]


def ring_mul(a, b, mod):
    """a * b in Z_mod[x]/(x^p - x - 1): x^k = x^(k-p+1) + x^(k-p) for k >= p."""
    c = _mul_full(a, b, mod) + [0]
    for k in range(len(c) - 1, P - 1, -1):
        if c[k]:
            c[k - P + 1] += c[k]
            c[k - P] += c[k]
            c[k] = 0
    return [x % mod for x in c[:P]]


def ring_inv(a, mod):
    """Inverse in Z_mod[x]/(x^p - x - 1) for a prime mod, or None (extended Euclid)."""
    def deg(v):
        d = len(v) - 1
        while d >= 0 and v[d] == 0:
            d -= 1
        return d

    r0, r1 = [x % mod for x in MODULUS], [x % mod for x in a] + [0]
    s0, s1 = [0], [1]
    while deg(r1) >= 0:
        d0, d1 = deg(r0), deg(r1)
        inv = pow(r1[d1], -1, mod)
        rem, quo = r0[:d0 + 1], [0] * (d0 - d1 + 1)
        for k in range(d0 - d1, -1, -1):
            c = rem[k + d1] * inv % mod
            quo[k] = c
            if c:
                rem[k:k + d1 + 1] = [(x - c * y) % mod for x, y in zip(rem[k:k + d1 + 1], r1)]
        qs = _mul_full(quo, s1, mod)
        n = max(len(s0), len(qs))
        s_new = [((s0[i] if i < len(s0) else 0) - (qs[i] if i < len(qs) else 0)) % mod for i in range(n)]
        r0, r1, s0, s1 = r1, rem, s1, s_new
    if deg(r0) != 0:
        return None
    c = pow(r0[0], -1, mod)
    return ([x * c % mod for x in s0] + [0] * P)[:P]


def center(x, mod):
    x %= mod
    return x - mod if x > mod // 2 else x


def small(rng=None):
    """A random small element: coefficients in {-1, 0, 1}."""
    rng = rng or secrets.SystemRandom()
    return [rng.choice((-1, 0, 1)) for _ in range(P)]


def short(rng=None):
    """A random short element: exactly w nonzero coefficients, each -1 or 1."""
    rng = rng or secrets.SystemRandom()
    v = [rng.choice((-1, 1)) for _ in range(W)] + [0] * (P - W)
    rng.shuffle(v)
    return v


def round3(v):
    """Round each centered coefficient of an element of R/q to the nearest multiple of 3."""
    return [3 * round(center(x, Q) / 3) for x in v]


def keygen(rng=None):
    while True:
        # @line L1
        g = small(rng)
        # @line L2
        v = ring_inv(g, 3)
        if v is not None:
            break
    # @line L3
    f = short(rng)
    # @line L4
    h = ring_mul(g, ring_inv([3 * x for x in f], Q), Q)
    # @line L5
    return h, (f, v)


def encrypt(h, r):
    # @line L6
    hr = ring_mul(h, r, Q)
    # @line L7
    return round3(hr)


def decrypt(sk, c):
    f, v = sk
    # @line L8
    e = [center(x, Q) for x in ring_mul([3 * x for x in f], c, Q)]
    # @line L9
    r = [center(x, 3) for x in ring_mul([x % 3 for x in e], v, 3)]
    # @line L10
    if sum(1 for x in r if x) == W:
        return r
    return [1] * W + [0] * (P - W)
