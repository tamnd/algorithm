# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/track-length-estimator/. The authors are listed in prov/QW4YNY.jsonl.
import math
import random

import pytest

from track_length_estimator import fly, track_length_estimator, uniform_isotropic_source


class FixedRng:
    def __init__(self, values):
        self.values = list(values)

    def random(self):
        return self.values.pop(0)


def expint(order, z, steps=2000):
    """E_n(z) = integral over u in (0, 1] of exp(-z/u) u^(n-2) du, by Simpson's rule (n >= 2)."""
    if z == 0.0:
        return 1.0 / (order - 1)
    h = 1.0 / steps
    total = 0.0
    for k in range(steps + 1):
        u = k * h
        f = 0.0 if u == 0.0 else math.exp(-z / u) * u ** (order - 2)
        total += f * (1 if k in (0, steps) else (4 if k % 2 else 2))
    return total * h / 3.0


def test_one_history_by_hand():
    # Beam on a slab of 2 cm, sigma_t = 1, pure absorber, two bins of 1 cm.
    # r = 0.25: xi = 0.75, flight -ln 0.75 = 0.287682, all in bin 0. r = 0.5: absorbed.
    phi, _ = track_length_estimator(1 + 1, 2.0, 1.0, 0.0, 2, FixedRng([0.25, 0.5, 0.9, 0.5]))
    # The second history: r = 0.9 gives a flight ln 10 = 2.302585, which leaves the slab.
    # It scores 1 cm in each bin. Totals: bin 0 = 1.287682, bin 1 = 1.0; N = 2.
    assert phi == pytest.approx([1.287682 / 2, 1.0 / 2], abs=1e-6)


def test_slanted_segment_and_reflection():
    hist = {}
    fly(0.25, 0.5, 1.0, 2.0, "vacuum", 1.0, 0.5, 4, hist)  # x goes from 0.25 to 0.75
    assert hist == pytest.approx({0: 0.5, 1: 0.5})
    hist = {}
    x, mu, inside = fly(1.5, 1.0, 1.0, 2.0, "reflect", 1.0, 1.0, 2, hist)
    assert inside and x == pytest.approx(1.5) and mu == -1.0
    assert hist == pytest.approx({1: 1.0})


def test_pure_absorber_beam_exact():
    sig, length, nb, n = 1.0, 2.0, 4, 20000
    phi, se = track_length_estimator(n, length, sig, 0.0, nb, random.Random(1))
    dx = length / nb
    for j in range(nb):
        exact = (math.exp(-sig * j * dx) - math.exp(-sig * (j + 1) * dx)) / (sig * dx)
        assert abs(phi[j] - exact) < 4.0 * se[j]


def test_reflecting_slab_is_infinite_medium():
    length, sig_t, sig_s, n = 2.0, 1.0, 0.5, 6000
    phi, se = track_length_estimator(n, length, sig_t, sig_s, 4, random.Random(2), uniform_isotropic_source, "reflect")
    exact = (1.0 / length) / (sig_t - sig_s)
    for p, e in zip(phi, se):
        assert abs(p - exact) < 4.0 * e


def test_pure_absorber_volume_source_against_e3():
    length, sig, nb, n = 2.0, 1.0, 4, 20000
    phi, se = track_length_estimator(n, length, sig, 0.0, nb, random.Random(3), uniform_isotropic_source)
    q, dx = 1.0 / length, length / nb
    for j in range(nb):
        a, b = j * dx, (j + 1) * dx
        left = (expint(3, sig * a) - expint(3, sig * b)) / sig
        right = (expint(3, sig * (length - b)) - expint(3, sig * (length - a))) / sig
        exact = q / (2.0 * sig * dx) * (2.0 * dx - left - right)
        assert abs(phi[j] - exact) < 4.0 * se[j]


def collision_tally(n, length, sig_t, sig_s, nbins, rng):
    """A plain collision estimator on the same problem, for comparison."""
    dx, p_abs = length / nbins, (sig_t - sig_s) / sig_t
    tot, tot_sq = [0.0] * nbins, [0.0] * nbins
    for _ in range(n):
        x, mu = 0.0, 1.0  # a normal beam on the left face
        hist = [0.0] * nbins
        while True:
            x += mu * -math.log(1.0 - rng.random()) / sig_t
            if not 0.0 <= x <= length:
                break
            hist[min(int(x / dx), nbins - 1)] += 1.0 / sig_t
            if rng.random() < p_abs:
                break
            mu = 2.0 * rng.random() - 1.0
        for j in range(nbins):
            tot[j] += hist[j]
            tot_sq[j] += hist[j] ** 2
    mean = [t / n for t in tot]
    se = [math.sqrt((s / n - m * m) / (n - 1)) / dx for s, m in zip(tot_sq, mean)]
    return [m / dx for m in mean], se


def test_thin_slab_track_length_beats_collision():
    # In an optically thin slab few histories collide, so the collision tally is noisy.
    # With a normal beam, every uncollided particle scores exactly dx in each bin.
    length, sig_t, sig_s, nb, n = 1.0, 0.1, 0.05, 4, 8000
    phi_t, se_t = track_length_estimator(n, length, sig_t, sig_s, nb, random.Random(4))
    phi_c, se_c = collision_tally(n, length, sig_t, sig_s, nb, random.Random(5))
    for j in range(nb):
        assert abs(phi_t[j] - phi_c[j]) < 4.0 * math.hypot(se_t[j], se_c[j])
        assert se_t[j] < 0.5 * se_c[j]
