# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/layer-normalization/. The authors are listed in prov/0KRVGN.jsonl.

import math
import random

from layer_normalization import layer_norm_batch, ln_backward, ln_forward, rms_backward, rms_forward

RNG = random.Random(0)
H = 6
X = [RNG.gauss(1.0, 3.0) for _ in range(H)]
GAMMA = [RNG.uniform(0.5, 2.0) for _ in range(H)]
BETA = [RNG.uniform(-1.0, 1.0) for _ in range(H)]


def close(a, b, tol=1e-9):
    return all(abs(u - v) < tol for u, v in zip(a, b))


def test_output_has_mean_zero_and_variance_about_one() -> None:
    y, (xhat, _) = ln_forward(X, [1.0] * H, [0.0] * H)
    assert abs(sum(xhat) / H) < 1e-12
    mu = sum(X) / H
    var = sum((v - mu) ** 2 for v in X) / H
    assert math.isclose(sum(v * v for v in xhat) / H, var / (var + 1e-5), rel_tol=1e-12)
    assert y == xhat


def test_invariant_to_scaling_and_shifting_the_input() -> None:
    y0, _ = ln_forward(X, GAMMA, BETA, 0.0)
    for a, b in [(2.0, 0.0), (0.01, 5.0), (1000.0, -3.0), (1.0, 7.5)]:
        y1, _ = ln_forward([a * v + b for v in X], GAMMA, BETA, 0.0)
        assert close(y0, y1)
    yneg, _ = ln_forward([-v for v in X], [1.0] * H, [0.0] * H, 0.0)
    ypos, _ = ln_forward(X, [1.0] * H, [0.0] * H, 0.0)
    assert close(yneg, [-v for v in ypos])


def test_epsilon_breaks_invariance_only_for_small_inputs() -> None:
    y0, _ = ln_forward(X, GAMMA, BETA, 1e-5)
    y_big, _ = ln_forward([100 * v for v in X], GAMMA, BETA, 1e-5)
    y_tiny, _ = ln_forward([1e-4 * v for v in X], GAMMA, BETA, 1e-5)
    assert close(y0, y_big, 1e-5)
    assert not close(y0, y_tiny, 1e-2)


def test_invariant_to_recentering_and_rescaling_the_weights() -> None:
    rng = random.Random(1)
    d = 4
    w = [[rng.gauss(0.0, 1.0) for _ in range(d)] for _ in range(H)]
    u = [rng.gauss(0.0, 1.0) for _ in range(d)]
    delta = [rng.gauss(0.0, 1.0) for _ in range(d)]
    z = [sum(a * b for a, b in zip(row, u)) for row in w]
    z2 = [sum((3.0 * a + c) * b for a, c, b in zip(row, delta, u)) for row in w]
    assert close(ln_forward(z, GAMMA, BETA, 0.0)[0], ln_forward(z2, GAMMA, BETA, 0.0)[0])


def test_rmsnorm_is_scale_invariant_but_not_shift_invariant() -> None:
    y0, _ = rms_forward(X, GAMMA, 0.0)
    assert close(y0, rms_forward([4.0 * v for v in X], GAMMA, 0.0)[0])
    assert not close(y0, rms_forward([v + 1.0 for v in X], GAMMA, 0.0)[0], 1e-3)


def test_same_function_for_any_batch() -> None:
    other = [[RNG.gauss(0.0, 1.0) for _ in range(H)] for _ in range(3)]
    alone = layer_norm_batch([X], GAMMA, BETA)[0]
    assert layer_norm_batch(other + [X], GAMMA, BETA)[-1] == alone


def numeric_grad(f, x, h=1e-6):
    out = []
    for k in range(len(x)):
        xp, xm = x[:], x[:]
        xp[k] += h
        xm[k] -= h
        out.append((f(xp) - f(xm)) / (2 * h))
    return out


def test_layer_norm_backward_matches_central_differences() -> None:
    c = [RNG.gauss(0.0, 1.0) for _ in range(H)]
    _, cache = ln_forward(X, GAMMA, BETA)
    dx, dgamma, dbeta = ln_backward(c, cache, GAMMA)
    loss_x = lambda x: sum(a * b for a, b in zip(c, ln_forward(x, GAMMA, BETA)[0]))
    loss_g = lambda g: sum(a * b for a, b in zip(c, ln_forward(X, g, BETA)[0]))
    loss_b = lambda b: sum(a * v for a, v in zip(c, ln_forward(X, GAMMA, b)[0]))
    assert close(dx, numeric_grad(loss_x, X), 1e-6)
    assert close(dgamma, numeric_grad(loss_g, GAMMA), 1e-6)
    assert close(dbeta, numeric_grad(loss_b, BETA), 1e-6)


def test_rmsnorm_backward_matches_central_differences() -> None:
    c = [RNG.gauss(0.0, 1.0) for _ in range(H)]
    _, r = rms_forward(X, GAMMA)
    dx, dgamma = rms_backward(c, X, r, GAMMA)
    loss_x = lambda x: sum(a * b for a, b in zip(c, rms_forward(x, GAMMA)[0]))
    loss_g = lambda g: sum(a * b for a, b in zip(c, rms_forward(X, g)[0]))
    assert close(dx, numeric_grad(loss_x, X), 1e-6)
    assert close(dgamma, numeric_grad(loss_g, GAMMA), 1e-6)
