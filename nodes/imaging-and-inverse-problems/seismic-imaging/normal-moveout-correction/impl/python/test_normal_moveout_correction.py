# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/normal-moveout-correction/. The authors are listed in prov/3TP2T7.jsonl.

import math
import random

from normal_moveout_correction import (
    interp_linear,
    nmo_correct,
    nmo_gather,
    nmo_time,
    one_layer_traveltime,
    stretch_factor,
)


def ricker(t, f):
    a = (math.pi * f * t) ** 2
    return (1.0 - 2.0 * a) * math.exp(-a)


def synthetic_gather(t0s, vels, amps, offsets, dt, n, f=25.0):
    """Hyperbolic events t = sqrt(t0^2 + x^2 / v^2) with a Ricker wavelet of peak frequency f."""
    gather = []
    for x in offsets:
        tr = [0.0] * n
        for t0, v, a in zip(t0s, vels, amps):
            tx = nmo_time(t0, x, v)
            for k in range(n):
                tr[k] += a * ricker(k * dt - tx, f)
        gather.append(tr)
    return gather


def argmax(v):
    return max(range(len(v)), key=lambda i: v[i])


def test_check_value():
    assert abs(nmo_time(1.0, 1000.0, 2000.0) - 1.118034) < 1e-6


def test_hyperbola_is_exact_for_one_flat_layer():
    rng = random.Random(1)
    for _ in range(50):
        z = rng.uniform(100.0, 3000.0)
        v = rng.uniform(1500.0, 5000.0)
        x = rng.uniform(0.0, 4000.0)
        t0 = 2.0 * z / v
        assert abs(one_layer_traveltime(z, x, v) - nmo_time(t0, x, v)) < 1e-12


def test_zero_offset_is_the_identity():
    rng = random.Random(2)
    tr = [rng.gauss(0.0, 1.0) for _ in range(100)]
    out, live = nmo_correct(tr, 0.004, 0.0, 2000.0)
    assert out == tr
    assert live == [1] * 100


def test_pythagorean_triple_moves_a_spike_exactly():
    # t0 = 0.3 s and x / v = 0.4 s give t = 0.5 s: sample 125 moves to sample 75.
    dt = 0.004
    tr = [0.0] * 200
    tr[125] = 1.0
    out, _ = nmo_correct(tr, dt, 800.0, 2000.0)
    assert abs(out[75] - 1.0) < 1e-9
    assert all(abs(out[j]) < 1e-9 for j in range(200) if j not in (74, 75, 76))


def test_linear_interpolation():
    tr = [0.0, 2.0, 4.0, 1.0]
    assert interp_linear(tr, 0.5, 0.25) == 1.0
    assert interp_linear(tr, 0.5, 1.5) == 1.0
    assert interp_linear(tr, 0.5, 1.25) == 2.5
    assert interp_linear(tr, 0.5, -0.1) == 0.0
    assert interp_linear(tr, 0.5, 1.6) == 0.0


def test_correct_velocity_flattens_the_event():
    dt, n = 0.004, 300
    offsets = [100.0 * i for i in range(13)]
    gather = synthetic_gather([0.6], [2200.0], [1.0], offsets, dt, n)
    flat = nmo_gather(gather, offsets, dt, 2200.0)
    peaks = [argmax(tr) for tr in flat]
    assert all(p == 150 for p in peaks)
    wrong = nmo_gather(gather, offsets, dt, 1800.0)
    assert argmax(wrong[-1]) < 150 - 5


def test_time_varying_velocity_flattens_two_events():
    dt, n = 0.004, 400
    offsets = [150.0 * i for i in range(11)]
    gather = synthetic_gather([0.5, 1.2], [1800.0, 2600.0], [1.0, -0.8], offsets, dt, n)
    vel = [1800.0 + (2600.0 - 1800.0) * min(1.0, max(0.0, (j * dt - 0.6) / 0.5)) for j in range(n)]
    flat = nmo_gather(gather, offsets, dt, vel)
    for tr in flat:
        assert argmax([abs(v) for v in tr[100:150]]) + 100 == 125
        assert argmax([-v for v in tr[275:325]]) + 275 == 300


def test_stretch_factor_matches_the_mapping():
    t0, x, v, h = 0.4, 1500.0, 2000.0, 1e-6
    t_a = nmo_time(t0, x, v)
    t_b = nmo_time(t0 + h, x, v)
    # An output interval h comes from an input interval t_b - t_a = h t0 / t.
    assert abs((t_b - t_a) / h - t0 / t_a) < 1e-5
    assert abs(stretch_factor(t0, x, v) - t_a / t0) < 1e-15


def test_stretch_mute():
    dt, n = 0.004, 250
    tr = [1.0] * n
    x, v, smax = 1000.0, 2000.0, 0.3
    out, live = nmo_correct(tr, dt, x, v, stretch_max=smax)
    for j in range(n):
        t0 = j * dt
        t = nmo_time(t0, x, v)
        if (t - t0) > smax * t0:
            assert live[j] == 0 and out[j] == 0.0
        else:
            assert live[j] == 1
    assert live[0] == 0
    assert live[-1] == 1


def test_two_layers_hyperbola_is_only_approximate():
    # Exact rays through two flat layers against the hyperbola with the rms velocity.
    h = [400.0, 600.0]
    v = [2000.0, 3000.0]
    dts = [2.0 * hk / vk for hk, vk in zip(h, v)]
    t0 = sum(dts)
    vrms = math.sqrt(sum(d * vk * vk for d, vk in zip(dts, v)) / t0)
    errors = []
    for k in range(1, 40):
        p = k * 0.0003 / 40.0 * 1.0
        c = [math.sqrt(1.0 - (p * vk) ** 2) for vk in v]
        x = sum(d * p * vk * vk / ck for d, vk, ck in zip(dts, v, c))
        t = sum(d / ck for d, ck in zip(dts, c))
        errors.append((x, abs(t - nmo_time(t0, x, vrms))))
    small = [e for x, e in errors if x < 300.0]
    assert small and max(small) < 1e-5
    assert max(e for _, e in errors) > 1e-4
