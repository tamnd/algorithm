# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/priority-cuts/. The authors are listed in prov/TMZ6X8.jsonl.

"""LUT mapping with priority cuts, after Mishchenko, Cho, Chatterjee and Brayton.

The network is a list `fanins` in topological order (every fanin of v is
smaller than v); a node with no fanins is a primary input. Each node
keeps at most C cuts of at most k leaves, its priority cuts. The cuts of
a node are the merges of the priority cuts of its fanins (each fanin
also offers its trivial cut), with the best cut of the last pass always
kept. They are sorted by a key, and the first C are kept. The first of
them is the best cut of the node.

Pass 1 sorts by (depth, number of leaves, area flow). It gives a mapping
and its depth D. The area passes keep the depth: a node may only use a
cut whose depth is at most the required time of the node in the last
mapping. Pass 2 sorts by area flow, pass 3 by exact area, the number of
LUTs that the cut adds to the current mapping.
"""

from typing import Sequence

INF = float("inf")


def drop_dominated(cuts) -> list:
    kept: list = []
    for c in sorted(set(cuts), key=lambda c: (len(c), sorted(c))):
        if not any(d <= c for d in kept):
            kept.append(c)
    return kept


class Mapper:
    def __init__(self, fanins: Sequence[Sequence[int]], outputs: Sequence[int], k: int, c: int) -> None:
        for v, fi in enumerate(fanins):
            if len(fi) > k:
                raise ValueError("the network is not k-bounded")
            if any(u >= v for u in fi):
                raise ValueError("fanins must come before the node")
        self.f, self.outs, self.k, self.c = fanins, list(outputs), k, c
        n = len(fanins)
        self.pis = [not fi for fi in fanins]
        self.fanout = [0] * n
        for fi in fanins:
            for u in fi:
                self.fanout[u] += 1
        for o in outputs:
            self.fanout[o] += 1
        self.prio: list = [[] for _ in range(n)]
        self.best: list = [None] * n
        self.arr = [0] * n
        self.af = [0.0] * n
        self.req = [INF] * n
        self.ref = [0] * n

    # ---- cut costs
    def depth(self, cut) -> int:
        return 1 + max(self.arr[u] for u in cut)

    def area_flow(self, cut) -> float:
        return 1 + sum(self.af[u] for u in cut)

    def ref_cut(self, cut) -> int:
        """Add the LUTs of a cut to the mapping; return how many are new."""
        area = 1
        for u in cut:
            if not self.pis[u]:
                self.ref[u] += 1
                if self.ref[u] == 1:
                    area += self.ref_cut(self.best[u])
        return area

    def deref_cut(self, cut) -> int:
        area = 1
        for u in cut:
            if not self.pis[u]:
                self.ref[u] -= 1
                if self.ref[u] == 0:
                    area += self.deref_cut(self.best[u])
        return area

    def exact_area(self, cut) -> int:
        a = self.ref_cut(cut)
        self.deref_cut(cut)
        return a

    # ---- one pass
    def candidates(self, v) -> list:
        acc = {frozenset()}
        for u in self.f[v]:  # @line L5: merge the priority cuts of the fanins
            offer = self.prio[u] + [frozenset([u])]
            acc = {a | b for a in acc for b in offer if len(a | b) <= self.k}
        cands = drop_dominated(acc)
        if self.best[v] is not None and self.best[v] not in cands:  # @line L6
            cands.append(self.best[v])
        return cands

    def run_pass(self, mode: str) -> None:
        for v in range(len(self.f)):  # @line L4
            if self.pis[v]:
                continue
            in_map = self.ref[v] > 0
            if mode == "exact" and in_map:  # @line L7
                self.deref_cut(self.best[v])
            cands = self.candidates(v)

            def key(cut):
                d = self.depth(cut)
                late = d > self.req[v]
                if mode == "depth":
                    return (d, len(cut), self.area_flow(cut))
                if mode == "flow":
                    return (late, self.area_flow(cut), d, len(cut))
                return (late, self.exact_area(cut), self.area_flow(cut), d, len(cut))

            cands.sort(key=lambda cut: (key(cut), sorted(cut)))  # @line L8
            self.prio[v] = cands[: self.c]  # @line L9
            self.best[v] = cands[0]
            self.arr[v] = self.depth(self.best[v])  # @line L10
            self.af[v] = self.area_flow(self.best[v]) / max(1, self.fanout[v])
            if mode == "exact" and in_map:  # @line L11
                self.ref_cut(self.best[v])

    def luts(self) -> dict:
        out: dict = {}
        todo = [o for o in self.outs if not self.pis[o]]
        while todo:
            v = todo.pop()
            if v not in out:
                out[v] = self.best[v]
                todo.extend(u for u in self.best[v] if not self.pis[u])
        return out

    def set_mapping(self, target: int) -> None:
        """Reference counts and required times of the current mapping."""
        self.ref = [0] * len(self.f)
        for o in self.outs:
            if not self.pis[o]:
                self.ref[o] += 1
                if self.ref[o] == 1:
                    self.ref_cut(self.best[o])
        self.req = [INF] * len(self.f)
        for o in self.outs:
            self.req[o] = target
        for v in range(len(self.f) - 1, -1, -1):
            if self.ref[v] > 0 and self.req[v] < INF:
                for u in self.best[v]:
                    self.req[u] = min(self.req[u], self.req[v] - 1)


def priority_cut_map(fanins, outputs, k: int, c: int, area_passes: int = 2):
    """Return (luts, depth after pass 1, depth at the end, mapper)."""
    m = Mapper(fanins, outputs, k, c)  # @line L1
    m.run_pass("depth")  # @line L2: the depth pass
    d1 = max((m.arr[o] for o in outputs), default=0)  # @line L12
    modes = ["flow", "exact"][:area_passes]
    for mode in modes:  # the area passes of line L2
        m.set_mapping(d1)  # @line L3
        m.run_pass(mode)
    luts = m.luts()  # @line L13
    return luts, d1, max((m.arr[o] for o in outputs), default=0), m
