# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/key-compromise-impersonation/. The authors are listed in prov/0KTA6M.jsonl.
"""Key compromise impersonation (KCI) on toy key exchanges.

Eve has stolen Alice's long-term secret a. Can she make Alice accept a
session "with Bob" whose key Eve knows? Alice is the initiator; Eve plays Bob.

- Static-static DH, K = H(g^(ab), X, Y): Eve computes g^(ab) = B^a. KCI works.
- Signed ephemeral DH: Alice checks Bob's signature on (X, Y, A). Eve has
  Alice's key, not Bob's. KCI fails.
- MQV: Alice computes K = (Y * B^e)^(x + d*a). With a, y and X Eve can make
  every factor except B^(x*e) = g^(b*x*e), a Diffie-Hellman value of B and X.
  Her best direct attempt gives a different key.

The group is the subgroup of prime order q of Z_p^* for a 256-bit safe prime.
For study only. This code is not constant time, it attacks only simulated
local parties, and it must not protect real data. Use a vetted library such
as libsodium, or a FIPS 140 validated module.
"""

from __future__ import annotations

import hashlib

P = 0xC00000000000000000000000000000000000000000000000000000000000A0EB
Q = (P - 1) // 2
G = 4
HALF = (Q.bit_length() + 1) // 2  # the MQV "half length" for the d and e values


def b32(x: int) -> bytes:
    return x.to_bytes(32, "big")


def kdf(*parts: int) -> bytes:
    return hashlib.sha256(b"".join(b32(p) for p in parts)).digest()


def valid(x: int) -> bool:
    return 1 < x < P and pow(x, Q, P) == 1


# ------------------------------------------------------------ static-static DH (no KCI resistance)


def static_dh_initiator(a: int, b_pub: int, x: int, y_pub: int) -> bytes:
    """Alice: K = H(B^a, X, Y). The ephemerals only make the key fresh; they add no authentication."""
    return kdf(pow(b_pub, a, P), pow(G, x, P), y_pub)


def kci_static_dh(stolen_a: int, b_pub: int, x_pub: int, y: int) -> bytes:
    """Eve, as Bob: g^(ab) = B^a with the stolen a. She picks y herself."""
    return kdf(pow(b_pub, stolen_a, P), x_pub, pow(G, y, P))


# ------------------------------------------------------------ signed ephemeral DH (KCI resistant)


def sign(sk: int, msg: bytes) -> tuple[int, int]:
    k = int.from_bytes(hashlib.sha256(b"k" + b32(sk) + msg).digest(), "big") % Q or 1
    e = int.from_bytes(hashlib.sha256(b32(pow(G, k, P)) + msg).digest(), "big") % Q
    return e, (k + e * sk) % Q


def verify(pk: int, msg: bytes, sig: tuple[int, int]) -> bool:
    e, s = sig
    if not (0 <= e < Q and 0 <= s < Q):
        return False
    r = pow(G, s, P) * pow(pk, Q - e, P) % P
    return int.from_bytes(hashlib.sha256(b32(r) + msg).digest(), "big") % Q == e


def signed_dh_initiator(b_pub: int, x: int, y_pub: int, sig: tuple[int, int]) -> bytes | None:
    """Alice accepts only if Bob's signature on (X, Y, "A") verifies. Returns K or None."""
    x_pub = pow(G, x, P)
    if not valid(y_pub) or not verify(b_pub, b32(x_pub) + b32(y_pub) + b"A", sig):
        return None
    return kdf(pow(y_pub, x, P), x_pub, y_pub)


def kci_signed_dh(stolen_a: int, x_pub: int, y: int) -> tuple[int, tuple[int, int]]:
    """Eve's best move: she can only sign with the key she has, which is Alice's."""
    y_pub = pow(G, y, P)
    return y_pub, sign(stolen_a, b32(x_pub) + b32(y_pub) + b"A")


# ------------------------------------------------------------ MQV (KCI resistant in practice)


def avf(r: int) -> int:
    """MQV's d or e: the low HALF bits of the element, with the top bit of that range set."""
    return (r % (1 << HALF)) + (1 << HALF)


def mqv_initiator(a: int, x: int, b_pub: int, y_pub: int) -> bytes | None:
    """Alice: s_A = x + d*a mod q with d = avf(X); sigma = (Y * B^e)^(s_A) with e = avf(Y)."""
    if not (valid(y_pub) and valid(b_pub)):
        return None
    x_pub = pow(G, x, P)
    s_a = (x + avf(x_pub) * a) % Q
    sigma = pow(y_pub * pow(b_pub, avf(y_pub), P) % P, s_a, P)
    return kdf(sigma, x_pub, y_pub)


def mqv_responder(b: int, y: int, a_pub: int, x_pub: int) -> bytes:
    """Bob: s_B = y + e*b; sigma = (X * A^d)^(s_B)."""
    y_pub = pow(G, y, P)
    s_b = (y + avf(y_pub) * b) % Q
    sigma = pow(x_pub * pow(a_pub, avf(x_pub), P) % P, s_b, P)
    return kdf(sigma, x_pub, y_pub)


def kci_mqv_attempt(stolen_a: int, x_pub: int, b_pub: int, y: int) -> bytes:
    """Eve knows a, X and y. Alice's sigma = Y^x * Y^(d*a) * B^(e*x) * B^(e*d*a).

    Eve computes Y^x = X^y, Y^(d*a) and B^(e*d*a), but B^(e*x) = g^(b*x*e) is a CDH
    value of (B, X). She leaves it out; the key is then wrong.
    """
    y_pub = pow(G, y, P)
    d, e = avf(x_pub), avf(y_pub)
    known = pow(x_pub, y, P) * pow(y_pub, d * stolen_a, P) * pow(b_pub, e * d * stolen_a, P) % P
    return kdf(known, x_pub, y_pub)
