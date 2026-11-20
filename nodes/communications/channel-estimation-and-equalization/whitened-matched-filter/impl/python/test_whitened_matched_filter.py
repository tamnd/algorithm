# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/whitened-matched-filter/. The authors are listed in prov/35K4A5.jsonl.

import itertools
import math
import random

import pytest

from whitened_matched_filter import (
    all_spectral_factors,
    autocorrelation,
    freq,
    min_phase_factor,
    poly_roots,
    whitened_matched_filter,
)


def cn(rng, var):
    s = math.sqrt(var / 2)
    return complex(rng.gauss(0, s), rng.gauss(0, s))


def conv(a, b):
    out = [0j] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for k, y in enumerate(b):
            out[i + k] += x * y
    return out


def random_channel(rng, taps):
    # zeros away from the unit circle, so the whitening filter decays fast
    while True:
        h = [cn(rng, 1.0) for _ in range(taps)]
        if h[0] != 0 and all(abs(abs(r) - 1) > 0.15 for r in poly_roots(h)):
            return h


def test_example_on_the_page() -> None:
    f = min_phase_factor([0.5, 1])
    assert max(abs(a - b) for a, b in zip(f, [1, 0.5])) < 1e-12
    assert autocorrelation([0.5, 1]) == [1.25, 0.5]
    f = min_phase_factor([0.407, 0.815, 0.407])
    assert abs(sum(abs(v) ** 2 for v in f) - (0.407**2 * 2 + 0.815**2)) < 1e-12
    x = [1, -1, -1, 1, 1]
    y = conv([complex(v) for v in x], [0.5, 1])
    _, yw = whitened_matched_filter([0.5, 1], y)
    want = conv([complex(v) for v in x], [1, 0.5])
    assert max(abs(a - b) for a, b in zip(yw, want)) < 1e-12


def test_roots_of_known_polynomials() -> None:
    r = sorted(poly_roots([1, -3, 2]), key=lambda v: v.real)
    assert abs(r[0] - 1) < 1e-12 and abs(r[1] - 2) < 1e-12
    r = poly_roots([1, 0, 1])
    assert sorted(round(v.imag, 12) for v in r) == [-1, 1]


def test_factor_has_the_same_spectrum_and_is_minimum_phase() -> None:
    rng = random.Random(7401)
    for _ in range(40):
        h = random_channel(rng, rng.randint(1, 6))
        f = min_phase_factor(h)
        assert len(f) == len(h) and f[0].real > 0 and abs(f[0].imag) < 1e-12
        for t in range(32):
            w = 2 * math.pi * t / 32
            assert abs(abs(freq(f, w)) ** 2 - abs(freq(h, w)) ** 2) < 1e-9
        assert all(abs(r) <= 1 + 1e-9 for r in poly_roots(f))
        rh, rf = autocorrelation(h), autocorrelation(f)
        assert max(abs(a - b) for a, b in zip(rh, rf)) < 1e-9


def test_minimum_phase_factor_has_the_largest_partial_energies() -> None:
    rng = random.Random(7402)
    for _ in range(20):
        h = random_channel(rng, rng.randint(2, 5))
        f = min_phase_factor(h)
        for g in all_spectral_factors(h):
            for n in range(len(g)):
                assert sum(abs(v) ** 2 for v in f[: n + 1]) >= sum(abs(v) ** 2 for v in g[: n + 1]) - 1e-9


def test_noiseless_output_is_f_convolved_with_x() -> None:
    rng = random.Random(7403)
    for _ in range(20):
        h = random_channel(rng, rng.randint(1, 5))
        x = [complex(rng.choice((-1, 1)), rng.choice((-1, 1))) for _ in range(30)]
        f, yw = whitened_matched_filter(h, conv(x, h))
        want = conv(x, f)
        assert max(abs(a - b) for a, b in zip(yw, want)) < 1e-9


def test_ml_decisions_agree_before_and_after_the_filter() -> None:
    # the two metrics differ by a constant, so the brute force minimizers agree on every vector
    rng = random.Random(7404)
    for _ in range(25):
        h = random_channel(rng, rng.randint(2, 4))
        n = 8
        x = [complex(rng.choice((-1, 1))) for _ in range(n)]
        y = [v + cn(rng, 0.5) for v in conv(x, h)]
        f, yw = whitened_matched_filter(h, y)
        best_y, best_w, diffs = None, None, []
        for cand in itertools.product((-1, 1), repeat=n):
            c = [complex(v) for v in cand]
            my = sum(abs(a - b) ** 2 for a, b in zip(y, conv(c, h)))
            mw = sum(abs(a - b) ** 2 for a, b in zip(yw, conv(c, f)))
            diffs.append(my - mw)
            if best_y is None or my < best_y[0]:
                best_y = (my, cand)
            if best_w is None or mw < best_w[0]:
                best_w = (mw, cand)
        assert best_y[1] == best_w[1]
        assert max(diffs) - min(diffs) < 1e-8


def test_noise_map_is_white_away_from_the_block_end() -> None:
    rng = random.Random(7405)
    h = [0.3 + 0.2j, 1.0, -0.4j]
    n = 40
    cols = []
    for t in range(n):
        e = [0j] * n
        e[t] = 1
        cols.append(whitened_matched_filter(h, e)[1])
    # entry (i, t) of the noise map is cols[t][i]
    for i in range(20):
        for k in range(20):
            g = sum(cols[t][i] * cols[t][k].conjugate() for t in range(n))
            assert abs(g - (1 if i == k else 0)) < 1e-6


def test_input_checks() -> None:
    with pytest.raises(ValueError):
        min_phase_factor([0, 1])
