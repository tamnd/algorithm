# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/elliptic-curve-cryptography/. The authors are listed in prov/HTEPPM.jsonl.
"""The group of points of a short Weierstrass curve y^2 = x^3 + a x + b over
F_p, with affine and Jacobian formulas, the Montgomery ladder, and SEC 1
point compression. The curves are P-256 and a textbook toy curve.

For study only. Python big integers are not constant time, the ladder
uses Python branches on the secret, and nothing here must protect real
data. Use a FIPS 140 validated module or libsodium.
"""

from dataclasses import dataclass

Affine = tuple[int, int] | None  # None is the point at infinity O
Jacobian = tuple[int, int, int]  # (X, Y, Z) stands for (X/Z^2, Y/Z^3); Z = 0 is O


@dataclass(frozen=True)
class Curve:
    p: int
    a: int
    b: int
    g: tuple[int, int]
    n: int  # the prime order of g
    h: int  # the cofactor


# NIST P-256 (FIPS 186-5, SP 800-186), also called secp256r1.
P256 = Curve(
    p=2**256 - 2**224 + 2**192 + 2**96 - 1,
    a=-3,
    b=0x5AC635D8AA3A93E7B3EBBD55769886BC651D06B0CC53B0F63BCE3C3E27D2604B,
    g=(
        0x6B17D1F2E12C4247F8BCE6E563A440F277037D812DEB33A0F4A13945D898C296,
        0x4FE342E2FE1A7F9B8EE7EB4A7C0F9E162BCE33576B315ECECBB6406837BF51F5,
    ),
    n=0xFFFFFFFF00000000FFFFFFFFFFFFFFFFBCE6FAADA7179E84F3B9CAC2FC632551,
    h=1,
)

# y^2 = x^3 + 2x + 2 over F_17: 19 points, so the group is cyclic of prime order.
TOY = Curve(p=17, a=2, b=2, g=(5, 1), n=19, h=1)


def is_nonsingular(c: Curve) -> bool:
    return (4 * c.a**3 + 27 * c.b**2) % c.p != 0


def on_curve(c: Curve, pt: Affine) -> bool:
    if pt is None:
        return True
    x, y = pt
    return 0 <= x < c.p and 0 <= y < c.p and (y * y - (x**3 + c.a * x + c.b)) % c.p == 0


def neg(c: Curve, pt: Affine) -> Affine:
    return None if pt is None else (pt[0], (-pt[1]) % c.p)


def add(c: Curve, p1: Affine, p2: Affine) -> Affine:
    """The chord-and-tangent law in affine coordinates. Cost: one inversion and a few multiplications."""
    if p1 is None:
        return p2
    if p2 is None:
        return p1
    (x1, y1), (x2, y2) = p1, p2
    if x1 == x2 and (y1 + y2) % c.p == 0:
        return None  # P + (-P) = O, including 2P = O when y = 0
    if p1 == p2:
        lam = (3 * x1 * x1 + c.a) * pow(2 * y1, -1, c.p) % c.p  # the tangent
    else:
        lam = (y2 - y1) * pow(x2 - x1, -1, c.p) % c.p  # the chord
    x3 = (lam * lam - x1 - x2) % c.p
    return x3, (lam * (x1 - x3) - y1) % c.p


def to_jacobian(pt: Affine) -> Jacobian:
    return (1, 1, 0) if pt is None else (pt[0], pt[1], 1)


def from_jacobian(c: Curve, q: Jacobian) -> Affine:
    """One inversion at the end. Cost: one inversion and three multiplications."""
    x, y, z = q
    if z % c.p == 0:
        return None
    zi = pow(z, -1, c.p)
    return x * zi * zi % c.p, y * zi * zi * zi % c.p


def jdouble(c: Curve, q: Jacobian) -> Jacobian:
    """Doubling in Jacobian coordinates with no inversion."""
    x, y, z = q
    p = c.p
    if z % p == 0 or y % p == 0:
        return 1, 1, 0
    s = 4 * x * y * y % p
    m = (3 * x * x + c.a * pow(z, 4, p)) % p
    x3 = (m * m - 2 * s) % p
    y3 = (m * (s - x3) - 8 * pow(y, 4, p)) % p
    return x3, y3, 2 * y * z % p


def jadd(c: Curve, q1: Jacobian, q2: Jacobian) -> Jacobian:
    """Addition in Jacobian coordinates with no inversion."""
    p = c.p
    x1, y1, z1 = q1
    x2, y2, z2 = q2
    if z1 % p == 0:
        return q2
    if z2 % p == 0:
        return q1
    u1, u2 = x1 * z2 * z2 % p, x2 * z1 * z1 % p
    s1, s2 = y1 * pow(z2, 3, p) % p, y2 * pow(z1, 3, p) % p
    if u1 == u2:
        return jdouble(c, q1) if s1 == s2 else (1, 1, 0)
    hh, r = (u2 - u1) % p, (s2 - s1) % p
    h2 = hh * hh % p
    h3 = h2 * hh % p
    x3 = (r * r - h3 - 2 * u1 * h2) % p
    y3 = (r * (u1 * h2 - x3) - s1 * h3) % p
    return x3, y3, hh * z1 * z2 % p


def ladder(c: Curve, k: int, pt: Affine) -> Affine:
    """k * pt by the Montgomery ladder: one addition and one doubling per bit.

    Cost: 2 log2(k) Jacobian operations and one inversion. The sequence of
    operations does not depend on the bits of k, but the Python branch does.
    """
    r0, r1 = to_jacobian(None), to_jacobian(pt)  # @line L1
    for i in reversed(range(k.bit_length())):  # @line L2
        if (k >> i) & 1 == 0:  # @line L3
            r0, r1 = jdouble(c, r0), jadd(c, r0, r1)  # @line L4
        else:
            r0, r1 = jadd(c, r0, r1), jdouble(c, r1)  # @line L5
    return from_jacobian(c, r0)  # @line L6


def compress(c: Curve, pt: tuple[int, int]) -> bytes:
    """SEC 1 compressed encoding: 02 or 03 (the parity of y), then x."""
    size = (c.p.bit_length() + 7) // 8
    return bytes([2 + (pt[1] & 1)]) + pt[0].to_bytes(size, "big")


def decompress(c: Curve, data: bytes) -> tuple[int, int]:
    """Inverse of compress, for p = 3 (mod 4). Cost: one exponentiation modulo p."""
    assert c.p % 4 == 3 and data[0] in (2, 3)
    x = int.from_bytes(data[1:], "big")
    rhs = (x**3 + c.a * x + c.b) % c.p
    y = pow(rhs, (c.p + 1) // 4, c.p)
    if y * y % c.p != rhs:
        raise ValueError("x is not the x-coordinate of a point")
    if y & 1 != data[0] & 1:
        y = c.p - y
    return x, y
