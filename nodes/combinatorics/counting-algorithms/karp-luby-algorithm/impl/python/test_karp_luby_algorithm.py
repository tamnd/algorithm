# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/karp-luby-algorithm/. The authors are listed in prov/68D09K.jsonl.

import random
from fractions import Fraction

import pytest

from karp_luby_algorithm import KarpLuby, karp_luby, prepare, sample_count

EXAMPLE = [[1, 2], [2, 3], [-1]]  # (x1 AND x2) OR (x2 AND x3) OR (NOT x1)


def satisfies(a, clause):
    return all((a >> (abs(l) - 1) & 1) == (l > 0) for l in clause)


def exact_count(clauses, n):
    """Reference: test all 2^n assignments."""
    return sum(1 for a in range(1 << n) if any(satisfies(a, c) for c in clauses))


def first_pairs(state):
    """The number of pairs (i, a) with a in S_i and C_i the first clause that a satisfies."""
    count = 0
    for i, (mask, value) in enumerate(state.clauses):
        for a in range(1 << state.n):
            if a & mask == value and not any(a & mj == vj for mj, vj in state.clauses[:i]):
                count += 1
    return count


def random_formula(rng, n, m):
    clauses = []
    for _ in range(m):
        k = rng.randint(1, n)
        vs = rng.sample(range(1, n + 1), k)
        clauses.append([v if rng.random() < 0.5 else -v for v in vs])
    return clauses


def bits(a, n):
    return "".join(str(a >> k & 1) for k in range(n))


def test_worked_example():
    state = KarpLuby(EXAMPLE, 3)
    assert state.prefix == [2, 4, 8] and state.W == 8
    assert exact_count(EXAMPLE, 3) == 6 == first_pairs(state)
    rng = random.Random(9)
    trials = [state.sample(rng) for _ in range(8)]
    assert [(i + 1, bits(a, 3), x) for i, a, x in trials] == [
        (3, "001", 1), (3, "010", 1), (2, "111", 0), (1, "110", 1),
        (3, "011", 0), (1, "110", 1), (1, "111", 1), (3, "000", 1),
    ]
    assert state.W * Fraction(sum(x for _, _, x in trials), 8) == 6
    assert sample_count(3, 0.5, 0.25) == 75


def test_edges():
    assert karp_luby([], 4, 0.5, 0.1) == 0
    assert karp_luby([[1, -1]], 3, 0.5, 0.1) == 0  # a contradictory clause is empty
    assert karp_luby([[]], 5, 0.5, 0.1, random.Random(1)) == 32  # the empty clause is always true
    assert karp_luby([[]], 0, 0.5, 0.1, random.Random(1)) == 1
    assert first_pairs(KarpLuby([[1], [1], [1, 2]], 2)) == 2  # only the first copy of a clause counts
    assert prepare([[2, -3, 2]], 3) == [(6, 2)]  # x2 = 1 and x3 = 0; the repeated literal is harmless
    with pytest.raises(ValueError):
        prepare([[4]], 3)
    with pytest.raises(ValueError):
        prepare([[0]], 3)
    with pytest.raises(ValueError):
        sample_count(2, 0, 0.1)
    with pytest.raises(ValueError):
        sample_count(2, 0.5, 1)


def test_one_clause_is_exact():
    rng = random.Random(5)
    for n in range(1, 40, 7):
        clause = [v if v % 2 else -v for v in range(1, n + 1, 3)]
        assert karp_luby([clause], n, 0.3, 0.1, rng) == 2 ** (n - len(clause))


def test_trial_distribution():
    """Every pair (i, a) with a in S_i appears with probability 1 / W."""
    state = KarpLuby(EXAMPLE, 3)
    rng = random.Random(77)
    T = 40000
    freq = {}
    for _ in range(T):
        i, a, _ = state.sample(rng)
        assert satisfies(a, EXAMPLE[i])
        freq[(i, a)] = freq.get((i, a), 0) + 1
    assert len(freq) == state.W
    for c in freq.values():
        assert abs(c / T - 1 / state.W) < 0.01


def test_mean_is_unbiased():
    rng = random.Random(11)
    clauses = [[1, 2, 3], [-1, 4], [2, -4, 5], [3, 5], [-2, -3]]
    state = KarpLuby(clauses, 6)
    T = 60000
    s = sum(state.sample(rng)[2] for _ in range(T))
    exact = exact_count(clauses, 6)
    assert abs(state.W * s / T - exact) < 0.02 * exact


def test_large_n():
    n = 200
    clauses = [[v for v in range(1, n + 1) if v % k == 0] for k in (2, 3, 5)]
    # inclusion-exclusion: the clauses in a set T hold together on 2^(n - |union of their variables|) assignments
    exact = 0
    for t in range(1, 8):
        chosen = [set(c) for k, c in enumerate(clauses) if t >> k & 1]
        exact += (-1) ** (len(chosen) + 1) * 2 ** (n - len(set().union(*chosen)))
    est = karp_luby(clauses, n, 0.1, 0.01, random.Random(3))
    assert abs(est - exact) <= Fraction(1, 10) * exact


def test_random_against_brute_force():
    """(eps, delta) = (0.5, 0.1): at most a fraction delta of the runs may miss."""
    rng = random.Random(20260611)
    eps, delta = 0.5, 0.1
    misses = 0
    runs = 600
    for _ in range(runs):
        n = rng.randint(1, 8)
        clauses = random_formula(rng, n, rng.randint(1, 6))
        exact = exact_count(clauses, n)
        state = KarpLuby(clauses, n)
        assert first_pairs(state) == exact
        est = karp_luby(clauses, n, eps, delta, rng)
        if not (1 - eps) * exact <= est <= (1 + eps) * exact:
            misses += 1
    assert misses <= delta * runs
