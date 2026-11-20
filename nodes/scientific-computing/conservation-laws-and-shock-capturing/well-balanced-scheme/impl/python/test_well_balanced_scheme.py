# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/well-balanced-scheme/. The authors are listed in prov/DMAAHD.jsonl.

import math
import random

import pytest

from well_balanced_scheme import G, hr_step, naive_step, run, rusanov


def lake(m, island=False, level=1.0):
    dx = 1.0 / m
    xs = [(i + 0.5) * dx for i in range(m)]
    if island:
        z = [max(0.0, 1.2 - 40 * (x - 0.5) ** 2) for x in xs]
    else:
        z = [0.5 * math.exp(-50 * (x - 0.5) ** 2) for x in xs]
    return xs, dx, [max(0.0, level - zi) for zi in z], [0.0] * m, z


def plain_rusanov_step(h, q, dx, dt):
    """Independent first-order Rusanov scheme for a flat bottom with walls."""
    H, Q = [h[0]] + h + [h[-1]], [-q[0]] + q + [-q[-1]]
    F = [rusanov(H[i], Q[i], H[i + 1], Q[i + 1]) for i in range(len(h) + 1)]
    lam = dt / dx
    return ([h[i] - lam * (F[i + 1][0] - F[i][0]) for i in range(len(h))],
            [q[i] - lam * (F[i + 1][1] - F[i][1]) for i in range(len(h))])


def test_face_by_hand():
    # Surface level 1 over a step: depths 1 and 0.5, bottoms 0 and 0.5.
    h, q, z = [1.0, 0.5], [0.0, 0.0], [0.0, 0.5]
    hn, qn = hr_step(h, q, z, 0.5, 0.01)
    assert hn == h and max(abs(v) for v in qn) < 1e-15
    f0, f1 = rusanov(0.5, 0.0, 0.5, 0.0)
    assert f0 == 0.0 and abs(f1 - G / 8) < 1e-15
    assert abs(rusanov(1.0, 0.0, 0.5, 0.0)[0] - 0.25 * (math.sqrt(G) + 0.0)) < 1e-12


@pytest.mark.parametrize("island", [False, True])
def test_lake_at_rest_is_kept_to_rounding(island):
    xs, dx, h, q, z = lake(80, island)
    hh, qq = run(hr_step, h, q, z, dx, 0.3)
    assert max(abs(v) for v in qq) < 1e-13
    for a, b, a0 in zip(hh, z, h):
        if a0 > 0:
            assert abs(a + b - 1.0) < 1e-13
        else:
            assert a == 0.0


@pytest.mark.parametrize("island", [False, True])
def test_naive_source_term_is_not_well_balanced(island):
    xs, dx, h, q, z = lake(80, island)
    hh, qq = run(naive_step, h, q, z, dx, 0.3)
    assert max(abs(v) for v in qq) > 1e-3


def test_naive_error_is_first_order_in_dx():
    err = []
    for m in (50, 100, 200):
        xs, dx, h, q, z = lake(m)
        err.append(max(abs(v) for v in run(naive_step, h, q, z, dx, 0.5)[1]))
    assert 1.7 < err[0] / err[1] < 2.3 and 1.7 < err[1] / err[2] < 2.3


def test_flat_bottom_reduces_to_the_rusanov_scheme():
    rng = random.Random(5)
    m = 30
    dx = 1.0 / m
    h = [rng.uniform(0.5, 1.5) for _ in range(m)]
    q = [rng.uniform(-0.3, 0.3) for _ in range(m)]
    a = hr_step(h, q, [0.0] * m, dx, 0.2 * dx / 4.5)
    b = plain_rusanov_step(h, q, dx, 0.2 * dx / 4.5)
    assert max(abs(x - y) for x, y in zip(a[0] + a[1], b[0] + b[1])) < 1e-14


def test_mass_conserved_and_depth_nonnegative_for_dam_break_onto_dry_bed_over_a_bump():
    m = 100
    dx = 1.0 / m
    xs = [(i + 0.5) * dx for i in range(m)]
    z = [0.3 * math.exp(-100 * (x - 0.7) ** 2) for x in xs]
    h = [1.0 if x < 0.4 else 0.0 for x in xs]
    q = [0.0] * m
    mass0 = sum(h) * dx
    t, steps = 0.0, 0
    while steps < 150:
        hh = run(hr_step, h, q, z, dx, 0.002)
        h, q = hh
        assert min(h) >= 0.0
        steps += 1
    assert abs(sum(h) * dx - mass0) < 1e-13
    assert max(h[int(0.8 * m):]) > 0.0                 # the water has passed the bump


def test_small_perturbation_stays_local():
    # A small bump on the surface: the well-balanced scheme leaves the far region at rest.
    xs, dx, h, q, z = lake(100)
    h = [a + (1e-3 if 0.1 < x < 0.2 else 0.0) for a, x in zip(h, xs)]
    hh, qq = run(hr_step, h, q, z, dx, 0.05)
    far = [i for i, x in enumerate(xs) if x > 0.6]
    assert max(abs(qq[i]) for i in far) < 1e-13
    hn, qn = run(naive_step, h, q, z, dx, 0.05)
    assert max(abs(qn[i]) for i in far) > 1e-3


def test_rejects_negative_depth():
    with pytest.raises(ValueError):
        run(hr_step, [-1.0, 1.0], [0.0, 0.0], [0.0, 0.0], 0.5, 0.1)
