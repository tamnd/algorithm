# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/quantile-normalization/. The authors are listed in prov/C7FM0S.jsonl.

import math
import random

import pytest

from quantile_normalization import normalize_to_target, quantile_normalize, target_distribution

PAGE = [
    [2, 4, 7],
    [5, 1, 3],
    [3, 6, 9],
    [8, 2, 5],
]


def close_rows(a, b, rel=1e-12):
    return all(math.isclose(x, y, rel_tol=rel, abs_tol=1e-12)
               for ra, rb in zip(a, b, strict=True) for x, y in zip(ra, rb, strict=True))


def brute_force(x):
    """Each entry gets the mean of the target over the positions where its value sits in the sorted column."""
    n, m = len(x), len(x[0])
    cols = [sorted(row[j] for row in x) for j in range(m)]
    t = [sum(cols[j][i] for j in range(m)) / m for i in range(n)]
    out = []
    for g in range(n):
        row = []
        for j in range(m):
            pos = [i for i in range(n) if cols[j][i] == x[g][j]]
            row.append(sum(t[i] for i in pos) / len(pos))
        out.append(row)
    return out


def test_page_example():
    t = target_distribution(PAGE)
    assert close_rows([t], [[2.0, 10 / 3, 16 / 3, 23 / 3]])
    assert close_rows(quantile_normalize(PAGE), [
        [2.0, 16 / 3, 16 / 3],
        [16 / 3, 2.0, 2.0],
        [10 / 3, 23 / 3, 23 / 3],
        [23 / 3, 10 / 3, 10 / 3],
    ])


def test_ties_share_the_mean_of_their_targets():
    x = [[1, 10], [1, 20], [3, 30]]
    # targets: (5.5, 10.5, 16.5); the two 1s share ranks 1 and 2
    assert close_rows(quantile_normalize(x), [[8.0, 5.5], [8.0, 10.5], [16.5, 16.5]])


def test_matches_brute_force_with_ties():
    rng = random.Random(31)
    for _ in range(200):
        n = rng.randint(1, 15)
        m = rng.randint(1, 5)
        x = [[rng.randint(0, 6) for _ in range(m)] for _ in range(n)]
        assert close_rows(quantile_normalize(x), brute_force(x))


def test_without_ties_every_column_gets_the_target():
    rng = random.Random(32)
    for _ in range(50):
        n = rng.randint(1, 30)
        m = rng.randint(1, 6)
        x = [[rng.random() for _ in range(m)] for _ in range(n)]
        t = target_distribution(x)
        y = quantile_normalize(x)
        for j in range(m):
            assert sorted(row[j] for row in y) == t


def test_order_in_each_column_is_kept_and_sums_agree():
    rng = random.Random(33)
    for _ in range(100):
        n = rng.randint(1, 20)
        m = rng.randint(1, 5)
        x = [[rng.randint(0, 9) for _ in range(m)] for _ in range(n)]
        y = quantile_normalize(x)
        total = sum(target_distribution(x))
        for j in range(m):
            for g in range(n):
                for h in range(n):
                    if x[g][j] < x[h][j]:
                        assert y[g][j] <= y[h][j]
                    if x[g][j] == x[h][j]:
                        assert y[g][j] == y[h][j]
            assert math.isclose(sum(row[j] for row in y), total, rel_tol=1e-12, abs_tol=1e-12)


def test_idempotent_without_ties():
    rng = random.Random(34)
    for _ in range(50):
        x = [[rng.gauss(0, 1) for _ in range(4)] for _ in range(rng.randint(1, 25))]
        y = quantile_normalize(x)
        assert close_rows(quantile_normalize(y), y, rel=1e-9)


def test_permuting_genes_and_samples_permutes_the_result():
    rng = random.Random(35)
    x = [[rng.randint(0, 20) for _ in range(5)] for _ in range(12)]
    y = quantile_normalize(x)
    rows = list(range(12))
    cols = list(range(5))
    rng.shuffle(rows)
    rng.shuffle(cols)
    xp = [[x[g][j] for j in cols] for g in rows]
    yp = quantile_normalize(xp)
    assert close_rows(yp, [[y[g][j] for j in cols] for g in rows])


def test_given_target_and_errors():
    x = [[3, 1], [1, 2], [2, 3]]
    assert normalize_to_target(x, [30, 10, 20]) == [[30, 10], [10, 20], [20, 30]]
    with pytest.raises(ValueError):
        normalize_to_target(x, [1, 2])
    with pytest.raises(ValueError):
        quantile_normalize([])
    with pytest.raises(ValueError):
        quantile_normalize([[1, 2], [3]])
