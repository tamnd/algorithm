# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/verifiable-random-function/. The authors are listed in prov/NY3QP4.jsonl.
"""ECVRF-EDWARDS25519-SHA512-TAI, the elliptic curve VRF of RFC 9381
(August 2023), Section 5, with the ciphersuite of Section 5.5
(suite_string 0x03, try-and-increment encode to curve, nonce generation
as in RFC 8032).

The edwards25519 arithmetic is a small local copy that follows RFC 8032,
Sections 5.1.3 (decoding) and 5.1.4 (point addition in extended
coordinates).

For study only. The code is not constant time (the scalar multiplication
branches on the bits of the secret, and try-and-increment takes a time
that depends on the input), and it must not protect real data. Use a
maintained library, for example libsodium, which has an ECVRF
implementation in its development history, or the reference code that
the RFC authors publish.
"""

import hashlib
from typing import Optional, Tuple

# ---------------------------------------------------------------- edwards25519 (RFC 8032, Section 5.1)

P = 2**255 - 19
Q = 2**252 + 27742317777372353535851937790883648493  # the prime order of the base point
D = -121665 * pow(121666, P - 2, P) % P
SQRT_M1 = pow(2, (P - 1) // 4, P)
COFACTOR = 8
SUITE = b"\x03"  # suite_string of ECVRF-EDWARDS25519-SHA512-TAI
C_LEN = 16  # length of the challenge in bytes
PT_LEN = 32
Q_LEN = 32

Point = Tuple[int, int, int, int]  # extended coordinates (X, Y, Z, T) with x = X/Z, y = Y/Z, xy = T/Z
IDENTITY: Point = (0, 1, 1, 0)


def point_add(p1: Point, p2: Point) -> Point:
    """Add two points with the formula of RFC 8032, Section 5.1.4."""
    x1, y1, z1, t1 = p1
    x2, y2, z2, t2 = p2
    a = (y1 - x1) * (y2 - x2) % P
    b = (y1 + x1) * (y2 + x2) % P
    c = 2 * t1 * t2 * D % P
    d = 2 * z1 * z2 % P
    e, f, g, h = b - a, d - c, d + c, b + a
    return (e * f % P, g * h % P, f * g % P, e * h % P)


def point_neg(p1: Point) -> Point:
    x, y, z, t = p1
    return (-x % P, y, z, -t % P)


def scalar_mult(s: int, p1: Point) -> Point:
    """Double and add, from the low bit up. Not constant time."""
    r = IDENTITY
    while s > 0:
        if s & 1:
            r = point_add(r, p1)
        p1 = point_add(p1, p1)
        s >>= 1
    return r


def point_equal(p1: Point, p2: Point) -> bool:
    return (p1[0] * p2[2] - p2[0] * p1[2]) % P == 0 and (p1[1] * p2[2] - p2[1] * p1[2]) % P == 0


def recover_x(y: int, sign: int) -> Optional[int]:
    """The x of the point with this y and this sign bit, or None (RFC 8032, Section 5.1.3)."""
    if y >= P:
        return None
    x2 = (y * y - 1) * pow(D * y * y + 1, P - 2, P) % P
    if x2 == 0:
        return None if sign else 0
    x = pow(x2, (P + 3) // 8, P)
    if (x * x - x2) % P != 0:
        x = x * SQRT_M1 % P
    if (x * x - x2) % P != 0:
        return None
    if (x & 1) != sign:
        x = P - x
    return x


def string_to_point(s: bytes) -> Optional[Point]:
    """Decode 32 bytes to a point, or None when they do not encode a point."""
    if len(s) != 32:
        return None
    y = int.from_bytes(s, "little")
    sign = y >> 255
    y &= (1 << 255) - 1
    x = recover_x(y, sign)
    if x is None:
        return None
    return (x, y, 1, x * y % P)


def point_to_string(p1: Point) -> bytes:
    zinv = pow(p1[2], P - 2, P)
    x, y = p1[0] * zinv % P, p1[1] * zinv % P
    return (y | ((x & 1) << 255)).to_bytes(32, "little")


_GY = 4 * pow(5, P - 2, P) % P
BASE: Point = (recover_x(_GY, 0), _GY, 1, recover_x(_GY, 0) * _GY % P)

# ---------------------------------------------------------------- ECVRF (RFC 9381, Section 5)


def sha512(b: bytes) -> bytes:
    return hashlib.sha512(b).digest()


def secret_scalar(sk: bytes) -> int:
    """The secret scalar x of an Ed25519 secret key (RFC 8032, Section 5.1.5)."""
    h = bytearray(sha512(sk)[:32])
    h[0] &= 248
    h[31] &= 127
    h[31] |= 64
    return int.from_bytes(h, "little")


def public_key(sk: bytes) -> bytes:
    return point_to_string(scalar_mult(secret_scalar(sk), BASE))


def encode_to_curve(salt: bytes, alpha: bytes) -> Point:
    """Try and increment, RFC 9381 Section 5.4.1.1. The salt is PK_string."""
    ctr = 0
    while True:
        hash_string = sha512(SUITE + b"\x01" + salt + alpha + bytes([ctr]) + b"\x00")
        h = string_to_point(hash_string[:32])
        if h is not None:
            h = scalar_mult(COFACTOR, h)
            if not point_equal(h, IDENTITY):
                return h
        ctr += 1


def nonce_generation(sk: bytes, h_string: bytes) -> int:
    """RFC 9381 Section 5.4.2.2, the nonce of RFC 8032."""
    truncated = sha512(sk)[32:64]
    return int.from_bytes(sha512(truncated + h_string), "little") % Q


def challenge_generation(*points: Point) -> int:
    """RFC 9381 Section 5.4.3, with the five points Y, H, Gamma, U, V."""
    s = SUITE + b"\x02" + b"".join(point_to_string(pt) for pt in points) + b"\x00"
    return int.from_bytes(sha512(s)[:C_LEN], "little")


def prove(sk: bytes, alpha: bytes) -> bytes:
    """ECVRF_prove, RFC 9381 Section 5.1. Returns the 80-byte proof pi."""
    x = secret_scalar(sk)
    y_point = scalar_mult(x, BASE)
    pk = point_to_string(y_point)
    h = encode_to_curve(pk, alpha)
    gamma = scalar_mult(x, h)
    k = nonce_generation(sk, point_to_string(h))
    c = challenge_generation(y_point, h, gamma, scalar_mult(k, BASE), scalar_mult(k, h))
    s = (k + c * x) % Q
    return point_to_string(gamma) + c.to_bytes(C_LEN, "little") + s.to_bytes(Q_LEN, "little")


def decode_proof(pi: bytes) -> Optional[Tuple[Point, int, int]]:
    """RFC 9381 Section 5.4.4."""
    if len(pi) != PT_LEN + C_LEN + Q_LEN:
        return None
    gamma = string_to_point(pi[:PT_LEN])
    if gamma is None:
        return None
    c = int.from_bytes(pi[PT_LEN:PT_LEN + C_LEN], "little")
    s = int.from_bytes(pi[PT_LEN + C_LEN:], "little")
    if s >= Q:
        return None
    return gamma, c, s


def proof_to_hash(pi: bytes) -> Optional[bytes]:
    """RFC 9381 Section 5.2. Returns the 64-byte output beta."""
    d = decode_proof(pi)
    if d is None:
        return None
    gamma = d[0]
    return sha512(SUITE + b"\x03" + point_to_string(scalar_mult(COFACTOR, gamma)) + b"\x00")


def verify(pk: bytes, alpha: bytes, pi: bytes, validate_key: bool = True) -> Optional[bytes]:
    """ECVRF_verify, RFC 9381 Section 5.3. Returns beta when pi is valid, else None."""
    y_point = string_to_point(pk)
    if y_point is None:
        return None
    if validate_key and point_equal(scalar_mult(COFACTOR, y_point), IDENTITY):
        return None
    d = decode_proof(pi)
    if d is None:
        return None
    gamma, c, s = d
    h = encode_to_curve(pk, alpha)
    u = point_add(scalar_mult(s, BASE), point_neg(scalar_mult(c, y_point)))
    v = point_add(scalar_mult(s, h), point_neg(scalar_mult(c, gamma)))
    if challenge_generation(y_point, h, gamma, u, v) != c:
        return None
    return proof_to_hash(pi)
