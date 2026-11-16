# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/topological-map/. The authors are listed in prov/KYBFGV.jsonl.

"""A topological map: places with signatures, joined by edges with action labels.

A place is an integer id with a signature, the value that the robot senses
there (for example the kind of junction). An edge joins two places. It has
a length and two action labels: the action that leads from the first place
to the second, and the action that leads back. At each place, an action
label leads to at most one place, so a route is a list of actions.

There is no global coordinate frame. The lengths are only used to rank
routes and must be >= 0.
"""

import heapq
import math


class TopologicalMap:
    def __init__(self):
        self.sig = []  # sig[v] is the signature of place v
        self.out = []  # out[v][action] = (w, length)

    def add_place(self, signature):
        """Add a place and return its id."""
        v = len(self.sig)  # @line L1
        self.sig.append(signature)
        self.out.append({})
        return v

    def add_edge(self, u, a, v, b, length):
        """Join u and v: action a leads from u to v, and action b from v to u."""
        if not (0 <= u < len(self.sig) and 0 <= v < len(self.sig)):
            raise ValueError("unknown place")
        if length < 0:
            raise ValueError("negative length")
        if a in self.out[u] or b in self.out[v] or (u == v and a == b):  # @line L2
            raise ValueError("an action label is used twice at one place")
        self.out[u][a] = (v, length)  # @line L3
        self.out[v][b] = (u, length)

    def step(self, v, a):
        """Return the place that action a leads to from v, or None."""
        e = self.out[v].get(a)
        return None if e is None else e[0]

    def route(self, s, t):
        """Return (length, places, actions) of a shortest route from s to t, or None.

        This is Dijkstra's algorithm on the directed graph of the actions.
        """
        dist = {s: 0}  # @line L4
        prev = {}
        heap = [(0, s)]
        while heap:  # @line L5
            d, u = heapq.heappop(heap)  # @line L6
            if d > dist[u]:
                continue
            if u == t:
                break
            for a, (v, length) in sorted(self.out[u].items(), key=lambda item: repr(item[0])):  # @line L7
                nd = d + length
                if nd < dist.get(v, math.inf):  # @line L8
                    dist[v] = nd
                    prev[v] = (u, a)
                    heapq.heappush(heap, (nd, v))
        if t not in dist:
            return None
        places, actions = [t], []  # @line L9
        while places[-1] != s:
            u, a = prev[places[-1]]
            places.append(u)
            actions.append(a)
        return dist[t], places[::-1], actions[::-1]

    def localize(self, first, steps):
        """Return the set of places where the robot can be.

        first is the signature sensed at the start, and steps is a list of
        (action, signature) pairs: the robot took the action and then sensed
        the signature. Perception and actions are assumed free of errors.
        """
        cands = {v for v in range(len(self.sig)) if self.sig[v] == first}  # @line L10
        for a, z in steps:  # @line L11
            nxt = set()
            for v in cands:
                w = self.step(v, a)
                if w is not None and self.sig[w] == z:  # @line L12
                    nxt.add(w)
            cands = nxt
        return cands  # @line L13
