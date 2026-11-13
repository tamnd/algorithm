# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/expectiminimax/. The authors are listed in prov/8K5D18.jsonl.

import itertools
import random
from fractions import Fraction

import pytest

from expectiminimax import best_move, expectiminimax, map_leaves

F = Fraction

# The tree of the page: MAX chooses a or b, then a die decides, then MIN chooses.
PAGE_TREE = (
    "max",
    [
        ("chance", [(F(1, 3), ("min", [("leaf", 3), ("leaf", 5)])), (F(2, 3), ("min", [("leaf", 4), ("leaf", 8)]))]),
        ("chance", [(F(1, 2), ("min", [("leaf", 6), ("leaf", 1)])), (F(1, 2), ("min", [("leaf", 9), ("leaf", 7)]))]),
    ],
)


def decision_nodes(root, kind):
    """Paths of all nodes of the given kind, found by an explicit stack."""
    out, stack = [], [(root, ())]
    while stack:
        (k, data), path = stack.pop()
        if k == kind:
            out.append((path, len(data)))
        if k != "leaf":
            for i, c in enumerate(data):
                stack.append((c[1] if k == "chance" else c, path + (i,)))
    return out


def expected_payoff(root, smax, smin):
    """Brute force: sum over every chance outcome of probability times leaf, under fixed pure strategies."""
    total, stack = F(0), [(root, (), F(1))]
    while stack:
        (k, data), path, p = stack.pop()
        if k == "leaf":
            total += p * data
        elif k == "max":
            i = smax[path]
            stack.append((data[i], path + (i,), p))
        elif k == "min":
            i = smin[path]
            stack.append((data[i], path + (i,), p))
        else:
            for i, (q, c) in enumerate(data):
                stack.append((c, path + (i,), p * q))
    return total


def strategies(root, kind):
    nodes = decision_nodes(root, kind)
    for choice in itertools.product(*[range(b) for _, b in nodes]):
        yield {path: c for (path, _), c in zip(nodes, choice)}


def brute_force_value(root):
    smins = list(strategies(root, "min"))
    smaxs = list(strategies(root, "max"))
    table = [[expected_payoff(root, a, b) for b in smins] for a in smaxs]
    maxmin = max(min(row) for row in table)
    minmax = min(max(table[i][j] for i in range(len(smaxs))) for j in range(len(smins)))
    return maxmin, minmax


def clairvoyant_value(root):
    """Expectation over all joint chance outcomes of the minimax value when the outcomes are known in advance."""
    chance = decision_nodes(root, "chance")
    total = F(0)
    for pick in itertools.product(*[range(b) for _, b in chance]):
        fixed = dict(zip([p for p, _ in chance], pick))

        def det(node, path):
            k, data = node
            if k == "leaf":
                return F(data), F(1)
            if k == "chance":
                i = fixed[path]
                v, _ = det(data[i][1], path + (i,))
                return v, F(1)
            vals = [det(c, path + (i,))[0] for i, c in enumerate(data)]
            return (max(vals) if k == "max" else min(vals)), F(1)

        prob = F(1)
        for (path, _), i in zip(chance, pick):
            prob *= _prob_at(root, path, i)
        total += prob * det(root, ())[0]
    return total


def _prob_at(root, path, i):
    node = root
    for step in path:
        k, data = node
        node = data[step][1] if k == "chance" else data[step]
    return F(node[1][i][0])


def random_tree(rng, depth, budget):
    """A random tree; budget[k] limits the number of MAX and MIN nodes so that brute force stays small."""
    if depth == 0:
        return ("leaf", rng.randint(-9, 9))
    kinds = [k for k in ("max", "min") if budget[k] > 0] + ["chance"]
    kind = rng.choice(kinds)
    if kind == "chance":
        k = rng.randint(2, 3)
        cuts = sorted(rng.sample(range(1, 12), k - 1))
        probs = [F(b - a, 12) for a, b in zip([0] + cuts, cuts + [12])]
        return ("chance", [(p, random_tree(rng, depth - 1, budget)) for p in probs])
    budget[kind] -= 1
    return (kind, [random_tree(rng, depth - 1, budget) for _ in range(2)])


def test_page_example():
    count = [0]
    assert expectiminimax(PAGE_TREE, count) == 4
    assert count[0] == 8
    assert best_move(PAGE_TREE) == 1
    assert expectiminimax(PAGE_TREE[1][0]) == F(11, 3)
    assert brute_force_value(PAGE_TREE) == (4, 4)
    # Knowing the dice in advance would be worth more: the order of max and expectation matters.
    assert clairvoyant_value(PAGE_TREE) == F(16, 3)


def test_leaf_and_single_paths():
    assert expectiminimax(("leaf", 7)) == 7
    assert expectiminimax(("chance", [(1, ("leaf", -2))])) == -2
    assert expectiminimax(("min", [("leaf", 5)])) == 5
    with pytest.raises(ValueError):
        best_move(("chance", [(1, ("leaf", 0))]))


def test_no_chance_is_minimax():
    tree = ("max", [("min", [("leaf", 3), ("leaf", 12)]), ("min", [("leaf", 2), ("leaf", 4)]), ("min", [("leaf", 14), ("leaf", 1)])])
    assert expectiminimax(tree) == 3 and best_move(tree) == 0


def test_monotone_transform_changes_decision():
    tree = ("max", [("chance", [(F(1, 2), ("leaf", 2)), (F(1, 2), ("leaf", 10))]), ("leaf", 7)])
    assert expectiminimax(tree) == 7 and best_move(tree) == 1
    squared = map_leaves(tree, lambda v: v * v)
    assert expectiminimax(squared) == 52 and best_move(squared) == 0


def test_monotone_transform_keeps_minimax_decision():
    rng = random.Random(7)
    for _ in range(200):
        tree = ("max", [("min", [("leaf", rng.randint(-9, 9)) for _ in range(3)]) for _ in range(3)])
        cubed = map_leaves(tree, lambda v: v * v * v + 5 * v)
        assert best_move(tree) == best_move(cubed)


def test_deep_chain_no_recursion_limit():
    tree = ("leaf", 1)
    for d in range(5000):
        tree = ("chance", [(F(1, 2), tree), (F(1, 2), ("leaf", 1))]) if d % 2 else ("max", [tree])
    assert expectiminimax(tree) == 1


def test_random_trees_against_brute_force():
    rng = random.Random(1966)
    for _ in range(500):
        tree = random_tree(rng, rng.randint(1, 4), {"max": 3, "min": 3})
        v = expectiminimax(tree)
        maxmin, minmax = brute_force_value(tree)
        assert v == maxmin == minmax


def test_clairvoyance_helps_a_lone_maximizer():
    # With no MIN node, knowing all dice in advance can only help MAX.
    rng = random.Random(1983)
    for _ in range(200):
        tree = random_tree(rng, rng.randint(1, 3), {"max": 4, "min": 0})
        if len(decision_nodes(tree, "chance")) > 6:
            continue
        assert clairvoyant_value(tree) >= expectiminimax(tree)
