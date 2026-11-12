# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hartigan-algorithm/. The authors are listed in prov/HBJAYD.jsonl.

import itertools
import random

from hartigan_algorithm import hartigan

DNA = "ACGT"

# The example of the page: leaves 0..6 hold A G G C A G C,
# node 7 = (0, 1, 2), node 8 = (3, 4), root 9 = (7, 8, 5, 6).
EX_CHILDREN = [[], [], [], [], [], [], [], [0, 1, 2], [3, 4], [7, 8, 5, 6]]
EX_LEAVES = dict(enumerate("AGGCAGC"))


def random_tree(rng: random.Random, n: int) -> tuple[list[list[int]], int]:
    """A random rooted tree with leaves 0..n-1, whose internal nodes have 1 to 4 children."""
    children: list[list[int]] = [[] for _ in range(n)]
    pool = list(range(n))
    while len(pool) > 1 or not children[pool[0]]:
        size = rng.randint(1, min(4, len(pool)))
        if size == 1 and rng.random() < 0.7:
            size = min(2, len(pool))
        group = rng.sample(pool, size)
        for g in group:
            pool.remove(g)
        children.append(group)
        pool.append(len(children) - 1)
    return children, pool[0]


def changes(children, label) -> int:
    return sum(1 for v, ws in enumerate(children) for w in ws if label[v] != label[w])


def brute_force(children, leaf_state):
    """The least number of changes, and for each node the set of its states in optimal labelings."""
    internal = [v for v in range(len(children)) if children[v]]
    best, optimal = None, []
    for states in itertools.product(DNA, repeat=len(internal)):
        label = dict(leaf_state)
        label.update(zip(internal, states))
        c = changes(children, label)
        if best is None or c < best:
            best, optimal = c, [label]
        elif c == best:
            optimal.append(label)
    return best, {v: frozenset(lab[v] for lab in optimal) for v in range(len(children))}


def test_example() -> None:
    score, upper, lower, final = hartigan(EX_CHILDREN, 9, EX_LEAVES)
    assert score == 4
    assert upper[7] == {"G"} and lower[7] == {"A"}
    assert upper[8] == {"A", "C"} and lower[8] == {"G"}
    assert upper[9] == {"C", "G"} and lower[9] == {"A"}
    assert final[9] == {"C", "G"}
    assert final[7] == {"G"}
    assert final[8] == {"A", "C", "G"}
    best, at = brute_force(EX_CHILDREN, EX_LEAVES)
    assert best == 4
    assert all(final[v] == at[v] for v in range(10))


def test_edges() -> None:
    score, upper, lower, final = hartigan([[]], 0, {0: "T"})
    assert score == 0 and final == {0: frozenset("T")}
    # a star: the score is the number of leaves minus the largest count
    star = [[], [], [], [], [], [0, 1, 2, 3, 4]]
    score, upper, _, final = hartigan(star, 5, dict(enumerate("AACCG")))
    assert score == 3 and upper[5] == {"A", "C"} and final[5] == {"A", "C"}
    # a chain of nodes with one child each
    chain = [[], [0], [1], [2]]
    assert hartigan(chain, 3, {0: "G"})[0] == 0
    assert hartigan(chain, 3, {0: "G"})[3] == {0: {"G"}, 1: {"G"}, 2: {"G"}, 3: {"G"}}


def test_against_brute_force() -> None:
    rng = random.Random(5)
    for _ in range(500):
        n = rng.randint(1, 6)
        children, root = random_tree(rng, n)
        if len(children) - n > 6:
            continue
        leaves = {v: rng.choice(DNA[: rng.randint(1, 4)]) for v in range(n)}
        score, upper, lower, final = hartigan(children, root, leaves)
        best, at = brute_force(children, leaves)
        assert score == best
        for v in range(len(children)):
            assert final[v] == at[v], (children, leaves, v)


def test_binary_upper_sets_are_fitch_sets() -> None:
    rng = random.Random(8)
    for _ in range(300):
        n = rng.randint(2, 8)
        children: list[list[int]] = [[] for _ in range(n)]
        pool = list(range(n))
        while len(pool) > 1:
            a, b = rng.sample(pool, 2)
            pool.remove(a)
            pool.remove(b)
            children.append([a, b])
            pool.append(len(children) - 1)
        leaves = {v: rng.choice(DNA) for v in range(n)}
        score, upper, _, _ = hartigan(children, pool[0], leaves)
        # Fitch's first pass, written out here as the reference
        sets, fitch_score = {}, 0
        for v in range(len(children)):
            if not children[v]:
                sets[v] = frozenset([leaves[v]])
            else:
                left, right = (sets[w] for w in children[v])
                sets[v] = left & right or left | right
                fitch_score += not (left & right)
        assert score == fitch_score
        assert all(upper[v] == sets[v] for v in range(len(children)))
