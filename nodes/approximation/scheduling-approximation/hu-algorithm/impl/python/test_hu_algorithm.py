# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hu-algorithm/. The authors are listed in prov/7VB7QV.jsonl.

import itertools
import random

from hu_algorithm import hu_algorithm, hu_lower_bound, levels


def check_feasible(succ, m, slot):
    n = len(succ)
    assert len(slot) == n
    assert all(s >= 1 for s in slot)
    for t in set(slot):
        assert sum(1 for s in slot if s == t) <= m
    for j in range(n):
        if succ[j] is not None:
            assert slot[j] < slot[succ[j]]


def brute_opt(pred_lists, n, m):
    """Least makespan of unit jobs under precedence, by breadth-first search over done sets."""
    predm = [sum(1 << p for p in pred_lists[v]) for v in range(n)]
    full = (1 << n) - 1
    frontier, t = {0}, 0
    while full not in frontier:
        t += 1
        nxt = set()
        for done in frontier:
            av = [v for v in range(n) if not done >> v & 1 and predm[v] & done == predm[v]]
            for c in itertools.combinations(av, min(m, len(av))):
                nxt.add(done | sum(1 << v for v in c))
        frontier = nxt
    return t


def random_in_forest(rng, n):
    """A random in-forest: job j points to a later job or is a root, then relabel."""
    succ = [None] * n
    for j in range(n - 1):
        if rng.random() < 0.85:
            succ[j] = rng.randrange(j + 1, n)
    perm = list(range(n))
    rng.shuffle(perm)
    out = [None] * n
    for j in range(n):
        out[perm[j]] = None if succ[j] is None else perm[succ[j]]
    return out


NAMES = "r p q a b c d e f g h i".split()
PARENT = {"p": "r", "q": "r", "a": "p", "b": "p", "c": "p", "d": "q", "e": "a", "f": "a", "g": "d", "h": "e", "i": "g"}


def example():
    idx = {x: k for k, x in enumerate(NAMES)}
    return [idx[PARENT[x]] if x in PARENT else None for x in NAMES], idx


def test_page_example():
    succ, idx = example()
    lv = levels(succ)
    assert [lv[idx[x]] for x in NAMES] == [1, 2, 2, 3, 3, 3, 3, 4, 4, 4, 5, 5]
    slot = hu_algorithm(succ, 3)
    check_feasible(succ, 3, slot)
    rows = [sorted(x for x in NAMES if slot[idx[x]] == t) for t in range(1, max(slot) + 1)]
    assert rows == [["f", "h", "i"], ["b", "e", "g"], ["a", "c", "d"], ["p", "q"], ["r"]]
    assert hu_lower_bound(succ, 3) == 5
    assert max(hu_algorithm(succ, 2)) == 7 == hu_lower_bound(succ, 2)


def test_edges():
    assert hu_algorithm([], 2) == []
    assert hu_algorithm([None], 3) == [1]
    chain = [1, 2, 3, None]
    assert hu_algorithm(chain, 4) == [1, 2, 3, 4]
    star = [4, 4, 4, 4, None]
    assert max(hu_algorithm(star, 2)) == 3
    assert max(hu_algorithm(star, 1)) == 5
    assert max(hu_algorithm([None] * 7, 3)) == 3


def test_against_brute_force():
    rng = random.Random(2024)
    for _ in range(500):
        n = rng.randint(1, 9)
        m = rng.randint(1, 4)
        succ = random_in_forest(rng, n)
        slot = hu_algorithm(succ, m)
        check_feasible(succ, m, slot)
        preds = [[i for i in range(n) if succ[i] == v] for v in range(n)]
        best = brute_opt(preds, n, m)
        assert max(slot) == best
        assert hu_lower_bound(succ, m) == best


def test_out_tree_by_reversal():
    """An out-tree reversed is an in-tree; reversing Hu's schedule in time is optimal for it."""
    rng = random.Random(77)
    for _ in range(200):
        n = rng.randint(1, 8)
        m = rng.randint(2, 3)
        succ = random_in_forest(rng, n)
        slot = hu_algorithm(succ, m)
        c = max(slot)
        rev = [c + 1 - s for s in slot]
        for j in range(n):
            if succ[j] is not None:
                assert rev[succ[j]] < rev[j]
        out_preds = [[succ[v]] if succ[v] is not None else [] for v in range(n)]
        assert c == brute_opt(out_preds, n, m)
