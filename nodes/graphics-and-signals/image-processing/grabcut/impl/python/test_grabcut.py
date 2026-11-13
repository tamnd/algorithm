# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/grabcut/. The authors are listed in prov/KQQ4Z2.jsonl.

import itertools
import math
import random

import pytest

from grabcut import (
    Gaussian,
    _colors,
    assign,
    best_component,
    contrast_beta,
    energy,
    fit_gaussian,
    grabcut,
    learn,
    neighbor_pairs,
    pair_weights,
    rect_trimap,
    segment,
)

EXAMPLE = [
    [30, 32, 31, 29, 30, 31],
    [31, 200, 205, 30, 198, 30],
    [29, 202, 199, 201, 203, 32],
    [30, 31, 30, 29, 31, 30],
]


def random_image(rng, h, w, colors):
    def pixel():
        base = rng.choice([20, 120, 220])
        v = [min(255, max(0, base + rng.randint(-15, 15))) for _ in range(colors)]
        return v[0] if colors == 1 else tuple(v)

    return [[pixel() for _ in range(w)] for _ in range(h)]


def direct_weights(img, gamma):
    """The smoothness weights from the definition, pair by pair."""
    h, w = len(img), len(img[0])
    z = _colors(img)
    pairs = []
    for y1, x1, y2, x2 in itertools.product(range(h), range(w), range(h), range(w)):
        if (y1, x1) < (y2, x2) and max(abs(x1 - x2), abs(y1 - y2)) == 1:
            pairs.append((y1 * w + x1, y2 * w + x2, math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)))
    mean = sum(sum((a - b) ** 2 for a, b in zip(z[i], z[j])) for i, j, _ in pairs) / len(pairs)
    beta = 1 / (2 * mean) if mean else 0.0
    return {(i, j): gamma / d * math.exp(-beta * sum((a - b) ** 2 for a, b in zip(z[i], z[j]))) for i, j, d in pairs}


def brute_force_min_energy(img, tri, theta, gamma):
    z = _colors(img)
    wts = direct_weights(img, gamma)
    unknown = [n for n in range(len(z)) if tri[n] == 2]
    best = math.inf
    for bits in itertools.product((0, 1), repeat=len(unknown)):
        alpha = [0 if v == 0 else 1 for v in tri]
        for n, b in zip(unknown, bits):
            alpha[n] = b
        e = sum(best_component(theta, alpha[n], z[n])[0] for n in range(len(z)))
        e += sum(wt for (i, j), wt in wts.items() if alpha[i] != alpha[j])
        best = min(best, e)
    return best


def test_neighbor_pairs_and_beta():
    rng = random.Random(1)
    for h, w in [(1, 1), (1, 4), (3, 1), (2, 2), (3, 5)]:
        img = random_image(rng, h, w, 3)
        pairs = neighbor_pairs(w, h)
        assert len(pairs) == 4 * w * h - 3 * w - 3 * h + 2
        got = {(i, j): wt for (i, j, _), wt in zip(pairs, pair_weights(_colors(img), pairs, 50.0))}
        want = direct_weights(img, 50.0) if pairs else {}
        assert got.keys() == want.keys()
        assert all(math.isclose(got[e], want[e], rel_tol=1e-12) for e in got)
    flat = [[7, 7], [7, 7]]
    assert contrast_beta(_colors(flat), neighbor_pairs(2, 2)) == 0.0


@pytest.mark.parametrize("colors", [1, 3])
def test_cut_is_a_minimum_over_all_labelings(colors):
    rng = random.Random(10 + colors)
    for _ in range(40):
        h, w = rng.randint(1, 3), rng.randint(2, 4)
        img = random_image(rng, h, w, colors)
        tri = [rng.choice([0, 0, 1, 2, 2, 2]) for _ in range(h * w)]
        if 2 not in tri:
            tri[0] = 2
        z = _colors(img)
        n_comp = rng.randint(1, 3)
        alpha = [rng.randint(0, 1) for _ in z]
        alpha[0], alpha[-1] = 0, 1
        k = [rng.randrange(n_comp) for _ in z]
        theta = learn(z, alpha, k, n_comp, 1.0)
        gamma = rng.choice([0.0, 5.0, 50.0])
        pairs = neighbor_pairs(w, h)
        weights = pair_weights(z, pairs, gamma)
        cut = segment(z, tri, theta, pairs, weights)
        assert all(cut[n] == tri[n] for n in range(len(z)) if tri[n] != 2)
        got = energy(z, cut, [best_component(theta, cut[n], z[n])[1] for n in range(len(z))], theta, pairs, weights)
        want = brute_force_min_energy(img, tri, theta, gamma)
        assert math.isclose(got, want, rel_tol=1e-9, abs_tol=1e-9)


def test_steps_one_and_two_minimize_the_energy():
    rng = random.Random(3)
    for _ in range(30):
        img = random_image(rng, 3, 4, 3)
        z = _colors(img)
        alpha = [rng.randint(0, 1) for _ in z]
        alpha[0], alpha[1] = 0, 1
        n_comp = 2
        k = [rng.randrange(n_comp) for _ in z]
        theta = learn(z, alpha, k, n_comp, 1.0)
        # Step 1: no other choice of k_n has a lower cost.
        k1 = assign(z, alpha, theta)
        for n in range(len(z)):
            costs = [theta[alpha[n]][c].cost(z[n]) for c in range(n_comp) if theta[alpha[n]][c] is not None]
            assert theta[alpha[n]][k1[n]].cost(z[n]) == min(costs)
        # Step 2: perturbing a weight, a mean or a covariance never lowers the data term.
        best = sum(theta[alpha[n]][k[n]].cost(z[n]) for n in range(len(z)))
        for _ in range(10):
            a, c = rng.randint(0, 1), rng.randrange(n_comp)
            g = theta[a][c]
            if g is None:
                continue
            mu = tuple(m + rng.uniform(-3, 3) for m in g.mu)
            f = 1 + rng.uniform(-0.2, 0.2)
            e = [rng.uniform(-1, 1) for _ in range(3)]
            scaled = [[g.cov[i][j] * f for j in range(3)] for i in range(3)]
            bumped = [[g.cov[i][j] + 2 * e[i] * e[j] for j in range(3)] for i in range(3)]
            for pi, m, s in [(g.pi, mu, g.cov), (g.pi, g.mu, scaled), (g.pi, g.mu, bumped), (g.pi * 0.9 if g.pi < 1 else g.pi, g.mu, g.cov)]:
                other = Gaussian(pi, m, s, 1.0)
                trial = [row[:] for row in theta]
                trial[a][c] = other
                if pi != g.pi:  # Keep the weights of the label summing to 1.
                    rest = [d for d in range(n_comp) if d != c and trial[a][d] is not None]
                    if not rest:
                        continue
                    d = rest[0]
                    od = trial[a][d]
                    trial[a][d] = Gaussian(od.pi + g.pi - pi, od.mu, od.cov, 1.0)
                value = sum(trial[alpha[n]][k[n]].cost(z[n]) for n in range(len(z)))
                assert value >= best - 1e-9


def test_fitted_covariance_is_the_sample_covariance_plus_eps():
    pts = [(1.0, 2.0), (3.0, 2.0), (2.0, 5.0)]
    g = fit_gaussian(pts, 6, 0.5)
    assert g.pi == 0.5 and g.mu == (2.0, 3.0)
    assert g.cov == [[2 / 3 + 0.5, 0.0], [0.0, 2.0 + 0.5]]


@pytest.mark.parametrize("colors", [1, 3])
def test_energy_never_increases_and_fixed_pixels_stay(colors):
    rng = random.Random(40 + colors)
    for _ in range(12):
        h, w = rng.randint(3, 6), rng.randint(3, 6)
        img = random_image(rng, h, w, colors)
        rect = (1, 1, w - 1, h - 1)
        tri = rect_trimap(w, h, rect)
        alpha, energies = grabcut(img, tri, random.Random(rng.randrange(10**6)), n_comp=rng.randint(1, 3))
        for a, b in zip(energies, energies[1:]):
            assert b <= a + 1e-9 * max(1.0, abs(a))
        for y in range(h):
            for x in range(w):
                if tri[y][x] == 0:
                    assert alpha[y][x] == 0


def test_user_foreground_stays_foreground():
    img = [[10, 10, 10, 10], [10, 10, 200, 10], [10, 10, 10, 10]]
    tri = [[0, 0, 0, 0], [0, 1, 2, 0], [0, 2, 2, 0]]
    alpha, _ = grabcut(img, tri, random.Random(0), n_comp=1)
    assert alpha[1][1] == 1 and alpha[1][2] == 1
    assert all(alpha[y][x] == 0 for y in range(3) for x in range(4) if tri[y][x] == 0)


def test_example():
    tri = rect_trimap(6, 4, (1, 1, 5, 3))
    alpha, energies = grabcut(EXAMPLE, tri, random.Random(1), n_comp=1)
    assert alpha == [[0, 0, 0, 0, 0, 0], [0, 1, 1, 0, 1, 0], [0, 1, 1, 1, 1, 0], [0, 0, 0, 0, 0, 0]]
    # The initial energy, then lines L4, L5 and L7 of three rounds; the third round changes nothing.
    assert [round(e, 1) for e in energies] == [607.2, 607.2, 607.2, 560.4, 560.4, 541.4, 541.4, 541.4, 541.4, 541.4]
    z = _colors(EXAMPLE)
    flat = [v for row in alpha for v in row]
    theta = learn(z, flat, [0] * 24, 1, 1.0)
    assert math.isclose(theta[1][0].mu[0], 1408 / 7)


def test_color_blob_is_found():
    rng = random.Random(5)
    img = [[(rng.randint(0, 60), rng.randint(0, 60), rng.randint(150, 255)) for _ in range(12)] for _ in range(10)]
    for y in range(3, 8):
        for x in range(3, 9):
            img[y][x] = (rng.randint(180, 255), rng.randint(100, 160), rng.randint(0, 50))
    alpha, _ = grabcut(img, rect_trimap(12, 10, (2, 2, 10, 9)), random.Random(2))
    assert alpha == [[1 if 3 <= y < 8 and 3 <= x < 9 else 0 for x in range(12)] for y in range(10)]
