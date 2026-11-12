# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sankoff-algorithm/. The authors are listed in prov/AZ0KEP.jsonl.

import itertools
import math
import random

from sankoff_algorithm import labeling_cost, sankoff, unit_cost

DNA = "ACGT"
TRANSITIONS = {("A", "G"), ("G", "A"), ("C", "T"), ("T", "C")}
# transitions cost 1 and transversions cost 2
TS_TV = {a: {b: 0 if a == b else (1 if (a, b) in TRANSITIONS else 2) for b in DNA} for a in DNA}

# The example of the page: ((A,C),(T,(G,A))).
EX_CHILDREN = [[], [], [], [], [], [0, 1], [3, 4], [2, 6], [5, 7]]
EX_LEAVES = {0: "A", 1: "C", 2: "T", 3: "G", 4: "A"}


def random_tree(rng: random.Random, n: int, binary: bool) -> tuple[list[list[int]], int]:
    """A random rooted tree with leaves 0..n-1. Non-binary trees join 2 or 3 subtrees at a time."""
    children: list[list[int]] = [[] for _ in range(n)]
    pool = list(range(n))
    while len(pool) > 1:
        size = 2 if binary or len(pool) == 2 else rng.choice([2, 3])
        group = rng.sample(pool, size)
        for g in group:
            pool.remove(g)
        children.append(group)
        pool.append(len(children) - 1)
    return children, pool[0]


def brute_force(children, leaf_state, alphabet, cost):
    internal = [v for v in range(len(children)) if children[v]]
    best = math.inf
    for states in itertools.product(alphabet, repeat=len(internal)):
        label = dict(leaf_state)
        label.update(zip(internal, states))
        best = min(best, labeling_cost(children, label, cost))
    return best


def test_example() -> None:
    score, table, label = sankoff(EX_CHILDREN, 8, EX_LEAVES, DNA, TS_TV)
    assert score == 5
    assert [table[5][a] for a in DNA] == [2, 2, 3, 3]
    assert [table[6][a] for a in DNA] == [1, 4, 1, 4]
    assert [table[7][a] for a in DNA] == [3, 4, 3, 3]
    assert [table[8][a] for a in DNA] == [5, 6, 6, 6]
    assert [label[v] for v in (5, 6, 7, 8)] == ["A", "A", "A", "A"]
    assert labeling_cost(EX_CHILDREN, label, TS_TV) == 5


def test_unit_cost_example() -> None:
    leaves = {0: "A", 1: "C", 2: "C", 3: "G", 4: "A"}
    assert sankoff(EX_CHILDREN, 8, leaves, DNA, unit_cost(DNA))[0] == 3


def test_edges() -> None:
    score, table, label = sankoff([[]], 0, {0: "G"}, DNA, TS_TV)
    assert score == 0 and label == {0: "G"}
    # a node with one child
    assert sankoff([[], [0]], 1, {0: "C"}, DNA, TS_TV)[0] == 0
    # forbidden changes: only A -> C is allowed
    one_way = {a: {b: (0 if a == b else (1 if (a, b) == ("A", "C") else math.inf)) for b in "AC"} for a in "AC"}
    assert sankoff([[], [], [0, 1]], 2, {0: "A", 1: "C"}, "AC", one_way)[0] == 1
    reverse = {a: {b: one_way[b][a] for b in "AC"} for a in "AC"}
    assert sankoff([[], [], [0, 1]], 2, {0: "A", 1: "C"}, "AC", reverse)[0] == 1
    assert sankoff([[], [], [2], [0, 1]], 3, {0: "C", 1: "C"}, "AC", one_way)[0] == 0


def test_against_brute_force() -> None:
    rng = random.Random(11)
    for trial in range(500):
        n = rng.randint(1, 6)
        children, root = random_tree(rng, n, binary=trial % 2 == 0)
        alphabet = DNA[: rng.randint(2, 4)]
        leaves = {v: rng.choice(alphabet) for v in range(n)}
        cost = {
            a: {b: 0 if a == b else rng.choice([1, 2, 3, 5, math.inf]) for b in alphabet}
            for a in alphabet
        }
        score, table, label = sankoff(children, root, leaves, alphabet, cost)
        assert score == brute_force(children, leaves, alphabet, cost)
        if score < math.inf:
            assert labeling_cost(children, label, cost) == score
            assert all(label[v] == leaves[v] for v in range(n))


def test_unit_cost_counts_changes() -> None:
    rng = random.Random(3)
    for _ in range(200):
        n = rng.randint(2, 6)
        children, root = random_tree(rng, n, binary=False)
        leaves = {v: rng.choice(DNA) for v in range(n)}
        score = sankoff(children, root, leaves, DNA, unit_cost(DNA))[0]
        assert score == brute_force(children, leaves, DNA, unit_cost(DNA))


def test_deep_tree() -> None:
    n = 2000
    children: list[list[int]] = [[] for _ in range(n)]
    children.append([0, 1])
    for v in range(2, n):
        children.append([len(children) - 1, v])
    leaves = {v: "AG"[v % 2] for v in range(n)}
    assert sankoff(children, len(children) - 1, leaves, DNA, TS_TV)[0] == n // 2
