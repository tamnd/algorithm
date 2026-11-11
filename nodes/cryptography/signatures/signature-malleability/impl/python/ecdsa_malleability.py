# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/signature-malleability/. The authors are listed in prov/67AG3K.jsonl.
"""ECDSA malleability: if (r, s) is a valid ECDSA signature, so is (r, n - s),
and anyone can compute it without the key. The low-s rule of BIP 62 and
BIP 146 (Bitcoin) and EIP-2 (Ethereum) accepts only s <= n/2, which leaves
one signature of each pair.

The curve arithmetic is written here in affine coordinates. The curves are a
toy curve y^2 = x^3 + 7 over F_97 with a group of prime order 79, and
secp256k1 with the constants of SEC 2, Section 2.4.1. The page is about the
signature, not the hash, so the hash is SHA-256 from hashlib.

For study only. The code is not constant time, it takes the nonce k from the
caller or from a seeded source in the tests, and it must not protect real
data. Use ECDSA or Ed25519 from the pyca/cryptography library or from a
FIPS 140 validated module.
"""

import hashlib
from dataclasses import dataclass
from typing import Optional, Tuple

Point = Optional[Tuple[int, int]]  # None is the point at infinity


@dataclass(frozen=True)
class Curve:
    p: int  # field prime
    a: int
    b: int
    g: Tuple[int, int]
    n: int  # prime order of g


TOY = Curve(p=97, a=0, b=7, g=(1, 28), n=79)

# SEC 2 version 2.0, Section 2.4.1, secp256k1.
SECP256K1 = Curve(
    p=0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F,
    a=0,
    b=7,
    g=(0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
       0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8),
    n=0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141,
)


def on_curve(c: Curve, pt: Point) -> bool:
    if pt is None:
        return True
    x, y = pt
    return (y * y - x * x * x - c.a * x - c.b) % c.p == 0


def add(c: Curve, P: Point, Q: Point) -> Point:
    if P is None:
        return Q
    if Q is None:
        return P
    (x1, y1), (x2, y2) = P, Q
    if x1 == x2 and (y1 + y2) % c.p == 0:
        return None
    if P == Q:
        lam = (3 * x1 * x1 + c.a) * pow(2 * y1, -1, c.p) % c.p
    else:
        lam = (y2 - y1) * pow(x2 - x1, -1, c.p) % c.p
    x3 = (lam * lam - x1 - x2) % c.p
    return x3, (lam * (x1 - x3) - y1) % c.p


def mul(c: Curve, k: int, P: Point) -> Point:
    """Double-and-add, from the low binary digit up. Not constant time."""
    R = None
    while k > 0:
        if k & 1:
            R = add(c, R, P)
        P = add(c, P, P)
        k >>= 1
    return R


def hash_to_z(c: Curve, message: bytes) -> int:
    """The leftmost bit-length(n) binary digits of SHA-256(message), as in SEC 1."""
    h = int.from_bytes(hashlib.sha256(message).digest(), "big")
    excess = 256 - c.n.bit_length()
    return h >> excess if excess > 0 else h


def sign_z(c: Curve, d: int, z: int, k: int) -> Tuple[int, int]:
    R = mul(c, k, c.g)
    r = R[0] % c.n
    s = pow(k, -1, c.n) * (z + r * d) % c.n
    if r == 0 or s == 0:
        raise ValueError("choose another k")
    return r, s


def verify_z(c: Curve, Q: Point, z: int, sig: Tuple[int, int]) -> bool:
    """Plain ECDSA verification: accepts both (r, s) and (r, n - s)."""
    r, s = sig
    if not (0 < r < c.n and 0 < s < c.n):
        return False
    w = pow(s, -1, c.n)
    X = add(c, mul(c, z * w % c.n, c.g), mul(c, r * w % c.n, Q))
    return X is not None and X[0] % c.n == r


def malleate(c: Curve, sig: Tuple[int, int]) -> Tuple[int, int]:
    """The third-party change: kG and -kG have the same x-coordinate."""
    r, s = sig
    return r, c.n - s


def is_low_s(c: Curve, sig: Tuple[int, int]) -> bool:
    return 0 < sig[1] <= c.n // 2


def normalize_low_s(c: Curve, sig: Tuple[int, int]) -> Tuple[int, int]:
    return sig if is_low_s(c, sig) else malleate(c, sig)


def verify_z_low_s(c: Curve, Q: Point, z: int, sig: Tuple[int, int]) -> bool:
    """The BIP 146 LOW_S rule (and EIP-2): reject s > n/2, then verify."""
    return is_low_s(c, sig) and verify_z(c, Q, z, sig)


def txid(payload: bytes, sig: Tuple[int, int], c: Curve = SECP256K1) -> str:
    """A toy transaction identifier that, like the pre-SegWit Bitcoin txid,
    hashes the signature together with the payload."""
    size = (c.n.bit_length() + 7) // 8
    data = payload + sig[0].to_bytes(size, "big") + sig[1].to_bytes(size, "big")
    return hashlib.sha256(hashlib.sha256(data).digest()).hexdigest()
