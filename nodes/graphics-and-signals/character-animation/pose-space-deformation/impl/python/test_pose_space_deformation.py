# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pose-space-deformation/. The authors are listed in prov/1BB6ZV.jsonl.
"""Tests of pose space deformation.

They check that every example pose gives its sculpted shape, that sculpts
equal to plain skinning give plain skinning at every pose, that the
corrections fade far from all examples, that the Gaussian matrix is
symmetric positive definite, that a correction moves with its bone, and the
check value of the page.
"""

import math
import random

from pose_space_deformation import deform, gaussian, skin, train

JOINTS = [(0.0, 0.0), (1.0, 0.0)]
SIGMA = 0.5


def strip():
    rest, weights = [], []
    for k in range(9):
        x = 0.25 * k
        t = min(1.0, max(0.0, (x - 0.75) / 0.5))
        w1 = t * t * (3 - 2 * t)
        for y in (-0.2, 0.2):
            rest.append((x, y))
            weights.append([(0, 1.0 - w1), (1, w1)])
    return rest, weights


def sculpt(rest, weights, pose):
    base = skin(rest, weights, pose, JOINTS)
    out = []
    for v, b in zip(rest, base):
        g = max(0.0, 1.0 - abs(v[0] - 1.0) / 0.5)
        amount = 0.1 * math.sin(abs(pose[1])) * g
        out.append((b[0], b[1] + math.copysign(amount, v[1])))
    return out


POSES = [(0.0, 0.0), (0.0, math.pi / 2), (0.0, -math.pi / 2), (math.pi / 4, math.pi / 3)]


def trained():
    rest, weights = strip()
    shapes = [sculpt(rest, weights, p) for p in POSES]
    coeffs = train(rest, weights, JOINTS, POSES, shapes, SIGMA)
    return rest, weights, shapes, coeffs


def close(a, b, tol):
    return all(abs(x - y) <= tol for p, q in zip(a, b) for x, y in zip(p, q))


def test_examples_are_reproduced():
    rest, weights, shapes, coeffs = trained()
    for p, s in zip(POSES, shapes):
        assert close(deform(rest, weights, JOINTS, POSES, coeffs, SIGMA, p), s, 1e-9)


def test_plain_skinning_sculpts_give_plain_skinning():
    rest, weights = strip()
    shapes = [skin(rest, weights, p, JOINTS) for p in POSES]
    coeffs = train(rest, weights, JOINTS, POSES, shapes, SIGMA)
    rng = random.Random(1)
    for _ in range(10):
        p = (rng.uniform(-1, 1), rng.uniform(-2, 2))
        got = deform(rest, weights, JOINTS, POSES, coeffs, SIGMA, p)
        assert close(got, skin(rest, weights, p, JOINTS), 1e-9)


def test_rest_pose_is_the_rest_mesh():
    rest, weights, _, coeffs = trained()
    assert close(deform(rest, weights, JOINTS, POSES, coeffs, SIGMA, (0.0, 0.0)), rest, 1e-9)


def test_corrections_fade_far_from_examples():
    rest, weights, _, coeffs = trained()
    p = (0.0, 6.0)
    got = deform(rest, weights, JOINTS, POSES, coeffs, SIGMA, p)
    assert close(got, skin(rest, weights, p, JOINTS), 1e-6)


def test_gaussian_matrix_is_positive_definite():
    rng = random.Random(2)
    pts = [(rng.uniform(-2, 2), rng.uniform(-2, 2)) for _ in range(8)]
    phi = [[gaussian(math.dist(p, q), SIGMA) for q in pts] for p in pts]
    for i in range(8):
        for j in range(8):
            assert phi[i][j] == phi[j][i]
    for _ in range(50):
        x = [rng.gauss(0, 1) for _ in range(8)]
        assert sum(x[i] * phi[i][j] * x[j] for i in range(8) for j in range(8)) > 0.0


def test_correction_turns_with_the_bone():
    # One example, evaluated at its own pose with the root turned: the RBF
    # value is 1 in both cases, and the corrected shape turns as a whole.
    rest, weights, _, coeffs = trained()
    turn = 0.7
    c, s = math.cos(turn), math.sin(turn)
    plain = deform(rest, weights, JOINTS, [(0.0, math.pi / 2)], [coeffs[1]], SIGMA, (0.0, math.pi / 2))
    turned = deform(rest, weights, JOINTS, [(turn, math.pi / 2)], [coeffs[1]], SIGMA, (turn, math.pi / 2))
    assert close(turned, [(c * x - s * y, s * x + c * y) for x, y in plain], 1e-12)


def test_check_value_one_joint():
    phi12 = gaussian(math.pi / 2, SIGMA)
    c1 = -0.1 * phi12 / (1 - phi12 * phi12)
    c2 = 0.1 / (1 - phi12 * phi12)
    r = gaussian(math.pi / 4, SIGMA)
    assert abs(r * (c1 + c2) - 0.1 * r / (1 + phi12)) < 1e-15
    assert abs(phi12 - 0.0071918833) < 1e-9
    assert abs(r * (c1 + c2) - 0.0289135) < 1e-6
