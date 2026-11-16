# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/joint-space-inertia-matrix/. The authors are listed in prov/FNGKHS.jsonl.

import math
import random

from joint_space_inertia_matrix import (
    PlanarArm,
    cholesky,
    coriolis_matrix,
    gravity_torque,
    inverse_dynamics,
    kinetic_energy,
    mass_matrix,
    mass_matrix_derivatives,
    points,
    two_link_point_mass,
)

G = 9.81


def close(a, b, tol):
    return abs(a - b) <= tol


def random_arm(rng, n):
    L = [rng.uniform(0.3, 1.5) for _ in range(n)]
    m = [rng.uniform(0.5, 5.0) for _ in range(n)]
    r = [rng.uniform(0.0, 1.0) * L[i] for i in range(n)]
    I = [rng.uniform(0.01, 0.5) for _ in range(n)]
    return PlanarArm(L, m, r, I)


def test_check_values_two_link():
    arm = two_link_point_mass()
    M0 = mass_matrix(arm, [0.0, 0.0])
    assert all(close(M0[a][b], [[5, 2], [2, 1]][a][b], 1e-12) for a in range(2) for b in range(2))
    M1 = mass_matrix(arm, [0.0, math.pi / 2])
    assert all(close(M1[a][b], [[3, 1], [1, 1]][a][b], 1e-12) for a in range(2) for b in range(2))
    for q2 in (0.0, 0.4, 1.0, 2.5, math.pi):
        M = mass_matrix(arm, [0.7, q2])
        c2 = math.cos(q2)
        assert close(M[0][0], 3 + 2 * c2, 1e-12)
        assert close(M[0][1], 1 + c2, 1e-12)
        assert close(M[1][1], 1.0, 1e-12)


def test_general_two_link_closed_form():
    rng = random.Random(7)
    for _ in range(20):
        arm = random_arm(rng, 2)
        q = [rng.uniform(-math.pi, math.pi) for _ in range(2)]
        a1 = arm.I[0] + arm.m[0] * arm.r[0] ** 2 + arm.m[1] * arm.L[0] ** 2
        a2 = arm.I[1] + arm.m[1] * arm.r[1] ** 2
        a3 = arm.m[1] * arm.L[0] * arm.r[1]
        c2 = math.cos(q[1])
        M = mass_matrix(arm, q)
        assert close(M[0][0], a1 + a2 + 2 * a3 * c2, 1e-12)
        assert close(M[0][1], a2 + a3 * c2, 1e-12)
        assert close(M[1][0], a2 + a3 * c2, 1e-12)
        assert close(M[1][1], a2, 1e-12)


def test_euler_lagrange_torques_two_link():
    # Closed form of the Euler-Lagrange equations of the check arm.
    arm = two_link_point_mass()
    cases = [
        ((0.0, math.pi / 2), (1.0, 1.0), (0.0, 0.0), 0.0, (-3.0, 1.0)),
        ((0.0, math.pi / 2), (1.0, 1.0), (0.0, 0.0), G, (2 * G - 3.0, 1.0)),
        ((0.0, 0.0), (0.0, 0.0), (0.0, 0.0), G, (3 * G, G)),
    ]
    for q, qd, qdd, g, want in cases:
        tau = inverse_dynamics(arm, q, qd, qdd, g)
        assert close(tau[0], want[0], 1e-6) and close(tau[1], want[1], 1e-6)
    rng = random.Random(11)
    for _ in range(20):
        q = [rng.uniform(-3, 3) for _ in range(2)]
        qd = [rng.uniform(-2, 2) for _ in range(2)]
        qdd = [rng.uniform(-2, 2) for _ in range(2)]
        s2, c2 = math.sin(q[1]), math.cos(q[1])
        c1, c12 = math.cos(q[0]), math.cos(q[0] + q[1])
        t1 = (3 + 2 * c2) * qdd[0] + (1 + c2) * qdd[1] - s2 * (2 * qd[0] * qd[1] + qd[1] ** 2) + 2 * G * c1 + G * c12
        t2 = (1 + c2) * qdd[0] + qdd[1] + s2 * qd[0] ** 2 + G * c12
        tau = inverse_dynamics(arm, q, qd, qdd, G)
        assert close(tau[0], t1, 1e-6) and close(tau[1], t2, 1e-6)


def test_symmetric_positive_definite():
    rng = random.Random(3)
    for n in (1, 2, 3, 5):
        for _ in range(10):
            arm = random_arm(rng, n)
            q = [rng.uniform(-math.pi, math.pi) for _ in range(n)]
            M = mass_matrix(arm, q)
            for a in range(n):
                for b in range(n):
                    assert close(M[a][b], M[b][a], 1e-12)
            cholesky(M)


def test_singular_when_mass_is_on_the_axis():
    # Link 2 is a point mass at joint 2: turning joint 2 moves no mass.
    arm = PlanarArm([1.0, 1.0], [1.0, 1.0], [1.0, 0.0], [0.0, 0.0])
    M = mass_matrix(arm, [0.3, 0.9])
    assert close(M[1][1], 0.0, 1e-12) and close(M[0][1], 0.0, 1e-12)
    try:
        cholesky(M)
    except ValueError:
        return
    raise AssertionError("cholesky accepted a singular M")


def test_kinetic_energy_matches_direct_sum():
    rng = random.Random(5)
    h = 1e-6
    for _ in range(10):
        arm = random_arm(rng, 3)
        q = [rng.uniform(-math.pi, math.pi) for _ in range(3)]
        qd = [rng.uniform(-2, 2) for _ in range(3)]
        _, cp = points(arm, [q[i] + h * qd[i] for i in range(3)])
        _, cm = points(arm, [q[i] - h * qd[i] for i in range(3)])
        K = 0.0
        for i in range(3):
            vx = (cp[i][0] - cm[i][0]) / (2 * h)
            vy = (cp[i][1] - cm[i][1]) / (2 * h)
            w = sum(qd[: i + 1])
            K += 0.5 * arm.m[i] * (vx * vx + vy * vy) + 0.5 * arm.I[i] * w * w
        assert close(kinetic_energy(arm, q, qd), K, 1e-6)
    arm = two_link_point_mass()
    assert close(kinetic_energy(arm, [0.0, math.pi / 2], [1.0, 1.0]), 3.0, 1e-12)


def test_gravity_is_gradient_of_potential():
    rng = random.Random(9)
    h = 1e-6
    for _ in range(10):
        arm = random_arm(rng, 3)
        q = [rng.uniform(-math.pi, math.pi) for _ in range(3)]

        def P(qq):
            _, coms = points(arm, qq)
            return sum(arm.m[i] * G * coms[i][1] for i in range(3))

        gq = gravity_torque(arm, q, G)
        for k in range(3):
            qp = list(q)
            qm = list(q)
            qp[k] += h
            qm[k] -= h
            assert close(gq[k], (P(qp) - P(qm)) / (2 * h), 1e-5)


def test_skew_symmetry_of_mdot_minus_2c():
    rng = random.Random(13)
    for _ in range(10):
        arm = random_arm(rng, 3)
        q = [rng.uniform(-math.pi, math.pi) for _ in range(3)]
        qd = [rng.uniform(-2, 2) for _ in range(3)]
        dM = mass_matrix_derivatives(arm, q)
        Md = [[sum(dM[k][a][b] * qd[k] for k in range(3)) for b in range(3)] for a in range(3)]
        C = coriolis_matrix(arm, q, qd)
        N = [[Md[a][b] - 2 * C[a][b] for b in range(3)] for a in range(3)]
        for a in range(3):
            for b in range(3):
                assert close(N[a][b], -N[b][a], 1e-6)


def test_first_joint_does_not_change_m():
    rng = random.Random(17)
    arm = random_arm(rng, 4)
    q = [rng.uniform(-math.pi, math.pi) for _ in range(4)]
    M = mass_matrix(arm, q)
    q2 = [q[0] + 1.234] + q[1:]
    M2 = mass_matrix(arm, q2)
    assert all(close(M[a][b], M2[a][b], 1e-12) for a in range(4) for b in range(4))
