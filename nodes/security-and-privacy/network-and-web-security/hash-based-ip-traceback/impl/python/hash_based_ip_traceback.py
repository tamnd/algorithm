# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hash-based-ip-traceback/. The authors are listed in prov/3RR23Q.jsonl.

"""Single-packet traceback with per-router Bloom filters of packet digests.

A synthetic model of SPIE (Snoeren et al., SIGCOMM 2001). Packets are tuples of
abstract fields with documentation addresses; routers are names in a small
graph given as an adjacency dict. No packet is built and no network is touched.
"""

from collections import deque
from hashlib import blake2b
from typing import Hashable, Mapping

Node = Hashable
# (source, destination, identification, ttl, payload)
Packet = tuple[str, str, int, int, bytes]


def invariant(x: Packet) -> bytes:
    """The fields that no router changes: the TTL is left out, and only the
    first 8 bytes of the payload are kept, as in Section 4 of Snoeren et al.
    Cost: O(1).
    """
    src, dst, ident, _ttl, payload = x
    return f"{src}|{dst}|{ident}|".encode() + payload[:8]


class DigestTable:
    """A Bloom filter of m bits with k keyed hash functions (one router, one time window)."""

    def __init__(self, m: int, k: int, key: bytes) -> None:
        """Precondition: m >= 1, 1 <= k <= 255, len(key) <= 64. Cost: O(m)."""
        self.m = m
        self.k = k
        self.key = key
        self.bits = bytearray(m)

    def indices(self, x: Packet) -> list[int]:
        """The k bit positions of x. Cost: O(k)."""
        data = invariant(x)
        return [
            int.from_bytes(blake2b(bytes([i]) + data, key=self.key, digest_size=8).digest(), "big") % self.m
            for i in range(self.k)
        ]

    def insert(self, x: Packet) -> None:
        """Record that this router forwarded x. Cost: O(k)."""
        for j in self.indices(x):  # @line L1
            self.bits[j] = 1  # @line L2

    def query(self, x: Packet) -> bool:
        """True if x may have been forwarded; never False for a recorded x. Cost: O(k)."""
        return all(self.bits[j] for j in self.indices(x))  # @line L3


def forward(path: list[Node], x: Packet, tables: Mapping[Node, DigestTable]) -> None:
    """Every router on path records x as it forwards it. Cost: O(k len(path))."""
    for r in path:
        tables[r].insert(x)


def trace(graph: Mapping[Node, list[Node]], v: Node, x: Packet, tables: Mapping[Node, "DigestTable | set"]) -> set[Node]:
    """Reverse-path flooding from the victim v (Section 5.4 of Snoeren et al.).

    A neighbor is asked only by a node that answered yes (or by v), and it is
    asked once. tables maps each router to a DigestTable or, for the exact
    oracle, to a set of packets. Returns the routers that answered yes.
    Cost: O(k (V + E)) for a graph with V nodes and E edges.
    """
    found: set[Node] = set()  # @line L4
    seen = {v}
    queue = deque([v])
    while queue:  # @line L5
        u = queue.popleft()  # @line L6
        for r in graph[u]:  # @line L7
            if r in seen or r not in tables:
                continue
            seen.add(r)
            t = tables[r]
            if (x in t) if isinstance(t, set) else t.query(x):  # @line L8
                found.add(r)  # @line L9
                queue.append(r)
    return found  # @line L10


def false_positive_rate(m: int, k: int, n: int) -> float:
    """(1 - (1 - 1/m)^(k n))^k: the chance that a packet not inserted passes the
    query after n insertions, for independent uniform hash functions.
    """
    return (1 - (1 - 1 / m) ** (k * n)) ** k
