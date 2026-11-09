# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/saturation-algorithm/. The authors are listed in prov/WW2T0H.jsonl.

"""Saturation (Ciardo, Luettgen and Siminiceanu 2001) on quasi-reduced MDDs.

A model has K levels, numbered K (top) down to 1. Level k has the local
states 0 .. sizes[k-1] - 1. A global state is a tuple s with s[k-1] the local
state of level k. An event is a dict {k: {i: [j, ...]}}: on each level k that
it names, the event moves local state i to any of the listed j, and it needs
i to be listed; on the other levels it changes nothing. This is the Kronecker
form: the successors of s under e are the product of the local choices.
Top(e) and Bot(e) are the highest and the lowest level that e names.

An MDD node is an int. Node 0 is the empty set and node 1 is the set that
holds the empty tuple. An inner node at level k has one child per local
state. A node is saturated when its set is closed under every event e with
Top(e) at most its level. Recursion depth is at most 2K.
"""

from itertools import product
from typing import Dict, List, Sequence, Tuple


class Saturation:
    def __init__(self, sizes: Sequence[int], events: List[Dict[int, Dict[int, List[int]]]]) -> None:
        self.sizes = list(sizes)
        self.K = len(sizes)
        self.events = events
        self.top = [max(e) for e in events]
        self.bot = [min(e) for e in events]
        self.by_top: Dict[int, List[int]] = {k: [] for k in range(1, self.K + 1)}
        for i, t in enumerate(self.top):
            self.by_top[t].append(i)
        self.level: List[int] = [0, 0]
        self.kids: List[Tuple[int, ...]] = [(), ()]
        self.unique: Dict[Tuple[int, Tuple[int, ...]], int] = {}
        self.union_cache: Dict[Tuple[int, int], int] = {}
        self.sat_cache: Dict[int, int] = {}
        self.fire_cache: Dict[Tuple[int, int], int] = {}
        self.firings = 0

    def node(self, k: int, ch: Sequence[int]) -> int:
        ch = tuple(ch)
        if not any(ch):
            return 0
        key = (k, ch)
        u = self.unique.get(key)
        if u is None:
            u = len(self.level)
            self.level.append(k)
            self.kids.append(ch)
            self.unique[key] = u
        return u

    def from_states(self, states) -> int:
        """The MDD of a set of global states, built level by level."""
        def build(k: int, group) -> int:
            if k == 0:
                return 1 if group else 0
            ch = [build(k - 1, [s for s in group if s[k - 1] == i]) for i in range(self.sizes[k - 1])]
            return self.node(k, ch)
        return build(self.K, list(states))

    def states(self, p: int) -> set:
        """The set of global states of the MDD p."""
        out = set()
        stack = [(p, self.K, ())]
        while stack:
            u, k, suffix = stack.pop()
            if u == 0:
                continue
            if k == 0:
                out.add(suffix[::-1])
                continue
            for i, c in enumerate(self.kids[u]):
                stack.append((c, k - 1, suffix + (i,)))
        return out

    def union(self, p: int, q: int) -> int:
        if p == 0 or p == q:
            return q
        if q == 0:
            return p
        if p > q:
            p, q = q, p
        key = (p, q)
        r = self.union_cache.get(key)
        if r is None:
            k = self.level[p]
            r = self.node(k, [self.union(a, b) for a, b in zip(self.kids[p], self.kids[q])])
            self.union_cache[key] = r
        return r

    def _fix(self, k: int, ch: List[int]) -> int:
        """Fire the events with Top = k on the node (k, ch) until nothing changes.

        The children in ch are saturated when this is called, so the result
        is saturated too.
        """
        changed = True
        while changed:  # @line L6
            changed = False
            for e in self.by_top[k]:  # @line L7
                local = self.events[e][k]
                for i in range(len(ch)):
                    if ch[i] == 0 or i not in local:
                        continue
                    f = self.rec_fire(e, k - 1, ch[i])  # @line L8
                    if f == 0:
                        continue
                    for j in local[i]:
                        u = self.union(ch[j], f)  # @line L9
                        if u != ch[j]:
                            ch[j] = u
                            changed = True  # @line L10
        return self.node(k, ch)  # @line L11

    def saturate(self, p: int) -> int:
        """The saturated node for the set of p and all that its low events reach."""
        if p <= 1:  # @line L1
            return p
        r = self.sat_cache.get(p)  # @line L2
        if r is None:
            k = self.level[p]
            ch = [self.saturate(c) for c in self.kids[p]]  # @line L3
            r = self._fix(k, ch)  # @line L4
            self.sat_cache[p] = r  # @line L5
            self.sat_cache[r] = r
        return r

    def rec_fire(self, e: int, l: int, q: int) -> int:
        """Saturated node for the image of the saturated node q at level l under e."""
        if l < self.bot[e] or q == 0:  # @line L12
            return q
        key = (e, q)
        r = self.fire_cache.get(key)  # @line L13
        if r is not None:
            return r
        self.firings += 1
        local = self.events[e].get(l)
        ch = [0] * self.sizes[l - 1]  # @line L14
        for i, c in enumerate(self.kids[q]):  # @line L15
            if c == 0:
                continue
            targets = [i] if local is None else local.get(i, [])
            if not targets:
                continue
            f = self.rec_fire(e, l - 1, c)  # @line L16
            if f == 0:
                continue
            for j in targets:
                ch[j] = self.union(ch[j], f)  # @line L17
        r = self._fix(l, ch)  # @line L18
        self.fire_cache[key] = r  # @line L19
        return r


def reachable_states(sizes: Sequence[int], events, init) -> Tuple[set, "Saturation", int]:
    """The reachable states from the set init, the engine, and the root node."""
    s = Saturation(sizes, events)
    root = s.saturate(s.from_states(init))
    return s.states(root), s, root


def successors(sizes: Sequence[int], event: Dict[int, Dict[int, List[int]]], state: Tuple[int, ...]):
    """Explicit successors of a state under one event, for the reference search."""
    choices = []
    for k in range(1, len(sizes) + 1):
        local = event.get(k)
        if local is None:
            choices.append([state[k - 1]])
        else:
            choices.append(local.get(state[k - 1], []))
    return [tuple(c) for c in product(*choices)]
