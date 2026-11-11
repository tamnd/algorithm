# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ecdsa/. The authors are listed in prov/QNKB84.jsonl.
"""ECDSA on the NIST curve P-256, with the low-s rule and public key recovery.

The steps follow FIPS 186-5 Section 6.4 and SEC 1 version 2.0 Sections 4.1.3
(signing), 4.1.4 (verification) and 4.1.6 (public key recovery). The curve
arithmetic is written here from the curve equation y^2 = x^3 - 3x + b. SHA-256
comes from hashlib: the page is about the signature, not the hash. The nonce k
is an argument, so that the tests can use the k of RFC 6979 Appendix A.2.5;
sign() draws a uniform k when none is given.

For study only. This code is not constant time, it branches on secret data,
and it must not be used to protect real data. Use a FIPS 140 validated module,
OpenSSL, BoringSSL or the platform library.
"""

import hashlib
import secrets

# NIST P-256 (FIPS 186-5 and SP 800-186), also called secp256r1.
P = 0xFFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFF
A = P - 3
B = 0x5AC635D8AA3A93E7B3EBBD55769886BC651D06B0CC53B0F63BCE3C3E27D2604B
N = 0xFFFFFFFF00000000FFFFFFFFFFFFFFFFBCE6FAADA7179E84F3B9CAC2FC632551
G = (
    0x6B17D1F2E12C4247F8BCE6E563A440F277037D812DEB33A0F4A13945D898C296,
    0x4FE342E2FE1A7F9B8EE7EB4A7C0F9E162BCE33576B315ECECBB6406837BF51F5,
)

Point = tuple[int, int] | None  # None is the point at infinity


def on_curve(pt: Point) -> bool:
    if pt is None:
        return False
    x, y = pt
    return 0 <= x < P and 0 <= y < P and (y * y - x * x * x - A * x - B) % P == 0


def point_add(a: Point, b: Point) -> Point:
    if a is None:
        return b
    if b is None:
        return a
    if a[0] == b[0] and (a[1] + b[1]) % P == 0:
        return None
    if a == b:
        lam = (3 * a[0] * a[0] + A) * pow(2 * a[1], -1, P) % P
    else:
        lam = (b[1] - a[1]) * pow(b[0] - a[0], -1, P) % P
    x3 = (lam * lam - a[0] - b[0]) % P
    return x3, (lam * (a[0] - x3) - a[1]) % P


def point_mul(a: Point, k: int) -> Point:
    result = None
    for bit in bin(k)[2:] if k > 0 else "":
        result = point_add(result, result)
        if bit == "1":
            result = point_add(result, a)
    return result


def hash_to_int(msg: bytes) -> int:
    """z = the leftmost 256 binary digits of SHA-256(m); n also has 256 digits."""
    return int.from_bytes(hashlib.sha256(msg).digest(), "big")


def public_key(d: int) -> Point:
    if not 1 <= d < N:
        raise ValueError("private key out of range")
    return point_mul(G, d)


def sign(d: int, msg: bytes, k: int | None = None, low_s: bool = False) -> tuple[int, int, int]:
    """Return (r, s, v), where v is the recovery id. k must be fresh, secret and uniform."""
    if not 1 <= d < N:
        raise ValueError("private key out of range")
    z = hash_to_int(msg)  # @line L1
    while True:
        kk = k if k is not None else secrets.randbelow(N - 1) + 1  # @line L2
        r_pt = point_mul(G, kk)  # @line L3
        assert r_pt is not None
        r = r_pt[0] % N  # @line L4
        s = pow(kk, -1, N) * (z + r * d) % N  # @line L5
        if r != 0 and s != 0:  # @line L6
            break
        if k is not None:
            raise ValueError("this k gives r = 0 or s = 0")
    v = (r_pt[1] & 1) | (2 if r_pt[0] >= N else 0)
    if low_s and s > N // 2:
        s, v = N - s, v ^ 1  # s -> n - s is the signature of -k, whose point has the other y
    return r, s, v  # @line L7


def verify(q_pt: Point, msg: bytes, r: int, s: int) -> bool:
    """ECDSA verification. It also checks the ranges, which CVE-2022-21449 skipped."""
    if not on_curve(q_pt):
        return False
    if not (1 <= r < N and 1 <= s < N):  # @line L8
        return False
    z = hash_to_int(msg)  # @line L9
    w = pow(s, -1, N)
    u1, u2 = z * w % N, r * w % N  # @line L10
    x_pt = point_add(point_mul(G, u1), point_mul(q_pt, u2))  # @line L11
    if x_pt is None:  # @line L12
        return False
    return x_pt[0] % N == r  # @line L13


def is_low_s(s: int) -> bool:
    return 1 <= s <= N // 2


def lift_x(x: int, odd: int) -> Point:
    """The curve point with this x and the given parity of y, or None."""
    if x >= P:
        return None
    c = (x * x * x + A * x + B) % P
    y = pow(c, (P + 1) // 4, P)  # p = 3 mod 4
    if y * y % P != c:
        return None
    return (x, y) if y & 1 == odd else (x, P - y)


def recover_public_key(msg: bytes, r: int, s: int, v: int) -> Point:
    """SEC 1 Section 4.1.6: Q = r^(-1) (s R - z G), where R is chosen by v."""
    if not (1 <= r < N and 1 <= s < N and 0 <= v <= 3):
        return None
    r_pt = lift_x(r + (v >> 1) * N, v & 1)
    if r_pt is None:
        return None
    z = hash_to_int(msg)
    sr = point_mul(r_pt, s)
    zg = point_mul(G, (-z) % N)
    return point_mul(point_add(sr, zg), pow(r, -1, N))
