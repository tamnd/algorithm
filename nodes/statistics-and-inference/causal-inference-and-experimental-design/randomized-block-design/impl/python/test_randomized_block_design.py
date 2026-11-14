# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/randomized-block-design/. The authors are listed in prov/24Z82C.jsonl.

import random
from fractions import Fraction

import pytest

from randomized_block_design import randomize, rcbd_anova, relative_efficiency

EXAMPLE = [[20, 26, 30, 18, 28], [23, 26, 34, 19, 31], [18, 24, 31, 17, 25], [24, 29, 34, 22, 31]]


def residual_ss(cols: list[list[Fraction]], y: list[Fraction]) -> Fraction:
    """Exact least squares residual sum of squares by Gauss-Jordan on the normal equations."""
    k = len(cols)
    m = [[sum(a * c for a, c in zip(cols[i], cols[j])) for j in range(k)]
         + [sum(a * v for a, v in zip(cols[i], y))] for i in range(k)]
    for c in range(k):
        piv = next(r for r in range(c, k) if m[r][c] != 0)
        m[c], m[piv] = m[piv], m[c]
        for r in range(k):
            if r != c and m[r][c] != 0:
                f = m[r][c] / m[c][c]
                m[r] = [x - f * z for x, z in zip(m[r], m[c])]
    beta = [m[i][k] / m[i][i] for i in range(k)]
    fit = [sum(b * col[n] for b, col in zip(beta, cols)) for n in range(len(y))]
    return sum((a - f) ** 2 for a, f in zip(y, fit))


def exact_by_model_comparison(table):
    t, b = len(table), len(table[0])
    cells = [(i, j) for i in range(t) for j in range(b)]
    y = [Fraction(table[i][j]) for i, j in cells]
    one = [[Fraction(1)] * len(cells)]
    treat = [[Fraction(int(i == a) - int(i == t - 1)) for i, _ in cells] for a in range(t - 1)]
    block = [[Fraction(int(j == c) - int(j == b - 1)) for _, j in cells] for c in range(b - 1)]
    rss_full = residual_ss(one + treat + block, y)
    rss_no_treat = residual_ss(one + block, y)
    rss_no_block = residual_ss(one + treat, y)
    return rss_no_treat - rss_full, rss_no_block - rss_full, rss_full


def test_example() -> None:
    a = rcbd_anova(EXAMPLE)
    assert abs(a.ss_treat - 74.6) < 1e-9 and abs(a.ss_block - 468.0) < 1e-9 and abs(a.ss_error - 12.4) < 1e-9
    assert (a.df_treat, a.df_block, a.df_error) == (3, 4, 12)
    assert abs(a.f_treat - 746 / 31) < 1e-9
    assert abs(relative_efficiency(EXAMPLE) - 14505 / 589) < 1e-9


def test_closed_form_equals_least_squares() -> None:
    rng = random.Random(1)
    for _ in range(10):
        t, b = rng.randint(2, 5), rng.randint(2, 5)
        table = [[rng.randint(0, 40) for _ in range(b)] for _ in range(t)]
        if len({v for r in table for v in r}) < 3:
            continue
        sst, ssb, sse = exact_by_model_comparison(table)
        try:
            a = rcbd_anova(table)
        except ValueError:
            assert sse == 0
            continue
        assert abs(a.ss_treat - float(sst)) < 1e-9 and abs(a.ss_block - float(ssb)) < 1e-9
        assert abs(a.ss_error - float(sse)) < 1e-9


def test_randomization_is_a_permutation_per_block() -> None:
    plan = randomize(4, 6, random.Random(2))
    assert len(plan) == 6 and all(sorted(p) == [0, 1, 2, 3] for p in plan)
    # every position gets each treatment equally often over many draws
    rng = random.Random(3)
    counts = [0] * 4
    for _ in range(4000):
        counts[randomize(4, 1, rng)[0][0]] += 1
    assert all(abs(c - 1000) < 4 * (4000 * 0.25 * 0.75) ** 0.5 for c in counts)


def test_ignoring_the_blocks() -> None:
    # the one-way analysis of the same table puts the block sum of squares into the error
    y = [[Fraction(v) for v in r] for r in EXAMPLE]
    means = [sum(r) / len(r) for r in y]
    ssw = sum((v - m) ** 2 for r, m in zip(y, means) for v in r)
    assert ssw == Fraction(2402, 5) == Fraction(468) + Fraction(62, 5)
    grand = sum(map(sum, y)) / 20
    ssa = 5 * sum((m - grand) ** 2 for m in means)
    f_one_way = (ssa / 3) / (ssw / 16)
    assert abs(float(f_one_way) - 0.8282) < 1e-4


def test_two_treatments_is_the_paired_t_test() -> None:
    rng = random.Random(5)
    for table in [EXAMPLE[:2]] + [[[rng.randint(0, 30) for _ in range(6)] for _ in range(2)] for _ in range(5)]:
        d = [Fraction(u - v) for u, v in zip(*table)]
        b = len(d)
        m = sum(d) / b
        s2 = sum((x - m) ** 2 for x in d) / (b - 1)
        if s2 == 0:
            continue
        t2 = m * m / (s2 / b)
        assert abs(rcbd_anova(table).f_treat - float(t2)) < 1e-9 * max(1.0, float(t2))
    assert abs(rcbd_anova(EXAMPLE[:2]).f_treat - 242 / 27) < 1e-9


def test_errors() -> None:
    with pytest.raises(ValueError):
        rcbd_anova([[1, 2, 3]])
    with pytest.raises(ValueError):
        rcbd_anova([[1, 2], [3]])
    with pytest.raises(ValueError):
        rcbd_anova([[1, 2], [3, 4]])  # additive exactly, so no error variance
