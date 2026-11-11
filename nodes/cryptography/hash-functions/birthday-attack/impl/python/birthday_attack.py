# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/birthday-attack/. The authors are listed in prov/4ZQ3BQ.jsonl.
"""Birthday attack: hash distinct inputs until two digests match.

For study only. The code is not constant time, and it is meant to run only on
toy targets, such as SHA-256 cut down to 24 to 32 bits. Do not use a truncated
hash to protect real data; use SHA-256 or SHA-3 at full length from the
standard library, a FIPS 140 validated module, or libsodium.

Cost: about 1.25 * 2^(n/2) hash calls on average for an n-bit random-looking
hash, and the same number of table entries of memory.
"""

import math
from typing import Callable

Hash = Callable[[bytes], int]


def birthday_attack(h: Hash, prefix: bytes = b"", max_queries: int = 1 << 24) -> tuple[bytes, bytes, int]:
    """Return (x1, x2, q): two distinct inputs with h(x1) == h(x2), and q hash calls.

    The inputs are prefix + an 8-byte counter, so they are distinct by
    construction. Raises RuntimeError after max_queries calls with no match.
    """
    table: dict[int, bytes] = {}  # @line L1
    for i in range(max_queries):  # @line L2
        x = prefix + i.to_bytes(8, "big")  # @line L3
        y = h(x)  # @line L4
        if y in table:  # @line L5
            return table[y], x, i + 1  # @line L5
        table[y] = x  # @line L6
    raise RuntimeError("no collision within max_queries")


def no_collision_probability(q: int, n: int) -> float:
    """Exact Pr[no collision] for q independent uniform values in a set of size 2^n."""
    big_n = float(1 << n)
    p = 1.0
    for i in range(1, q):
        p *= 1.0 - i / big_n
        if p == 0.0:
            break
    return p


def collision_probability(q: int, n: int) -> float:
    """Exact Pr[at least one collision] for q uniform values in a set of size 2^n."""
    return 1.0 - no_collision_probability(q, n)


def upper_bound(q: int, n: int) -> float:
    """The union bound q(q-1)/2^(n+1)."""
    return q * (q - 1) / float(1 << (n + 1))


def lower_bound(q: int, n: int) -> float:
    """The bound 1 - exp(-q(q-1)/2^(n+1)), which the exact probability always meets."""
    return 1.0 - math.exp(-q * (q - 1) / float(1 << (n + 1)))


def queries_for(p: float, n: int) -> float:
    """The q with 1 - exp(-q^2/2^(n+1)) = p, that is q = sqrt(2 ln(1/(1-p))) * 2^(n/2)."""
    return math.sqrt(2.0 * math.log(1.0 / (1.0 - p))) * 2.0 ** (n / 2)
