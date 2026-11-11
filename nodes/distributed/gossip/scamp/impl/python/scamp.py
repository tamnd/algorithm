# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/scamp/. The authors are listed in prov/7YXJZ9.jsonl.

"""SCAMP (Ganesh, Kermarrec and Massoulie 2003) in a seeded simulator.

Each node s has a PartialView (the nodes it gossips to) and an InView (the
nodes that hold s). A new node s sends its subscription to a contact. The
contact forwards s to every node of its PartialView and c more copies to
random nodes of its PartialView. A node j that receives a forwarded
subscription keeps s with probability 1 / (1 + |PartialView(j)|), if s is
not j and not already held; otherwise it forwards it to a random node of
its PartialView. A copy that has been forwarded max_hops times is dropped,
which the simulator counts.

Unsubscription: s asks the first l' - c - 1 nodes of its InView to replace
s by nodes of its PartialView, and the last c + 1 to just drop s.

Indirection: the subscription first takes a random walk of a few hops from
the contact the joiner knows, and the node where the walk ends acts as the
contact. Lease: every subscription expires after a fixed number of rounds;
the holders drop it, and a live node then subscribes again through a
random node of its PartialView. A crashed node cannot, so its arcs vanish.
"""

import math
import random


class Scamp:
    def __init__(self, c: int, seed: int, max_hops: int = 1000, indirection: int = 0):
        self.rng = random.Random(seed)
        self.c = c
        self.max_hops = max_hops
        self.indirection = indirection
        self.view: dict[int, set[int]] = {0: set()}
        self.inview: dict[int, set[int]] = {0: set()}
        self.alive = {0}
        self.dropped = 0
        self.next_id = 1

    # ------------------------------------------------------------ subscription

    def _add(self, j: int, s: int) -> None:
        self.view[j].add(s)
        self.inview[s].add(j)

    def _forward(self, j: int, s: int) -> None:
        """Handle one forwarded copy of the subscription of s, starting at j."""
        for _ in range(self.max_hops):
            v = self.view[j]
            if s != j and s not in v:                                    # @line L4
                if self.rng.random() < 1 / (1 + len(v)):                 # @line L5
                    self._add(j, s)
                    return
            live = [k for k in v if k in self.alive]
            if not live:
                break
            j = self.rng.choice(live)                                    # @line L6
        self.dropped += 1

    def subscribe(self, s: int, contact: int) -> None:
        for _ in range(self.indirection):
            live = [k for k in self.view[contact] if k in self.alive]
            if live:
                contact = self.rng.choice(live)
        self.view.setdefault(s, set())
        self.inview.setdefault(s, set())
        self.alive.add(s)
        self._add(s, contact)                                            # @line L1
        targets = [k for k in self.view[contact] if k in self.alive and k != s]
        if not targets:
            self._add(contact, s)
            return
        for j in targets:                                                # @line L2
            self._forward(j, s)
        for _ in range(self.c):                                          # @line L3
            self._forward(self.rng.choice(targets), s)

    def join(self, contact=None) -> int:
        s = self.next_id
        self.next_id += 1
        if contact is None:
            contact = self.rng.choice(sorted(self.alive))
        self.subscribe(s, contact)
        return s

    def grow(self, n: int) -> None:
        while len(self.alive) < n:
            self.join()

    # ------------------------------------------------------------ leaving

    def unsubscribe(self, s: int) -> None:
        out = sorted(self.view[s])                                       # @line L7
        ins = sorted(self.inview[s])
        self.rng.shuffle(ins)
        keep = max(0, len(ins) - self.c - 1)
        for k, j in enumerate(ins):
            self.view[j].discard(s)
            if k < keep and out:                                         # @line L8
                r = out[k % len(out)]
                if r != j and r not in self.view[j]:
                    self._add(j, r)
            # the last c + 1 nodes just drop s                           # @line L9
        for r in out:
            self.inview[r].discard(s)
        self.view[s] = set()
        self.inview[s] = set()
        self.alive.discard(s)

    def crash(self, s: int) -> None:
        self.alive.discard(s)

    def lease_round(self, period: int, t: int) -> None:
        """All subscriptions with phase t mod period expire now."""
        due = [s for s in list(self.view) if s % period == t % period and self.inview.get(s)]
        for s in due:
            for j in list(self.inview[s]):
                self.view[j].discard(s)
            self.inview[s] = set()
        for s in due:
            if s in self.alive:
                live = [k for k in self.view[s] if k in self.alive]
                if not live:
                    # isolation recovery: the paper lets an isolated node
                    # subscribe again through any node it can reach; here a
                    # random live node stands for that contact
                    live = sorted(self.alive - {s})
                self.subscribe(s, self.rng.choice(live))

    # ------------------------------------------------------------ measures

    def mean_view(self) -> float:
        return sum(len(self.view[s]) for s in self.alive) / len(self.alive)

    def dead_arcs(self) -> int:
        return sum(1 for s in self.alive for k in self.view[s] if k not in self.alive)

    def reach(self, src: int) -> int:
        """Number of live nodes reached by flooding along live PartialView arcs."""
        seen = {src}
        stack = [src]
        while stack:
            v = stack.pop()
            for w in self.view[v]:
                if w in self.alive and w not in seen:
                    seen.add(w)
                    stack.append(w)
        return len(seen)


def harmonic(n: int) -> float:
    return sum(1 / k for k in range(1, n + 1))


def predicted_mean_view(n: int, c: int, n0: int = 1, a0: float = 0.0) -> float:
    """The expected mean PartialView size after growing from n0 nodes with
    mean view a0 to n nodes, with uniform contacts and every copy kept:
    a0 + (c + 1)(H_n - H_n0). From one node this is (c + 1)(H_n - 1),
    about (c + 1) ln n."""
    return a0 + (c + 1) * (harmonic(n) - harmonic(n0))
