# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/active-constellation-extension/. The authors are listed in prov/6XWF0B.jsonl.

import cmath
import math
import random

import constel
from active_constellation_extension import (
    active_constellation_extension,
    clip_noise,
    fft,
    papr,
    project,
    to_bins,
    to_time,
)

QPSK = constel.qam(4)
QAM16 = constel.qam(16)


def direct_time(X, L):
    n = len(X)
    freqs = list(range(n // 2)) + list(range(-(n // 2), 0))
    size = L * n
    return [sum(X[k] * cmath.exp(2j * math.pi * freqs[k] * t / size) for k in range(n)) * math.sqrt(L) / math.sqrt(size) for t in range(size)]


def outer_of(points):
    return max(abs(p.real) for p in points)


def in_region(z, x0, outer):
    for u, u0 in ((z.real, x0.real), (z.imag, x0.imag)):
        if abs(abs(u0) - outer) > 1e-9:
            if abs(u - u0) > 1e-12:
                return False
        elif u * (1 if u0 > 0 else -1) < abs(u0) - 1e-12:
            return False
    return True


def test_transforms():
    rng = random.Random(11)
    X = [complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(16)]
    x = to_time(X, 4)
    assert max(abs(u - v) for u, v in zip(x, direct_time(X, 4))) < 1e-9
    assert max(abs(u - v) for u, v in zip(to_bins(x, 4), X)) < 1e-9
    a = [complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(32)]
    back = [v / 32 for v in fft(fft(a), inverse=True)]
    assert max(abs(u - v) for u, v in zip(a, back)) < 1e-9


def test_clip_noise():
    x = [3 + 4j, 0.5j, -2.0]
    e = clip_noise(x, 2.0)
    assert abs((x[0] + e[0]) - 2 * (3 + 4j) / 5) < 1e-12
    assert e[1] == 0 and e[2] == 0


def test_projection_is_nearest_point_of_region():
    rng = random.Random(4)
    for points in (QPSK, QAM16):
        outer = outer_of(points)
        for x0 in points:
            for _ in range(30):
                z = complex(rng.uniform(-2, 2), rng.uniform(-2, 2))
                p = project(z, x0, outer)
                assert in_region(p, x0, outer)
                assert project(p, x0, outer) == p
                for _ in range(20):
                    w = project(complex(rng.uniform(-2, 2), rng.uniform(-2, 2)), x0, outer)
                    assert abs(z - p) <= abs(z - w) + 1e-12


def test_decisions_kept_and_distances_grow():
    rng = random.Random(5)
    outer = outer_of(QAM16)
    for _ in range(4):
        X = [rng.choice(QAM16) for _ in range(64)]
        x, Y = active_constellation_extension(X, QAM16, 4, math.sqrt(10 ** 0.5), 1.0, 4)
        for x0, y in zip(X, Y):
            assert in_region(y, x0, outer)
            assert QAM16[constel.ml_detect(y, QAM16)] == x0
            for q in QAM16:
                assert abs(y - q) >= abs(x0 - q) - 1e-12


def test_symbol_is_band_limited():
    rng = random.Random(6)
    X = [rng.choice(QPSK) for _ in range(64)]
    x, Y = active_constellation_extension(X, QPSK, 4, math.sqrt(10 ** 0.5), 1.0, 3)
    assert max(abs(u - v) for u, v in zip(to_bins(x, 4), Y)) < 1e-9
    spec = fft(x)
    assert max(abs(spec[k]) for k in range(32, 256 - 32)) < 1e-9
    assert any(abs(u - v) > 1e-6 for u, v in zip(X, Y))


def clipped_energy(x, a):
    return 0.5 * sum((abs(v) - a) ** 2 for v in x if abs(v) > a)


def test_clipped_energy_never_grows():
    rng = random.Random(8)
    a = math.sqrt(10 ** 0.4)
    for points, mu in ((QPSK, 1.0), (QPSK, 2.0), (QAM16, 2.0)):
        X = [rng.choice(points) for _ in range(32)]
        f = [clipped_energy(active_constellation_extension(X, points, 4, a, mu, k)[0], a) for k in range(6)]
        assert f[0] > 0
        assert all(f[k + 1] <= f[k] + 1e-12 for k in range(5))
        assert f[5] < f[0]


def test_no_change_below_threshold():
    rng = random.Random(7)
    X = [rng.choice(QPSK) for _ in range(64)]
    x0 = to_time(X, 4)
    a = max(abs(v) for v in x0) + 0.01
    x, Y = active_constellation_extension(X, QPSK, 4, a, 1.0, 5)
    assert x == x0
    assert Y == X


def test_papr_drops():
    rng = random.Random(2)
    before, after = [], []
    for _ in range(40):
        X = [rng.choice(QPSK) for _ in range(64)]
        x, _ = active_constellation_extension(X, QPSK, 4, math.sqrt(10 ** 0.4), 2.0, 8)
        before.append(papr(to_time(X, 4)))
        after.append(papr(x))
    gain = 10 * math.log10(sum(before) / len(before)) - 10 * math.log10(sum(after) / len(after))
    assert gain > 1.0
