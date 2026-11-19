# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/delta-features/. The authors are listed in prov/AZKQ3W.jsonl.

import random

from delta_features import add_deltas, deltas


def test_ramp_gives_its_slope():
    c = [[2.0 * t + 1.0, -0.5 * t] for t in range(10)]
    d = deltas(c)
    for t in range(2, 8):  # away from the edges
        assert abs(d[t][0] - 2.0) < 1e-12 and abs(d[t][1] + 0.5) < 1e-12
    # at the edges the repeated frames lower the slope: t = 0 gives (1 * 2 + 2 * 4) / 10 = 1.0
    assert abs(d[0][0] - 1.0) < 1e-12
    assert abs(d[1][0] - (1 * 4.0 + 2 * 6.0) / 10.0) < 1e-12


def test_constant_gives_zero():
    d = deltas([[3.0, 4.0]] * 6)
    assert all(v == 0.0 for row in d for v in row)


def test_quadratic_gives_a_constant_acceleration():
    c = [[0.5 * t * t] for t in range(20)]
    full = add_deltas(c)
    for t in range(4, 16):
        assert abs(full[t][1] - t) < 1e-12  # the slope of t^2 / 2 is t
        assert abs(full[t][2] - 1.0) < 1e-12


def test_delta_is_the_least_squares_slope():
    rng = random.Random(6)
    c = [[rng.uniform(-1, 1)] for _ in range(30)]
    for theta in (1, 2, 3):
        d = deltas(c, theta)
        for t in range(theta, 30 - theta):
            xs = list(range(-theta, theta + 1))
            ys = [c[t + n][0] for n in xs]
            mean_y = sum(ys) / len(ys)
            slope = sum(x * (y - mean_y) for x, y in zip(xs, ys)) / sum(x * x for x in xs)
            assert abs(d[t][0] - slope) < 1e-12


def test_thirty_nine_numbers():
    rng = random.Random(1)
    c = [[rng.gauss(0, 1) for _ in range(13)] for _ in range(50)]
    full = add_deltas(c)
    assert len(full) == 50 and all(len(row) == 39 for row in full)
    assert all(row[:13] == list(s) for row, s in zip(full, c))


def test_edges_and_bad_input():
    assert deltas([]) == []
    assert deltas([[5.0]]) == [[0.0]]
    try:
        deltas([[1.0]], 0)
    except ValueError:
        pass
    else:
        raise AssertionError("theta 0 must fail")
