# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/umbrella-sampling/. The authors are listed in prov/H90CB5.jsonl.
import math
import random

import pytest

from umbrella_sampling import (
    bin_centers,
    double_well,
    harmonic_bias,
    histogram,
    join_windows,
    metropolis,
    umbrella_sampling,
    unbias,
)


def test_histogram_and_bin_centers():
    assert histogram([0.05, 0.15, 0.17, 0.99, 1.2, -0.1], 0.0, 1.0, 10) == [1, 2, 0, 0, 0, 0, 0, 0, 0, 1]
    assert bin_centers(0.0, 1.0, 4) == pytest.approx([0.125, 0.375, 0.625, 0.875])


def test_unbias_recovers_profile_from_exact_counts():
    # Counts proportional to exp(-(F + w)) give back F up to one constant.
    centers = bin_centers(-1.0, 1.0, 20)
    f = [math.sin(3 * s) for s in centers]
    w = harmonic_bias(0.3, 5.0)
    counts = [1e5 * math.exp(-(fb + w(s))) for fb, s in zip(f, centers)]
    prof = unbias(counts, w, centers, 1.0)
    shifts = [p - fb for p, fb in zip(prof, f)]
    assert max(shifts) - min(shifts) < 1e-12


def test_unbias_drops_sparse_bins():
    centers = bin_centers(0.0, 1.0, 3)
    prof = unbias([100, 3, 0], lambda s: 0.0, centers, 1.0, min_count=10)
    assert prof[1] is None and prof[2] is None
    assert prof[0] == pytest.approx(-math.log(100))


def test_join_removes_window_constants_exactly():
    true = [0.0, 1.0, 3.0, 2.0, 0.5, 1.5]
    a = [v + 7.0 for v in true[:4]] + [None, None]
    b = [None, None] + [v - 2.0 for v in true[2:]]
    joined = join_windows([a, b], [[100] * 6, [100] * 6])
    assert joined == pytest.approx(true)


def test_join_needs_shared_bins():
    with pytest.raises(ValueError):
        join_windows([[0.0, None], [None, 0.0]], [[100, 0], [0, 100]])


def test_plain_sampling_is_trapped_in_one_well():
    # Barrier of 8 kT: a plain chain started at x = -1 does not cross in 50000 steps.
    xs = metropolis(double_well(8.0), 1.0, -1.0, 0.3, 50000, random.Random(2))
    assert max(xs) < 0.0


def test_double_well_profile_against_exact():
    u = double_well(8.0)
    lo, hi, nb = -1.6, 1.6, 32
    windows = [-1.6 + 0.2 * k for k in range(17)]
    f, counts = umbrella_sampling(u, windows, 50.0, 1.0, 20000, 0.3, lo, hi, nb, random.Random(1))
    centers = bin_centers(lo, hi, nb)
    # Every bin below 9 kT has enough samples, including the barrier top.
    assert all(v is not None for v, s in zip(f, centers) if u(s) < 9.0)
    assert min(v for v in f if v is not None) == 0.0
    # Here s = x, so the exact profile is U up to a constant.
    pairs = [(v, u(s)) for v, s in zip(f, centers) if u(s) < 9.0]
    off = sum(e - v for v, e in pairs) / len(pairs)
    assert max(abs(v + off - e) for v, e in pairs) < 0.4
    i0, im, ip = 16, 6, 25  # bins centred at 0.05, -0.95 and 0.95
    assert centers[i0] == pytest.approx(0.05) and centers[im] == pytest.approx(-0.95)
    assert centers[ip] == pytest.approx(0.95)
    barrier = f[i0] - f[ip]
    assert barrier == pytest.approx(u(centers[i0]) - u(centers[ip]), abs=0.4)
    assert abs(f[im] - f[ip]) < 0.4
