# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/quartet-max-cut/. The authors are listed in prov/GXXKFF.jsonl.

"""Quartet MaxCut (Snir and Rao): divide and conquer quartet amalgamation.

A quartet is ((a, b), (c, d)) for the split ab|cd. Taxa are ints. For a set S
of taxa and the quartets on S, the method builds a graph: each quartet ab|cd
adds the bad edges ab and cd and the good edges ac, ad, bc and bd. It looks for
a cut (S1, S2), both sides of size two or more, with the largest ratio of good
to bad edges across the cut. It finds that ratio by the Dinkelbach iteration
on the score G(cut) - alpha * B(cut). Each side gets an artificial taxon that
stands for the other side, and a quartet with three taxa on one side goes to
that side with the fourth taxon replaced by the artificial one. The two trees
are joined at the artificial taxa. Sets of at most three taxa, or sets without
quartets, become stars.

The max cut is found exactly by trying all cuts when |S| <= exact_limit, and
by a seeded local search otherwise, so the method is a heuristic for maximum
quartet consistency. The exact cut costs O(2^s * m) time for s taxa and m
quartets per Dinkelbach step.
"""

import random
from fractions import Fraction
from typing import Dict, List, Optional, Sequence, Set, Tuple

Quartet = Tuple[Tuple[int, int], Tuple[int, int]]
Edge = Tuple[int, int]


def _cut_score(side: Dict[int, int], quartets: Sequence[Quartet]) -> Tuple[int, int]:
    """Good and bad edges across the cut; side[x] is 0 or 1."""
    good = bad = 0
    for (a, b), (c, d) in quartets:
        bad += (side[a] != side[b]) + (side[c] != side[d])
        good += (side[a] != side[c]) + (side[a] != side[d]) + (side[b] != side[c]) + (side[b] != side[d])
    return good, bad


def _best_cut(taxa: List[int], quartets: Sequence[Quartet], alpha: Fraction, exact_limit: int, rng: random.Random) -> Tuple[Fraction, Dict[int, int], int, int]:
    """Maximize G - alpha * B over cuts with two or more taxa on each side."""
    s = len(taxa)
    best: Optional[Tuple[Fraction, Dict[int, int], int, int]] = None
    if s <= exact_limit:
        for mask in range(1, 1 << (s - 1)):
            ones = bin(mask).count("1")
            if ones < 2 or s - ones < 2:
                continue
            side = {taxa[i]: (mask >> i) & 1 for i in range(s)}
            g, b = _cut_score(side, quartets)
            v = g - alpha * b
            if best is None or v > best[0]:
                best = (v, side, g, b)
        assert best is not None
        return best
    for _ in range(8):
        order = taxa[:]
        rng.shuffle(order)
        half = s // 2
        side = {x: (1 if i < half else 0) for i, x in enumerate(order)}
        g, b = _cut_score(side, quartets)
        v = g - alpha * b
        improved = True
        while improved:
            improved = False
            for x in order:
                ones = sum(side.values())
                if (side[x] == 1 and ones <= 2) or (side[x] == 0 and s - ones <= 2):
                    continue
                side[x] ^= 1
                g2, b2 = _cut_score(side, quartets)
                v2 = g2 - alpha * b2
                if v2 > v:
                    g, b, v = g2, b2, v2
                    improved = True
                else:
                    side[x] ^= 1
        if best is None or v > best[0]:
            best = (v, dict(side), g, b)
    assert best is not None
    return best


def max_ratio_cut(taxa: List[int], quartets: Sequence[Quartet], exact_limit: int = 12, rng: Optional[random.Random] = None) -> Dict[int, int]:
    """Cut with the largest ratio of good to bad edges, by Dinkelbach's iteration."""
    rng = rng or random.Random(0)
    alpha = Fraction(0)
    _, side, g, b = _best_cut(taxa, quartets, alpha, exact_limit, rng)  # @line L4
    while b > 0:  # @line L5
        alpha = Fraction(g, b)
        v, side2, g2, b2 = _best_cut(taxa, quartets, alpha, exact_limit, rng)  # @line L5
        if v <= 0:
            break
        side, g, b = side2, g2, b2
    return side


def quartet_max_cut(taxa: Sequence[int], quartets: Sequence[Quartet], exact_limit: int = 12, rng: Optional[random.Random] = None) -> Tuple[List[Edge], int]:
    """Return (edges, satisfied): an unrooted tree on taxa, and the number of quartets that the cuts satisfied.

    Leaves keep their labels. Internal nodes and artificial taxa get new labels
    larger than every taxon. Each quartet must have four distinct taxa of the set.
    """
    rng = rng or random.Random(0)
    taxa = list(taxa)
    if len(set(taxa)) != len(taxa):
        raise ValueError("a taxon occurs twice")
    tset = set(taxa)
    for (a, b), (c, d) in quartets:
        if len({a, b, c, d}) != 4 or not {a, b, c, d} <= tset:
            raise ValueError("a quartet needs four distinct taxa of the set")
    nxt = [max(taxa, default=-1) + 1]

    def fresh() -> int:
        nxt[0] += 1
        return nxt[0] - 1

    satisfied = 0
    result: Dict[int, List[Edge]] = {}
    tasks: List[Tuple[str, int, list, list]] = [("solve", 0, taxa, list(quartets))]
    plans: Dict[int, Tuple[int, int, int, int]] = {}
    count = 1
    while tasks:  # @line L1
        kind, tid, s, q = tasks.pop()
        if kind == "join":  # @line L10
            c1, c2, x1, x2 = plans[tid]
            result[tid] = _join(result.pop(c1), result.pop(c2), x1, x2)
            continue
        if len(s) <= 3 or not q:  # @line L2
            result[tid] = _star(s, fresh)
            continue
        side = max_ratio_cut(sorted(s), q, exact_limit, rng)  # @line L3
        s1 = [x for x in s if side[x] == 1]
        s2 = [x for x in s if side[x] == 0]
        x1, x2 = fresh(), fresh()  # @line L6
        q1: List[Quartet] = []
        q2: List[Quartet] = []
        for quart in q:  # @line L7
            (a, b), (c, d) = quart
            ones = side[a] + side[b] + side[c] + side[d]
            if ones == 2:
                if side[a] == side[b]:
                    satisfied += 1  # @line L8
                continue
            if ones >= 3:
                q1.append(_replace(quart, side, 0, x1))  # @line L9
            if ones <= 1:
                q2.append(_replace(quart, side, 1, x2))  # @line L9
        c1, c2 = count, count + 1
        count += 2
        plans[tid] = (c1, c2, x1, x2)
        tasks.append(("join", tid, [], []))
        tasks.append(("solve", c1, s1 + [x1], q1))
        tasks.append(("solve", c2, s2 + [x2], q2))
    return result[0], satisfied  # @line L11


def _replace(quart: Quartet, side: Dict[int, int], other: int, art: int) -> Quartet:
    """Replace the taxon on side `other` (at most one) by the artificial taxon."""
    (a, b), (c, d) = quart
    f = lambda x: art if side[x] == other else x  # noqa: E731
    return ((f(a), f(b)), (f(c), f(d)))


def _star(s: List[int], fresh) -> List[Edge]:
    if len(s) == 1:
        return []
    if len(s) == 2:
        return [(s[0], s[1])]
    c = fresh()
    return [(c, x) for x in s]


def _join(e1: List[Edge], e2: List[Edge], x1: int, x2: int) -> List[Edge]:
    """Glue the trees at the leaves x1 and x2: their neighbors become adjacent."""
    def cut(edges: List[Edge], x: int) -> Tuple[List[Edge], int]:
        rest, nb = [], -1
        for u, v in edges:
            if u == x:
                nb = v
            elif v == x:
                nb = u
            else:
                rest.append((u, v))
        return rest, nb

    r1, p = cut(e1, x1)
    r2, q = cut(e2, x2)
    return r1 + r2 + [(p, q)]


def splits(edges: List[Edge], taxa: Sequence[int]) -> Set[frozenset]:
    """Nontrivial splits of the tree, each as the side that does not hold min(taxa)."""
    adj: Dict[int, List[int]] = {}
    for u, v in edges:
        adj.setdefault(u, []).append(v)
        adj.setdefault(v, []).append(u)
    tset = set(taxa)
    ref = min(taxa)
    out: Set[frozenset] = set()
    for u, v in edges:
        seen = {u, v}
        stack = [v]
        part = set()
        while stack:
            x = stack.pop()
            if x in tset:
                part.add(x)
            for y in adj[x]:
                if y not in seen:
                    seen.add(y)
                    stack.append(y)
        if ref in part:
            part = tset - part
        if 2 <= len(part) <= len(tset) - 2:
            out.add(frozenset(part))
    return out


def displayed(sp: Set[frozenset], taxa: Sequence[int], quart: Quartet) -> bool:
    """Does the tree with the splits sp display the quartet?"""
    (a, b), (c, d) = quart
    tset = frozenset(taxa)
    for s in sp:
        for part in (s, tset - s):
            if a in part and b in part and c not in part and d not in part:
                return True
    return False
