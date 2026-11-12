# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rendezvous-hashing/. The authors are listed in prov/135CB9.jsonl.

"""Rendezvous (highest random weight) hashing, plain and weighted.

The score h(key, server) is the first 8 bytes of BLAKE2b over the two names
with a separator byte, read as an unsigned 64-bit integer. Any hash with
outputs that look independent and uniform works; this one is in the standard
library and gives the same value on every run.
"""

import hashlib
import math
from collections.abc import Iterable, Mapping

def score(key: str, server: str) -> int:
    """The 64-bit hash of the pair (key, server)."""
    data = key.encode() + b"\x00" + server.encode()
    return int.from_bytes(hashlib.blake2b(data, digest_size=8).digest(), "big")


def hrw(key: str, servers: Iterable[str]) -> str:
    """Return the server with the highest score for key.

    Ties of the 64-bit score are broken by the larger server name, so the
    result does not depend on the order of the servers.
    """
    best = None  # @line L1
    best_score = -1
    for s in servers:  # @line L2
        v = score(key, s)  # @line L3
        if v > best_score or (v == best_score and best is not None and s > best):  # @line L4
            best, best_score = s, v  # @line L5
    if best is None:
        raise ValueError("the set of servers is empty")
    return best  # @line L6


def unit(v: int) -> float:
    """Map a 64-bit integer to a number strictly between 0 and 1.

    The top 52 bits plus one half fit exactly in a double, so the result is
    never 0 and never 1, and ln(u) is never 0.
    """
    return ((v >> 12) + 0.5) / (1 << 52)


def weighted_score(u: float, w: float) -> float:
    """The logarithmic score -w / ln(u) for u in (0, 1) and a weight w > 0."""
    return -w / math.log(u)


def weighted_hrw(key: str, weights: Mapping[str, float]) -> str:
    """Weighted HRW: the server with the highest -w / ln(u(key, server))."""
    best = None
    best_score = -math.inf
    for s, w in weights.items():
        if w <= 0:
            continue
        v = weighted_score(unit(score(key, s)), w)
        if v > best_score or (v == best_score and best is not None and s > best):
            best, best_score = s, v
    if best is None:
        raise ValueError("no server has a positive weight")
    return best


def top_r(key: str, servers: Iterable[str], r: int) -> list[str]:
    """The r servers with the highest scores, best first (for r replicas)."""
    ranked = sorted(servers, key=lambda s: (score(key, s), s), reverse=True)
    return ranked[:r]
