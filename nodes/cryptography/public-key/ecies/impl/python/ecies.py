# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ecies/. The authors are listed in prov/YWSZYG.jsonl.
"""ECIES as in SEC 1 version 2.0, Section 5.1, on secp256k1.

Choices from the SEC 1 menus: the ANSI X9.63 key derivation function with
SHA-256, the XOR encryption scheme, and HMAC-SHA-256 with a 32-byte tag.
Points are encoded uncompressed (0x04 || x || y). The option
bind_ephemeral=True also feeds the encoded ephemeral point to the KDF, as
ISO 18033-2 and DHAES do; without it, the ciphertext with -R in place of R
decrypts to the same message (a benign malleability).

For study only. Nothing here is constant time: the scalar multiplication
branches on the bits of the secret and the field inversions leak timing.
"""

import hashlib
import hmac
import secrets
from dataclasses import dataclass

Point = tuple[int, int] | None  # None is the point at infinity O


@dataclass(frozen=True)
class Curve:
    """The curve y^2 = x^3 + a x + b over F_p, base point g of prime order n, cofactor h."""

    p: int
    a: int
    b: int
    g: tuple[int, int]
    n: int
    h: int

    @property
    def size(self) -> int:
        return (self.p.bit_length() + 7) // 8


# SEC 2 version 2.0, the curve secp256k1.
SECP256K1 = Curve(
    p=2**256 - 2**32 - 977,
    a=0,
    b=7,
    g=(
        0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
        0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8,
    ),
    n=0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141,
    h=1,
)

# A textbook toy curve for the worked example: 19 points, cofactor 1.
TOY = Curve(p=17, a=2, b=2, g=(5, 1), n=19, h=1)


class DecryptionError(Exception):
    """Raised for every rejected ciphertext."""


def on_curve(c: Curve, pt: Point) -> bool:
    if pt is None:
        return True
    x, y = pt
    return 0 <= x < c.p and 0 <= y < c.p and (y * y - x * x * x - c.a * x - c.b) % c.p == 0


def add(c: Curve, p1: Point, p2: Point) -> Point:
    """The chord-and-tangent group law in affine coordinates. Cost: one inversion."""
    if p1 is None:
        return p2
    if p2 is None:
        return p1
    x1, y1 = p1
    x2, y2 = p2
    if x1 == x2 and (y1 + y2) % c.p == 0:
        return None
    if p1 == p2:
        lam = (3 * x1 * x1 + c.a) * pow(2 * y1, -1, c.p) % c.p
    else:
        lam = (y2 - y1) * pow(x2 - x1, -1, c.p) % c.p
    x3 = (lam * lam - x1 - x2) % c.p
    return x3, (lam * (x1 - x3) - y1) % c.p


def neg(c: Curve, pt: Point) -> Point:
    return None if pt is None else (pt[0], (-pt[1]) % c.p)


def mul(c: Curve, k: int, pt: Point) -> Point:
    """k * pt by double-and-add from the top bit. Cost: Θ(log k) group operations."""
    acc: Point = None
    for bit in bin(k)[2:] if k > 0 else "":
        acc = add(c, acc, acc)
        if bit == "1":
            acc = add(c, acc, pt)
    return acc


def encode_point(c: Curve, pt: tuple[int, int]) -> bytes:
    return b"\x04" + pt[0].to_bytes(c.size, "big") + pt[1].to_bytes(c.size, "big")


def decode_point(c: Curve, data: bytes) -> tuple[int, int]:
    if len(data) != 1 + 2 * c.size or data[0] != 4:
        raise DecryptionError("bad point encoding")
    return int.from_bytes(data[1 : 1 + c.size], "big"), int.from_bytes(data[1 + c.size :], "big")


def kdf_x963(z: bytes, length: int, shared_info: bytes = b"") -> bytes:
    """ANSI X9.63 KDF with SHA-256 (SEC 1 Section 3.6.1). Cost: Θ(length) hashing."""
    out = b""
    counter = 1
    while len(out) < length:
        out += hashlib.sha256(z + counter.to_bytes(4, "big") + shared_info).digest()
        counter += 1
    return out[:length]


def keygen(c: Curve = SECP256K1, rand_below=secrets.randbelow) -> tuple[int, tuple[int, int]]:
    """Return (d, Q) with Q = d G. Cost: one scalar multiplication."""
    d = 1 + rand_below(c.n - 1)  # @line L1
    q = mul(c, d, c.g)  # @line L2
    assert q is not None
    return d, q  # @line L3


def _keys(c: Curve, z: tuple[int, int], r_bytes: bytes, n_enc: int, bind: bool) -> tuple[bytes, bytes]:
    info = r_bytes if bind else b""
    k = kdf_x963(z[0].to_bytes(c.size, "big"), n_enc + 32, info)
    return k[:n_enc], k[n_enc:]


def encrypt(
    q: tuple[int, int],
    m: bytes,
    c: Curve = SECP256K1,
    rand_below=secrets.randbelow,
    bind_ephemeral: bool = False,
) -> tuple[bytes, bytes, bytes]:
    """Return (R, ciphertext, tag). Cost: two scalar multiplications and Θ(len(m)) hashing."""
    k = 1 + rand_below(c.n - 1)  # @line L4
    r = mul(c, k, c.g)  # @line L5
    z = mul(c, c.h * k, q)  # @line L6
    assert r is not None and z is not None
    r_bytes = encode_point(c, r)
    k_enc, k_mac = _keys(c, z, r_bytes, len(m), bind_ephemeral)  # @line L7
    body = bytes(a ^ b for a, b in zip(m, k_enc))  # @line L8
    tag = hmac.new(k_mac, body, hashlib.sha256).digest()  # @line L9
    return r_bytes, body, tag  # @line L10


def decrypt(
    d: int,
    ct: tuple[bytes, bytes, bytes],
    c: Curve = SECP256K1,
    bind_ephemeral: bool = False,
    validate: bool = True,
) -> bytes:
    """Return the message or raise DecryptionError. Cost: one scalar multiplication.

    validate=False skips the public key validation of line L11; it exists only
    so that the tests can show the invalid curve attack.
    """
    r_bytes, body, tag = ct
    r = decode_point(c, r_bytes)
    if validate and not on_curve(c, r):  # @line L11
        raise DecryptionError("ephemeral point not on the curve")
    z = mul(c, c.h * d, r)  # @line L12
    if z is None:
        raise DecryptionError("shared point is the point at infinity")
    k_enc, k_mac = _keys(c, z, r_bytes, len(body), bind_ephemeral)  # @line L13
    if not hmac.compare_digest(hmac.new(k_mac, body, hashlib.sha256).digest(), tag):  # @line L14
        raise DecryptionError("bad tag")
    return bytes(a ^ b for a, b in zip(body, k_enc))  # @line L15
