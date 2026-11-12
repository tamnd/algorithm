# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bgp/. The authors are listed in prov/BXJ1W1.jsonl.

"""The BGP-4 decision process (RFC 4271, Section 9.1) and an AS-level
simulation of BGP under the Gao-Rexford policies.

decide() picks the best route to one prefix from a list of candidate
routes. ASNetwork runs one BGP speaker per autonomous system, with
customer, peer and provider links, the usual preference customer > peer >
provider, and valley-free export: routes from customers (and the AS's own
prefixes) go to every neighbour, routes from peers and providers go to
customers only. Links are reliable FIFO channels with seeded random delays,
and changes are batched as by the MRAI timer.
"""

import heapq
import random

IGP, EGP, INCOMPLETE = 0, 1, 2
CUSTOMER, PEER, PROVIDER = "customer", "peer", "provider"
PREF = {CUSTOMER: 300, PEER: 200, PROVIDER: 100}


class Route:
    __slots__ = ("as_path", "local_pref", "origin", "med", "neighbor_as",
                 "ebgp", "igp_cost", "bgp_id", "peer_addr", "next_hop_ok")

    def __init__(self, as_path, local_pref=100, origin=IGP, med=None,
                 neighbor_as=None, ebgp=True, igp_cost=0, bgp_id=0,
                 peer_addr=0, next_hop_ok=True):
        self.as_path = tuple(as_path)
        self.local_pref, self.origin, self.med = local_pref, origin, med
        self.neighbor_as = (neighbor_as if neighbor_as is not None
                            else (self.as_path[0] if self.as_path else None))
        self.ebgp, self.igp_cost = ebgp, igp_cost
        self.bgp_id, self.peer_addr = bgp_id, peer_addr
        self.next_hop_ok = next_hop_ok

    def __repr__(self):
        return "Route(%r, lp=%r)" % (self.as_path, self.local_pref)


def decide(routes, local_as):
    """RFC 4271, Section 9.1.2: the best route, or None."""
    rs = [r for r in routes
          if r.next_hop_ok and local_as not in r.as_path]  # @line L1
    if not rs:  # @line L2
        return None
    top = max(r.local_pref for r in rs)
    rs = [r for r in rs if r.local_pref == top]  # @line L3
    short = min(len(r.as_path) for r in rs)
    rs = [r for r in rs if len(r.as_path) == short]  # @line L4
    low = min(r.origin for r in rs)
    rs = [r for r in rs if r.origin == low]  # @line L5

    def med(r):                     # a missing MED counts as the lowest value
        return 0 if r.med is None else r.med
    least = {}
    for r in rs:
        least[r.neighbor_as] = min(least.get(r.neighbor_as, med(r)), med(r))
    rs = [r for r in rs if med(r) == least[r.neighbor_as]]  # @line L6
    if any(r.ebgp for r in rs):
        rs = [r for r in rs if r.ebgp]  # @line L7
    cost = min(r.igp_cost for r in rs)
    rs = [r for r in rs if r.igp_cost == cost]  # @line L8
    bid = min(r.bgp_id for r in rs)
    rs = [r for r in rs if r.bgp_id == bid]  # @line L9
    return min(rs, key=lambda r: r.peer_addr)  # @line L10


# ---------------------------------------------------------------- AS graph

def random_hierarchy(rng, n, tier1=3, peer_prob=0.1):
    """ASes 0..n-1. The first tier1 ASes form a full peer mesh; every other
    AS buys transit from one or two ASes with smaller numbers, so the
    customer-provider graph is acyclic. Some extra peer links are added."""
    rel = {a: {} for a in range(n)}            # rel[a][b]: what b is to a
    for a in range(tier1):
        for b in range(a + 1, tier1):
            rel[a][b] = rel[b][a] = PEER
    for a in range(tier1, n):
        for p in rng.sample(range(a), min(a, rng.randint(1, 2))):
            rel[a][p] = PROVIDER
            rel[p][a] = CUSTOMER
    for a in range(tier1, n):
        for b in range(a + 1, n):
            if b not in rel[a] and rng.random() < peer_prob:
                rel[a][b] = rel[b][a] = PEER
    return rel


class ASNetwork:
    def __init__(self, rel, prefix_origin, rng=None, max_delay=3, batch=3):
        self.rel = rel
        self.o = prefix_origin
        self.rng = rng if rng is not None else random.Random(0)
        self.max_delay, self.batch = max_delay, batch
        self.rib_in = {a: {} for a in rel}       # rib_in[a][b] = Route
        self.best = {a: None for a in rel}
        self.events, self.seq, self.now = [], 0, 0
        self.last_arrival, self.pending = {}, set()
        self.updates = 0
        self.best[self.o] = Route((), local_pref=1000, neighbor_as=self.o)
        self._send_all(self.o)

    def _push(self, t, ev):
        self.seq += 1
        heapq.heappush(self.events, (t, self.seq, ev))

    def learned_from(self, a):
        r = self.best[a]
        if r is None:
            return None
        return "self" if not r.as_path else self.rel[a][r.as_path[0]]

    def exports(self, a, b):
        """Valley-free export of a's best route to neighbour b."""
        src = self.learned_from(a)
        if src is None:
            return None
        if src in ("self", CUSTOMER) or self.rel[a][b] == CUSTOMER:  # @line L12
            return (a,) + self.best[a].as_path
        return None

    def _send_all(self, a):
        if a not in self.pending:
            self.pending.add(a)
            self._push(self.now + self.rng.randint(1, self.batch), ("flush", a))

    def _flush(self, a):
        self.pending.discard(a)
        for b in sorted(self.rel[a]):
            path = self.exports(a, b)            # None is a withdrawal
            self.updates += 1
            t = max(self.now + self.rng.randint(1, self.max_delay),
                    self.last_arrival.get((a, b), 0))
            self.last_arrival[(a, b)] = t
            self._push(t, ("upd", b, a, path))

    def _receive(self, a, b, path):
        if path is None:
            self.rib_in[a].pop(b, None)
        else:
            self.rib_in[a][b] = Route(path, local_pref=PREF[self.rel[a][b]],
                                      neighbor_as=b, bgp_id=b, peer_addr=b)  # @line L11
        if a == self.o:
            return
        new = decide(list(self.rib_in[a].values()), a)
        old = self.best[a]
        if (new is None) != (old is None) or (
                new is not None and new.as_path != old.as_path):
            self.best[a] = new
            self._send_all(a)

    def run(self, max_events=10 ** 6):
        n = 0
        while self.events and n < max_events:
            t, _, ev = heapq.heappop(self.events)
            self.now, n = t, n + 1
            if ev[0] == "flush":
                self._flush(ev[1])
            else:
                self._receive(ev[1], ev[2], ev[3])
        return not self.events

    def path(self, a):
        """The AS path from a to the origin, a first, or None."""
        r = self.best[a]
        return None if r is None else (a,) + r.as_path
