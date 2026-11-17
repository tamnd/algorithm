# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/maximum-likelihood-admixture-estimation/. The authors are listed in prov/KYJWNZ.jsonl.

import math
import random

import pytest

from maximum_likelihood_admixture_estimation import (admixture, block_round, gradients, log_likelihood,
                                                     project_simplex, update_f, update_q)


def simulate(rng, n, m, k):
    """Ancestry proportions from a Dirichlet(1/2, ..., 1/2) law, frequencies uniform on [0.05, 0.95]."""
    q = []
    for _ in range(n):
        w = [rng.gammavariate(0.5, 1.0) + 1e-12 for _ in range(k)]
        s = sum(w)
        q.append([v / s for v in w])
    f = [[rng.uniform(0.05, 0.95) for _ in range(m)] for _ in range(k)]
    g = []
    for i in range(n):
        row = []
        for j in range(m):
            phi = sum(q[i][c] * f[c][j] for c in range(k))
            row.append((rng.random() < phi) + (rng.random() < phi))
        g.append(row)
    return g, q, f


def test_log_likelihood_by_hand():
    g = [[0, 1, 2]]
    q = [[0.25, 0.75]]
    f = [[0.2, 0.4, 0.8], [0.6, 0.4, 0.4]]
    # phi = 0.5, 0.4, 0.5
    want = 2 * math.log(0.5) + (math.log(0.4) + math.log(0.6)) + 2 * math.log(0.5)
    assert log_likelihood(g, q, f) == pytest.approx(want)


def test_one_em_step_by_hand():
    g = [[2, 0]]
    q = [[0.5, 0.5]]
    f = [[0.8, 0.4], [0.2, 0.4]]
    # Site 0: phi = 0.5; both copies of allele 1 split 0.8 : 0.2. Site 1: phi = 0.4; both copies of allele 0 split 0.5 : 0.5.
    q1 = update_q(g, q, f)
    assert q1[0] == pytest.approx([(1.6 + 1.0) / 4, (0.4 + 1.0) / 4])
    f1 = update_f(g, q, f)
    assert f1[0] == pytest.approx([1.0, 0.0])
    assert f1[1] == pytest.approx([1.0, 0.0])


def test_block_steps_never_lower_likelihood():
    rng = random.Random(1)
    g, _, _ = simulate(rng, 10, 30, 3)
    q = [[1 / 3] * 3 for _ in range(10)]
    f = [[rng.uniform(0.1, 0.9) for _ in range(30)] for _ in range(3)]
    ll = log_likelihood(g, q, f)
    for _ in range(25):
        q = update_q(g, q, f)
        l1 = log_likelihood(g, q, f)
        assert l1 >= ll - 1e-9
        f = update_f(g, q, f)
        l2 = log_likelihood(g, q, f)
        assert l2 >= l1 - 1e-9
        ll = l2
    for row in q:
        assert sum(row) == pytest.approx(1.0)
        assert min(row) >= 0


def test_traces_are_monotone():
    rng = random.Random(2)
    g, _, _ = simulate(rng, 10, 30, 2)
    for acc in (True, False):
        _, _, trace = admixture(g, 2, random.Random(5), accelerate=acc, max_iter=80)
        for a, b in zip(trace, trace[1:]):
            assert b >= a - 1e-9


def test_q_block_against_grid():
    rng = random.Random(3)
    g, _, f = simulate(rng, 3, 40, 2)
    q = [[0.5, 0.5] for _ in range(3)]
    for _ in range(600):
        q = update_q(g, q, f)
    for i in range(3):
        def ll(t):
            return log_likelihood([g[i]], [[t, 1 - t]], f)
        best = max((t / 2000 for t in range(2001)), key=ll)
        assert q[i][0] == pytest.approx(best, abs=1e-3)


def test_f_block_kkt():
    rng = random.Random(6)
    g, q, f_true = simulate(rng, 8, 30, 2)
    f = [row[:] for row in f_true]
    for _ in range(400):
        f = update_f(g, q, f)
    _, gf = gradients(g, q, f)
    for c in range(2):
        for j in range(30):
            if 1e-3 < f[c][j] < 1 - 1e-3:
                assert abs(gf[c][j]) < 1e-3
            elif f[c][j] <= 1e-3:
                assert gf[c][j] <= 1e-3
            else:
                assert gf[c][j] >= -1e-3


def test_q_fixed_point_has_equal_gradients():
    rng = random.Random(12)
    g, _, f = simulate(rng, 4, 30, 3)
    q = [[1 / 3] * 3 for _ in range(4)]
    for _ in range(1500):
        q = update_q(g, q, f)
    gq, _ = gradients(g, q, f)
    for i in range(4):
        for c in range(3):
            if q[i][c] > 1e-2:
                assert gq[i][c] == pytest.approx(60.0, rel=1e-4)  # the multiplier is 2m
            else:
                assert gq[i][c] <= 60.0 * (1 + 1e-4)


def test_fit_beats_truth_and_recovers_ancestry():
    rng = random.Random(4)
    g, q_true, f_true = simulate(rng, 20, 60, 2)
    q, f, trace = admixture(g, 2, random.Random(7))
    assert trace[-1] >= log_likelihood(g, q_true, f_true)
    err_a = sum(abs(a[0] - b[0]) for a, b in zip(q, q_true)) / 20
    err_b = sum(abs(a[0] - b[1]) for a, b in zip(q, q_true)) / 20
    assert min(err_a, err_b) < 0.12  # up to the swap of the two labels


def test_one_population_is_allele_frequency():
    rng = random.Random(9)
    g, _, _ = simulate(rng, 10, 20, 1)
    q, f, _ = admixture(g, 1, random.Random(1))
    for j in range(20):
        assert f[0][j] == pytest.approx(sum(row[j] for row in g) / 20, abs=1e-9)
    assert all(row == [1.0] for row in q)


def test_project_simplex():
    assert project_simplex([0.5, 0.5, 0.5]) == pytest.approx([1 / 3] * 3)
    assert project_simplex([2.0, 0.0, 0.0]) == pytest.approx([1.0, 0.0, 0.0])
    assert project_simplex([0.2, 0.3, 0.5]) == pytest.approx([0.2, 0.3, 0.5])
    rng = random.Random(11)
    for _ in range(30):
        y = [rng.uniform(-1, 2) for _ in range(4)]
        p = project_simplex(y)
        assert sum(p) == pytest.approx(1.0) and min(p) >= 0
        d = sum((a - b) ** 2 for a, b in zip(p, y))
        for _ in range(100):
            w = [rng.random() for _ in range(4)]
            s = sum(w)
            z = [v / s for v in w]
            assert d <= sum((a - b) ** 2 for a, b in zip(z, y)) + 1e-12


def test_symmetric_start_and_errors():
    g = [[0, 2], [2, 0]]
    q = [[0.5, 0.5], [0.5, 0.5]]
    f = [[0.5, 0.5], [0.5, 0.5]]
    q1, f1 = block_round(g, q, f)
    assert q1 == q and f1 == f  # a symmetric start is a fixed point that is not the maximum
    with pytest.raises(ValueError):
        admixture([[0, 3]], 2, random.Random(1))
    with pytest.raises(ValueError):
        admixture([], 2, random.Random(1))
