# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/random-oracle-model/. The authors are listed in prov/6J2DGY.jsonl.
"""A lazily sampled random oracle, with the two powers a reduction uses: it sees
every query (extractability) and it may set answers in advance (programmability).

For study only. The code is not constant time, the group is a toy (p = 2039),
and a random oracle does not exist in the real world: a real system hashes with
SHA-256 or SHA-3 from the standard library, a FIPS 140 validated module, or
libsodium, and uses a reviewed signature library.

The demo signs Schnorr signatures with no secret key. That is the zero-knowledge
simulator from the security proof: it works only because the simulator controls
the oracle, so it does not break Schnorr signatures.
"""

import random


class LazyRandomOracle:
    """H: bytes -> range(size). Each new input gets a fresh uniform answer, chosen
    at the first query and remembered. The log lists the queries in order."""

    def __init__(self, size: int, rng: random.Random) -> None:
        self.size = size
        self._rng = rng
        self.table: dict[bytes, int] = {}
        self.log: list[bytes] = []

    def query(self, x: bytes) -> int:
        self.log.append(x)
        if x not in self.table:
            self.table[x] = self._rng.randrange(self.size)
        return self.table[x]

    def program(self, x: bytes, value: int) -> None:
        """Fix H(x) = value. Fails if H(x) was already chosen: the answer is then
        fixed, and changing it would make the oracle inconsistent."""
        if x in self.table:
            raise ValueError("oracle already defined at this point")
        if not 0 <= value < self.size:
            raise ValueError("value out of range")
        self.table[x] = value


# A toy Schnorr group: p = 2q + 1 with q prime, g = 4 of order q.
P, Q, G = 2039, 1019, 4


def _enc(r: int, msg: bytes) -> bytes:
    return r.to_bytes(2, "big") + msg


def keygen(rng: random.Random) -> tuple[int, int]:
    x = rng.randrange(1, Q)
    return x, pow(G, x, P)


def sign(h: LazyRandomOracle, x: int, msg: bytes, rng: random.Random) -> tuple[int, int]:
    k = rng.randrange(1, Q)
    r = pow(G, k, P)
    c = h.query(_enc(r, msg))
    return c, (k + c * x) % Q


def verify(h: LazyRandomOracle, y: int, msg: bytes, sig: tuple[int, int]) -> bool:
    c, s = sig
    r = pow(G, s, P) * pow(y, Q - c, P) % P  # g^s * y^(-c)
    return h.query(_enc(r, msg)) == c


def simulate_sign(h: LazyRandomOracle, y: int, msg: bytes, rng: random.Random) -> tuple[int, int]:
    """Make a valid signature with no secret key: pick c and s first, set
    R = g^s * y^(-c), then program H(R, msg) = c. Retries if (R, msg) was already queried."""
    while True:
        c, s = rng.randrange(Q), rng.randrange(Q)
        r = pow(G, s, P) * pow(y, Q - c, P) % P
        try:
            h.program(_enc(r, msg), c)
        except ValueError:
            continue
        return c, s
