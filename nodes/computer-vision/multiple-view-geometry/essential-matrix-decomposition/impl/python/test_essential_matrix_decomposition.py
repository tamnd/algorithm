# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/essential-matrix-decomposition/. The authors are listed in prov/CHAEFS.jsonl.
"""Tests of pose recovery from the essential matrix."""

import math
import random

import pytest

from cvla import det, matvec, mul, norm, scale, skew, sub, transpose
from essential_matrix_decomposition import (count_in_front, depths,
                                            pose_candidates, recover_pose)

R_EX = [[0.8, 0.0, 0.6], [0.0, 1.0, 0.0], [-0.6, 0.0, 0.8]]
T_EX = [1.0, 0.0, 0.0]
E_EX = [[0.0, 0.0, 0.0], [0.6, 0.0, -0.8], [0.0, 1.0, 0.0]]


def rotation(axis, angle):
    """Rodrigues formula, written out."""
    a = [c / norm(axis) for c in axis]
    k = skew(a)
    k2 = mul(k, k)
    s, c = math.sin(angle), math.cos(angle)
    return [[(1.0 if i == j else 0.0) + s * k[i][j] + (1.0 - c) * k2[i][j]
             for j in range(3)] for i in range(3)]


def rotation_angle(R1, R2):
    """The angle of R1^T R2. It equals arccos((tr(R1^T R2) - 1) / 2), but
    the form 2 asin(||R1 - R2||_F / (2 sqrt 2)) keeps its accuracy near 0."""
    d = norm(sub(R1, R2)) / (2.0 * math.sqrt(2.0))
    return 2.0 * math.asin(min(1.0, d))


def direction_angle(a, b):
    """The angle between two directions, as 2 asin(||a' - b'|| / 2) for the
    unit vectors a' and b'."""
    d = norm(sub(scale(a, 1.0 / norm(a)), scale(b, 1.0 / norm(b)))) / 2.0
    return 2.0 * math.asin(min(1.0, d))


def scene(rng, n, R, t):
    x1, x2 = [], []
    while len(x1) < n:
        X1 = [rng.uniform(-2.0, 2.0), rng.uniform(-2.0, 2.0), rng.uniform(4.0, 8.0)]
        X2 = [a + b for a, b in zip(matvec(R, X1), t)]
        if X2[2] > 0.5:
            x1.append([X1[0] / X1[2], X1[1] / X1[2]])
            x2.append([X2[0] / X2[2], X2[1] / X2[2]])
    return x1, x2


def random_pose(rng):
    R = rotation([rng.uniform(-1, 1) for _ in range(3)], rng.uniform(0.05, 0.8))
    t = [rng.uniform(-1, 1), rng.uniform(-0.5, 0.5), rng.uniform(-0.5, 0.5)]
    return R, scale(t, 1.0 / norm(t))


def test_worked_example():
    # X1 = (0, 0, 5) and X2 = (4, 0, 4): x1 = (0, 0), x2 = (1, 0).
    R, t, count = recover_pose(E_EX, [[0.0, 0.0]], [[1.0, 0.0]])
    assert count == 1
    assert norm(sub(R, R_EX)) <= 1e-12
    assert norm(sub(t, T_EX)) <= 1e-12
    l1, l2 = depths(R, t, [0.0, 0.0], [1.0, 0.0])
    assert abs(l1 - 5.0) <= 1e-12 and abs(l2 - 4.0) <= 1e-12


def test_four_candidates_of_the_example():
    cands = pose_candidates(E_EX)
    twisted = [[0.8, 0.0, 0.6], [0.0, -1.0, 0.0], [0.6, 0.0, -0.8]]  # (2 t t^T - I) R
    rots = [R for R, _ in cands]
    assert sum(norm(sub(R, R_EX)) <= 1e-12 for R in rots) == 2
    assert sum(norm(sub(R, twisted)) <= 1e-12 for R in rots) == 2
    ts = [t for _, t in cands]
    assert sum(norm(sub(t, T_EX)) <= 1e-12 for t in ts) == 2
    assert sum(norm(sub(t, scale(T_EX, -1.0))) <= 1e-12 for t in ts) == 2
    # depths for the four candidates: one has both positive
    signs = sorted((depths(R, t, [0.0, 0.0], [1.0, 0.0])[0] > 0, depths(R, t, [0.0, 0.0], [1.0, 0.0])[1] > 0)
                   for R, t in cands)
    assert signs == [(False, False), (False, True), (True, False), (True, True)]


@pytest.mark.parametrize("seed", range(5))
def test_candidates_are_valid_factorizations(seed):
    rng = random.Random(seed)
    R, t = random_pose(rng)
    E = scale(mul(skew(t), R), rng.choice([-1.0, 1.0]) * rng.uniform(0.1, 10.0))
    En = scale(E, 1.0 / norm(E))
    for Rc, tc in pose_candidates(E):
        assert abs(det(Rc) - 1.0) <= 1e-12
        assert norm(sub(mul(transpose(Rc), Rc), [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]])) <= 1e-12
        assert abs(norm(tc) - 1.0) <= 1e-12
        F = mul(skew(tc), Rc)
        F = scale(F, 1.0 / norm(F))
        assert min(norm(sub(F, En)), norm(sub(F, scale(En, -1.0)))) <= 1e-12


@pytest.mark.parametrize("seed", range(5, 11))
def test_exact_recovery(seed):
    rng = random.Random(seed)
    R, t = random_pose(rng)
    x1, x2 = scene(rng, 20, R, t)
    E = scale(mul(skew(t), R), rng.choice([-1.0, 1.0]) * rng.uniform(0.1, 10.0))
    Rr, tr, count = recover_pose(E, x1, x2)
    assert count == 20
    assert rotation_angle(Rr, R) <= 1e-8
    assert direction_angle(tr, t) <= 1e-8
    # exactly one candidate puts all points in front of both cameras
    counts = sorted(count_in_front(Rc, tc, x1, x2) for Rc, tc in pose_candidates(E))
    assert counts[-1] == 20 and counts[-2] < 20


def test_twisted_pair_flips_one_depth():
    # (R, t) and ((2 t t^T - I) R, t) give depths of opposite sign product.
    rng = random.Random(12)
    R, t = random_pose(rng)
    tw = mul(sub([[2.0 * a * b for b in t] for a in t], [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]), R)
    x1, x2 = scene(rng, 10, R, t)
    for p, q in zip(x1, x2):
        l1, l2 = depths(R, t, p, q)
        m1, m2 = depths(tw, t, p, q)
        assert l1 > 0 and l2 > 0
        assert m1 * m2 < 0


def test_majority_with_noise():
    # sigma = 0.001 in normalized coordinates (0.5 pixel at f = 500), 50 points.
    rng = random.Random(13)
    R, t = random_pose(rng)
    x1, x2 = scene(rng, 50, R, t)
    x1 = [[c + rng.gauss(0.0, 0.001) for c in p] for p in x1]
    x2 = [[c + rng.gauss(0.0, 0.001) for c in p] for p in x2]
    Rr, tr, count = recover_pose(mul(skew(t), R), x1, x2)
    assert count >= 45
    assert rotation_angle(Rr, R) <= 1e-8
    assert direction_angle(tr, t) <= 1e-8


def test_parallel_rays_give_zero_depths():
    I3 = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
    assert depths(I3, [1.0, 0.0, 0.0], [0.2, 0.1], [0.2, 0.1]) == (0.0, 0.0)


def test_rejects_empty_input():
    with pytest.raises(ValueError):
        recover_pose(E_EX, [], [])
