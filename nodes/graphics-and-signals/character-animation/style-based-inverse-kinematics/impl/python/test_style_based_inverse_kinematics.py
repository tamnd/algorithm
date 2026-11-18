# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/style-based-inverse-kinematics/. The authors are listed in prov/1FCH43.jsonl.
"""Tests of style-based inverse kinematics.

The analytic gradient is compared with central differences. The Gaussian
process reproduces the training poses with a small variance. The objective
decreases at every step. Without a constraint, the result is the mean pose
f(x) at the latent point that minimizes (D / 2) ln s2(x) + |x|^2 / 2, which
is checked against a grid search. With a constraint, a larger weight brings
the end effector closer, and a target reached by a training pose gives that
pose back, although other poses of the redundant chain reach it too. The
check values of the page hold.
"""

import math
import random

from anim import num_grad
from style_based_inverse_kinematics import SGPLVM, end_effector, objective, style_ik

S = [-1.0 + 0.25 * i for i in range(9)]
POSES = [(0.2 + 0.8 * s, 0.5 - 0.3 * s + 0.2 * s * s, 0.9 * s) for s in S]
MODEL = SGPLVM([[s] for s in S], POSES, alpha=1.0, gamma=2.0, beta=1e3)


def test_gradient_against_central_differences():
    rng = random.Random(7)
    target = (1.2, 1.5)
    for _ in range(10):
        x = [rng.uniform(-1.2, 1.2)]
        z = x + [a + rng.uniform(-0.1, 0.1) for a in MODEL.predict(x)[0]]
        for lam in (0.0, 50.0):
            _, g = objective(MODEL, z, target, lam)
            ng = num_grad(lambda q: objective(MODEL, q, target, lam)[0], z, h=1e-5)
            scale = 1.0 + max(abs(v) for v in g)
            assert max(abs(a - b) for a, b in zip(g, ng)) < 1e-5 * scale


def test_gaussian_process_reproduces_the_training_poses():
    for s, y in zip(S, POSES):
        f, s2, _, _ = MODEL.predict([s])
        assert max(abs(a - b) for a, b in zip(f, y)) < 0.01
        assert s2 < 0.003
    _, far, _, _ = MODEL.predict([6.0])
    assert abs(far - (1.0 + 1e-3)) < 1e-9


def test_objective_decreases_and_gradient_vanishes():
    target = (1.4, 1.7)
    _, _, hist = style_ik(MODEL, target, [0.0])
    assert all(hist[i + 1] <= hist[i] for i in range(len(hist) - 1))
    x, y, _ = style_ik(MODEL, target, [0.0])
    e, g = objective(MODEL, x + y, target, 1e3)
    assert math.sqrt(sum(v * v for v in g)) < 1e-3
    assert len(hist) < 100


def test_without_constraints_against_a_grid():
    latents = [[-1.0], [-0.7], [-0.5], [-0.2], [0.1], [0.5], [0.6], [1.0]]
    poses = [POSES[i] for i in (0, 1, 2, 3, 4, 6, 7, 8)]
    model = SGPLVM(latents, poses, alpha=1.0, gamma=2.0, beta=1e3)

    def reduced(x):
        return 1.5 * math.log(model.predict([x])[1]) + 0.5 * x * x

    best = min((reduced(-1.5 + 1e-3 * i), -1.5 + 1e-3 * i) for i in range(3001))
    x, y, _ = style_ik(model, None, [best[1] + 0.05], lam=0.0)
    f = model.predict(x)[0]
    assert max(abs(a - b) for a, b in zip(y, f)) < 1e-7
    assert reduced(x[0]) <= best[0] + 1e-9
    assert abs(x[0] - best[1]) < 2e-3


def test_larger_weight_brings_the_end_effector_closer():
    target = (1.45, 1.6)
    errs = []
    for lam in (10.0, 1e3, 1e5):
        _, y, _ = style_ik(MODEL, target, [0.0], lam=lam)
        p = end_effector(y)[0]
        errs.append(math.hypot(p[0] - target[0], p[1] - target[1]))
    assert errs[0] > errs[1] > errs[2]
    assert errs[2] < 1e-3


def test_target_of_a_training_pose_gives_that_pose():
    target = end_effector(POSES[6])[0]
    # the start is the latent point of the neighbor POSES[5]; the objective has other local minima
    _, y, _ = style_ik(MODEL, target, [S[5]], lam=1e5)
    assert max(abs(a - b) for a, b in zip(y, POSES[6])) < 0.01
    # plain inverse kinematics (minimum norm Newton steps from the pose POSES[0]) reaches the same target with another pose
    q = list(POSES[0])
    for _ in range(50):
        p, jac = end_effector(q)
        r = (p[0] - target[0], p[1] - target[1])
        a = [[sum(jac[i][k] * jac[j][k] for k in range(3)) for j in range(2)] for i in range(2)]
        det = a[0][0] * a[1][1] - a[0][1] * a[1][0]
        mu = ((a[1][1] * r[0] - a[0][1] * r[1]) / det, (a[0][0] * r[1] - a[1][0] * r[0]) / det)
        q = [q[k] - jac[0][k] * mu[0] - jac[1][k] * mu[1] for k in range(3)]
    p = end_effector(q)[0]
    assert math.hypot(p[0] - target[0], p[1] - target[1]) < 1e-10
    assert max(abs(a - b) for a, b in zip(q, POSES[6])) > 0.1


def test_check_values_of_the_page():
    model = SGPLVM([[-1.0], [1.0]], [(0.0, 0.0, 0.0), (1.0, 2.0, 3.0)], alpha=1.0, gamma=1.0, beta=100.0)
    f, s2, _, _ = model.predict([0.0])
    assert max(abs(a - b) for a, b in zip(f, (0.5, 1.0, 1.5))) < 1e-12
    want = 1.01 - 2.0 * math.exp(-1.0) / (1.01 + math.exp(-2.0))
    assert abs(s2 - want) < 1e-12
    assert abs(s2 - 0.3676) < 1e-4
