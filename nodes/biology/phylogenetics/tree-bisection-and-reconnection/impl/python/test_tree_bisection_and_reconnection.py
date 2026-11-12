# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tree-bisection-and-reconnection/. The authors are listed in prov/S23RH6.jsonl.

import random
from fractions import Fraction

from tree_bisection_and_reconnection import (
    all_trees,
    gamma,
    splits,
    tbr_hill_climb,
    tbr_neighbors,
    topology,
)


def restrict(split_set, keep):
    keep = frozenset(keep)
    ref = min(keep)
    out = set()
    for s in split_set:
        a = s & keep
        b = keep - a
        if len(a) >= 2 and len(b) >= 2:
            out.add(a if ref not in a else b)
    return frozenset(out)


def is_tbr_pair_brute(s1, s2, n):
    """T2 is one TBR move from T1 when the trees differ and some split A|B of both trees
    has T1|A = T2|A and T1|B = T2|B (cut that edge in each tree to get the same forest)."""
    everything = frozenset(range(n))
    if restrict(s1, everything) == restrict(s2, everything):
        return False
    for a in s1 & s2:
        b = everything - a
        if restrict(s1, a) == restrict(s2, a) and restrict(s1, b) == restrict(s2, b):
            return True
    return False


def caterpillar_size(n):
    return Fraction(2, 3) * n**3 - 4 * n**2 + Fraction(16, 3) * n + 2


def test_exact_size_on_all_small_trees():
    for n in range(4, 8):
        for t in all_trees(n):
            size = len(tbr_neighbors(t, n))
            assert size == 4 * gamma(t, n) - (4 * n - 2) * (n - 3)
            assert size <= (2 * n - 3) * (n - 3) ** 2
            assert size <= caterpillar_size(n)


def test_caterpillar_attains_maximum():
    for n in range(4, 9):
        # caterpillar 0-(1)-(2)-...-(n-1): internal vertices n .. 2n-3 in a path
        t = {i: set() for i in range(2 * n - 2)}

        def link(x, y):
            t[x].add(y)
            t[y].add(x)

        path = list(range(n, 2 * n - 2))
        for a, b in zip(path, path[1:]):
            link(a, b)
        link(0, path[0])
        link(1, path[0])
        for i in range(2, n - 2):
            link(i, path[i - 1])
        link(n - 2, path[-1])
        link(n - 1, path[-1])
        assert len(tbr_neighbors(t, n)) == caterpillar_size(n)


def test_neighbors_match_brute_force_definition():
    for n in range(4, 8):
        trees = all_trees(n)
        full = [set(splits(t, n)) for t in trees]
        step = max(1, len(trees) // 10)
        for i in range(0, len(trees), step):
            got = {topology(x, n) for x in tbr_neighbors(trees[i], n)}
            want = {restrict(full[j], range(n)) for j in range(len(trees)) if is_tbr_pair_brute(full[i], full[j], n)}
            assert got == want


def test_small_cases_reach_every_tree():
    # With 4 taxa one TBR move reaches both other trees. With 5 taxa it reaches 12 of the
    # other 14 trees. A 5-taxon tree is (cherry, middle leaf, cherry). The two trees out of
    # reach keep the middle leaf and pair the other four leaves into two new cherries.
    for n, size in ((4, 2), (5, 12)):
        for t in all_trees(n):
            assert len(tbr_neighbors(t, n)) == size


def fitch(tree, n, columns):
    parent = {0: -1}
    order = [0]
    stack = [0]
    while stack:
        v = stack.pop()
        for w in tree[v]:
            if w not in parent:
                parent[w] = v
                order.append(w)
                stack.append(w)
    total = 0
    for col in columns:
        sets = {}
        for v in reversed(order[1:]):
            kids = [w for w in tree[v] if parent.get(w) == v]
            if not kids:
                sets[v] = {col[v]}
                continue
            a, b = sets[kids[0]], sets[kids[1]]
            sets[v] = a & b if a & b else a | b
            total += 0 if a & b else 1
        total += 0 if col[0] in sets[order[1]] else 1
    return total


def test_hill_climb_local_optimum():
    rng = random.Random(8)
    for _ in range(8):
        n = rng.randint(5, 7)
        cols = ["".join(rng.choice("ACGT") for _ in range(n)) for _ in range(10)]
        trees = all_trees(n)
        best, s = tbr_hill_climb(rng.choice(trees), n, lambda t: fitch(t, n, cols))
        assert s == fitch(best, n, cols)
        assert all(fitch(x, n, cols) >= s for x in tbr_neighbors(best, n))
        assert s >= min(fitch(t, n, cols) for t in trees)
