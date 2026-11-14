# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/propensity-score-matching/. The authors are listed in prov/SWSA9A.jsonl.

import itertools
import random
from fractions import Fraction as Fr

import pytest

from propensity_score_matching import (
    att_from_pairs,
    greedy_match,
    nearest_with_replacement,
    optimal_pair_match,
    total_distance,
)

# The worked example of the page: scores in hundredths.
EX_S = [Fr(40, 100), Fr(50, 100)]  # treated
EX_C = [Fr(20, 100), Fr(48, 100), Fr(62, 100)]  # controls
EX_YT = [9, 12]
EX_YC = [3, 7, 10]


def brute_force(s, c):
    """Oracle: the least total distance over every injection of treated units into controls."""
    best = None
    for perm in itertools.permutations(range(len(c)), len(s)):
        cost = sum((abs(s[i] - c[j]) for i, j in enumerate(perm)), Fr(0))
        if best is None or cost < best:
            best = cost
    return best


def is_valid(pairs, m, n):
    treated = [i for i, _ in pairs]
    controls = [j for _, j in pairs]
    return sorted(treated) == list(range(m)) and len(set(controls)) == m and all(0 <= j < n for j in controls)


def test_worked_example():
    cost, pairs = optimal_pair_match(EX_S, EX_C)
    assert cost == Fr(20, 100)
    assert pairs == [(0, 1), (1, 2)]
    assert att_from_pairs(EX_YT, EX_YC, pairs) == 2
    g = greedy_match(EX_S, EX_C)  # 0.50 chooses first and takes 0.48
    assert g == [(0, 0), (1, 1)]
    assert total_distance(EX_S, EX_C, g) == Fr(22, 100)
    assert att_from_pairs(EX_YT, EX_YC, g) == Fr(11, 2)
    assert nearest_with_replacement(EX_S, EX_C) == [(0, 1), (1, 1)]
    assert att_from_pairs(EX_YT, EX_YC, nearest_with_replacement(EX_S, EX_C)) == Fr(7, 2)


def test_dp_table_of_example():
    """The page lists D[i][j]; recompute it with the same recurrence by hand."""
    s, c = sorted(EX_S), sorted(EX_C)
    D = {(0, j): Fr(0) for j in range(4)}
    for i in (1, 2):
        for j in range(i, 4):
            take = D[(i - 1, j - 1)] + abs(s[i - 1] - c[j - 1])
            D[(i, j)] = take if j == i else min(take, D[(i, j - 1)])
    assert [D[(1, j)] for j in (1, 2, 3)] == [Fr(20, 100), Fr(8, 100), Fr(8, 100)]
    assert [D[(2, j)] for j in (2, 3)] == [Fr(22, 100), Fr(20, 100)]


def test_edge_cases():
    assert optimal_pair_match([], []) == (0, [])
    assert optimal_pair_match([], [Fr(1, 2)]) == (0, [])
    assert optimal_pair_match([Fr(1, 3)], [Fr(1, 3)]) == (0, [(0, 0)])
    with pytest.raises(ValueError):
        optimal_pair_match([1, 2], [1])
    with pytest.raises(ValueError):
        nearest_with_replacement([1], [])
    with pytest.raises(ValueError):
        att_from_pairs([1], [1], [])
    # all scores tied: every matching costs 0
    cost, pairs = optimal_pair_match([Fr(1, 2)] * 3, [Fr(1, 2)] * 5)
    assert cost == 0 and is_valid(pairs, 3, 5)


def test_optimal_against_brute_force():
    rng = random.Random(20261114)
    for trial in range(800):
        m = rng.randint(1, 4)
        n = rng.randint(m, 6)
        grid = rng.choice([5, 10, 100])  # coarse grids make ties common
        s = [Fr(rng.randint(0, grid), grid) for _ in range(m)]
        c = [Fr(rng.randint(0, grid), grid) for _ in range(n)]
        cost, pairs = optimal_pair_match(s, c)
        assert is_valid(pairs, m, n), (s, c, pairs)
        assert total_distance(s, c, pairs) == cost
        assert cost == brute_force(s, c), (s, c)


def test_greedy_is_never_better_and_sometimes_worse():
    rng = random.Random(3)
    worse = 0
    for _ in range(600):
        m = rng.randint(1, 4)
        n = rng.randint(m, 6)
        s = [Fr(rng.randint(0, 100), 100) for _ in range(m)]
        c = [Fr(rng.randint(0, 100), 100) for _ in range(n)]
        order = list(range(m))
        rng.shuffle(order)
        g = greedy_match(s, c, order)
        assert is_valid(g, m, n)
        opt, _ = optimal_pair_match(s, c)
        gc = total_distance(s, c, g)
        assert gc >= opt
        worse += gc > opt
    assert worse > 0


def test_caliper_drops_far_units():
    s = [Fr(1, 10), Fr(9, 10)]
    c = [Fr(12, 100), Fr(5, 10)]
    assert greedy_match(s, c, caliper=Fr(1, 10)) == [(0, 0)]


def test_with_replacement_against_brute_force():
    rng = random.Random(11)
    for _ in range(600):
        m, n = rng.randint(1, 6), rng.randint(1, 6)
        s = [Fr(rng.randint(0, 20), 20) for _ in range(m)]
        c = [Fr(rng.randint(0, 20), 20) for _ in range(n)]
        out = nearest_with_replacement(s, c)
        assert [i for i, _ in out] == list(range(m))
        for i, j in out:
            assert abs(s[i] - c[j]) == min(abs(s[i] - v) for v in c)
        # each treated distance is at most its distance in the optimal pair matching
        if m <= n:
            _, pairs = optimal_pair_match(s, c)
            assert total_distance(s, c, out) <= total_distance(s, c, pairs)


def test_float_scores_agree_with_fractions():
    rng = random.Random(8)
    for _ in range(300):
        m = rng.randint(1, 5)
        n = rng.randint(m, 9)
        s = [Fr(rng.randint(0, 1000), 1000) for _ in range(m)]
        c = [Fr(rng.randint(0, 1000), 1000) for _ in range(n)]
        cost, _ = optimal_pair_match(s, c)
        fcost, fpairs = optimal_pair_match([float(v) for v in s], [float(v) for v in c])
        assert abs(float(cost) - fcost) < 1e-9
        assert abs(float(total_distance(s, c, fpairs)) - float(cost)) < 1e-9


def simulate(rng, n):
    """Superpopulation with known propensity; the effect is 1 + x, so the ATT exceeds the ATE."""
    rows = []
    for _ in range(n):
        x = rng.random()
        e = 0.1 + 0.5 * x
        t = 1 if rng.random() < e else 0
        y0 = 3 * x + rng.gauss(0, 0.5)
        rows.append((e, t, y0 + (1 + x) * t, x))
    return rows


def test_monte_carlo_matching_removes_most_bias():
    rng = random.Random(2026)
    r, n = 60, 300
    naive = opt = 0.0
    truth = 0.0
    for _ in range(r):
        rows = simulate(rng, n)
        tr = [row for row in rows if row[1] == 1]
        co = [row for row in rows if row[1] == 0]
        s, c = [row[0] for row in tr], [row[0] for row in co]
        _, pairs = optimal_pair_match(s, c)
        opt += att_from_pairs([row[2] for row in tr], [row[2] for row in co], pairs)
        naive += sum(row[2] for row in tr) / len(tr) - sum(row[2] for row in co) / len(co)
        truth += sum(1 + row[3] for row in tr) / len(tr)  # sample ATT
    naive, opt, truth = naive / r, opt / r, truth / r
    assert abs(naive - truth) > 0.5  # confounded: x raises both e and y0
    assert abs(opt - truth) < 0.25 * abs(naive - truth)
