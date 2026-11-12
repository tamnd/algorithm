# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fitch-algorithm/. The authors are listed in prov/NYTSYT.jsonl.

import itertools
import random
from collections import Counter

import pytest

from fitch_algorithm import changes, fitch, fitch_score

DNA = "ACGT"

# The example of the page: ((A,C),(C,(G,A))) as nodes 0..8.
# Leaves 0..4 hold A, C, C, G, A; node 5 = (0,1), node 6 = (3,4),
# node 7 = (2,6), node 8 = (5,7) is the root.
EX_CHILDREN = [[], [], [], [], [], [0, 1], [3, 4], [2, 6], [5, 7]]
EX_LEAVES = {0: "A", 1: "C", 2: "C", 3: "G", 4: "A"}


def random_binary_tree(rng: random.Random, n: int) -> tuple[list[list[int]], int]:
    """A random rooted binary tree with leaves 0..n-1, made by random joins."""
    children: list[list[int]] = [[] for _ in range(n)]
    pool = list(range(n))
    while len(pool) > 1:
        a, b = rng.sample(pool, 2)
        pool.remove(a)
        pool.remove(b)
        children.append([a, b])
        pool.append(len(children) - 1)
    return children, pool[0]


def brute_force(children, leaf_state, alphabet):
    """Least number of changes over all internal labelings, and the optimal labelings."""
    internal = [v for v in range(len(children)) if children[v]]
    best, optimal = None, []
    for states in itertools.product(alphabet, repeat=len(internal)):
        label = dict(leaf_state)
        label.update(zip(internal, states))
        c = changes(children, label)
        if best is None or c < best:
            best, optimal = c, [label]
        elif c == best:
            optimal.append(label)
    return best, optimal


def test_example() -> None:
    score, sets, label = fitch(EX_CHILDREN, 8, EX_LEAVES)
    assert score == 3
    assert sets[5] == {"A", "C"}
    assert sets[6] == {"A", "G"}
    assert sets[7] == {"A", "C", "G"}
    assert sets[8] == {"A", "C"}
    assert label == {8: "A", 5: "A", 7: "A", 0: "A", 1: "C", 2: "C", 6: "A", 3: "G", 4: "A"}
    assert changes(EX_CHILDREN, label) == 3


def test_example_first_pass_is_not_the_optimal_set() -> None:
    best, optimal = brute_force(EX_CHILDREN, EX_LEAVES, DNA)
    assert best == 3
    at = {v: {lab[v] for lab in optimal} for v in (5, 6, 7, 8)}
    assert at[8] == {"A", "C"}  # the root set is exact
    assert at[6] == {"A", "C", "G"}  # the first pass gave {A, G}
    assert at[7] == {"A", "C"}  # the first pass gave {A, C, G}
    assert len(optimal) == 4


def test_edges() -> None:
    assert fitch([[]], 0, {0: "A"}) == (0, {0: frozenset("A")}, {0: "A"})
    assert fitch([[], [], [0, 1]], 2, {0: "A", 1: "A"})[0] == 0
    assert fitch([[], [], [0, 1]], 2, {0: "A", 1: "G"})[0] == 1
    with pytest.raises(ValueError):
        fitch([[], [], [], [0, 1, 2]], 3, {0: "A", 1: "C", 2: "G"})


def test_sequences() -> None:
    seqs = {0: "AAG", 1: "CAG", 2: "CAT", 3: "GTT", 4: "AAT"}
    assert fitch_score(EX_CHILDREN, 8, seqs) == 3 + 1 + 1
    assert fitch_score(EX_CHILDREN, 8, {}) == 0


def test_against_brute_force() -> None:
    rng = random.Random(7)
    for _ in range(600):
        n = rng.randint(2, 6)
        children, root = random_binary_tree(rng, n)
        k = rng.randint(2, 4)
        leaves = {v: rng.choice(DNA[:k]) for v in range(n)}
        score, sets, label = fitch(children, root, leaves)
        best, optimal = brute_force(children, leaves, DNA)
        assert score == best
        assert changes(children, label) == best
        assert all(label[v] == leaves[v] for v in range(n))
        assert sets[root] == {lab[root] for lab in optimal}


def insertions(tree, leaf):
    """All rooted binary trees made by putting `leaf` on an edge of `tree` or above its root."""
    out = [(tree, leaf)]
    if isinstance(tree, tuple):
        left, right = tree
        out += [(t, right) for t in insertions(left, leaf)]
        out += [(left, t) for t in insertions(right, leaf)]
    return out


def all_trees(n: int) -> list[tuple[list[list[int]], int]]:
    """Every unrooted binary tree on leaves 0..n-1 (n >= 3), rooted on the edge of leaf 0."""
    rooted = [(1, 2)]
    for leaf in range(3, n):
        rooted = [t for r in rooted for t in insertions(r, leaf)]
    out = []
    for r in rooted:
        children: list[list[int]] = [[] for _ in range(n)]
        stack, ids = [(0, r)], {}
        # give ids to the internal nodes, parents first, then fill the lists
        order = []
        while stack:
            _, t = stack.pop()
            if isinstance(t, tuple):
                ids[id(t)] = len(children)
                children.append([])
                order.append(t)
                stack.extend((0, s) for s in t)
        for t in order:
            children[ids[id(t)]] = [ids[id(s)] if isinstance(s, tuple) else s for s in t]
        children.append([0, ids[id(r)]])
        out.append((children, len(children) - 1))
    return out


def clusters(children, root) -> set[frozenset[int]]:
    """The leaf sets below the internal nodes, except the root and its big child."""
    below: dict[int, frozenset[int]] = {}
    stack = [(root, False)]
    while stack:
        v, done = stack.pop()
        if not children[v]:
            below[v] = frozenset([v])
        elif done:
            below[v] = frozenset().union(*(below[w] for w in children[v]))
        else:
            stack.append((v, True))
            stack.extend((w, False) for w in children[v])
    n = sum(1 for ws in children if not ws)
    return {s for s in below.values() if 2 <= len(s) <= n - 2}


def test_number_of_trees() -> None:
    assert [len(all_trees(n)) for n in (3, 4, 5, 6)] == [1, 3, 15, 105]
    assert len({frozenset(clusters(c, r)) for c, r in all_trees(6)}) == 105


def test_maximum_parsimony_five_taxa() -> None:
    rows = ["AAGTTCGA", "AAGCTCGA", "AGGCTTGC", "GGACTTGC", "GGACATAC"]
    seqs = dict(enumerate(rows))
    scored = [(fitch_score(c, r, seqs), clusters(c, r)) for c, r in all_trees(5)]
    assert Counter(s for s, _ in scored) == {8: 1, 10: 2, 11: 2, 13: 10}
    best = min(scored, key=lambda p: p[0])
    # ((S1, S2), S3, (S4, S5)): the clusters away from S1 are {S4, S5} and {S3, S4, S5}
    assert best[1] == {frozenset({3, 4}), frozenset({2, 3, 4})}
    # sites 4, 5 and 7 cost 1 on every tree
    for site in (3, 4, 6):
        col = {v: s[site] for v, s in seqs.items()}
        assert {fitch(c, r, col)[0] for c, r in all_trees(5)} == {1}


def informative(column) -> bool:
    return sum(1 for c in Counter(column).values() if c >= 2) >= 2


def test_informative_sites_against_all_trees() -> None:
    rng = random.Random(3)
    trees = {n: all_trees(n) for n in (4, 5, 6)}
    for _ in range(300):
        n = rng.randint(4, 6)
        column = [rng.choice(DNA[: rng.randint(2, 4)]) for _ in range(n)]
        col = dict(enumerate(column))
        scores = {fitch(c, r, col)[0] for c, r in trees[n]}
        counts = Counter(column)
        assert min(scores) >= len(counts) - 1
        assert max(scores) <= n - max(counts.values())
        assert (len(scores) > 1) == informative(column)
        if not informative(column):
            assert scores == {len(counts) - 1}


def test_vertex_cover_reduction() -> None:
    # (edges, vertex cover number); taxa: the zero row and one row per edge
    graphs = [
        ([(0, 1), (1, 2)], 1),
        ([(0, 1), (2, 3)], 2),
        ([(0, 1), (1, 2), (0, 2)], 2),
        ([(0, 1), (0, 2), (0, 3)], 1),
        ([(0, 1), (1, 2), (2, 3)], 2),
        ([(0, 1), (1, 2), (2, 3), (3, 0)], 2),
        ([(0, 1), (1, 2), (0, 2), (2, 3)], 2),
        ([(0, 1), (1, 2), (2, 3), (3, 4), (4, 0)], 3),
        ([(0, 1), (0, 2), (0, 3), (0, 4), (1, 2)], 2),
    ]
    for edges, tau in graphs:
        k = 1 + max(max(e) for e in edges)
        rows = ["0" * k] + ["".join("1" if x in e else "0" for x in range(k)) for e in edges]
        seqs = dict(enumerate(rows))
        best = min(fitch_score(c, r, seqs) for c, r in all_trees(len(rows)))
        assert best == len(edges) + tau


def test_tree_with_deep_path() -> None:
    # a caterpillar with 3000 leaves: no recursion limit is hit
    n = 3000
    children: list[list[int]] = [[] for _ in range(n)]
    children.append([0, 1])
    for v in range(2, n):
        children.append([len(children) - 1, v])
    root = len(children) - 1
    leaves = {v: "AC"[v % 2] for v in range(n)}
    assert fitch(children, root, leaves)[0] == n // 2
