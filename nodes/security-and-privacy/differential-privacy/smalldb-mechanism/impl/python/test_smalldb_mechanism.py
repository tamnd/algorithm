# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/smalldb-mechanism/. The authors are listed in prov/3V0287.jsonl.

import itertools
import math
import random

import dpkit
from smalldb_mechanism import (
    compositions,
    max_error,
    small_size,
    smalldb,
    smalldb_pmf,
    utility,
)

UNIVERSE = (0, 1, 2)


def _subset_queries(U):
    return [[1 if (mask >> j) & 1 else 0 for j in range(U)] for mask in range(1, 2 ** U)]


def _hist(records, U=len(UNIVERSE)):
    h = [0] * U
    for r in records:
        h[r] += 1
    return tuple(h)


def test_compositions_are_all_small_databases() -> None:
    for U in range(1, 5):
        for m in range(0, 6):
            got = compositions(m, U)
            brute = sorted({_hist(c, U) for c in itertools.combinations_with_replacement(range(U), m)})
            assert sorted(got) == brute
            assert len(got) == math.comb(m + U - 1, U - 1)


def test_smalldb_is_epsilon_dp_on_all_replace_pairs() -> None:
    queries = _subset_queries(3)
    epsilon, m = 0.7, 2

    def mech_pmf(records):
        return smalldb_pmf(_hist(records), queries, epsilon, m)

    datasets = list(itertools.combinations_with_replacement(UNIVERSE, 3))
    pairs = [(x, y) for x in datasets for y in dpkit.neighbors_replace(x, UNIVERSE)]
    assert len(pairs) > 30
    assert dpkit.is_pure_dp(mech_pmf, pairs, epsilon)
    worst = max(dpkit.max_privacy_loss(mech_pmf(x), mech_pmf(y)) for x, y in pairs)
    assert 0.2 < worst <= epsilon + 1e-12


def test_pmf_against_direct_formula() -> None:
    # The oracle builds the candidates from multisets and the weights from the definition.
    rng = random.Random(1)
    for _ in range(500):
        U = rng.randrange(1, 4)
        x = [rng.randrange(0, 6) for _ in range(U)]
        x[rng.randrange(U)] += 1
        n = sum(x)
        queries = [[rng.randrange(2) for _ in range(U)] for _ in range(rng.randrange(1, 5))]
        m = rng.randrange(1, 4)
        epsilon = rng.choice([0.3, 1.0, 3.0])
        weights = {}
        for c in itertools.combinations_with_replacement(range(U), m):
            y = _hist(c, U)
            err = max(abs(sum(f[j] * x[j] for j in range(U)) / n - sum(f[j] for j in c) / m) for f in queries)
            weights[y] = math.exp(-epsilon * n * err / 2)
        z = sum(weights.values())
        got = smalldb_pmf(x, queries, epsilon, m)
        assert set(got) == set(weights)
        assert all(math.isclose(got[y], w / z, rel_tol=1e-9, abs_tol=1e-15) for y, w in weights.items())


def test_a_small_database_with_error_alpha_exists() -> None:
    # Dwork-Roth Proposition 4.1, checked by brute force over all databases of size m.
    rng = random.Random(2)
    queries = _subset_queries(3)
    cands = {}
    for alpha in (0.35, 0.5, 0.7):
        m = small_size(alpha, len(queries))
        cands[alpha] = [[sum(f[j] * y[j] for j in range(3)) / m for f in queries] for y in compositions(m, 3)]
    for _ in range(500):
        x = [rng.randrange(0, 20) for _ in range(3)]
        x[rng.randrange(3)] += 1
        n = sum(x)
        fx = [sum(f[j] * x[j] for j in range(3)) / n for f in queries]
        alpha = rng.choice([0.35, 0.5, 0.7])
        best = min(max(abs(a - b) for a, b in zip(fx, fy)) for fy in cands[alpha])
        assert best <= alpha


def test_accuracy_bound_holds_exactly() -> None:
    # The exponential mechanism bound: error <= alpha + 2 (ln|R| + ln(1/beta)) / (epsilon n)
    # with probability at least 1 - beta. We sum the exact pmf.
    rng = random.Random(3)
    queries = _subset_queries(3)
    for _ in range(60):
        x = [rng.randrange(0, 30) for _ in range(3)]
        x[rng.randrange(3)] += 1
        n = sum(x)
        alpha, epsilon, beta = 0.5, rng.choice([0.5, 1.0, 2.0]), 0.1
        m = small_size(alpha, len(queries))
        pmf = smalldb_pmf(x, queries, epsilon, m)
        bound = alpha + 2 * (math.log(len(pmf)) + math.log(1 / beta)) / (epsilon * n)
        assert sum(p for y, p in pmf.items() if max_error(x, y, queries) > bound) <= beta


def test_sampling_matches_pmf() -> None:
    rng = random.Random(4)
    queries = _subset_queries(3)
    x, epsilon, alpha = (5, 2, 1), 1.0, 1.0
    pmf = smalldb_pmf(x, queries, epsilon, small_size(alpha, len(queries)))
    n = 1500
    emp = dpkit.empirical_pmf(smalldb(x, queries, epsilon, alpha, rng) for _ in range(n))
    margin = dpkit.hoeffding_margin(n, 1e-6)
    assert all(abs(emp.get(y, 0.0) - p) <= margin for y, p in pmf.items())


def test_example_values() -> None:
    U = 4
    queries = _subset_queries(U)
    x = (40, 30, 20, 10)
    m = small_size(0.5, len(queries))
    assert m == 11 and len(compositions(m, U)) == 364
    pmf = smalldb_pmf(x, queries, 1.0, m)
    best = max(pmf, key=pmf.get)
    assert best == (5, 3, 2, 1)
    assert math.isclose(max_error(x, best, queries), 0.6 / 11)
    assert 0.87 < sum(p for y, p in pmf.items() if max_error(x, y, queries) <= 0.1) < 0.89


def test_utility_sensitivity_is_one_over_n() -> None:
    rng = random.Random(5)
    queries = _subset_queries(3)
    for _ in range(200):
        records = tuple(rng.randrange(3) for _ in range(rng.randrange(1, 6)))
        y = _hist([rng.randrange(3) for _ in range(3)])
        for other in dpkit.neighbors_replace(records, UNIVERSE):
            d = abs(utility(_hist(records), y, queries) - utility(_hist(other), y, queries))
            assert d <= 1 / len(records) + 1e-12


def test_bad_parameters() -> None:
    rng = random.Random(6)
    q = _subset_queries(2)
    for args in [((1, 1), q, 0.0, 0.5), ((0, 0), q, 1.0, 0.5), ((1, 1), [], 1.0, 0.5), ((1, 1), q, 1.0, 0.0)]:
        try:
            smalldb(*args, rng)
        except ValueError:
            pass
        else:
            raise AssertionError("expected ValueError")
