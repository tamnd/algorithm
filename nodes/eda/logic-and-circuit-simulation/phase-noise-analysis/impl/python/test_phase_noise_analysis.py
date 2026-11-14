# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/phase-noise-analysis/. The authors are listed in prov/Y2MTGG.jsonl.
import math
import random

from phase_noise_analysis import (
    BOLTZMANN,
    Oscillator,
    hopf_oscillator,
    lc_oscillator,
    orbit,
    phase_noise,
    ssb_phase_noise,
    stochastic_heun,
)

LC = (1e-6, 1e-9, 200.0)


def lc_case(noise_scale=1.0):
    l, c, r = LC
    osc = lc_oscillator(l, c, r, 25e-3, 0.1, noise_scale=noise_scale)
    return osc, phase_noise(osc, [0.3, 0.0], 2 * math.pi * math.sqrt(l * c), 400, [1e5, 1e6])


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def test_hopf_diffusion_constant_is_exact():
    mu, omega, sigma = 1.0, 2 * math.pi, 0.1
    osc = hopf_oscillator(mu, omega, sigma)
    res = phase_noise(osc, [1.0, 0.0], 1.0, 200, [1.0])
    assert abs(res["T"] - 2 * math.pi / omega) < 1e-7
    # the only error is the RK4 error of the orbit radius (measured 1.7e-8 relative)
    assert abs(res["c"] / (sigma ** 2 / (mu * omega ** 2)) - 1) < 1e-7
    for v, x in zip(res["v"], res["states"]):
        assert abs(dot(v, osc.F(x)) - 1) < 1e-12


def test_ppv_is_periodic_and_normalized_on_lc():
    osc, res = lc_case()
    v = res["v"]
    assert max(abs(a - b) for a, b in zip(v[0], v[-1])) < 1e-6 * max(abs(a) for a in v[0])
    for vk, x in zip(v, res["states"]):
        assert abs(dot(vk, osc.F(x)) - 1) < 1e-6


def test_ppv_matches_impulse_response_on_lc():
    # A small kick d at x_s(t_k) shifts the phase of the settled orbit by v_k^T d.
    osc, res = lc_case()
    xs, v, T = res["states"], res["v"], res["T"]
    S = len(xs) - 1
    for k in (S // 4, S // 3):
        f = osc.F(xs[k])
        for j, eps in ((0, 1e-6), (1, 1e-9)):
            ends = []
            for s in (eps, -eps):
                x = list(xs[k])
                x[j] += s
                ends.append(orbit(osc, x, 20 * T, 20 * S)[0][-1])
            d = [(a - b) / (2 * eps) for a, b in zip(*ends)]
            shift = dot(d, f) / dot(f, f)
            assert abs(shift - v[k][j]) < 1e-3 * abs(v[k][j])


def test_lc_diffusion_matches_sinusoidal_estimate():
    l, c, r = LC
    osc, res = lc_case()
    xs = res["states"]
    S = len(xs) - 1
    re = sum(xs[k][0] * math.cos(2 * math.pi * k / S) for k in range(S)) * 2 / S
    im = sum(xs[k][0] * math.sin(2 * math.pi * k / S) for k in range(S)) * 2 / S
    w0 = 2 * math.pi / res["T"]
    estimate = BOLTZMANN * 300 / (r * c * c * (re * re + im * im) * w0 * w0)
    assert abs(res["c"] / estimate - 1) < 0.02
    assert abs(res["L"][1] - res["L"][0] + 20) < 1e-3


def test_lorentzian_has_unit_power():
    c, f0 = 2e-4, 1.0
    total, n = 0.0, 200000
    for i in range(n):
        # f = a tan(u) maps (-pi/2, pi/2) onto the real line
        u = -math.pi / 2 + (i + 0.5) * math.pi / n
        a = math.pi * f0 * f0 * c
        f = a * math.tan(u)
        total += 10 ** (ssb_phase_noise(c, f0, f) / 10) * a / math.cos(u) ** 2 * math.pi / n
    assert abs(total - 1) < 1e-9


def phase_spread(values):
    m = sum(values) / len(values)
    return sum((a - m) ** 2 for a in values) / (len(values) - 1)


def test_hopf_monte_carlo_phase_variance():
    osc = hopf_oscillator(1.0, 2 * math.pi, 0.1)
    c = phase_noise(osc, [1.0, 0.0], 1.0, 200, [1.0])["c"]
    rng = random.Random(71)
    h, steps, paths = 0.02, 500, 600
    shifts = []
    for _ in range(paths):
        turn, prev = 0.0, 0.0
        for x in stochastic_heun(osc, [1.0, 0.0], h, steps, rng)[1:]:
            a = math.atan2(x[1], x[0])
            turn += (a - prev + math.pi) % (2 * math.pi) - math.pi
            prev = a
        shifts.append((turn - 2 * math.pi * steps * h) / (2 * math.pi))
    ratio = phase_spread(shifts) / (c * steps * h)
    assert abs(ratio - 1) < 0.25  # 600 paths: standard error about 0.06


def up_crossings(path, h):
    out = []
    for k in range(len(path) - 1):
        a, b = path[k][0], path[k + 1][0]
        if a < 0 <= b:
            out.append((k + a / (a - b)) * h)
    return out


def test_lc_monte_carlo_timing_jitter():
    osc, res = lc_case(noise_scale=1.3e4)
    T, c, x0 = res["T"], res["c"], res["x0"]
    S, periods, paths = 50, 40, 400
    h = T / S
    quiet = Oscillator(2, osc.F, osc.A, [[0.0], [0.0]])
    nominal = up_crossings(stochastic_heun(quiet, x0, h, S * periods, random.Random(0)), h)
    rng = random.Random(5)
    shifts = []
    for _ in range(paths):
        noisy = up_crossings(stochastic_heun(osc, x0, h, S * periods, rng), h)
        assert len(noisy) == len(nominal)
        shifts.append(nominal[-1] - noisy[-1])
    ratio = phase_spread(shifts) / (c * nominal[-1])
    assert abs(ratio - 1) < 0.3  # 400 paths: standard error about 0.07
