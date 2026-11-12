# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/amsgrad/. The authors are listed in prov/VZ3Q5P.jsonl.

import math
import random

from amsgrad import adam, amsgrad, clip_box, counterexample_grad, regret

C = 3
B2 = 1 / (1 + C * C)
BOX = clip_box(-1.0, 1.0)


def test_first_step_by_hand() -> None:
    # v_1 = (1 - beta2) * 9 = 8.1, step 0.5 * 3 / sqrt(8.1).
    s = amsgrad(counterexample_grad(C), [0.0], 1, alpha=0.5, beta2=B2, project=BOX)
    assert math.isclose(s[1][0], -0.5 * 3 / math.sqrt(8.1), rel_tol=1e-12)


def test_counterexample_adam_goes_to_the_wrong_end() -> None:
    for x0 in (-1.0, 0.0, 1.0):
        a = adam(counterexample_grad(C), [x0], 3000, alpha=0.5, beta2=B2, project=BOX)
        assert a[-1][0] == 1.0
        assert a[-3][0] > 0.95
        # Average regret near 2 (C - 2) / 3 = 2/3.
        assert abs(regret(C, a) / 3000 - 2 / 3) < 0.02


def test_counterexample_amsgrad_goes_to_the_optimum() -> None:
    for x0 in (-1.0, 0.0, 1.0):
        s = amsgrad(counterexample_grad(C), [x0], 3000, alpha=0.5, beta2=B2, project=BOX)
        assert all(x[0] < -0.98 for x in s[-30:])
    r = [regret(C, amsgrad(counterexample_grad(C), [0.0], T, alpha=0.5, beta2=B2, project=BOX)) / T
         for T in (300, 3000, 30000)]
    assert r[0] > r[1] > r[2] and r[2] < 0.01


def test_v_hat_is_monotone_and_effective_step_nonincreasing() -> None:
    rng = random.Random(5)
    gs = [[rng.gauss(0, 1) * (10 if rng.random() < 0.1 else 1)] for _ in range(200)]

    def grad(x, t):
        return gs[t - 1]

    # With beta1 = 0 the step is alpha_t g_t / sqrt(v_hat_t), so the
    # effective step |x_{t+1} - x_t| / |g_t| must never grow.
    path = amsgrad(grad, [0.0], 200, alpha=0.1, beta2=0.5)
    eff = [abs(path[t][0] - path[t - 1][0]) / abs(gs[t - 1][0]) for t in range(1, 201)]
    assert all(b <= a * (1 + 1e-9) for a, b in zip(eff, eff[1:]))
    # Adam on the same gradients does let the effective step grow.
    path = adam(grad, [0.0], 200, alpha=0.1, beta2=0.5)
    eff = [abs(path[t][0] - path[t - 1][0]) / abs(gs[t - 1][0]) for t in range(1, 201)]
    assert any(b > a * 1.01 for a, b in zip(eff, eff[1:]))


def test_amsgrad_equals_adam_when_v_never_falls() -> None:
    # With increasing gradient sizes v_t is increasing, so max(v_hat, v) = v.
    grad = lambda x, t: [float(t)]
    a = adam(grad, [0.0], 50, alpha=0.1, beta1=0.9, beta2=0.99)
    s = amsgrad(grad, [0.0], 50, alpha=0.1, beta1=0.9, beta2=0.99)
    assert a == s


def test_converges_on_a_quadratic() -> None:
    # f(x) = (x0 - 1)^2 + 10 (x1 + 2)^2 with exact gradients.
    grad = lambda x, t: [2 * (x[0] - 1), 20 * (x[1] + 2)]
    x = amsgrad(grad, [0.0, 0.0], 4000, alpha=0.5, beta1=0.9, beta2=0.999, eps=1e-8)[-1]
    assert abs(x[0] - 1) < 1e-2 and abs(x[1] + 2) < 1e-2
