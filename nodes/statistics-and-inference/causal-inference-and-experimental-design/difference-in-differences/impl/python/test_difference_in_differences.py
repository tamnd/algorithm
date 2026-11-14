# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/difference-in-differences/. The authors are listed in prov/XKDP5H.jsonl.

import math
import random
from fractions import Fraction as Fr

import pytest

from difference_in_differences import (
    att_gt,
    did_means,
    did_panel,
    did_regression,
    interval,
    twfe,
    twfe_dummies,
    twfe_weights,
)


def test_worked_example():
    pre = [10, 12, 14, 8, 9, 13]
    post = [15, 16, 20, 10, 10, 16]
    treated = [1, 1, 1, 0, 0, 0]
    r = did_panel([Fr(v) for v in pre], [Fr(v) for v in post], treated)
    assert r.tau == 3 and r.change_treated == 5 and r.change_control == 2
    assert abs(r.se - math.sqrt(2 / 3)) < 1e-12
    y = [Fr(v) for v in pre + post]
    treat = treated + treated
    per = [0] * 6 + [1] * 6
    assert did_regression(y, treat, per) == [10, 2, 2, 3]
    assert did_means(y, treat, per) == 3


def test_cell_means_equal_ols_interaction_exactly():
    """Unbalanced repeated cross-sections: the interaction coefficient is the DiD of the cell means."""
    rng = random.Random(1)
    for _ in range(100):
        sizes = {(a, b): rng.randint(1, 6) for a in (0, 1) for b in (0, 1)}
        y, treat, post = [], [], []
        for (a, b), k in sizes.items():
            for _ in range(k):
                y.append(Fr(rng.randint(-20, 20), rng.randint(1, 4)))
                treat.append(a)
                post.append(b)
        coef = did_regression(y, treat, post)
        assert coef[3] == did_means(y, treat, post)


def test_panel_equals_pooled_regression_exactly():
    rng = random.Random(2)
    for _ in range(50):
        n = rng.randint(4, 12)
        treated = [1, 1] + [0, 0] + [rng.randint(0, 1) for _ in range(n - 4)]
        pre = [Fr(rng.randint(-9, 9)) for _ in range(n)]
        post = [Fr(rng.randint(-9, 9)) for _ in range(n)]
        r = did_panel(pre, post, treated)
        coef = did_regression(pre + post, treated + treated, [0] * n + [1] * n)
        assert r.tau == coef[3]
        y = [[a, b] for a, b in zip(pre, post)]
        d = [[0, t] for t in treated]
        assert twfe(y, d) == r.tau  # two periods: unit fixed effects give the same number


def test_twfe_matches_dummy_regression_exactly():
    rng = random.Random(3)
    for _ in range(40):
        n, t = rng.randint(3, 5), rng.randint(3, 4)
        d = [[rng.randint(0, 1) for _ in range(t)] for _ in range(n)]
        y = [[Fr(rng.randint(-9, 9)) for _ in range(t)] for _ in range(n)]
        try:
            b = twfe(y, d)
        except ValueError:
            continue
        assert b == twfe_dummies(y, d)


def test_twfe_weights_are_exact_and_can_be_negative():
    # Two units, three periods: E treated from period 1, L from period 2 (0-based).
    d = [[0, 1, 1], [0, 0, 1]]
    w = twfe_weights(d)
    assert w == {(0, 1): 1, (0, 2): Fr(-1, 2), (1, 2): Fr(1, 2)}
    tau = [[0, 1, 4], [0, 0, 1]]  # all effects positive, the early group's effect grows
    a, b = [5, -2], [0, 3, 7]
    y = [[Fr(a[i] + b[s] + tau[i][s] * d[i][s]) for s in range(3)] for i in range(2)]
    assert twfe(y, d) == Fr(-1, 2)
    rng = random.Random(4)
    for _ in range(40):
        n, t = rng.randint(3, 6), rng.randint(3, 5)
        first = [rng.choice([None] + list(range(1, t))) for _ in range(n)]
        d = [[int(f is not None and s >= f) for s in range(t)] for f in first]
        try:
            w = twfe_weights(d)
        except (ValueError, ZeroDivisionError):
            continue
        if not w:
            continue
        assert sum(w.values()) == 1
        tau = [[Fr(rng.randint(-5, 5)) for _ in range(t)] for _ in range(n)]
        a_i = [Fr(rng.randint(-9, 9)) for _ in range(n)]
        b_t = [Fr(rng.randint(-9, 9)) for _ in range(t)]
        y = [[a_i[i] + b_t[s] + tau[i][s] * d[i][s] for s in range(t)] for i in range(n)]
        assert twfe(y, d) == sum(w[k] * tau[k[0]][k[1]] for k in w)


def test_group_time_effect_recovers_the_truth():
    """Staggered adoption with never-treated units, noise-free: att_gt is exact where TWFE is not."""
    first = [1, 1, 2, 2, None, None]
    t_len = 4
    d = [[int(f is not None and s >= f) for s in range(t_len)] for f in first]
    a = [3, 1, 4, 1, 5, 9]
    b = [0, 2, 1, 5]
    eff = {1: [0, 1, 3, 6], 2: [0, 0, 2, 4]}  # effects by group and period, growing with exposure
    y = [[Fr(a[i] + b[s] + (eff[first[i]][s] if first[i] else 0)) for s in range(t_len)] for i in range(6)]
    for g in (1, 2):
        for s in range(g, t_len):
            assert att_gt(y, first, g, s) == eff[g][s]
    w = twfe_weights(d)
    truth = sum(w[(i, s)] * eff[first[i]][s] for (i, s) in w)
    assert twfe(y, d) == truth
    plain = [eff[first[i]][s] for (i, s) in w]
    assert truth != sum(plain) / len(plain)  # TWFE is not the average of the cell effects


def test_monte_carlo_unbiased_and_covers():
    """Unit effects correlated with treatment, common shock, true effect 2. r = 1000 samples of 40 + 40
    units (seed 2026). DiD mean within 4 SE of 2; coverage of the 95% interval within 0.95 +- (4 SE +
    0.01) where the 0.01 is the normal approximation error; the post-period difference is biased by 3."""
    rng = random.Random(2026)
    r, est, cover, naive = 1000, [], 0, []
    for _ in range(r):
        treated = [1] * 40 + [0] * 40
        pre, post = [], []
        for t in treated:
            a = 3 * t + rng.gauss(0, 2)
            pre.append(a + rng.gauss(0, 1))
            post.append(a + 1.5 + 2 * t + rng.gauss(0, 1))
        res = did_panel(pre, post, treated)
        est.append(res.tau)
        lo, hi = interval(res)
        cover += lo <= 2 <= hi
        naive.append(sum(post[:40]) / 40 - sum(post[40:]) / 40)
    m = sum(est) / r
    sd = math.sqrt(sum((v - m) ** 2 for v in est) / (r - 1))
    assert abs(m - 2) < 4 * sd / math.sqrt(r)
    assert abs(cover / r - 0.95) < 4 * math.sqrt(0.95 * 0.05 / r) + 0.01
    assert abs(sum(naive) / r - 5) < 0.1


def test_input_checks():
    with pytest.raises(ValueError):
        did_panel([1, 2, 3], [1, 2], [1, 0, 0])
    with pytest.raises(ValueError):
        did_panel([1, 2, 3], [1, 2, 3], [1, 0, 0])
    with pytest.raises(ValueError):
        did_means([1, 2, 3], [0, 0, 1], [0, 1, 0])
    with pytest.raises(ValueError):
        att_gt([[1, 2], [3, 4]], [1, 1], 1, 1)
