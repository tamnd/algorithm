# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pq-tree/. The authors are listed in prov/HCBMN4.jsonl.
import random
from itertools import permutations

from pq_tree import consecutive_ones_order, frontiers, leaves, reduce, universal


def consecutive(order, s):
    pos = [i for i, x in enumerate(order) if x in s]
    return not pos or pos[-1] - pos[0] == len(pos) - 1


def brute(universe, sets):
    return {p for p in permutations(universe) if all(consecutive(p, s) for s in sets)}


def build(universe, sets):
    t = universal(universe)
    for s in sets:
        t = reduce(t, s)
        if t is None:
            return None
    return t


def check(universe, sets):
    t = build(universe, sets)
    want = brute(universe, sets)
    if t is None:
        assert want == set()
    else:
        assert sorted(leaves(t)) == sorted(universe)
        assert frontiers(t) == want
    return t


def test_example():
    u = [1, 2, 3, 4, 5]
    sets = [{1, 3}, {2, 3, 4}, {4, 5}, {2, 4}]
    t = check(u, sets)
    assert frontiers(t) == {(1, 3, 2, 4, 5), (5, 4, 2, 3, 1)}
    assert consecutive_ones_order(u, sets) in ([1, 3, 2, 4, 5], [5, 4, 2, 3, 1])


def test_example_steps():
    u = [1, 2, 3, 4, 5]
    t = reduce(universal(u), {2, 3, 4})
    assert len(frontiers(t)) == 3 * 2 * 6  # {2,3,4} as one block of a P-node
    t = reduce(t, {4, 5})
    # P(1, Q(P(2, 3), 4, 5)): 2 orders of the root, 2 of the Q-node, 2 of P(2, 3)
    assert t == ("P", [("leaf", 1), ("Q", [("P", [("leaf", 2), ("leaf", 3)]), ("leaf", 4), ("leaf", 5)])])
    assert len(frontiers(t)) == 8
    check(u, [{2, 3, 4}, {4, 5}])


def test_non_examples():
    assert check(list("abc"), [set("ab"), set("bc"), set("ac")]) is None
    assert check(list("abcd"), [set("ab"), set("ac"), set("ad")]) is None
    # clique matrix of a 4-cycle, transposed: each vertex in two consecutive edges
    assert check(["e1", "e2", "e3", "e4"], [{"e1", "e2"}, {"e2", "e3"}, {"e3", "e4"}, {"e4", "e1"}]) is None


def test_edge_cases():
    assert frontiers(universal([7])) == {(7,)}
    check([1, 2, 3], [])
    check([1, 2, 3], [set(), {2}, {1, 2, 3}])
    check([1, 2], [{1, 2}, {1}])
    # the same set twice, and nested sets
    check([1, 2, 3, 4], [{1, 2}, {1, 2}, {1, 2, 3}, {2}])


def test_random_against_brute_force():
    rng = random.Random(4)
    for _ in range(700):
        n = rng.randint(1, 6)
        u = list(range(n))
        sets = []
        for _ in range(rng.randint(0, 5)):
            k = rng.randint(0, n)
            sets.append(set(rng.sample(u, k)))
        check(u, sets)


def test_random_interval_families_always_succeed():
    rng = random.Random(9)
    for _ in range(200):
        n = rng.randint(1, 6)
        hidden = list(range(n))
        rng.shuffle(hidden)
        sets = []
        for _ in range(rng.randint(1, 6)):
            i = rng.randint(0, n - 1)
            j = rng.randint(i, n - 1)
            sets.append(set(hidden[i:j + 1]))
        t = check(list(range(n)), sets)
        assert t is not None and tuple(hidden) in frontiers(t)
