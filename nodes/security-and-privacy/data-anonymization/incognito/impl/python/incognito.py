# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/incognito/. The authors are listed in prov/KC05HR.jsonl.
"""Incognito: all k-anonymous full-domain generalizations, by an a priori search over attribute sets.

A table is a list of rows. Each row is a tuple of d quasi-identifier values.
A hierarchy for attribute a is a list of dicts: hierarchy[a][l] maps each raw
value of attribute a to its value at level l, and hierarchy[a][0] is the
identity. Each level must be a coarsening of the level below it, so that the
hierarchy is a tree. A node is a pair (attrs, levels): a sorted tuple of
attribute indices and one level for each of them.
"""

import heapq
from collections import Counter
from typing import Hashable, Optional, Sequence

Row = tuple[Hashable, ...]
Hierarchy = Sequence[Sequence[dict[Hashable, Hashable]]]
Node = tuple[tuple[int, ...], tuple[int, ...]]


def _up_maps(hierarchy: Hierarchy) -> list[list[dict[Hashable, Hashable]]]:
    """up[a][l] maps a value of attribute a at level l to its parent value at level l + 1."""
    up = []
    for levels in hierarchy:
        maps = []
        for lv in range(len(levels) - 1):
            maps.append({levels[lv][x]: levels[lv + 1][x] for x in levels[0]})
        up.append(maps)
    return up


def _frequency(table: Sequence[Row], hierarchy: Hierarchy, node: Node) -> Counter:
    attrs, levels = node
    return Counter(tuple(hierarchy[a][lv][row[a]] for a, lv in zip(attrs, levels)) for row in table)


def _roll_up(freq: Counter, up: list[list[dict[Hashable, Hashable]]], parent: Node, pos: int) -> Counter:
    """Frequency set of the node one level above parent at position pos, from the parent's set."""
    a, lv = parent[0][pos], parent[1][pos]
    out: Counter = Counter()
    for key, c in freq.items():
        new = key[:pos] + (up[a][lv][key[pos]],) + key[pos + 1:]
        out[new] += c
    return out


def _step(node: Node, pos: int, delta: int) -> Node:
    attrs, levels = node
    return attrs, levels[:pos] + (levels[pos] + delta,) + levels[pos + 1:]


def incognito(table: Sequence[Row], hierarchy: Hierarchy, k: int) -> tuple[list[tuple[int, ...]], list[tuple[int, ...]]]:
    """Return (all, minimal): every generalization vector over all d attributes whose
    generalized table is k-anonymous, and those of them with no k-anonymous direct
    specialization. Both lists are sorted.

    Precondition: d >= 1, k >= 1, and each hierarchy is a tree (each level coarsens the one below).
    Cost: at most 2^d g nodes are created, where g is the number of vectors of the full lattice.
    Each check takes O(n d) expected time for n rows, from the table or by a roll-up.
    """
    d = len(hierarchy)
    up = _up_maps(hierarchy)
    tops = [len(levels) - 1 for levels in hierarchy]
    cand: set[Node] = {((a,), (lv,)) for a in range(d) for lv in range(tops[a] + 1)}  # @line L1
    s: set[Node] = set()
    for i in range(1, d + 1):  # @line L2
        s = set(cand)  # @line L3
        marked: set[Node] = set()
        queue: list[tuple[int, Node]] = []
        parent_of: dict[Node, tuple[Counter, Node, int]] = {}
        for node in cand:
            if all(_step(node, p, -1) not in cand for p in range(i) if node[1][p] > 0):
                heapq.heappush(queue, (sum(node[1]), node))  # @line L4
        queued = {node for _, node in queue}
        while queue:  # @line L5
            _, node = heapq.heappop(queue)  # @line L6
            if node in marked:  # @line L7
                continue
            link: Optional[tuple[Counter, Node, int]] = parent_of.get(node)
            if link is None:  # @line L8
                freq = _frequency(table, hierarchy, node)
            else:
                freq = _roll_up(link[0], up, link[1], link[2])
            if all(c >= k for c in freq.values()):  # @line L9
                for p in range(i):
                    if node[1][p] < tops[node[0][p]]:
                        marked.add(_step(node, p, 1))  # @line L10
            else:
                s.discard(node)  # @line L11
                for p in range(i):  # @line L12
                    if node[1][p] < tops[node[0][p]]:
                        gen = _step(node, p, 1)
                        if gen in cand and gen not in queued:
                            parent_of[gen] = (freq, node, p)
                            queued.add(gen)
                            heapq.heappush(queue, (sum(gen[1]), gen))
        if i < d:  # @line L13
            cand = set()
            for x in s:
                for y in s:
                    if x[0][:-1] == y[0][:-1] and x[1][:-1] == y[1][:-1] and x[0][-1] < y[0][-1]:
                        new = (x[0] + (y[0][-1],), x[1] + (y[1][-1],))
                        subsets = ((new[0][:j] + new[0][j + 1:], new[1][:j] + new[1][j + 1:]) for j in range(i + 1))
                        if all(sub in s for sub in subsets):
                            cand.add(new)
    full = sorted(levels for _, levels in s)  # @line L14
    full_set = set(full)
    minimal = [
        v for v in full
        if all(v[:p] + (v[p] - 1,) + v[p + 1:] not in full_set for p in range(d) if v[p] > 0)
    ]  # @line L15
    return full, minimal  # @line L16
