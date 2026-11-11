# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/boneh-franklin-ibe/. The authors are listed in prov/BRDGNB.jsonl.
#
# Boneh-Franklin identity-based encryption (Crypto 2001): BasicIdent and FullIdent.
# The pairing is the modified reduced Tate pairing on the supersingular curve y^2 = x^3 + x over
# F_p, p = 3 (mod 4), with the distortion map (x, y) -> (-x, i y). The group order is q.
# H1 is a toy try-and-increment hash to G1, and H2, H3, H4 are built from SHA-256 with tags.
# For study only. The curves are toys and NOT secure, the hashes are not those of RFC 5091, and
# the code is not constant time. Use a maintained IBE or pairing library instead.

import hashlib
import random

N_BYTES = 32  # messages and the value sigma of FullIdent are n = 256 binary digits


class Curve:
    """E: y^2 = x^3 + x over F_p with a prime q dividing p + 1. Points are (x, y) or None."""

    def __init__(self, p: int, q: int):
        if p % 4 != 3 or (p + 1) % q != 0:
            raise ValueError("need p = 3 (mod 4) and q | p + 1")
        self.p, self.q = p, q
        self.cofactor = (p + 1) // q

    # ---- F_p2 = F_p[i], i^2 = -1; (a, b) means a + b*i ----

    def f2_mul(self, x, y):
        p = self.p
        return ((x[0] * y[0] - x[1] * y[1]) % p, (x[0] * y[1] + x[1] * y[0]) % p)

    def f2_inv(self, x):
        p = self.p
        t = pow((x[0] * x[0] + x[1] * x[1]) % p, p - 2, p)
        return (x[0] * t % p, -x[1] * t % p)

    def f2_pow(self, x, e):
        result = (1, 0)
        while e:
            if e & 1:
                result = self.f2_mul(result, x)
            x = self.f2_mul(x, x)
            e >>= 1
        return result

    def gt_bytes(self, z) -> bytes:
        size = (self.p.bit_length() + 7) // 8
        return z[0].to_bytes(size, "big") + z[1].to_bytes(size, "big")

    # ---- the curve ----

    def on_curve(self, T) -> bool:
        if T is None:
            return True
        x, y = T
        return 0 <= x < self.p and 0 <= y < self.p and (y * y - x * x * x - x) % self.p == 0

    def add(self, A, B):
        p = self.p
        if A is None:
            return B
        if B is None:
            return A
        (x1, y1), (x2, y2) = A, B
        if x1 == x2:
            if (y1 + y2) % p == 0:
                return None
            lam = (3 * x1 * x1 + 1) * pow(2 * y1, p - 2, p) % p
        else:
            lam = (y2 - y1) * pow(x2 - x1, p - 2, p) % p
        x3 = (lam * lam - x1 - x2) % p
        return (x3, (lam * (x1 - x3) - y1) % p)

    def mul(self, k: int, T):
        """k*T by double and add (k >= 0). Not constant time."""
        result = None
        while k:
            if k & 1:
                result = self.add(result, T)
            T = self.add(T, T)
            k >>= 1
        return result

    def in_g1(self, T) -> bool:
        return T is not None and self.on_curve(T) and self.mul(self.q, T) is None

    def generator(self):
        p, x = self.p, 1
        while True:
            rhs = (x * x * x + x) % p
            if rhs and pow(rhs, (p - 1) // 2, p) == 1:
                G = self.mul(self.cofactor, (x, pow(rhs, (p + 1) // 4, p)))
                if G is not None:
                    return G
            x += 1

    def pairing(self, A, B):
        """e(A, B) = f_{q,A}(psi(B))^((p^2 - 1)/q), with the vertical lines left out."""
        if A is None or B is None:
            return (1, 0)
        p = self.p
        xq, yq = B
        f, T = (1, 0), A
        for bit in bin(self.q)[3:]:
            xt, yt = T
            lam = (3 * xt * xt + 1) * pow(2 * yt, p - 2, p) % p
            f = self.f2_mul(self.f2_mul(f, f), ((lam * (xq + xt) - yt) % p, yq))
            T = self.add(T, T)
            if bit == "1":
                xt, yt = T
                if xt == A[0]:
                    T = None
                    continue
                lam = (A[1] - yt) * pow(A[0] - xt, p - 2, p) % p
                f = self.f2_mul(f, ((lam * (xq + xt) - yt) % p, yq))
                T = self.add(T, A)
        g = self.f2_mul((f[0], -f[1] % p), self.f2_inv(f))
        return self.f2_pow(g, self.cofactor)


TOY = Curve(170141183460469232340429858148299309287, 9223372036854775837)
TINY = Curve(59, 5)  # the curve of the worked example


# ---- the hash functions (toys, modelled as random oracles in the proof) ----


def _sha(tag: bytes, *parts: bytes) -> bytes:
    h = hashlib.sha256(tag)
    for part in parts:
        h.update(len(part).to_bytes(4, "big") + part)
    return h.digest()


def H1(C: Curve, identity: bytes):
    """Hash an identity to G1 \\ {O}: try x = SHA-256(ctr, id) until x^3 + x is a square."""
    p, ctr = C.p, 0
    while True:
        h = _sha(b"toy-BF-H1", ctr.to_bytes(4, "big"), identity)
        x = int.from_bytes(h + _sha(b"toy-BF-H1b", h), "big") % p
        rhs = (x * x * x + x) % p
        if rhs and pow(rhs, (p - 1) // 2, p) == 1:
            y = pow(rhs, (p + 1) // 4, p)
            Q = C.mul(C.cofactor, (x, y if h[-1] & 1 == 0 else -y % p))
            if Q is not None:
                return Q
        ctr += 1


def H2(C: Curve, z) -> bytes:
    return _sha(b"toy-BF-H2", C.gt_bytes(z))


def H3(C: Curve, sigma: bytes, M: bytes) -> int:
    return 1 + int.from_bytes(_sha(b"toy-BF-H3", sigma, M), "big") % (C.q - 1)


def H4(sigma: bytes) -> bytes:
    return _sha(b"toy-BF-H4", sigma)


def xor(a: bytes, b: bytes) -> bytes:
    if len(a) != len(b):
        raise ValueError("length mismatch")
    return bytes(x ^ y for x, y in zip(a, b))


# ---- the scheme ----


def setup(C: Curve, rng: random.Random):
    """Return the public parameters (C, P, P_pub) and the master key s."""
    P = C.generator()
    s = rng.randrange(1, C.q)  # @line L1
    Ppub = C.mul(s, P)  # @line L2
    return (C, P, Ppub), s  # @line L3


def extract_point(params, s: int, Q):
    C = params[0]
    return C.mul(s, Q)  # @line L5


def extract(params, s: int, identity: bytes):
    Q = H1(params[0], identity)  # @line L4
    return extract_point(params, s, Q)


def basic_encrypt_point(params, Q, M: bytes, r: int):
    """BasicIdent encryption to the point Q = H1(ID) with the randomness r."""
    C, P, Ppub = params
    g = C.pairing(Q, Ppub)  # @line L7
    return C.mul(r, P), xor(M, H2(C, C.f2_pow(g, r)))  # @line L8


def basic_encrypt(params, identity: bytes, M: bytes, rng: random.Random):
    C = params[0]
    r = rng.randrange(1, C.q)  # @line L6
    return basic_encrypt_point(params, H1(C, identity), M, r)


def basic_decrypt(params, d, ct) -> bytes:
    C = params[0]
    U, V = ct
    return xor(V, H2(C, C.pairing(d, U)))  # @line L9


def full_encrypt(params, identity: bytes, M: bytes, rng: random.Random):
    """FullIdent: BasicIdent with the Fujisaki-Okamoto transform."""
    C, P, Ppub = params
    if len(M) != N_BYTES:
        raise ValueError("FullIdent messages have n binary digits")
    sigma = bytes(rng.getrandbits(8) for _ in range(N_BYTES))
    r = H3(C, sigma, M)  # @line L10
    g = C.pairing(H1(C, identity), Ppub)  # @line L11
    return C.mul(r, P), xor(sigma, H2(C, C.f2_pow(g, r))), xor(M, H4(sigma))  # @line L12


def full_decrypt(params, d, ct):
    """Return M, or None for a rejected ciphertext."""
    C, P, Ppub = params
    U, V, W = ct
    if not C.in_g1(U):  # @line L13
        return None
    sigma = xor(V, H2(C, C.pairing(d, U)))  # @line L14
    M = xor(W, H4(sigma))
    if C.mul(H3(C, sigma, M), P) != U:  # @line L15
        return None
    return M  # @line L16
