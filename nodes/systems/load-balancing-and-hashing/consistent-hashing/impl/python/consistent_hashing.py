# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/consistent-hashing/. The authors are listed in prov/DAQ627.jsonl.

"""Consistent hashing on a ring of 2**64 positions.

Each server gets v points on the ring, at h(server, r) for r = 0 .. v - 1.
A key goes to the owner of the first point at or after h(key), wrapping
around from the end of the ring to the start. mod_hash is the scheme that
consistent hashing replaces.
"""

import bisect
import hashlib
from typing import Hashable, Iterable, Sequence

RING = 1 << 64


def h(data: str) -> int:
    """A 64-bit position on the ring from BLAKE2b."""
    return int.from_bytes(hashlib.blake2b(data.encode(), digest_size=8).digest(), "big")


class ConsistentHash:
    def __init__(self, servers: Iterable[str] = (), v: int = 1) -> None:
        if v < 1:
            raise ValueError("v must be at least 1")
        self.v = v
        self.pos: list[int] = []  # sorted positions of all points
        self.owner: list[str] = []  # owner[i] is the server of point pos[i]
        self.servers: set[str] = set()
        for s in servers:
            self.add(s)

    def points_of(self, server: str) -> list[int]:
        return [h(f"{server}#{r}") for r in range(self.v)]

    def add(self, server: str) -> None:
        if server in self.servers:
            raise ValueError(f"server {server!r} is already on the ring")
        self.servers.add(server)
        for p in self.points_of(server):  # @line L5
            i = bisect.bisect_left(self.pos, p)
            if i < len(self.pos) and self.pos[i] == p:
                raise ValueError("hash collision of two points")
            self.pos.insert(i, p)  # @line L6
            self.owner.insert(i, server)

    def remove(self, server: str) -> None:
        self.servers.remove(server)
        for p in self.points_of(server):  # @line L7
            i = bisect.bisect_left(self.pos, p)
            del self.pos[i]  # @line L8
            del self.owner[i]

    def lookup(self, key: str) -> str:
        if not self.pos:
            raise LookupError("no servers")
        x = h(key)  # @line L1
        i = bisect.bisect_left(self.pos, x)  # @line L2
        if i == len(self.pos):  # @line L3
            i = 0
        return self.owner[i]  # @line L4

    def shares(self) -> dict[str, float]:
        """The fraction of the ring that each server owns."""
        out = {s: 0.0 for s in self.servers}
        n = len(self.pos)
        for i in range(n):
            # point i owns the arc (pos[i - 1], pos[i]], with wrap-around for i = 0
            prev = self.pos[i - 1] if i > 0 else self.pos[-1] - RING
            out[self.owner[i]] += (self.pos[i] - prev) / RING
        return out


def mod_hash(key: str, servers: Sequence[str]) -> str:
    """The scheme that consistent hashing replaces: server number h(key) mod n."""
    return servers[h(key) % len(servers)]


def assignment(keys: Iterable[str], lookup) -> dict[str, Hashable]:
    return {k: lookup(k) for k in keys}


def moved_fraction(before: dict, after: dict) -> float:
    return sum(before[k] != after[k] for k in before) / len(before)
