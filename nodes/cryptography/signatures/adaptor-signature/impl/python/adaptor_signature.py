# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/adaptor-signature/. The authors are listed in prov/ZMDYYY.jsonl.
"""Schnorr adaptor signatures on secp256k1 whose adapted output is a BIP 340 signature.

pre_sign(d, m, T) makes a pre-signature (R_hat, s') for the statement
T = t G. Anyone can check it with pre_verify. adapt() with the witness t
turns it into an ordinary BIP 340 signature, and extract() recovers t from
the pre-signature and the published signature. The parity rule: R = R_hat + T
must stand for its even-y twin in BIP 340, so the sign eps of R decides
whether the signer uses k or -k and whether t is added or subtracted.

This follows the common construction (Poelstra's scriptless scripts) with
the BIP 340 parity handled as above; it is not the exact byte format of
any library. NOT SECURE: affine Python arithmetic, not constant time.
For study only.
"""

import hashlib
import random

P = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
G = (
    0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
    0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8,
)

Point = tuple[int, int] | None


def point_add(a: Point, b: Point) -> Point:
    if a is None:
        return b
    if b is None:
        return a
    if a[0] == b[0] and (a[1] + b[1]) % P == 0:
        return None
    if a == b:
        lam = 3 * a[0] * a[0] * pow(2 * a[1], -1, P) % P
    else:
        lam = (b[1] - a[1]) * pow(b[0] - a[0], -1, P) % P
    x3 = (lam * lam - a[0] - b[0]) % P
    return x3, (lam * (a[0] - x3) - a[1]) % P


def point_neg(a: Point) -> Point:
    return None if a is None else (a[0], (-a[1]) % P)


def point_mul(a: Point, k: int) -> Point:
    result = None
    for bit in bin(k % N)[2:] if k % N else "":
        result = point_add(result, result)
        if bit == "1":
            result = point_add(result, a)
    return result


def has_even_y(a: Point) -> bool:
    assert a is not None
    return a[1] % 2 == 0


def xbytes(a: Point) -> bytes:
    assert a is not None
    return a[0].to_bytes(32, "big")


def lift_x(x: int) -> Point:
    if x >= P:
        return None
    c = (pow(x, 3, P) + 7) % P
    y = pow(c, (P + 1) // 4, P)
    if y * y % P != c:
        return None
    return x, y if y % 2 == 0 else P - y


def challenge(r: Point, pub: Point, msg: bytes) -> int:
    t = hashlib.sha256(b"BIP0340/challenge").digest()
    h = hashlib.sha256(t + t + xbytes(r) + xbytes(pub) + msg).digest()
    return int.from_bytes(h, "big") % N


def keygen(d0: int) -> tuple[int, Point]:
    """Return the secret d with an even-y public key P = d G (BIP 340 style)."""
    pub = point_mul(G, d0)
    return (d0, pub) if has_even_y(pub) else (N - d0, point_neg(pub))


def schnorr_verify(msg: bytes, pubkey: bytes, sig: bytes) -> bool:
    """Plain BIP 340 verification."""
    pub = lift_x(int.from_bytes(pubkey, "big"))
    r = int.from_bytes(sig[:32], "big")
    s = int.from_bytes(sig[32:], "big")
    r_lift = lift_x(r)  # only its x coordinate enters the challenge
    if pub is None or r_lift is None or s >= N:
        return False
    r_pt = point_add(point_mul(G, s), point_neg(point_mul(pub, challenge(r_lift, pub, msg))))
    return r_pt is not None and has_even_y(r_pt) and r_pt[0] == r


def sign_of(r: Point) -> int:
    return 1 if has_even_y(r) else -1


def pre_sign(d: int, pub: Point, msg: bytes, stmt: Point, rng: random.Random) -> tuple[Point, int]:
    k = rng.randrange(1, N)
    r_hat = point_mul(G, k)
    r = point_add(r_hat, stmt)  # @line L1
    e = challenge(r, pub, msg)  # @line L2
    return r_hat, (sign_of(r) * k + e * d) % N  # @line L3


def pre_verify(pub: Point, msg: bytes, stmt: Point, presig: tuple[Point, int]) -> bool:
    r_hat, s_pre = presig
    r = point_add(r_hat, stmt)  # @line L4
    if r is None:
        return False
    e = challenge(r, pub, msg)
    rhs = point_add(r_hat if sign_of(r) == 1 else point_neg(r_hat), point_mul(pub, e))
    return point_mul(G, s_pre) == rhs  # @line L5


def adapt(presig: tuple[Point, int], stmt: Point, t: int) -> bytes:
    r_hat, s_pre = presig
    r = point_add(r_hat, stmt)
    s = (s_pre + sign_of(r) * t) % N  # @line L6
    return xbytes(r) + s.to_bytes(32, "big")


def extract(sig: bytes, presig: tuple[Point, int], stmt: Point) -> int:
    r_hat, s_pre = presig
    r = point_add(r_hat, stmt)
    t = sign_of(r) * (int.from_bytes(sig[32:], "big") - s_pre) % N  # @line L7
    if point_mul(G, t) != stmt:
        raise ValueError("the signature does not match this pre-signature")
    return t
