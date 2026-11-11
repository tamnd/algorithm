# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ed25519/. The authors are listed in prov/2THJ4W.jsonl.
"""Ed25519 (pure EdDSA on edwards25519) as in RFC 8032 Section 5.1.

The curve arithmetic uses extended coordinates (X : Y : Z : T) with x = X/Z,
y = Y/Z and x y = T/Z. SHA-512 comes from hashlib. verify() takes a flag that
selects the cofactored equation [8][S]B = [8]R + [8][k]A, which RFC 8032 and
ZIP 215 use, or the cofactorless equation [S]B = R + [k]A, which many
libraries use. The two agree on honest signatures and can disagree on others.

For study only. This code is not constant time, it branches on secret data,
and it must not be used to protect real data. Use libsodium or another
reviewed library.
"""

import hashlib

P = 2**255 - 19
L = 2**252 + 27742317777372353535851937790883648493  # the prime order of B
D = -121665 * pow(121666, -1, P) % P
SQRT_M1 = pow(2, (P - 1) // 4, P)  # a square root of -1 mod p

Point = tuple[int, int, int, int]  # extended coordinates (X, Y, Z, T)
IDENTITY: Point = (0, 1, 1, 0)


def point_add(a: Point, b: Point) -> Point:
    """Addition on -x^2 + y^2 = 1 + d x^2 y^2 (Hisil, Wong, Carter and Dawson; RFC 8032 Section 5.1.4)."""
    x1, y1, z1, t1 = a
    x2, y2, z2, t2 = b
    aa = (y1 - x1) * (y2 - x2) % P
    bb = (y1 + x1) * (y2 + x2) % P
    cc = 2 * t1 * t2 * D % P
    dd = 2 * z1 * z2 % P
    e, f, g, h = bb - aa, dd - cc, dd + cc, bb + aa
    return e * f % P, g * h % P, f * g % P, e * h % P


def point_mul(k: int, a: Point) -> Point:
    q = IDENTITY
    while k > 0:
        if k & 1:
            q = point_add(q, a)
        a = point_add(a, a)
        k >>= 1
    return q


def point_equal(a: Point, b: Point) -> bool:
    return (a[0] * b[2] - b[0] * a[2]) % P == 0 and (a[1] * b[2] - b[1] * a[2]) % P == 0


def recover_x(y: int, sign: int) -> int | None:
    """RFC 8032 Section 5.1.3, step 2 to 4: x from y and the sign bit, or None."""
    if y >= P:
        return None
    x2 = (y * y - 1) * pow(D * y * y + 1, -1, P) % P
    if x2 == 0:
        return None if sign else 0
    x = pow(x2, (P + 3) // 8, P)
    if (x * x - x2) % P != 0:
        x = x * SQRT_M1 % P
    if (x * x - x2) % P != 0:
        return None
    if x & 1 != sign:
        x = P - x
    return x


_BY = 4 * pow(5, -1, P) % P
_BX = recover_x(_BY, 0)
assert _BX is not None
B: Point = (_BX, _BY, 1, _BX * _BY % P)


def encode(a: Point) -> bytes:
    """32 bytes: y in little endian, with the low binary digit of x in the top bit."""
    zinv = pow(a[2], -1, P)
    x, y = a[0] * zinv % P, a[1] * zinv % P
    return (y | ((x & 1) << 255)).to_bytes(32, "little")


def decode(s: bytes) -> Point | None:
    if len(s) != 32:
        return None
    n = int.from_bytes(s, "little")
    y, sign = n & ((1 << 255) - 1), n >> 255
    x = recover_x(y, sign)
    if x is None:
        return None
    return (x, y, 1, x * y % P)


def sha512_int(*parts: bytes) -> int:
    return int.from_bytes(hashlib.sha512(b"".join(parts)).digest(), "little")


def expand_secret(sk: bytes) -> tuple[int, bytes]:
    if len(sk) != 32:
        raise ValueError("an Ed25519 secret key has 32 bytes")
    h = hashlib.sha512(sk).digest()  # @line L1
    a = int.from_bytes(h[:32], "little")
    a &= (1 << 254) - 8  # clear the 3 low binary digits and the top one
    a |= 1 << 254  # @line L2
    return a, h[32:]


def public_key(sk: bytes) -> bytes:
    a, _ = expand_secret(sk)
    return encode(point_mul(a, B))  # @line L3


def sign(sk: bytes, msg: bytes) -> bytes:
    a, prefix = expand_secret(sk)
    pk = encode(point_mul(a, B))
    r = sha512_int(prefix, msg) % L  # @line L4
    rs = encode(point_mul(r, B))  # @line L5
    k = sha512_int(rs, pk, msg) % L  # @line L6
    s = (r + k * a) % L  # @line L7
    return rs + s.to_bytes(32, "little")  # @line L8


def verify(pk: bytes, msg: bytes, sig: bytes, cofactored: bool = True) -> bool:
    if len(sig) != 64:
        return False
    a_pt, r_pt = decode(pk), decode(sig[:32])
    s = int.from_bytes(sig[32:], "little")
    if a_pt is None or r_pt is None or s >= L:  # @line L9
        return False
    k = sha512_int(sig[:32], pk, msg) % L  # @line L10
    lhs = point_mul(s, B)
    rhs = point_add(r_pt, point_mul(k, a_pt))
    if cofactored:  # @line L11
        return point_equal(point_mul(8, lhs), point_mul(8, rhs))
    return point_equal(lhs, rhs)


# ------------------------------------------------------- small order points
def torsion_point_of_order_8() -> Point:
    """A point T with 8T = O and 4T != O, found as L times a point of the full group."""
    y = 2
    while True:
        x = recover_x(y, 0)
        if x is not None:
            t = point_mul(L, (x, y, 1, x * y % P))
            if not point_equal(point_mul(4, t), IDENTITY):
                return t
        y += 1


def sign_with_torsion_key(a: int, prefix: bytes, t: Point, msg: bytes) -> tuple[bytes, bytes]:
    """Sign as an honest signer would, but under the public key A' = aB + T.

    The signer does not know a discrete log of T. The result passes the
    cofactored check for every message and the cofactorless check only when
    8 divides k, so two verifiers can disagree on it.
    """
    pk = encode(point_add(point_mul(a, B), t))
    r = sha512_int(prefix, msg) % L
    rs = encode(point_mul(r, B))
    k = sha512_int(rs, pk, msg) % L
    s = (r + k * a) % L
    return pk, rs + s.to_bytes(32, "little")
