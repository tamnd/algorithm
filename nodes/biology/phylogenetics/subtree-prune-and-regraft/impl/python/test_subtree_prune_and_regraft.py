# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/subtree-prune-and-regraft/. The authors are listed in prov/PCRYBM.jsonl.

import random

from subtree_prune_and_regraft import all_trees, spr_hill_climb, spr_neighbors, splits, topology


def all_splits(tree, n):
    """All 2n - 3 splits as frozensets of the side without leaf 0."""
    return set(splits(tree, n))


def restrict(split_set, n, keep):
    """Topology of the tree restricted to the leaf set keep, from its full split set."""
    keep = frozenset(keep)
    ref = min(keep)
    out = set()
    for s in split_set:
        a = s & keep
        b = keep - a
        if len(a) >= 2 and len(b) >= 2:
            out.add(a if ref not in a else b)
    return frozenset(out)


def is_spr_pair_brute(s1, s2, n):
    """Brute-force test from the definition, using splits only.

    T2 is one SPR move from T1 when there is a split A|B of both trees such that the trees
    agree on B (the part that stays) and on A plus one leaf b of B (the pruned subtree with
    its point of attachment). Both orientations of the split are tried.
    """
    if restrict(s1, n, range(n)) == restrict(s2, n, range(n)):
        return False
    everything = frozenset(range(n))
    for s in s1 & s2:
        for a in (s, everything - s):
            b = everything - a
            if len(b) < 2:
                continue
            pivot = min(b)
            if restrict(s1, n, b) == restrict(s2, n, b) and restrict(s1, n, a | {pivot}) == restrict(
                s2, n, a | {pivot}
            ):
                return True
    return False


def test_count_on_all_small_trees():
    for n in range(4, 8):
        for t in all_trees(n):
            assert len(spr_neighbors(t, n)) == 2 * (n - 3) * (2 * n - 7)


def test_count_on_random_larger_trees():
    rng = random.Random(2024)
    trees8 = all_trees(8)
    for _ in range(15):
        t = rng.choice(trees8)
        assert len(spr_neighbors(t, 8)) == 2 * 5 * 9


def test_neighbors_match_brute_force_definition():
    for n in range(4, 8):
        trees = all_trees(n)
        full = [all_splits(t, n) for t in trees]
        step = max(1, len(trees) // 12)
        for i in range(0, len(trees), step):
            got = {topology(x, n) for x in spr_neighbors(trees[i], n)}
            want = {restrict(full[j], n, range(n)) for j in range(len(trees)) if is_spr_pair_brute(full[i], full[j], n)}
            assert got == want


def test_nni_neighbors_are_spr_neighbors():
    n = 7
    trees = all_trees(n)
    keys = [topology(t, n) for t in trees]
    for i in range(0, len(trees), 97):
        nb = {topology(x, n) for x in spr_neighbors(trees[i], n)}
        nni = {k for k in keys if len(k ^ keys[i]) == 2}
        assert nni <= nb


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


def test_hill_climb_local_optimum_and_bound():
    rng = random.Random(99)
    for _ in range(12):
        n = rng.randint(5, 7)
        cols = ["".join(rng.choice("ACGT") for _ in range(n)) for _ in range(10)]
        trees = all_trees(n)
        best, s = spr_hill_climb(rng.choice(trees), n, lambda t: fitch(t, n, cols))
        assert s == fitch(best, n, cols)
        assert all(fitch(x, n, cols) >= s for x in spr_neighbors(best, n))
        assert s >= min(fitch(t, n, cols) for t in trees)
