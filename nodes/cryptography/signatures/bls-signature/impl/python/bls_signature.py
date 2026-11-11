# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bls-signature/. The authors are listed in prov/BWP8XH.jsonl.
"""BLS signatures over a toy symmetric pairing, and the rogue key attack.

The pairing: E is y^2 = x^3 + x over F_p with p = 3 mod 4, a supersingular
curve with p + 1 points. G1 is the subgroup of prime order R. The distortion
map psi(x, y) = (-x, i y), with i^2 = -1 in F_p^2, sends G1 to a second
subgroup, and the reduced Tate pairing e(P, psi(Q))^((p^2 - 1)/R), computed
with Miller's algorithm, is a symmetric bilinear map G1 x G1 -> F_p^2.

NOT SECURE. R has 32 binary digits and p has 62, so discrete logs in G1 and
in F_p^2 are easy. Real BLS uses BLS12-381 with an asymmetric pairing and the
hash to curve of RFC 9380. The hash to G1 here is try-and-increment followed
by a multiplication by the cofactor, which is not RFC 9380 and is not
constant time. For study only.
"""

import hashlib

P = 2305843081154396467  # prime, P = C * R - 1, P = 3 mod 4
R = 2147483659  # prime order of G1
C = 1073741852  # cofactor, #E(F_p) = P + 1 = C * R

Point = tuple[int, int] | None  # None is the point at infinity


# ---------------------------------------------------------- the curve
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


# --------------------------------------------- F_p^2 = F_p[i]/(i^2 + 1)
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
    """e(a, b) = f_{R,a}(psi(b))^((p^2 - 1)/R), the reduced Tate pairing with the distortion map.

    psi(b) = (-x_b, i y_b). Vertical lines take values in F_p at psi(b), and the
    final exponent, a multiple of p - 1, sends them to 1, so they are skipped.
    """
    if a is None or b is None:
        return (1, 0)
    qx, qy = (-b[0]) % P, b[1]  # psi(b) = (qx, qy * i)
    f = (1, 0)
    t = a
    for bit in bin(R)[3:]:
        # doubling step: the tangent at t, evaluated at psi(b)
        lam = (3 * t[0] * t[0] + 1) * pow(2 * t[1], -1, P) % P
        line = ((-t[1] - lam * (qx - t[0])) % P, qy)  # y - y_t - lam (x - x_t)
        f = f2_mul(f2_mul(f, f), line)
        t = add(t, t)
        if bit == "1":
            if t is not None and t[0] == a[0]:
                t = add(t, a)  # t = -a: a vertical line, skipped
                continue
            lam = (a[1] - t[1]) * pow(a[0] - t[0], -1, P) % P
            line = ((-t[1] - lam * (qx - t[0])) % P, qy)
            f = f2_mul(f, line)
            t = add(t, a)
    return f2_pow(f, FINAL_EXP)


# ------------------------------------------------------- hash to G1
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


# ------------------------------------------------------------- BLS
def keygen(x: int) -> Point:
    """pk = g^x, written x * GEN in additive notation."""
    if not 1 <= x < R:
        raise ValueError("secret key out of range")
    return mul(x, GEN)  # @line L1


def sign(x: int, msg: bytes) -> Point:
    h = hash_to_g1(msg)  # @line L2
    return mul(x, h)  # @line L3


def verify(pk: Point, msg: bytes, sig: Point) -> bool:
    if not in_g1(sig) or not in_g1(pk):  # @line L4
        return False
    h = hash_to_g1(msg)  # @line L5
    return pairing(sig, GEN) == pairing(h, pk)  # @line L6


# ------------------------------------- aggregation on one message
def aggregate(points: list[Point]) -> Point:
    out = None
    for pt in points:
        out = add(out, pt)
    return out


def verify_same_message(pks: list[Point], msg: bytes, agg_sig: Point) -> bool:
    """Naive: e(sigma, g) = e(H(m), pk_1 + ... + pk_n). Unsafe without one of the fixes."""
    return verify(aggregate(pks), msg, agg_sig)


def rogue_key(victim_pk: Point, beta: int) -> Point:
    """pk* = g^beta / pk_victim. The attacker knows no secret key for pk*."""
    return add(mul(beta, GEN), neg(victim_pk))


# ---------------------------------------------- fix: proof of possession
def pop_prove(x: int) -> Point:
    pk = mul(x, GEN)
    return mul(x, hash_to_g1(encode(pk), b"TOY-BLS-POP"))


def pop_verify(pk: Point, proof: Point) -> bool:
    if not in_g1(pk) or not in_g1(proof):
        return False
    return pairing(proof, GEN) == pairing(hash_to_g1(encode(pk), b"TOY-BLS-POP"), pk)


def encode(pt: Point) -> bytes:
    assert pt is not None
    return pt[0].to_bytes(8, "big") + pt[1].to_bytes(8, "big")


# ---------------------------------------- fix: message augmentation
def sign_aug(x: int, msg: bytes) -> Point:
    return sign(x, encode(mul(x, GEN)) + msg)


def verify_aug_aggregate(pks: list[Point], msgs: list[bytes], agg_sig: Point) -> bool:
    """e(sigma, g) = prod e(H(pk_i || m_i), pk_i): the inputs differ even for one message."""
    if not in_g1(agg_sig) or not all(in_g1(pk) for pk in pks):
        return False
    rhs = (1, 0)
    for pk, m in zip(pks, msgs):
        rhs = f2_mul(rhs, pairing(hash_to_g1(encode(pk) + m), pk))
    return pairing(agg_sig, GEN) == rhs
