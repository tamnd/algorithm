# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/combat/. The authors are listed in prov/PBAHAY.jsonl.

import math
import random

import pytest

from combat import combat, inverse_gamma_moments, mean, posterior, standardize, var

PAGE = [[1, 2, 3, 4, 5, 6], [2, 4, 6, 5, 6, 7], [3, 3, 4, 7, 9, 11], [5, 6, 7, 6, 8, 10]]
PAGE_BATCH = ["A"] * 3 + ["B"] * 3


def close(a, b, tol=5e-4):
    return all(math.isclose(x, y, abs_tol=tol) for x, y in zip(a, b))


def test_page_example():
    Z, stand, sigma, _ = standardize(PAGE, PAGE_BATCH)
    assert math.isclose(sigma[0] ** 2, 2 / 3) and stand[0] == [3.5] * 6
    zA = Z[0][:3]
    assert math.isclose(mean(zA), -1.5 / math.sqrt(2 / 3)) and math.isclose(var(zA), 1.5)
    # The priors of batch A over the four genes.
    zs = [z[:3] for z in Z]
    g_hat, d_hat = [mean(z) for z in zs], [var(z) for z in zs]
    lam, theta = inverse_gamma_moments(d_hat)
    assert close([mean(g_hat), var(g_hat), lam, theta], [-1.4359, 0.6283, 3.4837, 2.9375])
    gs, ds = posterior(zs[0], g_hat[0], d_hat[0], mean(g_hat), var(g_hat), lam, theta)
    assert close([gs, ds], [-1.6874, 1.1223])
    # Without shrinkage both batches of gene 1 become 2.684, 3.5, 4.316; with it they keep a small gap.
    ls = combat(PAGE, PAGE_BATCH, shrink=False)
    assert close(ls[0], [2.684, 3.5, 4.316] * 2, 1e-3)
    eb = combat(PAGE, PAGE_BATCH)
    assert close(eb[0], [2.441, 3.385, 4.329, 2.834, 3.619, 4.404], 1e-3)


def random_data(rng, G, sizes, covariate=False):
    batch, cov = [], []
    for i, n in enumerate(sizes):
        batch += [i] * n
        cov += [[float(rng.random() < 0.5)] for _ in range(n)]
    data = []
    for g in range(G):
        shift = [rng.gauss(0, 1) for _ in sizes]
        scale = [math.exp(rng.gauss(0, 0.4)) for _ in sizes]
        data.append([5 + 2 * cov[j][0] + shift[b] + scale[b] * rng.gauss(0, 1) for j, b in enumerate(batch)])
    return data, batch, (cov if covariate else None)


def test_location_scale_without_shrinkage_equalizes_batches_exactly():
    rng = random.Random(1)
    for covariate in (False, True):
        data, batch, cov = random_data(rng, 6, (4, 5, 6), covariate)
        out = combat(data, batch, cov, shrink=False)
        _, stand, sigma, _ = standardize(data, batch, cov)
        for g in range(6):
            for b in range(3):
                idx = [j for j in range(len(batch)) if batch[j] == b]
                resid = [out[g][j] - stand[g][j] for j in idx]
                assert abs(mean(resid)) < 1e-9
                assert math.isclose(var(resid), sigma[g] ** 2, rel_tol=1e-9)


def test_inverse_gamma_moments_match():
    rng = random.Random(2)
    for _ in range(20):
        d = [rng.uniform(0.2, 3.0) for _ in range(10)]
        lam, theta = inverse_gamma_moments(d)
        assert lam > 2
        assert math.isclose(theta / (lam - 1), mean(d))
        assert math.isclose(theta ** 2 / ((lam - 1) ** 2 * (lam - 2)), var(d))


def test_posterior_is_a_fixed_point_and_converges_monotonically():
    rng = random.Random(3)
    for _ in range(50):
        n = rng.randint(2, 6)
        z = [rng.gauss(1, 1.5) for _ in range(n)]
        g_hat, d_hat = mean(z), var(z)
        g_bar, t2 = rng.gauss(0, 1), rng.uniform(0.05, 2)
        lam, theta = rng.uniform(2.1, 8), rng.uniform(0.5, 8)
        hist = []
        gs, ds = posterior(z, g_hat, d_hat, g_bar, t2, lam, theta, conv=1e-13, history=hist)
        assert math.isclose(gs, (t2 * n * g_hat + ds * g_bar) / (t2 * n + ds), rel_tol=1e-9, abs_tol=1e-12)
        assert math.isclose(ds, (theta + 0.5 * sum((x - gs) ** 2 for x in z)) / (n / 2 + lam - 1), rel_tol=1e-9)
        assert min(g_hat, g_bar) - 1e-12 <= gs <= max(g_hat, g_bar) + 1e-12
        ds_seq = [d_hat] + [d for _, d in hist]
        steps = [b - a for a, b in zip(ds_seq[1:], ds_seq[2:])]
        assert all(s >= -1e-12 for s in steps) or all(s <= 1e-12 for s in steps)


def test_posterior_mean_matches_numerical_integration():
    """gamma* with delta^2 fixed is the posterior mean under a normal prior and a normal likelihood."""
    z, d2, g_bar, t2 = [0.8, 2.1, 1.4], 1.3, -0.5, 0.6
    n = len(z)
    want = (t2 * n * mean(z) + d2 * g_bar) / (t2 * n + d2)
    h = 1e-3
    grid = [-8 + h * i for i in range(16001)]

    def dens(g):
        return math.exp(-(g - g_bar) ** 2 / (2 * t2) - sum((x - g) ** 2 for x in z) / (2 * d2))

    w = [dens(g) for g in grid]
    got = sum(g * v for g, v in zip(grid, w)) / sum(w)
    assert math.isclose(got, want, abs_tol=1e-6)


def test_shift_and_scale_of_a_gene_carry_through():
    rng = random.Random(4)
    data, batch, cov = random_data(rng, 5, (3, 4), True)
    base = combat(data, batch, cov)
    shifted = [row[:] for row in data]
    shifted[2] = [v + 7.0 for v in data[2]]
    assert close(combat(shifted, batch, cov)[2], [v + 7.0 for v in base[2]], 1e-9)
    # Scaling all genes by one factor scales the output, because the priors use standardized data.
    scaled = [[3.0 * v for v in row] for row in data]
    out = combat(scaled, batch, cov)
    for g in range(5):
        assert close(out[g], [3.0 * v for v in base[g]], 1e-9)


def simulate(rng, G, sizes, group=None):
    """Data from the ComBat model with a known batch free signal."""
    batch = [i for i, n in enumerate(sizes) for _ in range(n)]
    group = group or [0] * len(batch)
    prior = [(rng.gauss(0, 1), 0.4, 4.0, 3.0) for _ in sizes]
    clean, obs = [], []
    for g in range(G):
        a = rng.gauss(6, 1)
        s = math.exp(rng.gauss(-0.5, 0.3))
        beta = rng.gauss(0, 1)
        gam = [rng.gauss(m, math.sqrt(t2)) for m, t2, _, _ in prior]
        dl = [math.sqrt(th / rng.gammavariate(lam, 1.0)) for _, _, lam, th in prior]
        c_row, o_row = [], []
        for j, b in enumerate(batch):
            e = rng.gauss(0, 1) * s
            base = a + beta * group[j]
            c_row.append(base + e)
            o_row.append(base + gam[b] * s + dl[b] * e)
        clean.append(c_row)
        obs.append(o_row)
    return clean, obs, batch


def test_shrinkage_lowers_the_error_with_small_batches_measured():
    """A measurement: 300 genes, 3 batches of 3 samples. EB beats the plain location and scale fix."""
    rng = random.Random(2007)
    clean, obs, batch = simulate(rng, 300, (3, 3, 3))

    def err(out):
        return sum((o - c - (mean(oo) - mean(cc))) ** 2 for oo, cc in zip(out, clean)
                   for o, c in zip(oo, cc)) / (300 * 9)

    eb = combat(obs, batch)
    ls = combat(obs, batch, shrink=False)
    raw = err(obs)
    assert err(eb) < err(ls) < raw


def test_covariate_keeps_an_unbalanced_group_difference_measured():
    """A measurement: group 1 sits mostly in batch 1. Without the covariate ComBat removes much of its effect."""
    rng = random.Random(11)
    group = [0, 0, 0, 0, 0, 1] + [0, 1, 1, 1, 1, 1]
    batch = [0] * 6 + [1] * 6
    data = []
    for g in range(60):
        eff = 2.0 if g < 20 else 0.0
        shift = rng.gauss(1.0, 0.3)
        data.append([5 + eff * group[j] + shift * batch[j] + rng.gauss(0, 0.5) for j in range(12)])

    def group_diff(out):
        d = [mean([r[j] for j in range(12) if group[j]]) - mean([r[j] for j in range(12) if not group[j]]) for r in out[:20]]
        return mean(d)

    with_cov = combat(data, batch, [[float(x)] for x in group])
    without = combat(data, batch)
    assert abs(group_diff(with_cov) - 2.0) < 0.3
    assert group_diff(without) < 1.5


def test_errors():
    with pytest.raises(ValueError):
        combat([[1, 2, 3]], [0, 0, 1])
    with pytest.raises(ValueError):
        combat([[1, 2, 3], [2, 3, 5]], [0, 0, 1])
    with pytest.raises(ValueError):
        inverse_gamma_moments([1.0, 1.0, 1.0])
