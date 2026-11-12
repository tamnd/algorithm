# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/scalar-quantization/. The authors are listed in prov/E3908F.jsonl.

import math
import random

from scalar_quantization import (
    GAUSSIAN,
    cells,
    deadzone_index,
    deadzone_value,
    decode,
    distortion,
    encode,
    lloyd_max,
    midrise,
    midtread,
    uniform_moments,
    uniform_quantizer,
)


def test_encode_decode_example() -> None:
    t = [-1.0, 0.0, 1.0]
    y = [-1.5, -0.5, 0.5, 1.5]
    assert [encode(x, t) for x in (-3.0, -1.0, -0.2, 0.0, 0.7, 2.0)] == [0, 0, 1, 1, 2, 3]
    assert decode(encode(0.7, t), y) == 0.5


def test_uniform_examples() -> None:
    assert midtread(0.24, 0.5) == 0.0
    assert midtread(0.26, 0.5) == 0.5
    assert midtread(-0.75, 0.5) == -1.0
    assert midrise(0.24, 0.5) == 0.25
    assert midrise(-0.01, 0.5) == -0.25
    # A midtread quantizer has a level at 0, a midrise one does not.
    assert midtread(0.0, 1.0) == 0.0 and midrise(0.0, 1.0) == 0.5


def test_deadzone() -> None:
    step = 2.0
    assert [deadzone_index(x, step) for x in (-4.5, -1.9, 0.0, 1.9, 2.0, 5.9)] == [-2, 0, 0, 0, 1, 2]
    rng = random.Random(3)
    for _ in range(2000):
        x = rng.uniform(-50, 50)
        q = deadzone_index(x, step)
        e = abs(x - deadzone_value(q, step))
        # The zero cell (-step, step) has error below step; the others at most step / 2.
        assert e < step if q == 0 else e <= step / 2 + 1e-12


def test_high_rate_d_is_step_squared_over_12() -> None:
    rng = random.Random(1)
    xs = [rng.gauss(0.0, 1.0) for _ in range(60000)]
    for step in (0.1, 0.25):
        for q in (midtread, midrise):
            d = sum((x - q(x, step)) ** 2 for x in xs) / len(xs)
            assert abs(d / (step * step / 12) - 1) < 0.03
    # For a uniform input on a whole number of cells, the formula is exact.
    t, y = uniform_quantizer(8, 0.25)
    assert abs(distortion(t, y, uniform_moments(-1.0, 1.0)) - 0.25 ** 2 / 12) < 1e-15


def test_six_db_per_bit() -> None:
    # Uniform input on [-1, 1], b bits: SNR = 20 log10(2) b exactly.
    for b in range(1, 9):
        step = 2.0 / 2 ** b
        t, y = uniform_quantizer(2 ** b, step)
        d = distortion(t, y, uniform_moments(-1.0, 1.0))
        snr = 10 * math.log10((1.0 / 3.0) / d)
        assert abs(snr - 20 * math.log10(2) * b) < 1e-9


def test_lloyd_max_two_levels_closed_form() -> None:
    t, y, _ = lloyd_max([-0.1, 0.3], GAUSSIAN)
    assert abs(t[0]) < 1e-9
    assert abs(y[1] - math.sqrt(2 / math.pi)) < 1e-9
    assert abs(distortion(t, y, GAUSSIAN) - (1 - 2 / math.pi)) < 1e-9


def test_lloyd_max_conditions_and_monotone() -> None:
    m0, m1, _ = GAUSSIAN
    for n in (3, 4, 8):
        t, y, hist = lloyd_max([i - (n - 1) / 2 for i in range(n)], GAUSSIAN)
        assert all(a >= b - 1e-15 for a, b in zip(hist, hist[1:]))
        for i in range(n - 1):  # nearest neighbor condition
            assert abs(t[i] - (y[i] + y[i + 1]) / 2) < 1e-12
        for (a, b), v in zip(cells(t), y):  # centroid condition
            assert abs(v - m1(a, b) / m0(a, b)) < 1e-9
        # The optimum beats every uniform quantizer with the same number of levels.
        best_uniform = min(distortion(*uniform_quantizer(n, s / 200), GAUSSIAN) for s in range(20, 600))
        assert hist[-1] <= best_uniform + 1e-12
    # Four levels on the unit Gaussian, as computed by the iteration.
    t, y, hist = lloyd_max([-1.5, -0.5, 0.5, 1.5], GAUSSIAN)
    assert [round(v, 4) for v in y] == [-1.5104, -0.4528, 0.4528, 1.5104]
    assert round(t[2], 4) == 0.9816 and round(hist[-1], 4) == 0.1175


def test_lloyd_max_uniform_density_gives_uniform_quantizer() -> None:
    rng = random.Random(5)
    start = sorted(rng.uniform(-1, 1) for _ in range(4))
    t, y, _ = lloyd_max(start, uniform_moments(-1.0, 1.0))
    assert all(abs(a - b) < 1e-6 for a, b in zip(y, [-0.75, -0.25, 0.25, 0.75]))
