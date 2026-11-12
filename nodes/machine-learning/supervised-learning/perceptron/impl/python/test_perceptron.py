# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/perceptron/. The authors are listed in prov/83YNZY.jsonl.

import math
import random

from perceptron import averaged_perceptron, dot, kernel_perceptron, kernel_predict, perceptron

EXAMPLE_X = [(2, 1), (0, 2), (-1, 0), (1, -2), (-2, 1), (3, 3)]
EXAMPLE_Y = [1, 1, -1, -1, -1, 1]


def separable(rng: random.Random, n: int, d: int, gamma: float, offset: float):
    """Points in [-1, 1]^d labelled by a random unit u and an offset, kept at margin >= gamma."""
    u = [rng.gauss(0, 1) for _ in range(d)]
    norm = math.sqrt(dot(u, u))
    u = [v / norm for v in u]
    xs, ys = [], []
    while len(xs) < n:
        x = [rng.uniform(-1, 1) for _ in range(d)]
        s = dot(u, x) + offset
        if abs(s) >= gamma:
            xs.append(x)
            ys.append(1 if s > 0 else -1)
    return u, xs, ys


def test_worked_example() -> None:
    w, b, m, ok = perceptron(EXAMPLE_X, EXAMPLE_Y)
    assert ok and w == [3, 2] and b == -1 and m == 3
    assert all(y * (dot(w, x) + b) > 0 for x, y in zip(EXAMPLE_X, EXAMPLE_Y))


def test_mistake_bound_through_origin() -> None:
    rng = random.Random(7)
    for _ in range(20):
        u, xs, ys = separable(rng, 200, 5, 0.1, 0.0)
        r = max(math.sqrt(dot(x, x)) for x in xs)
        g = min(y * dot(u, x) for x, y in zip(xs, ys))
        w, b, m, ok = perceptron(xs, ys, bias=False, rng=rng)
        assert ok and b == 0.0
        assert m <= (r / g) ** 2
        assert all(y * dot(w, x) > 0 for x, y in zip(xs, ys))


def test_mistake_bound_with_bias() -> None:
    rng = random.Random(11)
    for _ in range(20):
        off = rng.uniform(-0.5, 0.5)
        u, xs, ys = separable(rng, 150, 3, 0.1, off)
        r2 = max(dot(x, x) for x in xs) + 1.0  # the constant feature 1
        g = min(y * (dot(u, x) + off) for x, y in zip(xs, ys)) / math.sqrt(1 + off * off)
        w, b, m, ok = perceptron(xs, ys, rng=rng)
        assert ok and m <= r2 / g**2
        assert all(y * (dot(w, x) + b) > 0 for x, y in zip(xs, ys))


def test_xor_never_converges_and_weights_stay_small() -> None:
    xs = [(0, 0), (1, 1), (1, 0), (0, 1)]
    ys = [-1, -1, 1, 1]
    w, b, m, ok = perceptron(xs, ys, max_epochs=500)
    assert not ok and m >= 500
    assert abs(w[0]) + abs(w[1]) + abs(b) <= 10


def test_kernel_perceptron_with_linear_kernel_equals_primal() -> None:
    rng = random.Random(3)
    _, xs, ys = separable(rng, 60, 4, 0.05, 0.2)
    w, b, m, _ = perceptron(xs, ys)
    a, ok = kernel_perceptron(xs, ys, dot)
    assert ok and sum(a) == m
    w2 = [sum(a[j] * ys[j] * xs[j][k] for j in range(len(xs))) for k in range(4)]
    assert all(abs(p - q) < 1e-9 for p, q in zip(w, w2))
    assert abs(b - sum(a[j] * ys[j] for j in range(len(xs)))) < 1e-9


def test_kernel_perceptron_learns_xor() -> None:
    xs = [(0, 0), (1, 1), (1, 0), (0, 1)]
    ys = [-1, -1, 1, 1]

    def k(p, q):
        return (dot(p, q) + 1) ** 2

    a, ok = kernel_perceptron(xs, ys, k)
    assert ok
    assert [kernel_predict(xs, ys, a, k, x) for x in xs] == ys


def test_averaged_perceptron_is_the_mean_of_the_iterates() -> None:
    xs, ys = EXAMPLE_X, EXAMPLE_Y
    w, b = [0.0, 0.0], 0.0
    hist = []
    for _ in range(2):
        for x, y in zip(xs, ys):
            if y * (dot(w, x) + b) <= 0:
                w = [w[0] + y * x[0], w[1] + y * x[1]]
                b += y
            hist.append((w, b))
    aw, ab = averaged_perceptron(xs, ys, 2)
    assert abs(aw[0] - sum(h[0][0] for h in hist) / 12) < 1e-12
    assert abs(aw[1] - sum(h[0][1] for h in hist) / 12) < 1e-12
    assert abs(ab - sum(h[1] for h in hist) / 12) < 1e-12


def test_empty_and_one_point() -> None:
    assert perceptron([], []) == ([], 0.0, 0, True)
    w, b, m, ok = perceptron([(1.0,)], [-1])
    assert ok and m == 1 and w == [-1.0] and b == -1.0
