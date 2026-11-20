# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/nose-hoover-thermostat/. The authors are listed in prov/GC1X6T.jsonl.
import pytest

from nose_hoover_thermostat import harmonic, kinetic, nose_hoover_thermostat


def sample_oscillator(steps_per_sample, samples, h=0.05, q=1.0):
    """One oscillator, m = k = kT = 1, from x = 1, v = 0; returns (x, v) samples."""
    x, v, xi, eta = [[1.0]], [[0.0]], 0.0, 0.0
    out = []
    for _ in range(samples):
        x, v, xi, eta, _ = nose_hoover_thermostat(x, v, [1.0], harmonic(1.0), h, steps_per_sample, 1.0, q, 1, xi, eta)
        out.append((x[0][0], v[0][0]))
    return out


def test_extended_energy_is_conserved_with_second_order_error():
    spreads = []
    for h in (0.1, 0.05, 0.025):
        n = round(20 / h)
        _, _, _, _, es = nose_hoover_thermostat([[1.0], [0.3]], [[0.0], [0.7]], [1.0, 2.0], harmonic(1.0), h, n, 1.0, 0.5, 2)
        spreads.append(max(es) - min(es))
    assert spreads[0] / spreads[1] == pytest.approx(4.0, rel=0.15)
    assert spreads[1] / spreads[2] == pytest.approx(4.0, rel=0.15)
    assert spreads[2] < 5e-3


def test_time_reversible():
    m = [1.0, 2.0]
    x0, v0 = [[1.0], [0.3]], [[0.0], [0.7]]
    x, v, xi, eta, _ = nose_hoover_thermostat(x0, v0, m, harmonic(1.0), 0.05, 300, 1.0, 0.5, 2)
    x, v, xi, eta, _ = nose_hoover_thermostat(x, [[-c for c in p] for p in v], m, harmonic(1.0), 0.05, 300, 1.0, 0.5, 2, -xi, eta)
    assert x == [pytest.approx(p, abs=1e-9) for p in x0]
    assert [[-c for c in p] for p in v] == [pytest.approx(p, abs=1e-9) for p in v0]
    assert xi == pytest.approx(0.0, abs=1e-9)


def test_time_average_of_kinetic_energy_matches_target():
    # Q dxi/dt = 2K - N_f kT and xi stays bounded, so the time average of
    # 2K tends to N_f kT, here 1.
    out = sample_oscillator(5, 2000)
    mean_2k = sum(v * v for _, v in out) / len(out)
    assert mean_2k == pytest.approx(1.0, abs=0.05)


def test_single_oscillator_is_not_canonical():
    # The canonical law gives <x^2> = 1 and <x^4> / <x^2>^2 = 3. One
    # oscillator with one Nose-Hoover thermostat is not ergodic: its
    # trajectory stays near a torus and gives other values.
    out = sample_oscillator(10, 1000)
    x2 = sum(x * x for x, _ in out) / len(out)
    x4 = sum(x ** 4 for x, _ in out) / len(out)
    assert x2 < 0.9
    assert x4 / (x2 * x2) < 2.0


def test_large_thermostat_mass_is_velocity_verlet():
    x, v, xi, _, _ = nose_hoover_thermostat([[1.0]], [[0.0]], [1.0], harmonic(1.0), 0.05, 200, 1.0, 1e15, 1)
    assert abs(xi) < 1e-12
    assert kinetic(v, [1.0]) + 0.5 * x[0][0] ** 2 == pytest.approx(0.5, abs=1e-3)


def test_bad_arguments_raise():
    with pytest.raises(ValueError):
        nose_hoover_thermostat([[1.0]], [[0.0]], [1.0], harmonic(1.0), 0.05, 1, 1.0, 0.0, 1)
