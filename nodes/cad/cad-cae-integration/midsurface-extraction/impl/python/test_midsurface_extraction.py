# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/midsurface-extraction/. The authors are listed in prov/FG99C0.jsonl.

import math
import random

from midsurface_extraction import (
    medial_points,
    midline,
    sector_samples,
    shrinking_ball,
    strip_samples,
    tangent_radius,
)

L, T, S = 10.0, 1.0, 0.1


def test_shrinking_ball_returns_the_smallest_tangent_radius() -> None:
    """Lemma 1: the loop stops at r* = min over samples of the tangent radius, for any point set."""
    rng = random.Random(7)
    found = 0
    for _ in range(30):
        pts = [(rng.uniform(-1, 1), rng.uniform(-1, 1)) for _ in range(40)]
        a = rng.uniform(0, 2 * math.pi)
        nrm = [(math.cos(a), math.sin(a))] * len(pts)
        for i in range(0, 40, 7):
            c, r, j, _ = shrinking_ball(pts, nrm, i, 1e6)
            best = min(tangent_radius(pts[i], nrm[i], q) for k, q in enumerate(pts) if k != i)
            if best == math.inf:  # no sample on the inner side: the disk never shrinks
                assert j is None and r == 1e6
                continue
            found += 1
            assert j is not None and abs(r - best) <= 1e-12 * max(1.0, best)
            assert abs(tangent_radius(pts[i], nrm[i], pts[j]) - r) <= 1e-12 * max(1.0, r)
            # no sample lies strictly inside the final disk
            assert all(math.hypot(q[0] - c[0], q[1] - c[1]) >= r * (1 - 1e-9) for q in pts)
    assert found > 100


def test_strip_aligned_samples_give_the_exact_midline() -> None:
    """Theorem 2: aligned samples on a strip give centers on y = 0 with radius t/2 exactly."""
    pts, nrm = strip_samples(L, T, S)
    mp = medial_points(pts, nrm, 120.0)
    assert len(mp) > 150
    for c, r, _, _, ang in mp:
        assert abs(c[1]) < 1e-12 and abs(r - T / 2) < 1e-12 and ang > 179.9
    xs = [m[0][0] for m in mp]
    # the medial axis of the strip runs from x = t/2 to x = L - t/2
    assert T / 2 - 1e-9 <= min(xs) <= T / 2 + S and L - T / 2 - S <= max(xs) <= L - T / 2 + 1e-9


def test_strip_staggered_samples_meet_the_error_bound() -> None:
    """Theorem 2: with offset d between the sides, the error of the center and of the radius is d^2 / (2t)."""
    pts, nrm = strip_samples(L, T, S, stagger=True)
    mp = medial_points(pts, nrm, 120.0)
    bound = S * S / (8 * T)
    errs = [abs(c[1]) for c, _, _, _, _ in mp] + [abs(r - T / 2) for _, r, _, _, _ in mp]
    assert max(errs) <= bound * (1 + 1e-9)
    assert max(errs) >= bound * (1 - 1e-9)  # the bound is attained for d = s/2


def test_separation_angle_prunes_the_corner_branches() -> None:
    pts, nrm = strip_samples(L, T, S)
    raw = medial_points(pts, nrm, 0.0, r_min=0.0)
    assert any(abs(c[1]) > T / 4 for c, _, _, _, _ in raw)  # corner bisector points exist
    assert all(abs(ang - 90) < 1e-6 or ang > 179.9 for _, _, _, _, ang in raw)
    kept = medial_points(pts, nrm, 120.0)
    assert all(abs(c[1]) < 1e-12 for c, _, _, _, _ in kept)


def test_annular_sector_midline_is_the_mean_arc() -> None:
    r1, r2, phi = 2.0, 2.5, math.pi / 2
    pts, nrm = sector_samples(r1, r2, phi, 120, 10)
    mp = medial_points(pts, nrm, 120.0)
    rm, t = (r1 + r2) / 2, r2 - r1
    theta0 = math.asin(t / (2 * rm))
    angles = []
    for c, r, _, _, _ in mp:
        assert abs(math.hypot(*c) - rm) < 1e-12 and abs(r - t / 2) < 1e-12
        angles.append(math.atan2(c[1], c[0]))
    h = phi / 120
    assert theta0 - h <= min(angles) <= theta0 + h
    assert phi - theta0 - h <= max(angles) <= phi - theta0 + h


def test_tapered_strip_gives_the_perpendicular_thickness() -> None:
    """Sides y = +-(t0/2 + k x): the midline is y = 0 and 2r is the thickness normal to the sides."""
    t0, k, n = 1.0, 0.05, 100
    pts, nrm = [], []
    m = 1 / math.sqrt(1 + k * k)
    for i in range(n):
        x = (i + 0.5) * L / n
        h = t0 / 2 + k * x
        pts += [(x, -h), (x, h)]
        nrm += [(k * m, m), (k * m, -m)]
    for i in range(10):
        y = -0.5 + (i + 0.5) / 10
        pts += [(0.0, y * t0), (L, y * (t0 + 2 * k * L))]
        nrm += [(1.0, 0.0), (-1.0, 0.0)]
    mp = medial_points(pts, nrm, 120.0)
    assert len(mp) > 150
    for c, r, _, _, _ in mp:
        assert abs(c[1]) < 1e-12
        assert abs(r - (t0 / 2 + k * c[0]) * m) < 1e-12


def test_midline_is_one_ordered_chain_with_thickness() -> None:
    pts, nrm = strip_samples(L, T, S)
    chains = midline(pts, nrm)
    assert len(chains) == 1
    ch = chains[0]
    xs = [p[0] for p in ch]
    assert xs == sorted(xs) or xs == sorted(xs, reverse=True)
    assert all(abs(p[2] - T) < 1e-12 for p in ch)
    assert abs(abs(xs[-1] - xs[0]) - (L - T)) < 2 * S
