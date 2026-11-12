# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/multi-probe-consistent-hashing/. The authors are listed in prov/JQ763C.jsonl.

"""Multi-probe consistent hashing of Appleton and O'Reilly (2015).

Each node has one point on a ring of size 2^64. A key is hashed k times
with k different seeds. For each probe point we find the next node point
clockwise and its clockwise distance; the key goes to the node with the
smallest distance over all probes.

The hash is BLAKE2b with the probe number as salt, so that the k probe
functions are different but fixed.
"""

import bisect
import hashlib
from collections.abc import Iterable

RING = 1 << 64


def point(data: str, seed: int) -> int:
    """A 64-bit ring position of data under the hash function number seed."""
    salt = seed.to_bytes(8, "big")
    d = hashlib.blake2b(data.encode(), digest_size=8, salt=salt).digest()
    return int.from_bytes(d, "big")


class MultiProbeRing:
    """A ring with one point per node and k probes per key."""

    def __init__(self, nodes: Iterable[str], k: int = 21) -> None:
        if k < 1:
            raise ValueError("k must be at least 1")
        self.k = k
        self.points: list[int] = []
        self.owner: dict[int, str] = {}
        for n in nodes:
            self.add(n)

    def add(self, node: str) -> None:
        p = point(node, 0)
        if p in self.owner:
            raise ValueError("two nodes hash to the same point")
        bisect.insort(self.points, p)
        self.owner[p] = node

    def remove(self, node: str) -> None:
        p = point(node, 0)
        i = bisect.bisect_left(self.points, p)
        if i == len(self.points) or self.points[i] != p:
            raise KeyError(node)
        del self.points[i]
        del self.owner[p]

    def lookup(self, key: str) -> str:
        if not self.points:
            raise ValueError("the ring is empty")
        best_dist = RING  # @line L1
        best = None
        for i in range(self.k):  # @line L2
            q = point(key, i + 1)  # @line L3
            j = bisect.bisect_left(self.points, q)  # @line L4
            if j == len(self.points):
                j = 0  # wrap around the ring
            p = self.points[j]
            d = (p - q) % RING  # @line L5
            if d < best_dist:  # @line L6
                best_dist, best = d, p  # @line L7
        return self.owner[best]  # @line L8


def loads(ring: MultiProbeRing, keys: Iterable[str]) -> dict[str, int]:
    """The number of keys on each node."""
    out = {ring.owner[p]: 0 for p in ring.points}
    for key in keys:
        out[ring.lookup(key)] += 1
    return out


def peak_to_mean(counts: dict[str, int]) -> float:
    """The largest load divided by the mean load."""
    return max(counts.values()) * len(counts) / sum(counts.values())


def arcs(ring: MultiProbeRing) -> dict[str, float]:
    """For each node, the length of the arc that ends at its point, as a fraction of the ring."""
    pts = ring.points
    return {ring.owner[p]: ((p - pts[i - 1]) % RING or RING) / RING for i, p in enumerate(pts)}


def exact_shares(arc: dict[str, float], k: int) -> dict[str, float]:
    """The exact fraction of keys on each node when the k probes are independent and uniform.

    One probe has distance more than t to its next node with probability
    G(t) = sum of max(a_j - t, 0). Node i wins when one probe lands in its arc
    at distance t and the other k - 1 probes have distance more than t, so the
    share of node i is k times the integral of G(t)^(k-1) for t from 0 to a_i.
    G is linear between the sorted arc lengths, so each piece integrates exactly.
    """
    names = sorted(arc, key=arc.get)
    lengths = [arc[x] for x in names]
    n = len(lengths)
    total = sum(lengths)
    out: dict[str, float] = {}
    acc = 0.0  # k * integral of G^(k-1) from 0 to the current breakpoint
    t0, g0 = 0.0, total
    for idx, name in enumerate(names):
        t1 = lengths[idx]
        c = n - idx  # arcs longer than t on the open piece (t0, t1)
        g1 = g0 - c * (t1 - t0)
        if t1 > t0:
            acc += (g0 ** k - g1 ** k) / c
        out[name] = acc
        t0, g0 = t1, g1
    return out
