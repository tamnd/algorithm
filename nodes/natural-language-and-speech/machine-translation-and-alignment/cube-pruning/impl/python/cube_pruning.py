# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cube-pruning/. The authors are listed in prov/6RZK3C.jsonl.

"""Cube pruning (Chiang 2007) for one cell of a chart decoder.

A cell receives hyperedges. A hyperedge is a rule with a score and a target
pattern, and a list of child cells; each child cell is a list of items sorted
by score, best first. An item is (score, words). Choosing item j_i in child
cell i gives a grid point j = (j_1, ..., j_r); its item has the words of the
target pattern with each variable replaced by the words of its child item,
and the score

    rule score + sum of the child scores + lm_weight * (new bigram scores),

where the new bigrams are those of the result that are not inside a child item.
With lm_weight = 0 the score is monotone in each j_i, and cube pruning pops the
exact k best grid points (the lazy k-best enumeration of Huang and Chiang 2005).
With a language model the score is not monotone, and cube pruning is a heuristic.
"""

import heapq
import itertools
from dataclasses import dataclass, field

Item = tuple[float, tuple[str, ...]]


class BigramScores:
    """Bigram log probabilities (natural log) with a default for unseen pairs."""

    def __init__(self, table: dict[tuple[str, str], float], default: float) -> None:
        self.table, self.default = dict(table), default

    def inside(self, words: tuple[str, ...]) -> float:
        return sum(self.table.get(p, self.default) for p in zip(words, words[1:]))


@dataclass
class Edge:
    rule_score: float
    pattern: tuple  # words (str) and variables (int index into children)
    children: list[list[Item]] = field(default_factory=list)


def combine(edge: Edge, j: tuple[int, ...], lm: BigramScores, lm_weight: float) -> Item:
    """The item of grid point j of the edge."""
    words: list[str] = []
    score = edge.rule_score
    lm_old = 0.0
    for sym in edge.pattern:
        if isinstance(sym, int):
            s, w = edge.children[sym][j[sym]]
            score += s
            lm_old += lm.inside(w)
            words.extend(w)
        else:
            words.append(sym)
    out = tuple(words)
    return score + lm_weight * (lm.inside(out) - lm_old), out


def cube_prune(edges: list[Edge], k: int, lm: BigramScores, lm_weight: float = 1.0) -> list[Item]:
    """Pop at most k grid points in the order of a heap, starting from the corner
    of each edge; return the popped items sorted by score, best first."""
    heap: list = []  # @line L1
    buf: list[Item] = []
    seen: set = set()
    for e, edge in enumerate(edges):  # @line L2
        if any(len(c) == 0 for c in edge.children):
            continue
        j = tuple(0 for _ in edge.children)
        score, words = combine(edge, j, lm, lm_weight)
        heapq.heappush(heap, (-score, e, j, words))
        seen.add((e, j))
    while heap and len(buf) < k:  # @line L3
        neg, e, j, words = heapq.heappop(heap)  # @line L4
        buf.append((-neg, words))  # @line L5
        edge = edges[e]
        for i in range(len(j)):  # @line L6
            nj = j[:i] + (j[i] + 1,) + j[i + 1 :]
            if nj[i] < len(edge.children[i]) and (e, nj) not in seen:  # @line L7
                seen.add((e, nj))
                score, w = combine(edge, nj, lm, lm_weight)
                heapq.heappush(heap, (-score, e, nj, w))  # @line L8
    buf.sort(key=lambda it: -it[0])  # @line L9
    return buf  # @line L10


def pop_order(edges: list[Edge], k: int, lm: BigramScores, lm_weight: float = 1.0) -> list[tuple[int, tuple[int, ...], float]]:
    """The grid points in the order cube pruning pops them (for traces)."""
    heap: list = []
    seen: set = set()
    out = []
    for e, edge in enumerate(edges):
        if any(len(c) == 0 for c in edge.children):
            continue
        j = tuple(0 for _ in edge.children)
        heapq.heappush(heap, (-combine(edge, j, lm, lm_weight)[0], e, j))
        seen.add((e, j))
    while heap and len(out) < k:
        neg, e, j = heapq.heappop(heap)
        out.append((e, j, -neg))
        for i in range(len(j)):
            nj = j[:i] + (j[i] + 1,) + j[i + 1 :]
            if nj[i] < len(edges[e].children[i]) and (e, nj) not in seen:
                seen.add((e, nj))
                heapq.heappush(heap, (-combine(edges[e], nj, lm, lm_weight)[0], e, nj))
    return out


def exhaustive_k_best(edges: list[Edge], k: int, lm: BigramScores, lm_weight: float = 1.0) -> list[Item]:
    """Score every grid point of every edge and keep the k best."""
    allitems = []
    for edge in edges:
        for j in itertools.product(*[range(len(c)) for c in edge.children]):
            allitems.append(combine(edge, j, lm, lm_weight))
    allitems.sort(key=lambda it: -it[0])
    return allitems[:k]
