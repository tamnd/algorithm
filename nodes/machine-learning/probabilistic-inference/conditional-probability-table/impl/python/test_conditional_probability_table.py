# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/conditional-probability-table/. The authors are listed in prov/FEM89D.jsonl.

import random
from fractions import Fraction as F
from itertools import product

from conditional_probability_table import CPT, mle_from_counts, noisy_or, noisy_or_by_mechanism


def test_wet_grass_noisy_or_example() -> None:
    cpt = noisy_or([F(9, 10), F(8, 10)], F(1, 100))
    assert cpt.prob(1, (0, 0)) == F(1, 100)
    assert cpt.prob(1, (1, 0)) == F(901, 1000)
    assert cpt.prob(1, (0, 1)) == F(802, 1000)
    assert cpt.prob(1, (1, 1)) == F(4901, 5000)


def test_noisy_or_rows_sum_to_one_and_match_formula() -> None:
    rng = random.Random(1988)
    for k in range(0, 7):
        lam = [F(rng.randint(0, 20), 20) for _ in range(k)]
        leak = F(rng.randint(0, 10), 100)
        cpt = noisy_or(lam, leak)
        assert len(cpt.rows) == 2 ** k
        for u in product((0, 1), repeat=k):
            row = cpt.rows[u]
            assert sum(row) == 1 and min(row) >= 0
            off = (1 - leak)
            for j in range(k):
                if u[j]:
                    off *= 1 - lam[j]
            assert row[0] == off
            if k <= 5:
                assert row[1] == noisy_or_by_mechanism(lam, leak, u)
        # a full CPT has 2^k free numbers, noisy-OR has k + 1
        assert cpt.free_parameters() == 2 ** k


def test_noisy_or_is_monotone_in_parents() -> None:
    cpt = noisy_or([F(1, 3), F(1, 2), F(1, 5)], F(1, 50))
    for u in product((0, 1), repeat=3):
        for j in range(3):
            if not u[j]:
                v = list(u)
                v[j] = 1
                assert cpt.prob(1, tuple(v)) >= cpt.prob(1, u)


def test_parameter_counts() -> None:
    # child with 3 values, parents with 2 and 4 values: (3 - 1) * 2 * 4 = 16
    rows = {u: [F(1, 3)] * 3 for u in product(range(2), range(4))}
    assert CPT(3, [2, 4], rows).free_parameters() == 16
    # a root node: r - 1
    assert CPT(5, [], {(): [F(1, 5)] * 5}).free_parameters() == 4


def test_rejects_bad_rows() -> None:
    for rows in ({(0,): [F(1, 2), F(1, 2)]}, {(0,): [F(1, 2), F(1, 3)], (1,): [F(1, 2), F(1, 2)]}):
        try:
            CPT(2, [2], rows)
        except ValueError:
            continue
        raise AssertionError("expected ValueError")


def test_mle_and_dirichlet_estimates() -> None:
    data = [(1, (0,)), (0, (0,)), (1, (0,)), (1, (1,)), (1, (1,)), (1, (1,))]
    mle = mle_from_counts(2, [2], data)
    assert mle.rows[(0,)] == [F(1, 3), F(2, 3)] and mle.rows[(1,)] == [F(0), F(1)]
    smooth = mle_from_counts(2, [2], data, F(1))
    assert smooth.rows[(1,)] == [F(1, 5), F(4, 5)]
