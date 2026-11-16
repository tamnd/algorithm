# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/triad-method/. The authors are listed in prov/FY3PHK.jsonl.

import math
import random

import pytest

import rbm
from triad_method import triad, wahba_loss


def random_unit(rng):
    while True:
        v = [rng.gauss(0.0, 1.0) for _ in range(3)]
        n = rbm.norm(v)
        if n > 1e-3:
            return [x / n for x in v]


def random_rotation(rng):
    q = [rng.gauss(0.0, 1.0) for _ in range(4)]
    return rbm.quat_to_rot(q)


def max_diff(a, b):
    return max(abs(a[i][j] - b[i][j]) for i in range(3) for j in range(3))


def angle_between(u, v):
    c = rbm.dot(u, v) / (rbm.norm(u) * rbm.norm(v))
    return math.acos(max(-1.0, min(1.0, c)))


def rotation_angle(a, b):
    """Return the angle of the rotation a b^T."""
    return rbm.norm(rbm.so3_log(rbm.mul(a, rbm.transpose(b))))


def test_check_rotation():
    # The area check rotation: R_sb is 120 degrees about (1, 1, 1) / sqrt(3),
    # so A = R_bs = R_sb^T.
    r_sb = [[0.0, 0.0, 1.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]]
    a_true = rbm.transpose(r_sb)
    r1, r2 = [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]
    b1, b2 = rbm.matvec(a_true, r1), rbm.matvec(a_true, r2)
    assert b1 == [0.0, 0.0, 1.0] and b2 == [1.0, 0.0, 0.0]
    assert max_diff(triad(b1, b2, r1, r2), a_true) < 1e-15
    # The other order of the pairs gives the same matrix for exact data.
    assert max_diff(triad(b2, b1, r2, r1), a_true) < 1e-15


def test_noise_free_recovery():
    rng = random.Random(1)
    for _ in range(200):
        a_true = random_rotation(rng)
        r1, r2 = random_unit(rng), random_unit(rng)
        s1, s2 = rng.uniform(0.1, 10.0), rng.uniform(0.1, 10.0)
        # Body vectors need not be unit: TRIAD uses only their directions.
        b1 = rbm.scale(rbm.matvec(a_true, r1), s1)
        b2 = rbm.scale(rbm.matvec(a_true, r2), s2)
        assert max_diff(triad(b1, b2, r1, r2), a_true) < 1e-12


def test_output_is_a_rotation_with_noise():
    rng = random.Random(2)
    for _ in range(200):
        r1, r2 = random_unit(rng), random_unit(rng)
        b1, b2 = random_unit(rng), random_unit(rng)
        a = triad(b1, b2, r1, r2)
        ata = rbm.mul(rbm.transpose(a), a)
        assert max_diff(ata, rbm.eye(3)) < 1e-13
        assert abs(rbm.det(a) - 1.0) < 1e-13


def test_first_vector_matched_exactly():
    rng = random.Random(3)
    a_true = random_rotation(rng)
    for _ in range(200):
        r1, r2 = random_unit(rng), random_unit(rng)
        b1 = rbm.matvec(rbm.mul(rbm.so3_exp([rng.gauss(0.0, 0.05) for _ in range(3)]), a_true), r1)
        b2 = rbm.matvec(rbm.mul(rbm.so3_exp([rng.gauss(0.0, 0.05) for _ in range(3)]), a_true), r2)
        a = triad(b1, b2, r1, r2)
        assert rbm.norm(rbm.sub(rbm.matvec(a, r1), b1)) < 1e-12
        # The second pair is matched only up to the angle the noise put
        # between the pairs: the angle of b2 to the plane is not removed.
        assert angle_between(rbm.matvec(a, r2), b2) < 0.5


def test_collinear_input_is_rejected():
    with pytest.raises(ValueError):
        triad([0.0, 0.0, 1.0], [0.0, 0.0, -2.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0])
    with pytest.raises(ValueError):
        triad([0.0, 0.0, 1.0], [1.0, 0.0, 0.0], [1.0, 0.0, 0.0], [3.0, 0.0, 0.0])
    with pytest.raises(ValueError):
        triad([0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0])


def descend_wahba(a, bs, rs, weights, steps=400):
    """Minimize the Wahba loss on SO(3) by gradient steps from a.

    With A = A0 exp([w]) and B = sum a_i b_i r_i^T, the loss is
    lambda0 - tr(A^T B), and its gradient in w is -vee(A^T B - B^T A).
    A step of size h along that direction lowers the loss for small h.
    """
    bmat = rbm.zeros(3, 3)
    for wi, b, r in zip(weights, bs, rs):
        for i in range(3):
            for j in range(3):
                bmat[i][j] += wi * b[i] * r[j]
    for _ in range(steps):
        m = rbm.mul(rbm.transpose(a), bmat)
        g = [m[2][1] - m[1][2], m[0][2] - m[2][0], m[1][0] - m[0][1]]
        a = rbm.mul(a, rbm.so3_exp(rbm.scale(g, 0.25)))
    return a


def test_triad_is_not_optimal():
    # Measurement: TRIAD loss >= optimal loss, and in most noisy draws the
    # gap is strictly positive, so TRIAD is not the Wahba minimizer.
    rng = random.Random(4)
    gaps = []
    for _ in range(30):
        a_true = random_rotation(rng)
        r1, r2 = random_unit(rng), random_unit(rng)
        bs = []
        for r in (r1, r2):
            noise = rbm.so3_exp([rng.gauss(0.0, 0.05) for _ in range(3)])
            bs.append(rbm.matvec(rbm.mul(noise, a_true), r))
        weights = [0.5, 0.5]
        a_triad = triad(bs[0], bs[1], r1, r2)
        a_opt = descend_wahba(a_triad, bs, [r1, r2], weights)
        lt = wahba_loss(a_triad, bs, [r1, r2], weights)
        lo = wahba_loss(a_opt, bs, [r1, r2], weights)
        assert lo <= lt + 1e-15
        gaps.append(lt - lo)
    assert sum(1 for g in gaps if g > 1e-6) >= 25


def test_order_matters_with_noise():
    rng = random.Random(5)
    a_true = random_rotation(rng)
    r1, r2 = random_unit(rng), random_unit(rng)
    b1 = rbm.matvec(rbm.mul(rbm.so3_exp([0.03, -0.02, 0.01]), a_true), r1)
    b2 = rbm.matvec(rbm.mul(rbm.so3_exp([-0.01, 0.04, 0.02]), a_true), r2)
    a12 = triad(b1, b2, r1, r2)
    a21 = triad(b2, b1, r2, r1)
    assert rotation_angle(a12, a21) > 1e-3
    assert rbm.norm(rbm.sub(rbm.matvec(a21, r2), b2)) < 1e-12


def test_order_does_not_matter_without_noise():
    rng = random.Random(6)
    a_true = random_rotation(rng)
    r1, r2 = random_unit(rng), random_unit(rng)
    b1, b2 = rbm.matvec(a_true, r1), rbm.matvec(a_true, r2)
    assert max_diff(triad(b1, b2, r1, r2), triad(b2, b1, r2, r1)) < 1e-12


def test_error_grows_as_vectors_become_parallel():
    # Measurement: with fixed noise, the attitude error grows as the angle
    # between the two reference directions shrinks.
    rng = random.Random(7)
    errs = []
    for sep in (math.pi / 2.0, 0.3, 0.05):
        total = 0.0
        for _ in range(50):
            a_true = random_rotation(rng)
            r1 = [0.0, 0.0, 1.0]
            r2 = [math.sin(sep), 0.0, math.cos(sep)]
            b1 = rbm.matvec(rbm.mul(rbm.so3_exp([rng.gauss(0.0, 0.01) for _ in range(3)]), a_true), r1)
            b2 = rbm.matvec(rbm.mul(rbm.so3_exp([rng.gauss(0.0, 0.01) for _ in range(3)]), a_true), r2)
            total += rotation_angle(triad(b1, b2, r1, r2), a_true)
        errs.append(total / 50)
    assert errs[0] < errs[1] < errs[2]
