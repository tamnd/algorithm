# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/aggregate-signature/. The authors are listed in prov/YB3MDA.jsonl.
"""BGLS aggregate signatures over a toy symmetric pairing, and the rogue key attack.

The toy pairing is the reduced Tate pairing on y^2 = x^3 + x over F_p,
p = 3 mod 4, with the distortion map (x, y) -> (-x, i y), the same as on the
BLS signature page. BLS signs with sigma = x H(m) (additive notation).
aggregate() adds signatures, and aggregate_verify() checks
e(sigma, g) = prod e(H(m_i), pk_i) after it rejects repeated messages, as
in Boneh, Gentry, Lynn and Shacham. The function without that check shows
the rogue key attack with equal messages and no proof of possession.

NOT SECURE. The groups are tiny (r has 32 binary digits), the hash to the
group is try-and-increment rather than RFC 9380, and the code is not
constant time. The attack runs only against this local verifier. For study only.
"""

import hashlib

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


def keygen(x: int) -> Point:
    return mul(x, GEN)


def sign(x: int, msg: bytes) -> Point:
    return mul(x, hash_to_g1(msg))


def aggregate(sigs: list[Point]) -> Point:
    out = None
    for s in sigs:  # @line L1
        out = add(out, s)
    return out


def aggregate_verify(pks: list[Point], msgs: list[bytes], sig: Point, distinct: bool = True) -> bool:
    """BGLS AggregateVerify. distinct=False drops the check of line L2 (unsafe)."""
    if len(pks) != len(msgs) or not pks:
        return False
    if distinct and len(set(msgs)) != len(msgs):  # @line L2
        return False
    if not in_g1(sig) or not all(in_g1(pk) for pk in pks):  # @line L3
        return False
    rhs = (1, 0)
    for pk, m in zip(pks, msgs):
        rhs = f2_mul(rhs, pairing(hash_to_g1(m), pk))
    return pairing(sig, GEN) == rhs  # @line L4


def rogue_key(victim_pk: Point, beta: int) -> Point:
    """pk* = g^beta / pk_victim, a key with no known secret."""
    return add(mul(beta, GEN), neg(victim_pk))
