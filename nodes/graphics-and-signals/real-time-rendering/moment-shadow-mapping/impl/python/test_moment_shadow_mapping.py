# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/moment-shadow-mapping/. The authors are listed in prov/ZPXE0M.jsonl.

import random

from moment_shadow_mapping import canonical_nodes, msm_lookup, power_moments, shadow_intensity

TOL = 1e-7


def solve3(a, r):
    """Gaussian elimination with partial pivoting on a 3 x 3 system."""
    m = [row[:] + [v] for row, v in zip(a, r)]
    for c in range(3):
        p = max(range(c, 3), key=lambda k: abs(m[k][c]))
        m[c], m[p] = m[p], m[c]
        for k in range(c + 1, 3):
            f = m[k][c] / m[c][c]
            for j in range(c, 4):
                m[k][j] -= f * m[c][j]
    x = [0.0] * 3
    for c in (2, 1, 0):
        x[c] = (m[c][3] - sum(m[c][j] * x[j] for j in range(c + 1, 3))) / m[c][c]
    return x


def random_distribution(rng):
    """3 to 7 distinct depths in [0, 1], at least 0.05 apart, with weights."""
    while True:
        k = rng.randrange(3, 8)
        zs = sorted(rng.uniform(0.0, 1.0) for _ in range(k))
        if all(b - a >= 0.05 for a, b in zip(zs, zs[1:])):
            ws = [rng.randrange(1, 10) for _ in range(k)]
            return zs, ws


def occluded(zs, ws, zf):
    return sum(w for z, w in zip(zs, ws) if z < zf) / sum(ws)


def vsm_bound(b, t):
    m1, m2 = b[0], b[1]
    if t <= m1:
        return 1.0
    v = m2 - m1 * m1
    return v / (v + (t - m1) ** 2)


def test_lower_bound_on_the_occluded_fraction():
    rng = random.Random(1)
    for _ in range(400):
        zs, ws = random_distribution(rng)
        b = power_moments(zs, ws)
        for _ in range(5):
            zf = rng.uniform(0.0, 1.0)
            g = shadow_intensity(b, zf)
            assert g <= occluded(zs, ws, zf) + TOL
            assert 1 - min(max(g, 0.0), 1.0) >= 1 - occluded(zs, ws, zf) - TOL


def test_sharp_the_canonical_measure_attains_the_bound():
    rng = random.Random(2)
    for _ in range(300):
        zs, ws = random_distribution(rng)
        b = power_moments(zs, ws)
        zf = rng.uniform(0.0, 1.0)
        nodes = canonical_nodes(b, zf)
        assert abs(nodes[1] - nodes[2]) > 1e-9
        assert min(abs(nodes[0] - nodes[1]), abs(nodes[0] - nodes[2])) > 1e-9
        # Weights from the 3 x 3 Vandermonde system on moments 0, 1, 2.
        vand = [[x ** k for x in nodes] for k in range(3)]
        w = solve3(vand, [1.0, b[0], b[1]])
        assert min(w) > -TOL
        # The same weights reproduce moments 3 and 4 as well.
        assert abs(sum(wi * x ** 3 for wi, x in zip(w, nodes)) - b[2]) < 1e-6
        assert abs(sum(wi * x ** 4 for wi, x in zip(w, nodes)) - b[3]) < 1e-6
        g = sum(wi for wi, x in zip(w, nodes) if x < zf)
        assert abs(g - shadow_intensity(b, zf)) < 1e-6


def test_four_moments_are_at_least_as_tight_as_two():
    rng = random.Random(3)
    for _ in range(400):
        zs, ws = random_distribution(rng)
        b = power_moments(zs, ws)
        t = rng.uniform(0.0, 1.0)
        assert msm_lookup(b, t) <= vsm_bound(b, t) + TOL


def test_moment_bias_costs_at_most_half_alpha():
    rng = random.Random(4)
    for _ in range(300):
        zs, ws = random_distribution(rng)
        b = power_moments(zs, ws)
        alpha = rng.choice([3e-5, 1e-3, 0.05])
        zf = rng.uniform(0.01, 1.0)
        lit = 1 - occluded(zs, ws, zf)
        assert msm_lookup(b, zf, alpha=alpha) >= lit - alpha / 2 - TOL


def test_bias_makes_two_point_maps_usable():
    # Two depths give a singular Hankel matrix; the moment bias fixes it.
    b = power_moments([0.1, 0.9], [1, 1])
    got = msm_lookup(b, 1.0, alpha=3e-5)
    assert 0.0 <= got <= 1.0
    try:
        shadow_intensity(b, 1.0)
    except ValueError:
        pass
    else:
        raise AssertionError("an unbiased two-point map must be rejected")


def test_receiver_in_front_is_lit():
    rng = random.Random(5)
    for _ in range(200):
        zs, ws = random_distribution(rng)
        b = power_moments(zs, ws)
        zf = rng.uniform(-0.5, zs[0])
        assert abs(msm_lookup(b, zf) - 1.0) < TOL
