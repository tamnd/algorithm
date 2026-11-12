# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/backpropagation/. The authors are listed in prov/7N4K94.jsonl.

import copy
import math
import random

from backpropagation import backprop, batch_gradient, init, loss, train


def numeric(W, b, acts, x, y, h=1e-6):
    """Central differences for every weight and bias (the oracle)."""
    gW = [[[0.0] * len(r) for r in Wl] for Wl in W]
    gb = [[0.0] * len(bl) for bl in b]
    for l in range(len(W)):
        for i in range(len(W[l])):
            for j in range(len(W[l][i])):
                Wp, Wm = copy.deepcopy(W), copy.deepcopy(W)
                Wp[l][i][j] += h
                Wm[l][i][j] -= h
                gW[l][i][j] = (loss(Wp, b, acts, x, y) - loss(Wm, b, acts, x, y)) / (2 * h)
            bp, bm = copy.deepcopy(b), copy.deepcopy(b)
            bp[l][i] += h
            bm[l][i] -= h
            gb[l][i] = (loss(W, bp, acts, x, y) - loss(W, bm, acts, x, y)) / (2 * h)
    return gW, gb


def flat(gW, gb):
    out = []
    for Wl, bl in zip(gW, gb):
        for r in Wl:
            out.extend(r)
        out.extend(bl)
    return out


def rel_err(a, b):
    return max(abs(p - q) / max(abs(p), abs(q), 1e-8) for p, q in zip(a, b))


def test_worked_example():
    W = [[[0.5, -1.0], [1.0, 0.5]], [[1.0, -2.0]]]
    b = [[0.0, 0.5], [0.5]]
    acts = ["relu", "identity"]
    assert loss(W, b, acts, [1.0, 2.0], [1.0]) == 15.125
    gW, gb = backprop(W, b, acts, [1.0, 2.0], [1.0])
    assert gW == [[[0.0, 0.0], [11.0, 22.0]], [[0.0, -13.75]]]
    assert gb == [[0.0, 11.0], [-5.5]]


def test_against_central_differences():
    rng = random.Random(7)
    for trial in range(40):
        sizes = [rng.randint(1, 4) for _ in range(rng.randint(2, 4))]
        acts = [rng.choice(["tanh", "sigmoid", "identity"]) for _ in sizes[1:]]
        W, b = init(sizes, rng, 1.5)
        for l in range(len(b)):
            b[l] = [rng.uniform(-0.5, 0.5) for _ in b[l]]
        x = [rng.uniform(-1, 1) for _ in range(sizes[0])]
        y = [rng.uniform(-1, 1) for _ in range(sizes[-1])]
        a = flat(*backprop(W, b, acts, x, y))
        n = flat(*numeric(W, b, acts, x, y))
        assert all(abs(p - q) <= 1e-7 + 1e-6 * abs(q) for p, q in zip(a, n)), trial


def test_relu_away_from_kinks():
    rng = random.Random(8)
    checked = 0
    while checked < 30:
        W, b = init([3, 4, 2], rng, 1.5)
        x = [rng.uniform(-1, 1) for _ in range(3)]
        z = [sum(w * v for w, v in zip(r, x)) for r in W[0]]
        if min(abs(t) for t in z) < 1e-3:
            continue  # a central difference across a kink is not a valid oracle
        y = [0.3, -0.2]
        a = flat(*backprop(W, b, ["relu", "identity"], x, y))
        n = flat(*numeric(W, b, ["relu", "identity"], x, y))
        assert all(abs(p - q) <= 1e-7 + 1e-6 * abs(q) for p, q in zip(a, n))
        checked += 1


def test_one_layer_is_linear_regression_gradient():
    # for a single identity layer the gradient is (Wx + b - y) x^T
    W = [[[2.0, -1.0, 0.5]]]
    b = [[0.25]]
    x = [1.0, 3.0, -2.0]
    gW, gb = backprop(W, b, ["identity"], x, [4.0])
    r = 2.0 - 3.0 - 1.0 + 0.25 - 4.0
    assert gW == [[[r * v for v in x]]] and gb == [[r]]


def test_batch_gradient_is_mean():
    rng = random.Random(9)
    W, b = init([2, 3, 1], rng)
    X = [[rng.uniform(-1, 1) for _ in range(2)] for _ in range(5)]
    Y = [[rng.uniform(-1, 1)] for _ in range(5)]
    sW, sb = batch_gradient(W, b, ["tanh", "identity"], X, Y)
    parts = [flat(*backprop(W, b, ["tanh", "identity"], x, y)) for x, y in zip(X, Y)]
    mean = [sum(col) / 5 for col in zip(*parts)]
    assert rel_err(flat(sW, sb), mean) < 1e-12


def test_xor_reaches_small_loss():
    X = [[0.0, 0.0], [0.0, 1.0], [1.0, 0.0], [1.0, 1.0]]
    Y = [[0.0], [1.0], [1.0], [0.0]]
    W, b = init([2, 4, 1], random.Random(0), 2.0)
    start = sum(loss(W, b, ["tanh", "identity"], x, y) for x, y in zip(X, Y)) / 4
    final = train(W, b, ["tanh", "identity"], X, Y, 0.2, 1000)
    assert start > 0.1
    assert final < 1e-10
    for x, y in zip(X, Y):
        assert math.isclose(loss(W, b, ["tanh", "identity"], x, y), 0.0, abs_tol=1e-9)
