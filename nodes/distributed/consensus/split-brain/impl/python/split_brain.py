# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/split-brain/. The authors are listed in prov/Z2JAHA.jsonl.

"""Leases with fencing tokens, and the stale writes they stop.

A lock service grants a lease for a fixed time, with a token that grows by
one at each grant. A storage service accepts a write only if its token is at
least the largest token it has seen. A client can pause (a garbage collection
pause, a stopped virtual machine) or have a clock that runs wrong, so it can
believe that it holds the lease after the lease has expired. That is split
brain: two clients act as the holder. The tokens make the storage refuse the
older one.

A seeded simulator runs clients with random pauses and clock errors, with and
without fencing, and records the writes that the storage accepts.
"""

from __future__ import annotations

import random
from typing import Optional


class LockService:
    """Grants one lease at a time. Time is the lock service's own clock."""

    def __init__(self, ttl: int) -> None:
        self.ttl = ttl
        self.token = 0
        self.holder: Optional[int] = None
        self.expires = -1

    def acquire(self, client: int, now: int) -> Optional[tuple[int, int]]:
        if self.holder is not None and now < self.expires and self.holder != client:
            return None
        self.token += 1  # @line L1
        self.holder, self.expires = client, now + self.ttl
        return self.token, self.expires


class Storage:
    def __init__(self, fencing: bool = True) -> None:
        self.fencing = fencing
        self.max_token = 0
        self.accepted: list[tuple[int, int, object]] = []  # (token, client, value)

    def write(self, token: int, client: int, value: object) -> bool:
        if self.fencing and token < self.max_token:
            return False  # @line L2
        self.max_token = max(self.max_token, token)  # @line L3
        self.accepted.append((token, client, value))
        return True


class Client:
    def __init__(self, cid: int, skew: int) -> None:
        self.cid, self.skew = cid, skew  # the client's clock reads true time + skew
        self.lease: Optional[tuple[int, int]] = None  # (token, expiry in lock service time)
        self.paused_until = 0
        self.writes = 0

    def believes_holder(self, now: int) -> bool:
        return self.lease is not None and now + self.skew < self.lease[1]


def run(seed: int, fencing: bool, clients: int = 3, steps: int = 300, ttl: int = 10) -> Storage:
    """Random runs. Each step, one client acts: it acquires, writes as the holder, or pauses."""
    rng = random.Random(seed)
    lock, store = LockService(ttl), Storage(fencing)
    cs = [Client(i, rng.choice([0, 0, -3, -8])) for i in range(clients)]  # some clocks run late
    for now in range(steps):
        c = cs[rng.randrange(clients)]
        if now < c.paused_until:
            continue
        r = rng.random()
        if r < 0.1:
            c.paused_until = now + rng.randrange(5, 25)  # a long pause, maybe past the lease
        elif c.believes_holder(now):
            store.write(c.lease[0], c.cid, (c.cid, c.writes))  # @line L5
            c.writes += 1
        else:
            c.lease = lock.acquire(c.cid, now)  # @line L4
    return store


def stale_writes(store: Storage) -> int:
    """Count accepted writes whose token is below a token accepted earlier."""
    bad, top = 0, 0
    for token, _, _ in store.accepted:
        if token < top:
            bad += 1
        top = max(top, token)
    return bad
