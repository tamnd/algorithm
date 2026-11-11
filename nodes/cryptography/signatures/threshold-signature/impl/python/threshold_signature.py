# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/threshold-signature/. The authors are listed in prov/YVV26W.jsonl.
"""Threshold BLS (Boldyreva 2003) with Shamir sharing, over a toy symmetric pairing.

deal() shares a BLS secret key with a polynomial of degree t - 1 and
publishes the verification keys y_i = x_i g. Each party signs with its
share, partial_verify() checks one partial signature with a pairing, and
combine() interpolates any t partial signatures in the exponent to the
ordinary BLS signature x H(m). pedersen_dkg() is a simple joint Feldman DKG
in the style of Pedersen (1991), without complaints, for the semi-honest case.

The toy pairing is the reduced Tate pairing on y^2 = x^3 + x over F_p,
p = 3 mod 4, with the distortion map (x, y) -> (-x, i y), the same as on
the BLS signature page.

NOT SECURE. The groups are tiny (r has 32 binary digits), the hash to the
group is try-and-increment rather than RFC 9380, the DKG has no complaint
phase, and the code is not constant time. For study only.
"""

import hashlib
import random

P = 2305843081154396467  # prime, P = C * R - 1, P = 3 mod 4
R = 2147483659  # prime order of G1
C = 1073741852  # cofactor

Point = tuple[int, int] | None


def on_curve(a: Point) -> bool:
    return a is None or (a[1] * a[1] - a[0] ** 3 - a[0]) % P == 0


def add(a: Point, b: Point) -> Point:
    if a is None:
        return b
    if b is None:
        return a
    if a[0] == b[0] and (a[1] + b[1]) % P == 0:
        return None
    if a == b:
        lam = (3 * a[0] * a[0] + 1) * pow(2 * a[1], -1, P) % P
    else:
        lam = (b[1] - a[1]) * pow(b[0] - a[0], -1, P) % P
    x3 = (lam * lam - a[0] - b[0]) % P
    return x3, (lam * (a[0] - x3) - a[1]) % P


def neg(a: Point) -> Point:
    return None if a is None else (a[0], (-a[1]) % P)


def mul(k: int, a: Point) -> Point:
    if k < 0:
        k, a = -k, neg(a)
    out = None
    while k:
        if k & 1:
            out = add(out, a)
        a = add(a, a)
        k >>= 1
    return out


def in_g1(a: Point) -> bool:
    return a is not None and on_curve(a) and mul(R, a) is None


def f2_mul(a: tuple[int, int], b: tuple[int, int]) -> tuple[int, int]:
    return (a[0] * b[0] - a[1] * b[1]) % P, (a[0] * b[1] + a[1] * b[0]) % P


def f2_pow(a: tuple[int, int], e: int) -> tuple[int, int]:
    out = (1, 0)
    while e:
        if e & 1:
            out = f2_mul(out, a)
        a = f2_mul(a, a)
        e >>= 1
    return out


FINAL_EXP = (P * P - 1) // R


def pairing(a: Point, b: Point) -> tuple[int, int]:
    """The reduced Tate pairing f_{R,a}(psi(b))^((p^2 - 1)/R), vertical lines skipped."""
    if a is None or b is None:
        return (1, 0)
    qx, qy = (-b[0]) % P, b[1]
    f, t = (1, 0), a
    for bit in bin(R)[3:]:
        lam = (3 * t[0] * t[0] + 1) * pow(2 * t[1], -1, P) % P
        f = f2_mul(f2_mul(f, f), ((-t[1] - lam * (qx - t[0])) % P, qy))
        t = add(t, t)
        if bit == "1":
            if t is not None and t[0] == a[0]:
                t = add(t, a)
                continue
            lam = (a[1] - t[1]) * pow(a[0] - t[0], -1, P) % P
            f = f2_mul(f, ((-t[1] - lam * (qx - t[0])) % P, qy))
            t = add(t, a)
    return f2_pow(f, FINAL_EXP)


def hash_to_g1(msg: bytes, dst: bytes = b"TOY-BLS-SIG") -> Point:
    """Try-and-increment, then multiply by the cofactor. Not RFC 9380."""
    ctr = 0
    while True:
        h = hashlib.sha256(dst + ctr.to_bytes(4, "big") + msg).digest()
        x = int.from_bytes(h, "big") % P
        rhs = (x * x * x + x) % P
        y = pow(rhs, (P + 1) // 4, P)
        if y * y % P == rhs:
            pt = mul(C, (x, min(y, P - y)))
            if pt is not None:
                return pt
        ctr += 1


GEN = hash_to_g1(b"generator", b"TOY-BLS-GEN")


# ------------------------------------------------------------ Shamir sharing
def poly_eval(coeffs: list[int], z: int) -> int:
    out = 0
    for c in reversed(coeffs):
        out = (out * z + c) % R
    return out


def deal(x: int, t: int, n: int, rng: random.Random) -> tuple[Point, dict[int, int], dict[int, Point]]:
    """Trusted dealer: shares x_i = f(i) for i = 1..n, keys y = x g and y_i = x_i g."""
    coeffs = [x % R] + [rng.randrange(R) for _ in range(t - 1)]  # @line L1
    shares = {i: poly_eval(coeffs, i) for i in range(1, n + 1)}
    return mul(x, GEN), shares, {i: mul(s, GEN) for i, s in shares.items()}


def pedersen_dkg(t: int, n: int, rng: random.Random) -> tuple[Point, dict[int, int], dict[int, Point]]:
    """Joint Feldman DKG: each party deals a random secret, and party i adds its n shares.

    Each party checks the share it receives against the dealer's commitments
    C_{j,k} = c_{j,k} g. There is no complaint phase, so this models honest
    dealers only. GJKR (1999) showed that this protocol lets a corrupt party
    bias the public key.
    """
    shares = {i: 0 for i in range(1, n + 1)}
    pub = None
    for _dealer in range(1, n + 1):
        coeffs = [rng.randrange(R) for _ in range(t)]
        commits = [mul(c, GEN) for c in coeffs]
        for i in range(1, n + 1):
            s = poly_eval(coeffs, i)
            expected = None
            for k, ck in enumerate(commits):
                expected = add(expected, mul(pow(i, k, R), ck))
            if mul(s, GEN) != expected:
                raise ValueError("a share does not match the commitments")
            shares[i] = (shares[i] + s) % R
        pub = add(pub, commits[0])
    return pub, shares, {i: mul(s, GEN) for i, s in shares.items()}


# ------------------------------------------------------------ threshold BLS
def partial_sign(share: int, msg: bytes) -> Point:
    return mul(share, hash_to_g1(msg))  # @line L2


def partial_verify(y_i: Point, msg: bytes, sigma_i: Point) -> bool:
    return in_g1(sigma_i) and pairing(sigma_i, GEN) == pairing(hash_to_g1(msg), y_i)  # @line L3


def lagrange_at_zero(ids: list[int], i: int) -> int:
    num, den = 1, 1
    for j in ids:  # @line L4
        if j != i:
            num = num * j % R
            den = den * (j - i) % R
    return num * pow(den, -1, R) % R


def combine(partials: dict[int, Point]) -> Point:
    """Interpolate the partial signatures of the parties in partials at 0."""
    ids = sorted(partials)
    out = None
    for i in ids:
        out = add(out, mul(lagrange_at_zero(ids, i), partials[i]))  # @line L5
    return out


def verify(pub: Point, msg: bytes, sig: Point) -> bool:
    if not in_g1(sig) or not in_g1(pub):
        return False
    return pairing(sig, GEN) == pairing(hash_to_g1(msg), pub)  # @line L6
