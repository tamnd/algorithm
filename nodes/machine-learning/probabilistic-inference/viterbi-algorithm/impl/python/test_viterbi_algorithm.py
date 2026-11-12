# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/viterbi-algorithm/. The authors are listed in prov/KSAB3R.jsonl.

import math
import random
from fractions import Fraction as F
from itertools import product

import pytest

from viterbi_algorithm import NEG_INF, viterbi, viterbi_log

PI = [F(1, 2), F(1, 2)]
A = [[F(7, 10), F(3, 10)], [F(2, 10), F(8, 10)]]
B = [[F(9, 10), F(1, 10)], [F(2, 10), F(8, 10)]]
OBS = [0, 0, 1, 0]


def path_prob(pi, a, b, obs, q):
    p = pi[q[0]] * b[q[0]][obs[0]]
    for t in range(1, len(obs)):
        p *= a[q[t - 1]][q[t]] * b[q[t]][obs[t]]
    return p


def path_score(lp, la, lb, obs, q):
    s = lp[q[0]] + lb[q[0]][obs[0]]
    for t in range(1, len(obs)):
        s = s + la[q[t - 1]][q[t]] + lb[q[t]][obs[t]]
    return s


def brute_best(lp, la, lb, obs):
    """The best path by enumeration, with the page's tie rule:
    the largest score, then the smallest reversed path in lexicographic order."""
    n = len(lp)
    paths = list(product(range(n), repeat=len(obs)))
    best = max(path_score(lp, la, lb, obs, q) for q in paths)
    winners = [q for q in paths if path_score(lp, la, lb, obs, q) == best]
    return list(min(winners, key=lambda q: q[::-1])), best


def rand_row(rng: random.Random, m: int) -> list:
    while True:
        w = [rng.randint(0, 5) for _ in range(m)]
        if sum(w):
            return [F(x, sum(w)) for x in w]


def test_worked_example() -> None:
    path, score = viterbi(PI, A, B, OBS)
    assert path == [0, 0, 0, 0]
    assert path_prob(PI, A, B, OBS, path) == F(250047, 20000000)
    assert math.isclose(score, math.log(0.01250235), rel_tol=1e-12)
    # the second best path R R D R is close behind
    assert path_prob(PI, A, B, OBS, (0, 0, 1, 0)) == F(15309, 1250000)


def test_edges() -> None:
    with pytest.raises(ValueError):
        viterbi(PI, A, B, [])
    assert viterbi([1.0], [[1.0]], [[1.0]], [0, 0, 0]) == ([0, 0, 0], 0.0)
    # impossible sequence: state 0 only emits symbol 0 and never leaves
    with pytest.raises(ValueError):
        viterbi([1.0, 0.0], [[1.0, 0.0], [0.0, 1.0]], [[1.0, 0.0], [0.0, 1.0]], [0, 1])
    assert viterbi(PI, A, B, [1])[0] == [1]


def test_against_brute_force_probabilities() -> None:
    rng = random.Random(1967)
    done = 0
    for _ in range(500):
        n, m, T = rng.randint(1, 3), rng.randint(1, 3), rng.randint(1, 5)
        pi, a, b = rand_row(rng, n), [rand_row(rng, n) for _ in range(n)], [rand_row(rng, m) for _ in range(n)]
        obs = [rng.randrange(m) for _ in range(T)]
        best = max(path_prob(pi, a, b, obs, q) for q in product(range(n), repeat=T))
        if best == 0:
            with pytest.raises(ValueError):
                viterbi(pi, a, b, obs)
            continue
        path, score = viterbi(pi, a, b, obs)
        # float logs may break an exact tie either way, so compare exact probabilities
        assert path_prob(pi, a, b, obs, path) == best
        assert math.isclose(score, math.log(best), rel_tol=1e-12, abs_tol=1e-12)
        done += 1
    assert done > 300


def test_ties_with_exact_weights() -> None:
    # Integer weights (for example log2 of powers of two) make ties exact.
    rng = random.Random(73)
    choices = [0, -1, -1, -2, -3, NEG_INF]
    for _ in range(600):
        n, m, T = rng.randint(1, 3), rng.randint(1, 3), rng.randint(1, 5)
        lp = [rng.choice(choices) for _ in range(n)]
        la = [[rng.choice(choices) for _ in range(n)] for _ in range(n)]
        lb = [[rng.choice(choices) for _ in range(m)] for _ in range(n)]
        obs = [rng.randrange(m) for _ in range(T)]
        ref_path, ref_score = brute_best(lp, la, lb, obs)
        if ref_score == NEG_INF:
            with pytest.raises(ValueError):
                viterbi_log(lp, la, lb, obs)
            continue
        assert viterbi_log(lp, la, lb, obs) == (ref_path, ref_score)


def test_all_paths_tied() -> None:
    n, T = 3, 4
    z = [[0] * n for _ in range(n)]
    assert viterbi_log([0] * n, z, z, [0] * T) == ([0] * T, 0)


def test_tie_rule_prefers_small_last_states() -> None:
    # two optimal paths (0,1) and (1,0); the rule compares q_T first, so (1,0) wins
    lp = [0, 0]
    la = [[NEG_INF, 0], [0, NEG_INF]]
    lb = [[0], [0]]
    assert viterbi_log(lp, la, lb, [0, 0]) == ([1, 0], 0)


def test_long_sequence_no_underflow() -> None:
    rng = random.Random(2)
    pi = [0.5, 0.5]
    a = [[0.9, 0.1], [0.1, 0.9]]
    b = [[0.8, 0.2], [0.3, 0.7]]
    obs = [rng.randrange(2) for _ in range(5000)]
    path, score = viterbi(pi, a, b, obs)
    assert len(path) == 5000 and math.isfinite(score) and score < -2000
    lp, la, lb = [math.log(x) for x in pi], [[math.log(x) for x in r] for r in a], [[math.log(x) for x in r] for r in b]
    assert math.isclose(path_score(lp, la, lb, obs, path), score, rel_tol=1e-9)
