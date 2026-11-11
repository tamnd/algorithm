# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ecdh/. The authors are listed in prov/79PZ04.jsonl.
"""Elliptic curve Diffie-Hellman on short Weierstrass curves (NIST SP 800-56A Rev. 3).

The curve is y^2 = x^3 + a x + b over GF(p), with a base point G of prime
order n and cofactor h. The code gives key generation, the full and the
partial public key validation of SP 800-56A Rev. 3 (Sections 5.6.2.3.3 and
5.6.2.3.4), and the ECC CDH primitive of Section 5.7.1.2. The curves P-256
and P-384 use the parameters of RFC 5903 Section 3 (the same as FIPS 186 and
SP 800-186).

For study only. The code is not constant time: the double-and-add loop
branches on the bits of the private key, and Python integers leak timing.
Do not use it to protect real data. Use the ECDH of OpenSSL or BoringSSL,
the Python package cryptography, or a FIPS 140 validated module instead.

Cost: a scalar multiplication by an m-bit scalar does m point doublings and
about m/2 point additions in Jacobian coordinates, each a few field
multiplications, and one field inversion at the end.
"""

import random
import secrets
from dataclasses import dataclass
from typing import Optional

Point = Optional[tuple[int, int]]  # an affine point, or None for the point at infinity O


@dataclass(frozen=True)
class Curve:
    name: str
    p: int
    a: int
    b: int
    gx: int
    gy: int
    n: int
    h: int

    @property
    def g(self) -> tuple[int, int]:
        return (self.gx, self.gy)

    @property
    def size(self) -> int:
        """The length in bytes of a field element, ceil(log_256 p)."""
        return (self.p.bit_length() + 7) // 8


# RFC 5903 Section 3.1 (256-bit random ECP group, NIST P-256), copied by hand.
P256 = Curve(
    name="P-256",
    p=0xFFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFF,
    a=0xFFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFF - 3,
    b=0x5AC635D8AA3A93E7B3EBBD55769886BC651D06B0CC53B0F63BCE3C3E27D2604B,
    gx=0x6B17D1F2E12C4247F8BCE6E563A440F277037D812DEB33A0F4A13945D898C296,
    gy=0x4FE342E2FE1A7F9B8EE7EB4A7C0F9E162BCE33576B315ECECBB6406837BF51F5,
    n=0xFFFFFFFF00000000FFFFFFFFFFFFFFFFBCE6FAADA7179E84F3B9CAC2FC632551,
    h=1,
)

# RFC 5903 Section 3.2 (384-bit random ECP group, NIST P-384), copied by hand.
_P384_P = int(
    "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFE"
    "FFFFFFFF0000000000000000FFFFFFFF",
    16,
)
P384 = Curve(
    name="P-384",
    p=_P384_P,
    a=_P384_P - 3,
    b=int(
        "B3312FA7E23EE7E4988E056BE3F82D19181D9C6EFE8141120314088F5013875A"
        "C656398D8A2ED19D2A85C8EDD3EC2AEF",
        16,
    ),
    gx=int(
        "AA87CA22BE8B05378EB1C71EF320AD746E1D3B628BA79B9859F741E082542A38"
        "5502F25DBF55296C3A545E3872760AB7",
        16,
    ),
    gy=int(
        "3617DE4A96262C6F5D9E98BF9292DC29F8F41DBD289A147CE9DA3113B5F0B8C0"
        "0A60B1CE1D7E819D7A431D7C90EA0E5F",
        16,
    ),
    n=int(
        "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFC7634D81F4372DDF"
        "581A0DB248B0A77AECEC196ACCC52973",
        16,
    ),
    h=1,
)


class ValidationError(ValueError):
    """A public key failed validation, or the shared point is O."""


# ---------------------------------------------------------------- arithmetic
# Jacobian coordinates (X, Y, Z) stand for the affine point (X/Z^2, Y/Z^3).
# Z = 0 stands for O. The formulas do not use b: this is what makes an
# invalid curve attack possible when a point is not checked.

_INF = (1, 1, 0)


def _jacobian_double(c: Curve, pt: tuple[int, int, int]) -> tuple[int, int, int]:
    x, y, z = pt
    p = c.p
    if z == 0 or y == 0:
        return _INF
    yy = y * y % p
    s = 4 * x * yy % p
    zz = z * z % p
    m = (3 * x * x + c.a * zz * zz) % p
    x3 = (m * m - 2 * s) % p
    y3 = (m * (s - x3) - 8 * yy * yy) % p
    z3 = 2 * y * z % p
    return (x3, y3, z3)


def _jacobian_add(c: Curve, p1: tuple[int, int, int], p2: tuple[int, int, int]) -> tuple[int, int, int]:
    if p1[2] == 0:
        return p2
    if p2[2] == 0:
        return p1
    p = c.p
    x1, y1, z1 = p1
    x2, y2, z2 = p2
    z1z1 = z1 * z1 % p
    z2z2 = z2 * z2 % p
    u1 = x1 * z2z2 % p
    u2 = x2 * z1z1 % p
    s1 = y1 * z2 * z2z2 % p
    s2 = y2 * z1 * z1z1 % p
    if u1 == u2:
        if s1 != s2:
            return _INF
        return _jacobian_double(c, p1)
    hh = (u2 - u1) % p
    r = (s2 - s1) % p
    h2 = hh * hh % p
    h3 = hh * h2 % p
    u1h2 = u1 * h2 % p
    x3 = (r * r - h3 - 2 * u1h2) % p
    y3 = (r * (u1h2 - x3) - s1 * h3) % p
    z3 = hh * z1 * z2 % p
    return (x3, y3, z3)


def _to_affine(c: Curve, pt: tuple[int, int, int]) -> Point:
    x, y, z = pt
    if z == 0:
        return None
    zi = pow(z, c.p - 2, c.p)
    zi2 = zi * zi % c.p
    return (x * zi2 % c.p, y * zi2 * zi % c.p)


def point_add(c: Curve, p1: Point, p2: Point) -> Point:
    """The sum of two affine points (None is O)."""
    j1 = _INF if p1 is None else (p1[0], p1[1], 1)
    j2 = _INF if p2 is None else (p2[0], p2[1], 1)
    return _to_affine(c, _jacobian_add(c, j1, j2))


def scalar_mult(c: Curve, k: int, pt: Point) -> Point:
    """k * pt by left-to-right double-and-add. Not constant time."""
    if pt is None or k == 0:
        return None
    if k < 0:
        k, pt = -k, (pt[0], (-pt[1]) % c.p)
    acc = _INF
    base = (pt[0], pt[1], 1)
    for bit in bin(k)[2:]:
        acc = _jacobian_double(c, acc)
        if bit == "1":
            acc = _jacobian_add(c, acc, base)
    return _to_affine(c, acc)


def is_on_curve(c: Curve, pt: Point) -> bool:
    """True if pt is O or satisfies y^2 = x^3 + a x + b mod p."""
    if pt is None:
        return True
    x, y = pt
    return (y * y - (x * x * x + c.a * x + c.b)) % c.p == 0


# ---------------------------------------------------------------- SP 800-56A


def generate_key_pair(c: Curve, rng: Optional[random.Random] = None) -> tuple[int, Point]:
    """A private key d uniform in [1, n - 1] and the public key Q = dG."""
    r = rng or secrets.SystemRandom()
    d = r.randrange(1, c.n)  # @line L1
    q = scalar_mult(c, d, c.g)  # @line L2
    return d, q  # @line L3


def validate_public_key(c: Curve, q: Point, full: bool = True) -> None:
    """ECC full (or partial) public key validation, SP 800-56A Rev. 3, 5.6.2.3.3 (5.6.2.3.4).

    Raises ValidationError if q is not a valid public key. The partial
    routine skips the check n Q = O; it is enough when h = 1, where each
    point of the curve other than O has order n.
    """
    if q is None:  # @line L4
        raise ValidationError("the public key is the point at infinity")
    x, y = q
    if not (0 <= x < c.p and 0 <= y < c.p):  # @line L5
        raise ValidationError("a coordinate is out of range")
    if not is_on_curve(c, q):  # @line L6
        raise ValidationError("the point is not on the curve")
    if full and scalar_mult(c, c.n, q) is not None:  # @line L7
        raise ValidationError("the point does not have order n")


def ecc_cdh(c: Curve, d: int, q: Point) -> bytes:
    """The ECC CDH primitive, SP 800-56A Rev. 3, Section 5.7.1.2.

    Returns Z, the x-coordinate of h d Q as a byte string of ceil(log_256 p)
    bytes. The caller must validate q first; this function does not.
    """
    pt = scalar_mult(c, c.h * d, q)  # @line L8
    if pt is None:  # @line L9
        raise ValidationError("the shared point is the point at infinity")
    return pt[0].to_bytes(c.size, "big")  # @line L10


def ecdh_shared(c: Curve, d: int, q: Point) -> bytes:
    """Validate the peer public key q (full validation), then return Z."""
    validate_public_key(c, q, full=True)
    return ecc_cdh(c, d, q)
