# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/adafactor/. The authors are listed in prov/39XP8M.jsonl.

import math
import random
from fractions import Fraction as F

from adafactor import (adafactor, adafactor_matrix_step, expand, factor, i_divergence, new_state, rms,
                       state_size)


def test_rank_one_matrix_is_reproduced_exactly() -> None:
    u = [F(1), F(3, 2), F(2, 7)]
    w = [F(5), F(1, 3), F(4), F(9, 8)]
    v = [[a * b for b in w] for a in u]
    r, c = factor(v)
    assert expand(r, c) == v


def test_row_and_column_sums_are_kept() -> None:
    rng = random.Random(2)
    v = [[F(rng.randint(1, 50), rng.randint(1, 9)) for _ in range(5)] for _ in range(4)]
    r, c = factor(v)
    vh = expand(r, c)
    assert factor(vh) == (r, c)


def test_factored_estimate_minimizes_the_i_divergence() -> None:
    rng = random.Random(7)
    v = [[rng.uniform(0.1, 3.0) for _ in range(4)] for _ in range(3)]
    r, c = factor(v)
    best = i_divergence(v, expand(r, c))
    s = sum(r)
    for _ in range(300):
        rr = [a * math.exp(rng.gauss(0, 0.3)) for a in r]
        cc = [b * math.exp(rng.gauss(0, 0.3)) / s for b in c]
        other = [[a * b for b in cc] for a in rr]
        assert i_divergence(v, other) >= best - 1e-12


def test_state_is_n_plus_m() -> None:
    x = [[0.0] * 300 for _ in range(200)]
    assert state_size(new_state(x)) == 500
    assert state_size(new_state([0.0] * 7)) == 7


def test_first_step_on_a_rank_one_gradient_is_a_sign_step() -> None:
    # beta2_hat_1 = 0, so V_hat = G^2 exactly when G = a b^T; then U = sign(G).
    a, b = [1.0, -2.0, 0.5], [3.0, -1.0]
    g = [[ai * bj for bj in b] for ai in a]
    x = [[0.2, -0.4], [0.1, 0.3], [-0.5, 0.6]]
    alpha = max(1e-3, rms(x)) * 1e-2
    new = adafactor_matrix_step(x, g, new_state(x), 1)
    for i in range(3):
        for j in range(2):
            assert math.isclose(new[i][j], x[i][j] - alpha * math.copysign(1, g[i][j]), rel_tol=1e-12)


def test_update_clipping_bounds_the_rms() -> None:
    x = [[1.0, 1.0], [1.0, 1.0]]
    st = new_state(x)
    step = lambda t: 1.0
    x1 = adafactor_matrix_step(x, [[1e-3, 1e-3], [1e-3, 1e-3]], st, 1, step=step)
    # A sudden large gradient: the unclipped update would have RMS far above 1.
    g = [[10.0, 1e-3], [1e-3, 1e-3]]
    alpha = max(1e-3, rms(x1))
    x2 = adafactor_matrix_step(x1, g, st, 2, step=step)
    upd = [[(a - b) / alpha for a, b in zip(r1, r2)] for r1, r2 in zip(x1, x2)]
    assert math.isclose(rms(upd), 1.0, rel_tol=1e-9)


def test_relative_step_uses_eps2_for_zero_parameters() -> None:
    x = [[0.0, 0.0], [0.0, 0.0]]
    g = [[1.0, 1.0], [1.0, 1.0]]
    new = adafactor_matrix_step(x, g, new_state(x), 1)
    assert all(math.isclose(a, -1e-3 * 1e-2, rel_tol=1e-12) for row in new for a in row)


def test_fits_a_linear_map() -> None:
    rng = random.Random(4)
    target = [[rng.uniform(-1, 1) for _ in range(3)] for _ in range(2)]
    data = [[rng.gauss(0, 1) for _ in range(3)] for _ in range(20)]

    def loss_grad(w):
        g = [[0.0] * 3 for _ in range(2)]
        loss = 0.0
        for a in data:
            for i in range(2):
                e = sum(w[i][k] * a[k] for k in range(3)) - sum(target[i][k] * a[k] for k in range(3))
                loss += e * e / len(data)
                for k in range(3):
                    g[i][k] += 2 * e * a[k] / len(data)
        return loss, g

    w0 = [[rng.uniform(-0.5, 0.5) for _ in range(3)] for _ in range(2)]
    w = adafactor(lambda ps, t: [loss_grad(ps[0])[1]], [w0], 400, step=lambda t: 0.05 / math.sqrt(t / 50 + 1))[0]
    assert loss_grad(w)[0] < 1e-2 * loss_grad(w0)[0]
