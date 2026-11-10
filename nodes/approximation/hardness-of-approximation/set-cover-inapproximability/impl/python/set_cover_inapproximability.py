# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/set-cover-inapproximability/. The authors are listed in prov/H4FSRY.jsonl.
"""The reduction from label cover to set cover with a partition system.

A game is (nu, nw, su, sw, edges) with edges (u, w, proj), proj[a] the right label that left label a needs.
A partition system is (m, cs): a ground set 0 .. m-1 and sets cs[0 .. sw-1]. For small instances only.
"""

import math
import random
from fractions import Fraction
from itertools import combinations, product

Game = tuple[int, int, int, int, list[tuple[int, int, tuple[int, ...]]]]


def hypercube_system(labels: int) -> tuple[int, list[frozenset[int]]]:
    """Ground set {0,1}^labels as bit masks; C_b holds the points with bit b set."""
    m = 1 << labels
    return m, [frozenset(x for x in range(m) if x >> b & 1) for b in range(labels)]


def has_property(m: int, cs: list[frozenset[int]], h: int) -> bool:
    """True if no h sets among the C_b and their complements cover the ground set without a pair C_b, not C_b."""
    full = frozenset(range(m))
    for size in range(1, min(h, len(cs)) + 1):
        for idx in combinations(range(len(cs)), size):
            for signs in product((0, 1), repeat=size):
                union = set()
                for b, s in zip(idx, signs):
                    union |= cs[b] if s else full - cs[b]
                if len(union) == m:
                    return False
    return True


def random_system(labels: int, h: int, seed: int = 0) -> tuple[int, list[frozenset[int]]]:
    """A partition system with m = ceil(2^h h ln(2 labels)) + 1 points, by random choice and a check."""
    m = math.ceil(2**h * h * math.log(2 * labels)) + 1
    rng = random.Random(seed)
    while True:
        cs = [frozenset(x for x in range(m) if rng.random() < 0.5) for _ in range(labels)]
        if has_property(m, cs, h):
            return m, cs


def reduce(game: Game, system: tuple[int, list[frozenset[int]]]) -> tuple[int, list[frozenset[int]], list[tuple[str, int, int]]]:
    """Universe E x B. S(w, b) = blocks of edges at w, points of C_b. S(u, a) = blocks of edges at u, points outside C_pi(a)."""
    nu, nw, su, sw, edges = game
    m, cs = system
    full = frozenset(range(m))
    sets, names = [], []
    for u in range(nu):
        for a in range(su):
            sets.append(frozenset(i * m + x for i, (eu, _, proj) in enumerate(edges) if eu == u for x in full - cs[proj[a]]))
            names.append(("U", u, a))
    for w in range(nw):
        for b in range(sw):
            sets.append(frozenset(i * m + x for i, (_, ew, _) in enumerate(edges) if ew == w for x in cs[b]))
            names.append(("W", w, b))
    return len(edges) * m, sets, names


def cover_from_labeling(game: Game, left: list[int], right: list[int]) -> list[int]:
    nu, nw, su, sw, _ = game
    return [u * su + left[u] for u in range(nu)] + [nu * su + w * sw + right[w] for w in range(nw)]


def decode(game: Game, names: list[tuple[str, int, int]], chosen: list[int]) -> tuple[list[set[int]], list[set[int]]]:
    """The label lists L(u) and L(w) of a family of sets."""
    nu, nw = game[0], game[1]
    lu: list[set[int]] = [set() for _ in range(nu)]
    lw: list[set[int]] = [set() for _ in range(nw)]
    for j in chosen:
        side, v, lab = names[j]
        (lu if side == "U" else lw)[v].add(lab)
    return lu, lw


def expected_value(game: Game, lu: list[set[int]], lw: list[set[int]]) -> Fraction:
    """The expected fraction of satisfied edges when each vertex takes a uniform label from its list."""
    total = Fraction(0)
    for u, w, proj in game[4]:
        if lu[u] and lw[w]:
            hits = sum(proj[a] == b for a in lu[u] for b in lw[w])
            total += Fraction(hits, len(lu[u]) * len(lw[w]))
    return total / len(game[4])


def is_cover(n: int, sets: list[frozenset[int]], chosen: list[int]) -> bool:
    covered = set()
    for j in chosen:
        covered |= sets[j]
    return len(covered) == n


def min_cover(n: int, sets: list[frozenset[int]]) -> int:
    for size in range(len(sets) + 1):
        for c in combinations(range(len(sets)), size):
            if is_cover(n, sets, list(c)):
                return size
    raise ValueError("no cover")


def value(game: Game) -> Fraction:
    nu, nw, su, sw, edges = game
    best = 0
    for right in product(range(sw), repeat=nw):
        score = [[0] * su for _ in range(nu)]
        for u, w, proj in edges:
            for a in range(su):
                score[u][a] += proj[a] == right[w]
        best = max(best, sum(max(row) for row in score))
    return Fraction(best, len(edges))


def regularize(game: Game) -> Game:
    """Make both sides the same size and every degree equal: |W| copies of each u and |U| copies of each w."""
    nu, nw, su, sw, edges = game
    new_edges = [(u * nw + i, w * nu + j, proj) for u, w, proj in edges for i in range(nw) for j in range(nu)]
    return nu * nw, nw * nu, su, sw, new_edges
