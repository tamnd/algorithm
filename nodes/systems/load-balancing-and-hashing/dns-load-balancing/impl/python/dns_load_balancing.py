# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dns-load-balancing/. The authors are listed in prov/1TFQQ5.jsonl.

"""DNS load balancing: round-robin answers, SRV selection and resolver caches.

Authority answers each query for a name with its address records rotated by
one more place than the last answer (cyclic order, as in the BIND option
rrset-order cyclic; RFC 1794 instead rotated the zone every 300 seconds). srv_order orders SRV records as in RFC 2782: by
priority, and within one priority by repeated weighted draws with running
sums. simulate() models resolvers that cache an answer for TTL time units and
clients that use the first address of the cached answer; it counts the
requests that reach each server.
"""

import random
from typing import Dict, List, Sequence, Tuple

Srv = Tuple[int, int, str]  # (priority, weight, target)


def rotate(rrset: Sequence[str], k: int) -> List[str]:
    n = len(rrset)
    if n == 0:
        return []
    k %= n
    return list(rrset[k:]) + list(rrset[:k])


class Authority:
    """Authoritative server that rotates its answer for each query."""

    def __init__(self, rrset: Sequence[str], ttl: int) -> None:
        self.rrset = list(rrset)
        self.ttl = ttl
        self.q = 0

    def answer(self) -> Tuple[List[str], int]:
        out = rotate(self.rrset, self.q)  # @line L1
        self.q += 1
        return out, self.ttl  # @line L2


def srv_pick_index(cands: Sequence[Srv], r: int) -> int:
    """Index of the first record (in the given order) whose running sum is >= r."""
    run = 0
    for i, (_, w, _) in enumerate(cands):
        run += w
        if run >= r:  # @line L7
            return i
    raise ValueError("r is larger than the sum of the weights")


def srv_order(records: Sequence[Srv], rng: random.Random) -> List[Srv]:
    """Order SRV records for contact as in RFC 2782."""
    for p, w, _ in records:
        if p < 0 or w < 0:
            raise ValueError("priority and weight must be non-negative")
    order: List[Srv] = []
    for p in sorted({rec[0] for rec in records}):  # @line L3
        cands = [rec for rec in records if rec[0] == p]
        cands = [rec for rec in cands if rec[1] == 0] + [rec for rec in cands if rec[1] > 0]  # @line L4
        while cands:  # @line L5
            total = sum(w for _, w, _ in cands)
            r = rng.randint(0, total)  # @line L6
            i = srv_pick_index(cands, r)
            order.append(cands.pop(i))  # @line L8
    return order  # @line L9


def srv_first_probabilities(cands: Sequence[Srv]) -> List[Tuple[int, int]]:
    """Exact chance (numerator, denominator) that each record is drawn first,
    by enumerating every value of r in 0..sum."""
    total = sum(w for _, w, _ in cands)
    hits = [0] * len(cands)
    for r in range(total + 1):
        hits[srv_pick_index(cands, r)] += 1
    return [(h, total + 1) for h in hits]


def simulate(clients: Sequence[int], rrset: Sequence[str], ttl: int, horizon: int,
             dead: Sequence[str] = (), dead_from: int = 0) -> Dict[str, int]:
    """Resolver r serves clients[r] clients. At each time t in 0..horizon-1, the
    resolvers in index order refresh an expired answer from the authority,
    then each client sends one request to the first address of its resolver's
    answer. Requests sent to a server in dead at time >= dead_from fail and are
    counted under the key 'failed'."""
    auth = Authority(rrset, ttl)
    cache: List[Tuple[List[str], int]] = [([], -1) for _ in clients]
    counts: Dict[str, int] = {a: 0 for a in rrset}
    counts["failed"] = 0
    for t in range(horizon):
        for r, m in enumerate(clients):
            ans, expires = cache[r]
            if t >= expires:
                ans, ttl_got = auth.answer()
                cache[r] = (ans, t + ttl_got)
            target = ans[0]
            if target in dead and t >= dead_from:
                counts["failed"] += m
            else:
                counts[target] += m
    return counts
