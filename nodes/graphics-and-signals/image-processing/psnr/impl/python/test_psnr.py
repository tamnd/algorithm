# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/psnr/. The authors are listed in prov/T7XT8F.jsonl.

import math
import random
from fractions import Fraction

import pytest

from psnr import mse, psnr, psnr_sequence


def direct(x, y, peak):
    """The formula written out over a flat list of pixels."""
    fx = [v for row in x for v in row]
    fy = [v for row in y for v in row]
    e = Fraction(sum((a - b) * (a - b) for a, b in zip(fx, fy)), len(fx))
    return e, (math.inf if e == 0 else 10 * math.log10(Fraction(peak * peak) / e))


def test_known_values() -> None:
    x = [[10, 20], [30, 40]]
    y = [[11, 21], [31, 41]]
    assert mse(x, y) == 1
    assert math.isclose(psnr(x, y), 20 * math.log10(255))
    assert round(psnr(x, y), 4) == 48.1308
    assert psnr(x, x) == math.inf
    # an error of 10 at every pixel gives MSE 100
    z = [[v + 10 for v in row] for row in x]
    assert round(psnr(x, z), 2) == 28.13
    # the peak convention changes the number: 10-bit peak 1023
    assert math.isclose(psnr(x, y, 1023) - psnr(x, y, 255), 20 * math.log10(1023 / 255))


def test_random_against_direct() -> None:
    rng = random.Random(555)
    for _ in range(600):
        peak = rng.choice([1, 15, 255, 1023])
        w, h = rng.randint(1, 6), rng.randint(1, 6)
        x = [[rng.randint(0, peak) for _ in range(w)] for _ in range(h)]
        y = [[rng.randint(0, peak) for _ in range(w)] for _ in range(h)]
        e, p = direct(x, y, peak)
        assert mse(x, y) == e
        assert mse(x, y) == mse(y, x)
        got = psnr(x, y, peak)
        assert got == p or math.isclose(got, p, rel_tol=1e-12)


def test_sequence_mean_order() -> None:
    rng = random.Random(8)
    for _ in range(500):
        frames = rng.randint(1, 4)
        xs, ys = [], []
        for _ in range(frames):
            x = [[rng.randint(0, 255) for _ in range(3)] for _ in range(2)]
            y = [[min(255, max(0, v + rng.randint(-9, 9))) for v in row] for row in x]
            if x == y:
                y[0][0] = (x[0][0] + 1) % 256
            xs.append(x)
            ys.append(y)
        mean_of_psnr, psnr_of_mean = psnr_sequence(xs, ys)
        assert mean_of_psnr >= psnr_of_mean - 1e-9


def test_float_images_and_errors() -> None:
    x = [[0.0, 0.5], [1.0, 0.25]]
    y = [[0.1, 0.5], [0.9, 0.25]]
    assert math.isclose(mse(x, y), 0.005)
    assert math.isclose(psnr(x, y, 1.0), 10 * math.log10(1 / 0.005))
    with pytest.raises(ValueError):
        mse([[1, 2]], [[1]])
    with pytest.raises(ValueError):
        mse([], [])
