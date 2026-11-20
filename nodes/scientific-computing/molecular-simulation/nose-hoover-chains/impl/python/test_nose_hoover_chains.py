# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/nose-hoover-chains/. The authors are listed in prov/KYF8ST.jsonl.
import pytest

from nose_hoover_chains import chain_masses, harmonic, kinetic, nose_hoover_chains


def sample_oscillator(q, steps_per_sample, samples, h=0.05):
    """One oscillator, m = k = kT = 1, from x = 1, v = 0; returns x samples."""
    x, v, xi, eta = [[1.0]], [[0.0]], None, None
    out = []
    for _ in range(samples):
        x, v, xi, eta, _ = nose_hoover_chains(x, v, [1.0], harmonic(1.0), h, steps_per_sample, 1.0, q, 1, xi, eta)
        out.append(x[0][0])
    return out


def test_single_oscillator_becomes_canonical_with_a_chain():
    # Canonical values: <x^2> = 1 and <x^4> / <x^2>^2 = 3. A single
    # Nose-Hoover thermostat gives about 0.79 and 1.54 on this system.
    xs = sample_oscillator([1.0] * 4, 10, 1000)
    x2 = sum(x * x for x in xs) / len(xs)
    x4 = sum(x ** 4 for x in xs) / len(xs)
    assert x2 == pytest.approx(1.0, abs=0.15)
    assert x4 / (x2 * x2) == pytest.approx(3.0, abs=0.4)


def test_extended_energy_is_conserved_with_second_order_error():
    q = chain_masses(2, 1.0, 1.0, 3)
    spreads = []
    for h in (0.1, 0.05, 0.025):
        n = round(20 / h)
        _, _, _, _, es = nose_hoover_chains([[1.0], [0.3]], [[0.0], [0.7]], [1.0, 2.0], harmonic(1.0), h, n, 1.0, q, 2)
        spreads.append(max(es) - min(es))
    assert spreads[0] / spreads[1] == pytest.approx(4.0, rel=0.2)
    assert spreads[1] / spreads[2] == pytest.approx(4.0, rel=0.2)


def test_time_reversible():
    q = [0.5, 1.0, 2.0]
    m = [1.0, 2.0]
    x0, v0 = [[1.0], [0.3]], [[0.0], [0.7]]
    x, v, xi, eta, _ = nose_hoover_chains(x0, v0, m, harmonic(1.0), 0.05, 300, 1.0, q, 2)
    back = [[-c for c in p] for p in v]
    x, v, xi, eta, _ = nose_hoover_chains(x, back, m, harmonic(1.0), 0.05, 300, 1.0, q, 2, [-z for z in xi], eta)
    assert x == [pytest.approx(p, abs=1e-9) for p in x0]
    assert [[-c for c in p] for p in v] == [pytest.approx(p, abs=1e-9) for p in v0]
    assert xi == pytest.approx([0.0, 0.0, 0.0], abs=1e-9)


def test_chain_of_length_one_is_nose_hoover():
    # With one link the update is the Nose-Hoover update: the extended
    # energy K + U + Q xi^2 / 2 + N_f kT eta is conserved.
    x, v, xi, eta, es = nose_hoover_chains([[1.0]], [[0.0]], [1.0], harmonic(1.0), 0.02, 500, 1.0, [1.0], 1)
    assert max(abs(e - 0.5) for e in es) < 1e-3
    e = kinetic(v, [1.0]) + 0.5 * x[0][0] ** 2 + 0.5 * xi[0] ** 2 + eta[0]
    assert e == pytest.approx(es[-1], abs=1e-12)


def test_chain_masses_follow_martyna_klein_tuckerman():
    assert chain_masses(30, 2.0, 0.5, 3) == pytest.approx([15.0, 0.5, 0.5])


def test_bad_arguments_raise():
    with pytest.raises(ValueError):
        nose_hoover_chains([[1.0]], [[0.0]], [1.0], harmonic(1.0), 0.05, 1, 1.0, [1.0, 0.0], 1)
