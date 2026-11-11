# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hash-and-sign-paradigm/. The authors are listed in prov/R0VXSE.jsonl.
"""The hash-and-sign template with a toy RSA signer, and Yuval's birthday
attack (1979) that turns one collision of the hash into a forgery.

The signer signs H(M) with textbook RSA. With a hash cut to 24 binary digits,
two sets of about 2^14 variants of a harmless and a harmful message contain a
pair with equal hashes. The attacker asks for a signature on the harmless one,
and that signature is also valid on the harmful one.

The page is about the paradigm, not about the hash, so the hash is SHA-256
from hashlib, cut short on purpose to make collisions cheap.

For study only. The code is not constant time, the attack runs only on a toy
hash and a toy key against a local signer, and nothing here may protect real
data. Use RSA-PSS or Ed25519 from the pyca/cryptography library or from a
FIPS 140 validated module.
"""

import hashlib
from itertools import product
from typing import Callable, Dict, Iterator, List, Optional, Tuple

# A toy RSA key: two known primes (the 10000th and the 100000th prime).
P, Q, E = 104729, 1299709, 65537
N = P * Q
D = pow(E, -1, (P - 1) * (Q - 1))


def toy_hash(message: bytes, bits: int = 24) -> int:
    """SHA-256 cut to its leftmost `bits` binary digits. Far too short for real use."""
    return int.from_bytes(hashlib.sha256(message).digest(), "big") >> (256 - bits)


def keygen() -> Tuple[int, int]:
    """The base scheme is textbook RSA on the fixed toy key; the hash has no key."""
    return N, E  # @line L1


def sign(message: bytes, hash_fn: Callable[[bytes], int] = toy_hash) -> int:
    r = b""  # @line L2 (this instance uses no random value)
    h = hash_fn(r + message)  # @line L3
    sigma = pow(h, D, N)  # @line L4
    return sigma  # @line L5


def verify(message: bytes, s: int, hash_fn: Callable[[bytes], int] = toy_hash) -> bool:
    h = hash_fn(message)  # @line L6
    return 0 <= s < N and pow(s, E, N) == h  # @line L7


class SigningOracle:
    """Signs what it is given and records the messages."""

    def __init__(self) -> None:
        self.queries: List[bytes] = []

    def __call__(self, message: bytes) -> int:
        self.queries.append(message)
        return sign(message)


def variants(words: List[str], choices: int) -> Iterator[bytes]:
    """2^choices texts with the same meaning: after each of the first `choices`
    words put one space or two."""
    for bits in product((0, 1), repeat=choices):
        parts = []
        for i, w in enumerate(words):
            parts.append(w)
            if i < len(words) - 1:
                parts.append("  " if i < choices and bits[i] else " ")
        yield "".join(parts).encode()


def yuval_collision(fair: Iterator[bytes], unfair: Iterator[bytes],
                    hash_fn: Callable[[bytes], int] = toy_hash) -> Optional[Tuple[bytes, bytes]]:
    """Store the hashes of the harmless variants, then look up each harmful one."""
    table: Dict[int, bytes] = {}
    for m in fair:
        table.setdefault(hash_fn(m), m)
    for m in unfair:
        hit = table.get(hash_fn(m))
        if hit is not None:
            return hit, m
    return None


def collision_forgery(oracle: Callable[[bytes], int], fair: bytes, unfair: bytes) -> Tuple[bytes, int]:
    """One query on the harmless text gives a signature on the harmful one."""
    return unfair, oracle(fair)
