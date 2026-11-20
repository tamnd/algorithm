# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/coded-slotted-aloha/. The authors are listed in prov/KAWTQF.jsonl.

"""Coded slotted ALOHA: repetition of packets in random slots and iterative interference cancellation.

Model (the collision channel of Casini et al. 2007, Liva 2011 and Paolini et al. 2015):
- A frame has M slots and K active users. User u draws a degree d from the distribution
  Lambda (a dict {d: Lambda_d}) and sends d copies of its packet in d distinct slots,
  chosen uniformly at random.
- A slot with exactly one copy is decoded. A slot with two or more copies is a collision
  and gives nothing by itself. Every copy carries pointers to the slots of its twins,
  so a decoded packet lets the receiver cancel all its other copies perfectly.

A frame is given as user_slots: a list with, for each user, the list of its slots.
The decoder works on the bipartite graph of users and slots and costs O(K + M + E)
word operations for E copies in total (word-RAM model).

The file also has the density evolution recursion of Paolini, Liva and Chiani 2015
(Corollary 3.1) for the asymptotic threshold, and the bound of their Theorem 4.1.
"""

import math
import random
from collections import deque


def transmit(rng: random.Random, k: int, m: int, dist: dict) -> list[list[int]]:
    """Draw the slots of k users in a frame of m slots, with degree distribution dist."""
    if m <= 0 or k < 0:
        raise ValueError("need m > 0 and k >= 0")
    if any(d < 1 or d > m for d in dist) or abs(sum(dist.values()) - 1.0) > 1e-9:
        raise ValueError("dist must be a probability distribution on degrees 1..m")
    degrees = sorted(dist)
    weights = [dist[d] for d in degrees]
    frame = []
    for _ in range(k):
        d = rng.choices(degrees, weights)[0]  # @line L1
        frame.append(sorted(rng.sample(range(m), d)))  # @line L2
    return frame


def decode(user_slots: list[list[int]], m: int, rng: random.Random | None = None) -> list[int]:
    """Iterative interference cancellation (peeling). Returns the resolved users in decoding order.

    With rng given, the next singleton slot is taken at random instead of first in, first out.
    The set of resolved users does not depend on this choice (see proofs/correctness.md).
    """
    slots = [set() for _ in range(m)]
    for u, ss in enumerate(user_slots):
        if len(set(ss)) != len(ss):
            raise ValueError("a user sends at most one copy per slot")
        for s in ss:
            slots[s].add(u)  # @line L3
    queue = deque(s for s in range(m) if len(slots[s]) == 1)  # @line L4
    resolved = []
    while queue:  # @line L5
        if rng is None:
            s = queue.popleft()  # @line L6
        else:
            i = rng.randrange(len(queue))
            queue[i], queue[-1] = queue[-1], queue[i]
            s = queue.pop()  # @line L6
        if len(slots[s]) != 1:  # @line L7
            continue
        (u,) = slots[s]  # @line L8
        resolved.append(u)  # @line L9
        for t in user_slots[u]:  # @line L10
            slots[t].discard(u)  # @line L11
            if len(slots[t]) == 1:  # @line L12
                queue.append(t)  # @line L13
    return resolved  # @line L14


def unresolved_brute_force(user_slots: list[list[int]], m: int) -> set[int]:
    """The largest stopping set, by search over all subsets of users (small K only).

    A set S of users is a stopping set if every slot used by a user of S holds at least
    two users of S. The union of two stopping sets is a stopping set, so a largest one exists.
    """
    k = len(user_slots)
    best = set()
    for mask in range(1 << k):
        count = [0] * m
        members = [u for u in range(k) if mask >> u & 1]
        for u in members:
            for s in user_slots[u]:
                count[s] += 1
        if all(count[s] >= 2 for u in members for s in user_slots[u]) and len(members) > len(best):
            best = set(members)
    return best


def rate(dist: dict) -> float:
    """The rate R = 1 / Lambda'(1) of the repetition code: one packet over the mean number of copies."""
    return 1.0 / sum(d * p for d, p in dist.items())


def de_step(dist: dict, g: float, p: float) -> float:
    """One step of density evolution: p <- 1 - exp(-G sum_d d Lambda_d p^(d-1))."""
    return 1.0 - math.exp(-g * sum(d * lam * p ** (d - 1) for d, lam in dist.items()))


def de_converges(dist: dict, g: float, iters: int = 20000, tol: float = 1e-9) -> bool:
    """True if density evolution from p = 1 goes to 0 at the load G = g."""
    p = 1.0
    for _ in range(iters):
        q = de_step(dist, g, p)
        if q < tol:
            return True
        if abs(q - p) < 1e-15:
            return False
        p = q
    return False


def threshold(dist: dict, tol: float = 1e-5) -> float:
    """The asymptotic threshold G* = sup of the loads at which density evolution goes to 0."""
    lo, hi = 0.0, 1.0
    while hi - lo > tol:
        mid = 0.5 * (lo + hi)
        if de_converges(dist, mid):
            lo = mid
        else:
            hi = mid
    return lo


def load_bound(r: float, tol: float = 1e-12) -> float:
    """The unique positive root G of G = 1 - exp(-G / R), for 0 < R < 1 (Paolini et al. 2015, Theorem 4.1)."""
    if not 0.0 < r < 1.0:
        raise ValueError("need 0 < R < 1")
    lo, hi = 1e-9, 1.0
    while hi - lo > tol:
        mid = 0.5 * (lo + hi)
        if 1.0 - math.exp(-mid / r) > mid:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)
