# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/monte-carlo-criticality/. The authors are listed in prov/1ER0M9.jsonl.
import math
import random

import pytest

from monte_carlo_criticality import (
    gauss_legendre,
    monte_carlo_criticality,
    run_cycle,
    shannon_entropy,
    sn_k_eigenvalue,
)


class FixedRng:
    """Returns the given numbers in order, so that a cycle can be checked by hand."""

    def __init__(self, values):
        self.values = list(values)

    def random(self):
        return self.values.pop(0)


def test_hand_trace_of_one_neutron():
    # L = 2, sigma_t = 1, sigma_s = 0.5, nu_sigma_f = 0.6, k_prev = 1, one site at x = 1.
    # r = 0.75: mu = 0.5. r = 0.5: s = ln 2, x = 1.346574. Score 0.6.
    # r = 0.3: floor(0.6 + 0.3) = 0 sites. r = 0.2 < 0.5: scatter. r = 0.0: mu = -1.
    # r = 0.6: s = -ln 0.4 = 0.916291, x = 0.430283. Score 0.6, total 1.2.
    # r = 0.7: floor(0.6 + 0.7) = 1 site. r = 0.9 >= 0.5: absorbed.
    rng = FixedRng([0.75, 0.5, 0.3, 0.2, 0.0, 0.6, 0.7, 0.9])
    bank, k = run_cycle([1.0], 2.0, 1.0, 0.5, 0.6, 1.0, rng)
    assert k == pytest.approx(1.2)
    assert len(bank) == 1
    assert bank[0] == pytest.approx(1.0 + 0.5 * math.log(2.0) - math.log(2.5), abs=1e-12)
    assert bank[0] == pytest.approx(0.430283, abs=1e-6)


def test_leak_on_first_flight():
    rng = FixedRng([1.0 - 1e-12, 0.99])  # mu close to 1, flight -ln(0.01) = 4.6 > L - x
    bank, k = run_cycle([1.0], 2.0, 1.0, 0.5, 0.6, 1.0, rng)
    assert bank == [] and k == 0.0


def test_entropy_values():
    assert shannon_entropy([0.3] * 50, 1.0, 8) == 0.0
    assert shannon_entropy([(j + 0.5) / 8 for j in range(8)], 1.0, 8) == pytest.approx(3.0)
    assert shannon_entropy([0.1, 0.1, 0.9, 0.9], 1.0, 2) == pytest.approx(1.0)


def test_infinite_medium_k_inf():
    # k_inf = nu_sigma_f / sigma_a = 0.12 / 0.1 = 1.2; each neutron has 1 / (1 - c) = 10 collisions.
    r = monte_carlo_criticality(math.inf, 1.0, 0.9, 0.12, 500, 2, 20, random.Random(1))
    assert abs(r["k"] - 1.2) < 4.0 * r["std_error"]
    assert 0.004 < r["std_error"] < 0.02


def test_gauss_legendre():
    nodes, weights = gauss_legendre(8)
    assert sum(weights) == pytest.approx(2.0, abs=1e-13)
    for p in range(0, 16):  # exact for polynomials of degree 2n - 1 = 15
        exact = 2.0 / (p + 1) if p % 2 == 0 else 0.0
        assert sum(w * x**p for x, w in zip(nodes, weights)) == pytest.approx(exact, abs=1e-13)


def test_sn_reference_limits():
    # A very thick slab tends to k_inf; a thin one leaks and has k below the diffusion value.
    k_thick, _ = sn_k_eigenvalue(400.0, 1.0, 0.9, 0.12, cells=200, order=8)
    assert k_thick == pytest.approx(1.2, abs=2e-3)
    k_slab, phi = sn_k_eigenvalue(20.0, 1.0, 0.9, 0.12, cells=80, order=8)
    assert 1.1088 < k_slab < 1.2  # above the diffusion value without extrapolation, 1.108804
    assert min(phi) > 0.0 and phi[0] == pytest.approx(phi[-1], rel=1e-9)  # positive and symmetric
    k_odd, _ = sn_k_eigenvalue(20.0, 1.0, 0.9, 0.12, cells=80, order=8, parity=-1)
    assert 0.80 < k_odd / k_slab < 0.87  # the dominance ratio


def test_bare_slab_against_sn():
    k_ref, _ = sn_k_eigenvalue(20.0, 1.0, 0.9, 0.12, cells=80, order=8)
    r = monte_carlo_criticality(20.0, 1.0, 0.9, 0.12, 500, 10, 30, random.Random(2))
    assert abs(r["k"] - k_ref) < 4.0 * r["std_error"] + 0.003
    assert len(r["k_cycles"]) == 40 and len(r["entropy"]) == 40


def test_entropy_rises_from_a_point_source():
    r = monte_carlo_criticality(20.0, 1.0, 0.9, 0.12, 1000, 0, 30, random.Random(3), start=1.0)
    h = r["entropy"]
    assert h[0] < 3.0  # the first bank is near x = 1
    late = sum(h[20:]) / 10
    assert 4.05 < late < 4.32  # near the entropy of the fundamental mode, 4.185, and below log2(20)
    assert sum(r["k_cycles"][:2]) / 2 < sum(r["k_cycles"][20:]) / 10  # early cycles leak more
