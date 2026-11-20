# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cadis/. The authors are listed in prov/VERVKH.jsonl.
import math
import random

import pytest

from cadis import apply_window, cadis_parameters, gauss_legendre, run_monte_carlo, sn_solve

L, M = 10.0, 40
H = L / M
Q = [1.0 if i < 4 else 0.0 for i in range(M)]  # source in [0, 1]
SD = [1.0 if i >= 36 else 0.0 for i in range(M)]  # detector in [9, 10]


class FixedRng:
    def __init__(self, values):
        self.values = list(values)

    def random(self):
        return self.values.pop(0)


def reference_response(c):
    """R on a mesh 4 times finer with S_32, per source particle."""
    m = 4 * M
    h = L / m
    q = [1.0 if i < 16 else 0.0 for i in range(m)]  # density 1 on [0, 1]: one source particle
    phi = sn_solve(q, L, 1.0, c, order=32)
    return sum(p * h for i, p in enumerate(phi) if i >= 144)


def test_gauss_legendre():
    nodes, weights = gauss_legendre(16)
    assert sum(weights) == pytest.approx(2.0, abs=1e-13)
    assert sum(w * x**2 for x, w in zip(nodes, weights)) == pytest.approx(2.0 / 3.0, abs=1e-13)


def test_sn_infinite_medium_limit():
    # A thick slab with a uniform source: the center flux tends to q / sigma_a = 1 / 0.5 = 2.
    phi = sn_solve([1.0] * 100, 100.0, 1.0, 0.5, order=8)
    assert phi[50] == pytest.approx(2.0, rel=1e-6)


def test_sn_pure_absorber_beam_like():
    # A source in the first cell only and no scattering: the flux far away falls at least like e^(-x).
    phi = sn_solve([1.0] + [0.0] * 39, 10.0, 1.0, 0.0, order=16)
    assert all(phi[i + 1] < phi[i] * math.exp(-H) * 1.0001 for i in range(1, 39))


@pytest.mark.parametrize("c", [0.5, 0.9])
def test_adjoint_reciprocity(c):
    # <q, phi+> from the adjoint solve equals <sigma_d, phi> from the forward solve.
    p = cadis_parameters(Q, SD, L, 1.0, c)
    phi = sn_solve(p["q"], L, 1.0, c)
    forward = sum(s * f * H for s, f in zip(SD, phi))
    assert p["response"] == pytest.approx(forward, rel=1e-9)


def test_consistent_source_and_windows():
    p = cadis_parameters(Q, SD, L, 1.0, 0.5, c_u=5.0)
    assert sum(p["source_pdf"]) == pytest.approx(1.0, abs=1e-12)
    for i in range(M):
        # the weight times the biased probability is the true probability: the source is unbiased
        assert p["birth_weight"][i] * p["source_pdf"][i] == pytest.approx(p["q"][i] * H, abs=1e-15)
        # particles are born at the target weight, inside their window
        assert p["lower"][i] < p["birth_weight"][i] < p["upper"][i]
        assert p["upper"][i] / p["lower"][i] == pytest.approx(5.0)
        assert (p["lower"][i] + p["upper"][i]) / 2 == pytest.approx(p["target"][i])
    # the importance grows toward the detector, so the targets fall
    assert all(p["target"][i] > p["target"][i + 1] for i in range(30))


def test_window_game_keeps_the_weight():
    lower, upper, target = [1.0], [5.0], [3.0]
    stack = []
    w = apply_window(0.0, 1.0, 12.0, 0, lower, upper, target, FixedRng([]), stack)
    assert w == pytest.approx(4.0) and len(stack) == 2  # ceil(12 / 5) = 3 copies of 4
    assert w + sum(s[2] for s in stack) == pytest.approx(12.0)
    assert apply_window(0.0, 1.0, 0.6, 0, lower, upper, target, FixedRng([0.19]), []) == 3.0  # 0.19 < 0.2
    assert apply_window(0.0, 1.0, 0.6, 0, lower, upper, target, FixedRng([0.21]), []) == 0.0
    assert apply_window(0.0, 1.0, 2.0, 0, lower, upper, target, FixedRng([]), []) == 2.0
    # the roulette keeps the mean: 0.6 = P(survive) * 3 = 0.2 * 3


@pytest.mark.parametrize("c", [0.5, 0.9])
def test_cadis_and_analog_agree_with_reference(c):
    ref = reference_response(c)
    p = cadis_parameters(Q, SD, L, 1.0, c)
    m, se, _ = run_monte_carlo(4000, L, 1.0, c, SD, random.Random(11), params=p)
    assert abs(m - ref) < 4.0 * se + 0.01 * ref
    m, se, _ = run_monte_carlo(20000, L, 1.0, c, SD, random.Random(12), q=Q)
    assert abs(m - ref) < 4.0 * se + 0.01 * ref


def test_cadis_beats_analog():
    # Measured with fixed seeds: the figure of merit per flight is far larger with CADIS.
    p = cadis_parameters(Q, SD, L, 1.0, 0.5)
    m_c, se_c, f_c = run_monte_carlo(4000, L, 1.0, 0.5, SD, random.Random(7), params=p)
    m_a, se_a, f_a = run_monte_carlo(40000, L, 1.0, 0.5, SD, random.Random(7), q=Q)
    fom_c = 1.0 / ((se_c / m_c) ** 2 * f_c)
    fom_a = 1.0 / ((se_a / m_a) ** 2 * f_a)
    assert fom_c > 10.0 * fom_a
