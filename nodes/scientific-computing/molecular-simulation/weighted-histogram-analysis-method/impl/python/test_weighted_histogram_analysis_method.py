# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/weighted-histogram-analysis-method/. The authors are listed in prov/53HG7A.jsonl.
import math
import random

import pytest

from weighted_histogram_analysis_method import (
    double_well,
    free_energy_profile,
    histogram,
    metropolis,
    objective,
    wham,
)

LO, HI, NB = -1.6, 1.6, 32
WIDTH = (HI - LO) / NB
CENTERS = [LO + (b + 0.5) * WIDTH for b in range(NB)]
U = double_well(8.0)


def true_bin_probabilities():
    p = [math.exp(-U(s)) for s in CENTERS]
    z = sum(p)
    return [x / z for x in p]


def windows(spacing, kappa):
    cs = [LO + spacing * k for k in range(int(round((HI - LO) / spacing)) + 1)]
    return cs, [[0.5 * kappa * (s - c) ** 2 for s in CENTERS] for c in cs]


def test_expected_histograms_give_the_true_distribution():
    # Each window gets the exact expected counts N_k p(b) e^{-w_k(b)} / Z_k.
    pt = true_bin_probabilities()
    cs, bias = windows(0.4, 50.0)
    counts = []
    for wk in bias:
        q = [x * math.exp(-w) for x, w in zip(pt, wk)]
        z = sum(q)
        counts.append([1000.0 * x / z for x in q])
    p, f, _ = wham(counts, bias, 1.0, tol=1e-13)
    assert max(abs(a - b) for a, b in zip(p, pt)) < 1e-12
    # f_k is -kT ln of the biased partition function, relative to the normalised p.
    for fk, wk in zip(f, bias):
        assert fk == pytest.approx(-math.log(sum(x * math.exp(-w) for x, w in zip(pt, wk))), abs=1e-10)


def test_one_window_reduces_to_unbiasing():
    bias = [[0.5 * 20.0 * (s - 0.3) ** 2 for s in CENTERS]]
    rng = random.Random(3)
    counts = [[rng.randint(1, 50) for _ in CENTERS]]
    p, _, _ = wham(counts, bias, 1.0)
    q = [n * math.exp(w) for n, w in zip(counts[0], bias[0])]
    z = sum(q)
    assert p == pytest.approx([x / z for x in q], rel=1e-9)


def test_zero_bias_gives_the_pooled_histogram():
    rng = random.Random(4)
    counts = [[rng.randint(0, 9) for _ in CENTERS] for _ in range(3)]
    p, f, _ = wham(counts, [[0.0] * NB] * 3, 1.0)
    pooled = [sum(c[b] for c in counts) for b in range(NB)]
    total = sum(pooled)
    assert p == pytest.approx([x / total for x in pooled], abs=1e-12)
    assert f == pytest.approx([0.0, 0.0, 0.0], abs=1e-12)


def test_solution_minimises_the_convex_objective():
    rng = random.Random(5)
    cs, bias = windows(0.4, 50.0)
    counts = [histogram(metropolis(lambda x, c=c: U(x) + 25.0 * (x - c) ** 2, 1.0, c, 0.3, 2000, rng),
                        LO, HI, NB) for c in cs]
    _, f, _ = wham(counts, bias, 1.0, tol=1e-12)
    base = objective(f, counts, bias, 1.0)
    # The objective does not change when every f_k moves by the same constant.
    assert objective([x + 1.7 for x in f], counts, bias, 1.0) == pytest.approx(base, rel=1e-12)
    # The gradient is zero at the solution.
    h = 1e-5
    for k in range(len(f)):
        up = list(f)
        dn = list(f)
        up[k] += h
        dn[k] -= h
        grad = (objective(up, counts, bias, 1.0) - objective(dn, counts, bias, 1.0)) / (2 * h)
        assert abs(grad) < 1e-3
    # Any other point that is not a constant shift has a larger value.
    for _ in range(20):
        g = [x + rng.gauss(0.0, 0.3) for x in f]
        assert objective(g, counts, bias, 1.0) > base


def test_double_well_profile_against_exact():
    rng = random.Random(1)
    cs, bias = windows(0.2, 50.0)
    counts = [histogram(metropolis(lambda x, c=c: U(x) + 25.0 * (x - c) ** 2, 1.0, c, 0.3, 20000, rng),
                        LO, HI, NB) for c in cs]
    p, _, _ = wham(counts, bias, 1.0, tol=1e-8)
    f = free_energy_profile(p, 1.0)
    # The exact free energy of each bin, -ln of the integral of e^{-U} over the bin.
    exact = []
    for b in range(NB):
        a = LO + b * WIDTH
        exact.append(-math.log(sum(math.exp(-U(a + (i + 0.5) * WIDTH / 100)) for i in range(100)) * WIDTH / 100))
    pairs = [(v, e) for v, e, s in zip(f, exact, CENTERS) if U(s) < 9.0]
    assert all(v is not None for v, _ in pairs)
    off = sum(e - v for v, e in pairs) / len(pairs)
    assert max(abs(v + off - e) for v, e in pairs) < 0.4
    assert f[16] - f[25] == pytest.approx(exact[16] - exact[25], abs=0.3)  # barrier, 0.05 against 0.95
    assert abs(f[6] - f[25]) < 0.35  # the two wells, -0.95 against 0.95


def test_window_without_samples_raises():
    with pytest.raises(ValueError):
        wham([[1, 2], [0, 0]], [[0.0, 0.0], [0.0, 0.0]], 1.0)
