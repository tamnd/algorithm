# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/signcryption/. The authors are listed in prov/G5XJ7C.jsonl.
"""Zheng's signcryption (Crypto 1997), in its SDSS1 and SDSS2 forms.

Alice (x_a, y_a = g^x_a) sends m to Bob (x_b, y_b = g^x_b):

    signcrypt:    x random, K = y_b^x, (k1, k2) = H(K)
                  c = E_k1(m),  r = KH_k2(m)
                  s = x / (r + x_a)    (SDSS1)   or   x / (1 + x_a r)   (SDSS2)
    unsigncrypt:  K = (y_a g^r)^(s x_b)  (SDSS1)  or  (g y_a^r)^(s x_b)  (SDSS2)
                  m = D_k1(c), accept if KH_k2(m) = r

Here H is SHA-256, KH is HMAC-SHA-256 reduced modulo q, and E is a stream
cipher whose key stream is SHA-256(k1 || counter). The tag r is reduced
modulo q because it is used as an exponent; with the toy q it has only about
ten bits.

The group is a toy: p = 2039 = 2q + 1, q = 1019, and g = 4 generates the
subgroup of order q. For study only: the code is not constant time, the
parameters give no security, and the stream cipher is a teaching device.
"""

import hashlib
import hmac
import random
import secrets
from dataclasses import dataclass

P, Q, G = 2039, 1019, 4


def keygen(rng: random.Random | None = None) -> tuple[int, int]:
    rng = rng or secrets.SystemRandom()
    x = rng.randrange(1, Q)
    return x, pow(G, x, P)


def in_group(y: int) -> bool:
    return 1 < y < P and pow(y, Q, P) == 1


def split_key(K: int) -> tuple[bytes, bytes]:
    d = hashlib.sha512(b"SIGNCRYPT-KEY|%d" % K).digest()
    return d[:32], d[32:]


def stream_xor(k1: bytes, data: bytes) -> bytes:
    out = bytearray()
    for i in range(0, len(data), 32):
        block = hashlib.sha256(k1 + i.to_bytes(8, "big")).digest()
        out += bytes(a ^ b for a, b in zip(data[i : i + 32], block))
    return bytes(out)


def tag(k2: bytes, msg: bytes) -> int:
    return int.from_bytes(hmac.new(k2, msg, hashlib.sha256).digest(), "big") % Q


@dataclass(frozen=True)
class Signcryptext:
    c: bytes
    r: int
    s: int


def signcrypt(x_a: int, y_b: int, msg: bytes, variant: int = 1, rng: random.Random | None = None) -> Signcryptext:
    if variant not in (1, 2):
        raise ValueError("variant is 1 (SDSS1) or 2 (SDSS2)")
    rng = rng or secrets.SystemRandom()
    while True:
        x = rng.randrange(1, Q)  # @line L1
        k1, k2 = split_key(pow(y_b, x, P))  # @line L2
        c = stream_xor(k1, msg)  # @line L3
        r = tag(k2, msg)  # @line L4
        denom = (r + x_a) % Q if variant == 1 else (1 + x_a * r) % Q
        if denom != 0:  # probability 1/q of a retry
            return Signcryptext(c, r, x * pow(denom, -1, Q) % Q)  # @line L5


def unsigncrypt(y_a: int, x_b: int, ct: Signcryptext, variant: int = 1) -> bytes | None:
    """Bob recovers m and checks it came from Alice; None means reject."""
    if not in_group(y_a) or not (0 <= ct.r < Q and 0 < ct.s < Q):
        return None
    base = y_a * pow(G, ct.r, P) % P if variant == 1 else G * pow(y_a, ct.r, P) % P
    K = pow(base, ct.s * x_b % Q, P)  # @line L6
    k1, k2 = split_key(K)
    msg = stream_xor(k1, ct.c)  # @line L7
    return msg if hmac.compare_digest(tag(k2, msg).to_bytes(2, "big"), ct.r.to_bytes(2, "big")) else None  # @line L8
