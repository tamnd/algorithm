# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/provot-strain-limiting/. The authors are listed in prov/SR6S3F.jsonl.

"""Tests of Provot's strain limiting: one correction, the projection property, sweeps and a hanging cloth."""

import math
import random

import provot_strain_limiting as p


def test_one_spring_both_free_and_one_fixed():
    x = [(0.0, 0.0), (1.5, 0.0)]
    s = (0, 1, 1.0, 1.0)
    y, _ = p.limit_strain(x, [1.0, 1.0], [s], 0.1)
    assert abs(math.dist(y[0], y[1]) - 1.1) < 1e-15
    assert abs((y[0][0] + y[1][0]) / 2 - 0.75) < 1e-15  # the midpoint stays
    y, _ = p.limit_strain(x, [0.0, 1.0], [s], 0.1)
    assert y[0] == (0.0, 0.0) and abs(y[1][0] - 1.1) < 1e-15
    y, _ = p.limit_strain(x, [0.0, 0.0], [s], 0.1)
    assert y == x
    # a short spring is not touched: the method limits stretch only
    y, _ = p.limit_strain([(0.0, 0.0), (0.5, 0.0)], [1.0, 1.0], [s], 0.1)
    assert y == [(0.0, 0.0), (0.5, 0.0)]


def test_correction_is_the_closest_point():
    """Against brute force: no random point of the allowed set is closer."""
    rng = random.Random(3)
    for weights, inv in (("equal", [1.0, 1.0]), ("mass", [2.0, 0.5]), ("equal", [0.0, 1.0])):
        a = (rng.uniform(-1, 1), rng.uniform(-1, 1))
        b = (a[0] + 2.0, a[1] + 0.7)
        y, _ = p.limit_strain([a, b], inv, [(0, 1, 1.0, 1.0)], 0.1, weights=weights)
        free = [i for i in range(2) if inv[i] > 0.0]
        # the metric is sum |dx_i|^2 / w_i over the free particles (w = 1 for Provot's rule)
        wt = [1.0 / inv[i] if weights == "mass" else 1.0 for i in range(2)]

        def cost(q):
            return sum(wt[i] * math.dist(q[i], [a, b][i]) ** 2 for i in free)

        best = cost(y)
        for _ in range(4000):
            q = [a, b]
            q = [(c[0] + rng.uniform(-1, 1), c[1] + rng.uniform(-1, 1)) if i in free else c for i, c in enumerate(q)]
            if math.dist(q[0], q[1]) <= 1.1:
                assert cost(q) >= best - 1e-12


def test_mass_weights_keep_the_centre_of_mass():
    rng = random.Random(5)
    x, st, sh = p.grid(6, 6, 0.1, 1.0, 1.0)
    x = [(c[0] * rng.uniform(1.0, 1.6), c[1] * rng.uniform(1.0, 1.6)) for c in x]
    mass = [rng.uniform(0.5, 2.0) for _ in x]
    inv = [1.0 / m for m in mass]
    y, _ = p.limit_strain(x, inv, st + sh, 0.1, sweeps=5, weights="mass")
    for d in range(2):
        before = sum(m * c[d] for m, c in zip(mass, x))
        after = sum(m * c[d] for m, c in zip(mass, y))
        assert abs(before - after) <= 1e-10 * sum(m * abs(c[d]) for m, c in zip(mass, x))


def test_one_sweep_is_not_enough():
    # a - b - c with both springs too long: the second correction stretches the first spring again
    x = [(0.0, 0.0), (1.5, 0.0), (3.5, 0.0)]
    springs = [(0, 1, 1.0, 1.0), (1, 2, 1.0, 1.0)]
    y, _ = p.limit_strain(x, [1.0, 1.0, 1.0], springs, 0.1, sweeps=1)
    assert p.strain(y, springs[0]) > 0.1 + 1e-3
    assert abs(p.strain(y, springs[1]) - 0.1) < 1e-12
    y, n = p.limit_strain(x, [1.0, 1.0, 1.0], springs, 0.1, sweeps=None, slack=1e-3)
    assert 1 < n < 10000 and p.max_strain(y, springs) <= 0.1


def test_repeated_sweeps_end_when_the_limits_can_hold():
    """Pins at rest positions: the rest shape satisfies every limit, so the sweeps stop."""
    rng = random.Random(8)
    x, st, sh = p.grid(8, 8, 0.1, 1.0, 1.0)
    inv = [1.0] * len(x)
    inv[0] = inv[7] = 0.0
    y = [c if inv[i] == 0.0 else (c[0] + rng.uniform(-0.08, 0.08), c[1] + rng.uniform(-0.08, 0.08))
         for i, c in enumerate(x)]
    assert p.max_strain(y, st + sh) > 0.5
    z, n = p.limit_strain(y, inv, st + sh, 0.1, sweeps=None, slack=1e-3)
    assert n < 10000
    for s in st + sh:
        assert math.dist(z[s[0]], z[s[1]]) <= 1.1 * s[2]
    assert z[0] == x[0] and z[7] == x[7]


def test_fixed_ends_forcing_a_stretch_do_not_converge():
    """Bridson et al. 2002, Section 4: fixed boundaries that force more than 10% cannot be met."""
    n = 6
    x = [(1.3 * i, 0.0) for i in range(n)]
    inv = [1.0] * n
    inv[0] = inv[-1] = 0.0
    springs = [(i, i + 1, 1.0, 1.0) for i in range(n - 1)]
    y, sweeps = p.limit_strain(x, inv, springs, 0.1, sweeps=None, slack=1e-3)
    assert sweeps == 10000
    # the springs sum to at least 6.5, so one of the five is at least 30% too long
    assert p.max_strain(y, springs) >= 0.3 - 1e-12


def hanging(sweeps, limit, steps=1000):
    x, st, sh = p.grid(9, 9, 0.1, 50.0, 50.0)
    n = len(x)
    mass = [0.01] * n
    inv = [100.0] * n
    inv[0] = inv[8] = 0.0  # hung by the two top corners
    v = [(0.0, 0.0)] * n
    worst = 0.0
    for _ in range(steps):
        x, v = p.step(x, v, mass, inv, st + sh, 0.002, tau=0.1, sweeps=sweeps,
                      limited=st if limit else [], damping=0.05, slack=1e-3 if sweeps is None else 0.0)
        worst = max(worst, p.max_strain(x, st))
    return worst


def test_hanging_cloth_super_elastic_and_limited():
    soft = hanging(0, False)
    one = hanging(1, True)
    two = hanging(2, True)
    full = hanging(None, True)
    assert soft > 0.5  # the corner springs of the soft cloth stretch by more than 50%
    assert full <= 0.1  # repeated sweeps: no structural spring is longer than 110%
    assert 0.1 < two < one < 0.2  # one or two sweeps leave a small excess; two is better
