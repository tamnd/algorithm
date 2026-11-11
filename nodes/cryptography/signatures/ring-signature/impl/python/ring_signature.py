# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ring-signature/. The authors are listed in prov/6JAF6Z.jsonl.
"""The Abe-Ohkubo-Suzuki (AOS) ring signature with Schnorr keys.

Every member i has a key y_i = g^x_i in a group of prime order q. The signer
s picks the ring y_0, ..., y_{n-1}, chooses a random alpha, and closes a ring
of hash challenges:

    e_{s+1} = H(L, m, g^alpha)
    e_{i+1} = H(L, m, g^z_i * y_i^e_i)   for i = s+1, ..., s-1 (random z_i)
    z_s     = alpha - x_s * e_s mod q

so that g^z_s * y_s^e_s = g^alpha. The signature is (e_0, z_0, ..., z_{n-1}).
The verifier walks the ring once from e_0 and checks that it comes back to e_0.

The group is a toy: p = 2039 = 2q + 1, q = 1019, and g = 4 generates the
subgroup of order q. With q this small, discrete logarithms take a moment and
a random signature verifies with chance 1/q. For study only: the code is not
constant time and the parameters give no security.
"""

import hashlib
import random
import secrets
from dataclasses import dataclass

P, Q, G = 2039, 1019, 4


def h(ring: list[int], msg: bytes, point: int) -> int:
    data = b"AOS|" + b",".join(str(y).encode() for y in ring) + b"|" + msg + b"|" + str(point).encode()
    return int.from_bytes(hashlib.sha256(data).digest(), "big") % Q


def keygen(rng: random.Random | None = None) -> tuple[int, int]:
    rng = rng or secrets.SystemRandom()
    x = rng.randrange(1, Q)
    return x, pow(G, x, P)


def in_group(y: int) -> bool:
    return 1 < y < P and pow(y, Q, P) == 1


@dataclass(frozen=True)
class Signature:
    e0: int
    z: tuple[int, ...]


def sign(
    ring: list[int],
    s: int,
    x: int,
    msg: bytes,
    coins: tuple[int, list[int]] | None = None,
) -> Signature:
    """Member s of the ring signs msg with its secret key x.

    coins = (alpha, z) fixes the random choices (z[s] is ignored); the tests
    use it to show that every member can reach the same signature.
    """
    n = len(ring)
    if not 0 <= s < n or pow(G, x, P) != ring[s]:
        raise ValueError("x is not the secret key of member s")
    if coins is None:
        alpha = secrets.randbelow(Q)  # @line L1
        z = [secrets.randbelow(Q) for _ in range(n)]
    else:
        alpha, z = coins[0], list(coins[1])
    e = [0] * n
    e[(s + 1) % n] = h(ring, msg, pow(G, alpha, P))  # @line L2
    i = (s + 1) % n
    while i != s:  # @line L3
        e[(i + 1) % n] = h(ring, msg, pow(G, z[i], P) * pow(ring[i], e[i], P) % P)  # @line L4
        i = (i + 1) % n
    z[s] = (alpha - x * e[s]) % Q  # @line L5
    return Signature(e[0], tuple(z))  # @line L6


def verify(ring: list[int], msg: bytes, sig: Signature) -> bool:
    if len(sig.z) != len(ring) or not ring or not all(in_group(y) for y in ring):
        return False
    if not (0 <= sig.e0 < Q and all(0 <= zi < Q for zi in sig.z)):
        return False
    e = sig.e0
    for i, y in enumerate(ring):  # @line L7
        e = h(ring, msg, pow(G, sig.z[i], P) * pow(y, e, P) % P)  # @line L8
    return e == sig.e0  # @line L9


def coins_for(ring: list[int], msg: bytes, sig: Signature, j: int, x_j: int) -> tuple[int, list[int]]:
    """The random choices with which member j would have made exactly sig.

    Walk the ring to find e_j, then alpha = z_j + x_j * e_j. Every member has
    exactly one such choice, so all members are equally likely signers.
    """
    e = sig.e0
    for i in range(j):
        e = h(ring, msg, pow(G, sig.z[i], P) * pow(ring[i], e, P) % P)
    return (sig.z[j] + x_j * e) % Q, list(sig.z)
