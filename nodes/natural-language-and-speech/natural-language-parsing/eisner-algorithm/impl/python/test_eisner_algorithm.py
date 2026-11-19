# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/eisner-algorithm/. The authors are listed in prov/JTW3A2.jsonl.

import itertools
import math
import random
from fractions import Fraction as F

import pytest

from eisner_algorithm import eisner, eisner_inside, is_projective, is_tree, tree_score
from nlslog import COUNTING, LOG, PROB, log_sum

# John saw Mary, words 1..3; the matrix is scores[h][d].
JOHN_SAW_MARY = [
    [0, 9, 10, 9],
    [0, 0, 20, 3],
    [0, 30, 0, 30],
    [0, 11, 0, 0],
]


def all_trees(n):
    """Brute force: every head list of n words that forms a tree rooted at 0."""
    out = []
    for hs in itertools.product(range(n + 1), repeat=n):
        heads = [-1] + list(hs)
        if is_tree(heads):
            out.append(heads)
    return out


TREES = {n: all_trees(n) for n in range(1, 6)}
PROJ = {n: [t for t in TREES[n] if is_projective(t)] for n in TREES}


def root_children(heads):
    return sum(1 for h in heads[1:] if h == 0)


def random_scores(rng, n, lo=-10, hi=10):
    return [[rng.randint(lo, hi) for _ in range(n + 1)] for _ in range(n + 1)]


def test_tree_counts():
    assert [len(TREES[n]) for n in range(1, 6)] == [1, 3, 16, 125, 1296]
    assert [len(PROJ[n]) for n in range(1, 6)] == [1, 3, 12, 55, 273]
    single = [sum(1 for t in PROJ[n] if root_children(t) == 1) for n in range(1, 6)]
    assert single == [1, 2, 7, 30, 143]


def test_counting_semiring_gives_projective_counts():
    for n in range(1, 6):
        ones = [[1] * (n + 1) for _ in range(n + 1)]
        assert eisner_inside(ones, COUNTING) == len(PROJ[n])
        assert eisner_inside(ones, COUNTING, single_root=True) == sum(
            1 for t in PROJ[n] if root_children(t) == 1
        )
    ones = [[1] * 11 for _ in range(11)]
    # Projective trees over n words rooted at 0: 1, 3, 12, 55, 273, 1428, 7752, 43263, 246675, 1430715.
    assert eisner_inside(ones, COUNTING) == 1430715


def test_example_john_saw_mary():
    score, heads = eisner(JOHN_SAW_MARY)
    assert score == 70
    assert heads == [-1, 2, 0, 2]


@pytest.mark.parametrize("single_root", [False, True])
def test_against_brute_force(single_root):
    rng = random.Random(7)
    for n in range(1, 6):
        for _ in range(30 if n < 5 else 12):
            s = random_scores(rng, n)
            pool = [t for t in PROJ[n] if not single_root or root_children(t) == 1]
            best = max(tree_score(s, t) for t in pool)
            score, heads = eisner(s, single_root=single_root)
            assert score == best
            assert is_tree(heads) and is_projective(heads)
            assert tree_score(s, heads) == score
            if single_root:
                assert root_children(heads) == 1


def test_exact_fractions():
    rng = random.Random(11)
    n = 4
    s = [[F(rng.randint(-20, 20), rng.randint(1, 7)) for _ in range(n + 1)] for _ in range(n + 1)]
    score, heads = eisner(s)
    assert score == max(tree_score(s, t) for t in PROJ[n])
    assert isinstance(score, F)


def test_best_projective_can_lose_to_a_non_projective_tree():
    # The non-projective tree 0 -> 2, 2 -> 4, 4 -> 1, 2 -> 3 gets the high scores.
    n = 4
    s = [[0] * (n + 1) for _ in range(n + 1)]
    s[0][2] = s[2][4] = s[4][1] = s[2][3] = 10
    nonproj = [-1, 4, 0, 2, 2]
    assert is_tree(nonproj) and not is_projective(nonproj)
    score, heads = eisner(s)
    assert tree_score(s, nonproj) == 40
    assert score == max(tree_score(s, t) for t in PROJ[n]) < 40
    assert max(tree_score(s, t) for t in TREES[n]) == 40


def test_log_partition_function():
    rng = random.Random(3)
    for n in range(1, 6):
        s = [[rng.uniform(-2, 2) for _ in range(n + 1)] for _ in range(n + 1)]
        logz = eisner_inside(s, LOG)
        assert logz == pytest.approx(log_sum(tree_score(s, t) for t in PROJ[n]), abs=1e-9)


def test_log_space_avoids_underflow():
    n = 10
    s = [[-100.0] * (n + 1) for _ in range(n + 1)]
    probs = [[math.exp(x) for x in row] for row in s]
    # Each tree has probability exp(-1000), which is 0.0 in double precision.
    assert eisner_inside(probs, PROB) == 0.0
    assert eisner_inside(s, LOG) == pytest.approx(-1000.0 + math.log(1430715), abs=1e-9)


def test_small_inputs():
    assert eisner([[0]]) == (0, [-1])
    assert eisner([[0, 5], [0, 0]]) == (5, [-1, 0])
    with pytest.raises(ValueError):
        eisner([[0, 1]])
