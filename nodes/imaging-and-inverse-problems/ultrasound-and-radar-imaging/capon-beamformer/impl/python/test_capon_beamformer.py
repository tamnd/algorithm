# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/capon-beamformer/. The authors are listed in prov/EAKMFX.jsonl.

import random

from capon_beamformer import (capon_pixel, capon_power, capon_weights, delayed_snapshots, element_positions,
                              outer_sum, output_power, simulate_iq, steering_vector)
from imgla import dot

F0, SIGMA, FS, T0, NS = 5.0, 0.1, 40.0, 7.0, 120
ELEMENTS = element_positions(16, 0.3)
XS = [round(-1.5 + 0.1 * k, 10) for k in range(31)]


def _random_covariance(rng, n, k):
    snaps = [[complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(n)] for _ in range(k)]
    return outer_sum(snaps)


def _interference(m, u_signal, u_int, power_int):
    a1 = steering_vector(m, 0.5, u_int)
    r = [[power_int * a1[i] * a1[j].conjugate() + (1.0 if i == j else 0.0) for j in range(m)] for i in range(m)]
    return r, steering_vector(m, 0.5, u_signal), a1


def test_distortionless_constraint() -> None:
    rng = random.Random(4401)
    for n in (2, 5, 8):
        r = _random_covariance(rng, n, 3 * n)
        a = steering_vector(n, 0.5, rng.uniform(-1, 1))
        w = capon_weights(r, a)
        assert abs(dot(w, a) - 1) < 1e-10


def test_least_power_among_feasible_weights() -> None:
    rng = random.Random(4402)
    n = 6
    r = _random_covariance(rng, n, 20)
    a = steering_vector(n, 0.5, 0.3)
    w = capon_weights(r, a)
    p_min = output_power(r, w)
    assert abs(p_min - capon_power(r, a)) < 1e-10 * p_min
    for _ in range(200):
        v = [complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(n)]
        # move v onto the feasible set w^H a = 1 along a
        c = (1 - dot(v, a)) / dot(a, a)
        u = [vi + c.conjugate() * ai for vi, ai in zip(v, a)]
        assert abs(dot(u, a) - 1) < 1e-10
        assert output_power(r, u) >= p_min * (1 - 1e-12)


def test_white_noise_gives_the_das_weights() -> None:
    m = 7
    r = [[2.5 if i == j else 0.0 for j in range(m)] for i in range(m)]
    a = steering_vector(m, 0.5, 0.2)
    w = capon_weights(r, a)
    assert all(abs(wi - ai / m) < 1e-12 for wi, ai in zip(w, a))
    assert abs(capon_power(r, a) - 2.5 / m) < 1e-12


def test_interferer_response_matches_the_closed_form() -> None:
    # R = I + s a1 a1^H; by the Woodbury identity w^H a1 = (a0^H a1) / ((1 + M s) a0^H R^-1 a0)
    m, s = 8, 100.0
    r, a0, a1 = _interference(m, 0.0, 0.4, s)
    w = capon_weights(r, a0)
    c01 = dot(a0, a1)
    denom = m - s * abs(c01) ** 2 / (1 + m * s)
    assert abs(abs(dot(w, a1)) - abs(c01) / ((1 + m * s) * denom)) < 1e-12
    das_gain = abs(c01) / m
    assert abs(dot(w, a1)) < 0.02 * das_gain


def test_resolves_two_close_sources_that_das_merges() -> None:
    m = 8
    a1 = steering_vector(m, 0.5, 0.1)
    a2 = steering_vector(m, 0.5, -0.1)
    r = [[a1[i] * a1[j].conjugate() + a2[i] * a2[j].conjugate() + (0.01 if i == j else 0.0) for j in range(m)]
         for i in range(m)]
    cap = {u: capon_power(r, steering_vector(m, 0.5, u)) for u in (-0.1, 0.0, 0.1)}
    das = {u: output_power(r, [v / m for v in steering_vector(m, 0.5, u)]) for u in (-0.1, 0.0, 0.1)}
    assert cap[0.0] < 0.05 * cap[0.1] and cap[0.0] < 0.05 * cap[-0.1]
    assert das[0.0] > das[0.1]


def test_aligned_channels_return_the_value() -> None:
    v = 0.7 - 1.1j
    snaps = [[v] * 12 for _ in range(5)]
    for sub_len in (1, 4, 12):
        assert abs(capon_pixel(snaps, sub_len, 0.01) - v) < 1e-10


def test_large_loading_gives_das() -> None:
    rng = random.Random(4403)
    snaps = [[complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(10)] for _ in range(3)]
    centre = snaps[1]
    assert abs(capon_pixel(snaps, 10, 1e9) - sum(centre) / 10) < 1e-6
    # with L = 1 there is nothing to adapt: the result is the plain average
    assert abs(capon_pixel(snaps, 1, 0.01) - sum(centre) / 10) < 1e-10


def _profile(data, combiner):
    prof = [abs(combiner(delayed_snapshots(data, ELEMENTS, px, 6.0, T0, FS, F0, 2))) for px in XS]
    peak = max(prof)
    return [v / peak for v in prof], peak


def _das(snaps):
    return sum(snaps[len(snaps) // 2]) / len(snaps[0])


def _capon(snaps):
    return capon_pixel(snaps, 8, 0.01)


def test_point_target_is_narrower_than_das() -> None:
    data = simulate_iq(ELEMENTS, [(0.0, 6.0, 1.0)], F0, SIGMA, FS, T0, NS)
    p_das, peak_das = _profile(data, _das)
    p_cap, peak_cap = _profile(data, _capon)
    i0 = XS.index(0.0)
    assert p_das.index(1.0) == i0 and p_cap.index(1.0) == i0
    # both outputs keep the unit gain at the target
    assert abs(peak_das - 1) < 0.01 and abs(peak_cap - 1) < 0.01
    assert p_cap[i0 + 1] < 0.1 < 0.8 < p_das[i0 + 1]


def test_two_targets_are_better_separated_than_with_das() -> None:
    data = simulate_iq(ELEMENTS, [(-0.3, 6.0, 1.0), (0.3, 6.0, 1.0)], F0, SIGMA, FS, T0, NS)
    p_das, _ = _profile(data, _das)
    p_cap, _ = _profile(data, _capon)
    i0 = XS.index(0.0)
    assert p_cap[i0] < 0.4 and p_das[i0] > 0.6
