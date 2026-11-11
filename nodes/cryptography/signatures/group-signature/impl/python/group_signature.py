# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/group-signature/. The authors are listed in prov/852SRK.jsonl.
"""A simple group signature with linear size. A toy, not a practical scheme.

This is not BMW, BBS or any standard scheme. It is the textbook idea behind
them, in the simplest form that has all three parts:

- The group public key is the list of member keys y_j = g^x_j and the
  opener's key Y = g^x_o. Each member makes its own x_j, so the opener cannot
  sign for a member.
- Member i signs m by encrypting y_i to the opener with ElGamal,
  (C1, C2) = (g^rho, y_i * Y^rho), and by a Fiat-Shamir OR proof over all j
  that it knows (x_j, rho) with y_j = g^x_j, C1 = g^rho and
  C2 / y_j = Y^rho. The proof shows that the ciphertext holds the key of a
  member who signed, without saying which.
- The opener decrypts y = C2 / C1^x_o and proves with a Chaum-Pedersen proof
  that it decrypted correctly, so a judge can check the opening.

The signature has 3n + 2 numbers, so it grows with the group. Real schemes
(BMW 2003, BBS 2004) have constant size: members get certificates from a
manager and prove knowledge of a certificate instead of listing all keys.

The group is a toy: p = 2039 = 2q + 1, q = 1019, and g = 4 generates the
subgroup of order q. For study only: the code is not constant time and the
parameters give no security.
"""

import hashlib
import random
import secrets
from dataclasses import dataclass

P, Q, G = 2039, 1019, 4


def _h(*parts: object) -> int:
    data = "|".join(str(x) for x in parts).encode()
    return int.from_bytes(hashlib.sha256(data).digest(), "big") % Q


def keygen(rng: random.Random | None = None) -> tuple[int, int]:
    rng = rng or secrets.SystemRandom()
    x = rng.randrange(1, Q)
    return x, pow(G, x, P)


def in_group(y: int) -> bool:
    return 1 < y < P and pow(y, Q, P) == 1


@dataclass(frozen=True)
class GroupKey:
    members: tuple[int, ...]  # y_0, ..., y_{n-1}
    opener: int  # Y = g^x_o


@dataclass(frozen=True)
class Signature:
    C1: int
    C2: int
    c: tuple[int, ...]
    u: tuple[int, ...]
    v: tuple[int, ...]


@dataclass(frozen=True)
class Opening:
    index: int
    y: int
    A: int
    B: int
    z: int


def _commitments(gk: GroupKey, C1: int, C2: int, j: int, c: int, u: int, v: int) -> tuple[int, int, int]:
    yj = gk.members[j]
    ratio = C2 * pow(yj, -1, P) % P
    return (
        pow(G, u, P) * pow(yj, c, P) % P,
        pow(G, v, P) * pow(C1, c, P) % P,
        pow(gk.opener, v, P) * pow(ratio, c, P) % P,
    )


def sign(gk: GroupKey, i: int, x_i: int, msg: bytes, rng: random.Random | None = None) -> Signature:
    rng = rng or secrets.SystemRandom()
    n = len(gk.members)
    if not 0 <= i < n or pow(G, x_i, P) != gk.members[i]:
        raise ValueError("x_i is not the key of member i")
    rho = rng.randrange(1, Q)  # @line L1
    C1, C2 = pow(G, rho, P), gk.members[i] * pow(gk.opener, rho, P) % P
    c, u, v = [0] * n, [0] * n, [0] * n
    T: list[tuple[int, int, int]] = [(0, 0, 0)] * n
    for j in range(n):
        if j != i:
            c[j], u[j], v[j] = rng.randrange(Q), rng.randrange(Q), rng.randrange(Q)  # @line L2
            T[j] = _commitments(gk, C1, C2, j, c[j], u[j], v[j])
    a, b = rng.randrange(Q), rng.randrange(Q)  # @line L3
    T[i] = (pow(G, a, P), pow(G, b, P), pow(gk.opener, b, P))
    total = _h("GS", gk.members, gk.opener, msg.hex(), C1, C2, T)  # @line L4
    c[i] = (total - sum(c[j] for j in range(n) if j != i)) % Q
    u[i] = (a - c[i] * x_i) % Q  # @line L5
    v[i] = (b - c[i] * rho) % Q
    return Signature(C1, C2, tuple(c), tuple(u), tuple(v))  # @line L6


def verify(gk: GroupKey, msg: bytes, sig: Signature) -> bool:
    n = len(gk.members)
    if not (n and in_group(gk.opener) and all(in_group(y) for y in gk.members)):
        return False
    if not (in_group(sig.C1) and in_group(sig.C2) and len(sig.c) == len(sig.u) == len(sig.v) == n):
        return False
    T = [_commitments(gk, sig.C1, sig.C2, j, sig.c[j], sig.u[j], sig.v[j]) for j in range(n)]  # @line L7
    return sum(sig.c) % Q == _h("GS", gk.members, gk.opener, msg.hex(), sig.C1, sig.C2, T)  # @line L8


def open_signature(gk: GroupKey, x_o: int, msg: bytes, sig: Signature, rng: random.Random | None = None) -> Opening:
    """The opener finds the signer and proves that it decrypted correctly."""
    rng = rng or secrets.SystemRandom()
    if not verify(gk, msg, sig):
        raise ValueError("invalid signature")
    y = sig.C2 * pow(sig.C1, -x_o, P) % P  # @line L9
    if y not in gk.members:
        raise ValueError("the decryption is not a member key")
    w = rng.randrange(Q)  # @line L10
    A, B = pow(G, w, P), pow(sig.C1, w, P)
    e = _h("OPEN", gk.opener, sig.C1, sig.C2, y, A, B)
    return Opening(gk.members.index(y), y, A, B, (w + e * x_o) % Q)


def judge(gk: GroupKey, msg: bytes, sig: Signature, op: Opening) -> bool:
    """Anyone can check that op names the member whose key sig encrypts."""
    if not verify(gk, msg, sig) or not (0 <= op.index < len(gk.members)) or gk.members[op.index] != op.y:
        return False
    e = _h("OPEN", gk.opener, sig.C1, sig.C2, op.y, op.A, op.B)
    ratio = sig.C2 * pow(op.y, -1, P) % P
    return (
        pow(G, op.z, P) == op.A * pow(gk.opener, e, P) % P
        and pow(sig.C1, op.z, P) == op.B * pow(ratio, e, P) % P
    )
