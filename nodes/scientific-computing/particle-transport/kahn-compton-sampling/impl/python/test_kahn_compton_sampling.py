# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kahn-compton-sampling/. The authors are listed in prov/7W42N2.jsonl.
import math
import random

import pytest

from kahn_compton_sampling import kahn_efficiency, kahn_sample, klein_nishina_mu_density, scattered_energy


def kn_moments(alpha, steps=4000):
    """Exact mean of mu and mu^2 under Klein-Nishina, by Simpson's rule in mu."""
    h = 2.0 / steps
    z = m1 = m2 = 0.0
    for i in range(steps + 1):
        mu = -1.0 + i * h
        f = klein_nishina_mu_density(alpha, mu) * (1 if i in (0, steps) else (4 if i % 2 else 2))
        z += f
        m1 += f * mu
        m2 += f * mu * mu
    return m1 / z, m2 / z


def reference_sample(alpha, rng):
    """Brute force: uniform mu, accepted with density / max (the max is at mu = 1, where it is 2)."""
    while True:
        mu = 2.0 * rng.random() - 1.0
        if 2.0 * rng.random() <= klein_nishina_mu_density(alpha, mu):
            return mu


@pytest.mark.parametrize("alpha", [0.1, 1.0, 5.0])
def test_moments_match_klein_nishina(alpha):
    rng = random.Random(int(alpha * 10) + 1)
    n = 20000
    mus = [kahn_sample(alpha, rng)[1] for _ in range(n)]
    e1, e2 = kn_moments(alpha)
    m1 = sum(mus) / n
    m2 = sum(m * m for m in mus) / n
    sd1 = math.sqrt(max(e2 - e1 * e1, 1e-12))
    assert abs(m1 - e1) < 4.0 * sd1 / math.sqrt(n)
    assert abs(m2 - e2) < 4.0 / math.sqrt(n)  # mu^2 lies in [0, 1], so its sd is below 1


def test_histogram_matches_brute_force():
    alpha, n, nb = 1.0, 20000, 8
    rng = random.Random(42)
    a = [kahn_sample(alpha, rng)[1] for _ in range(n)]
    b = [reference_sample(alpha, rng) for _ in range(n)]
    for j in range(nb):
        lo, hi = -1.0 + 2.0 * j / nb, -1.0 + 2.0 * (j + 1) / nb
        pa = sum(1 for m in a if lo <= m < hi) / n
        pb = sum(1 for m in b if lo <= m < hi) / n
        assert abs(pa - pb) < 4.0 * math.sqrt(2.0 * max(pa, 1e-3) / n)


@pytest.mark.parametrize("alpha", [0.1, 1.0, 5.0])
def test_acceptance_rate(alpha):
    rng = random.Random(7)
    n = 20000
    tries = sum(kahn_sample(alpha, rng)[2] for _ in range(n))
    eff = kahn_efficiency(alpha)
    assert 0.0 < eff <= 1.0
    assert n / tries == pytest.approx(eff, abs=4.0 * math.sqrt(eff * (1 - eff) / tries))


def test_thomson_limit_and_ranges():
    rng = random.Random(3)
    n = 20000
    out = [kahn_sample(1e-4, rng) for _ in range(n)]
    m2 = sum(mu * mu for _, mu, _ in out) / n
    assert abs(m2 - 0.4) < 4.0 * 0.3 / math.sqrt(n)  # (1 + mu^2) law: <mu^2> = 2/5
    rng = random.Random(4)
    for _ in range(2000):
        a_out, mu, _ = kahn_sample(2.0, rng)
        assert -1.0 - 1e-12 <= mu <= 1.0 + 1e-12
        assert 2.0 / 5.0 - 1e-12 <= a_out <= 2.0 + 1e-12
        assert a_out == pytest.approx(2.0 / (1.0 + 2.0 * (1.0 - mu)))


def test_hand_values():
    # A 511 keV photon has alpha = 1; at 90 degrees, q = 2 and E' is half of E.
    assert scattered_energy(510.99895, 0.0) == pytest.approx(255.499475)
    # Back scattering of a 1 MeV photon: E' = E / (1 + 2 alpha).
    assert scattered_energy(1000.0, -1.0) == pytest.approx(1000.0 / (1.0 + 2000.0 / 510.99895))
