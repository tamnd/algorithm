# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/link-state-routing/. The authors are listed in prov/454KX4.jsonl.

"""Link-state routing as a discrete-event simulation.

Each router originates a link-state advertisement (LSA): its id, a sequence
number, an age and the costs of its working links. LSAs spread by reliable
flooding: a router installs and forwards an LSA only if it is newer than its
copy, acknowledges every LSA it receives, and retransmits an unacknowledged
LSA after RXMT ticks. Each router then runs Dijkstra on the links that both
ends report and keeps the first hop of each shortest path.

The clock is an integer. Messages take one tick and are lost with a seeded
probability. seq_bits=None compares sequence numbers as integers (as OSPF
does in its linear space); seq_bits=b uses the circular rule of the 1980
ARPANET, in which n is newer than m when 0 < (n - m) mod 2^b <= 2^(b-1).
"""

import heapq
import random

_LINK, _MSG, _TIMER = 0, 1, 2


class LSA:
    __slots__ = ("origin", "seq", "age", "links")

    def __init__(self, origin, seq, age, links):
        self.origin, self.seq, self.age, self.links = origin, seq, age, dict(links)

    def key(self):
        return (self.origin, self.seq, tuple(sorted(self.links.items(), key=repr)))


def dijkstra_next_hops(graph, s):
    """Dijkstra from s on a dict graph; returns (dist, first_hop).

    Ties between equal distances go to the smaller (distance, node) key, so
    every router that has the same database gets the same distances.
    O((n + m) log n) time with a binary heap.
    """
    dist, first = {s: 0}, {s: s}
    done = set()
    pq = [(0, repr(s), s, s)]
    while pq:
        d, _, u, f = heapq.heappop(pq)
        if u in done:
            continue
        done.add(u)
        first[u] = f
        for v, c in graph.get(u, {}).items():
            nd = d + c
            if v not in done and nd < dist.get(v, float("inf")):
                dist[v] = nd
                heapq.heappush(pq, (nd, repr(v), v, v if u == s else f))
    return dist, first


class LSNetwork:
    """graph: dict node -> dict neighbour -> positive cost (symmetric)."""

    def __init__(self, graph, loss=0.0, rng=None, rxmt=5, maxage=None,
                 refresh=None, seq_bits=None):
        self.w = {u: dict(nb) for u, nb in graph.items()}
        self.loss, self.rxmt = loss, rxmt
        self.maxage, self.refresh, self.seq_bits = maxage, refresh, seq_bits
        self.rng = rng if rng is not None else random.Random(0)
        self.now, self.seqno, self.events = 0, 0, []
        self.sent = 0
        self.DB = {u: {} for u in self.w}           # DB[y][origin] = (lsa, t_installed)
        self.unacked = {u: {} for u in self.w}      # unacked[y][(z, origin)] = lsa
        self.next = {u: {} for u in self.w}
        self.dist = {u: {} for u in self.w}
        self.myseq = {u: 0 for u in self.w}
        for u in sorted(self.w, key=repr):
            self._push(0, _TIMER, ("originate", u))

    def _push(self, t, cls, ev):
        self.seqno += 1
        heapq.heappush(self.events, (t, cls, self.seqno, ev))

    # ----------------------------------------------------------- helpers
    def newer(self, a, b):
        """Is sequence number a newer than b?"""
        if self.seq_bits is None:
            return a > b
        half = 1 << (self.seq_bits - 1)
        diff = (a - b) % (1 << self.seq_bits)
        return 0 < diff <= half

    def age_of(self, y, origin):
        lsa, t0 = self.DB[y][origin]
        return lsa.age + (self.now - t0)

    def _send(self, y, z, msg):
        self.sent += 1
        if z not in self.w[y]:
            return
        if self.loss and self.rng.random() < self.loss:
            return
        self._push(self.now + 1, _MSG, ("msg", z, y, msg))

    # ---------------------------------------------------------- handlers
    def _originate(self, y):
        self.myseq[y] += 1
        seq = self.myseq[y]
        if self.seq_bits is not None:
            seq %= 1 << self.seq_bits
        lsa = LSA(y, seq, 0, self.w[y])  # @line L1
        self._install(y, lsa)
        self._flood(y, lsa, None)  # @line L2

    def _receive(self, y, x, msg):
        kind, lsa = msg
        if kind == "ack":
            self.unacked[y].pop((x, lsa.key()), None)
            return
        self._send(y, x, ("ack", lsa))  # @line L3
        if self.maxage is not None and lsa.age >= self.maxage:
            self.DB[y].pop(lsa.origin, None)   # a flushed LSA
            self._route(y)
            return
        cur = self.DB[y].get(lsa.origin)  # @line L4
        if cur is None or self.newer(lsa.seq, cur[0].seq):  # @line L5
            if lsa.origin == y:
                # an old copy of our own LSA survives: jump past it
                self.myseq[y] = max(self.myseq[y], lsa.seq)
                self._originate(y)
                return
            self._install(y, lsa)
            self._flood(y, lsa, x)
        elif self.newer(cur[0].seq, lsa.seq):
            mine = cur[0]
            self._send_lsa(y, x, LSA(mine.origin, mine.seq,
                                     self.age_of(y, mine.origin), mine.links))  # @line L6

    def _send_lsa(self, y, z, lsa):
        hop = LSA(lsa.origin, lsa.seq, lsa.age + 1, lsa.links)
        self.unacked[y][(z, lsa.key())] = hop
        self._send(y, z, ("lsa", hop))
        self._push(self.now + self.rxmt, _TIMER, ("rxmt", y, z, lsa.key()))

    def _flood(self, y, lsa, came_from):
        for z in sorted(self.w[y], key=repr):  # @line L7
            if z != came_from:
                self._send_lsa(y, z, lsa)

    def _retransmit(self, y, z, key):
        hop = self.unacked[y].get((z, key))
        if hop is not None and z not in self.w[y]:
            del self.unacked[y][(z, key)]       # the link is gone
        elif hop is not None:
            self._send(y, z, ("lsa", hop))  # @line L8
            self._push(self.now + self.rxmt, _TIMER, ("rxmt", y, z, key))

    def _install(self, y, lsa):
        self.DB[y][lsa.origin] = (lsa, self.now)  # @line L9
        self._route(y)

    def _route(self, y):
        g = {}
        db = self.DB[y]
        for u, (lsa, _) in db.items():  # @line L10
            for v, c in lsa.links.items():
                if v in db and u in db[v][0].links:      # both ends report it
                    g.setdefault(u, {})[v] = c
        dist, first = dijkstra_next_hops(g, y)  # @line L11
        self.dist[y] = dist
        self.next[y] = {t: first[t] for t in dist if t != y}

    def _age_check(self, y):
        if self.maxage is None:
            return
        gone = [o for o in self.DB[y] if o != y and self.age_of(y, o) >= self.maxage]
        for o in gone:  # @line L12
            del self.DB[y][o]
        if gone:
            self._route(y)

    # ----------------------------------------------------------- driver
    def link_down(self, t, u, v):
        self._push(t, _LINK, ("down", u, v))

    def set_cost(self, t, u, v, c):
        self._push(t, _LINK, ("cost", u, v, c))

    def inject(self, t, at, lsa):
        """Deliver a forged or stale LSA to router at, as if from itself."""
        self._push(t, _MSG, ("inject", at, lsa))

    def run(self, until, max_events=10 ** 7):
        n = 0
        while self.events and self.events[0][0] <= until and n < max_events:
            t, _, _, ev = heapq.heappop(self.events)
            self.now, n = t, n + 1
            kind = ev[0]
            if kind == "msg":
                self._receive(ev[1], ev[2], ev[3])
            elif kind == "originate":
                self._originate(ev[1])
                if self.refresh:
                    self._push(self.now + self.refresh, _TIMER, ("originate", ev[1]))
            elif kind == "rxmt":
                self._retransmit(*ev[1:])
            elif kind == "inject":
                at, lsa = ev[1], ev[2]
                cur = self.DB[at].get(lsa.origin)
                if cur is None or self.newer(lsa.seq, cur[0].seq):
                    self._install(at, lsa)
                    self._flood(at, lsa, None)
            elif kind == "down":
                _, u, v = ev
                self.w[u].pop(v, None)
                self.w[v].pop(u, None)
                self._originate(u)
                self._originate(v)
            elif kind == "cost":
                _, u, v, c = ev
                self.w[u][v] = self.w[v][u] = c
                self._originate(u)
                self._originate(v)
            for y in self.w:
                self._age_check(y)
        if not self.events or self.events[0][0] > until:
            self.now = until
        return self

    def quiet(self):
        """True when no LSA is in flight or waiting for an acknowledgement."""
        return all(not q for q in self.unacked.values()) and not any(
            ev[3][0] == "msg" for ev in self.events)
