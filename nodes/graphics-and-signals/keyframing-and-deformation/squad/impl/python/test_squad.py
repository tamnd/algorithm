# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/squad/. The authors are listed in prov/5MKSXN.jsonl.
"""Tests of squad and of the shared helper anim.py.

The squad tests check the round trip through the keys, the unit norm, the
continuity of the first derivative at the inner keys (one sided differences
against the closed form tangent q_i (a - b) / 2 of the proof), the reduction
to slerp for two keys and for keys on one great circle at equal steps, and
the invariance under a change of the world frame.
"""

import math
import random

import anim
from squad import Squad, align_signs, arc, control_points


def rand_unit(rng, n=4):
    while True:
        v = [rng.gauss(0.0, 1.0) for _ in range(n)]
        s = math.sqrt(sum(x * x for x in v))
        if s > 1e-3:
            return tuple(x / s for x in v)


def rand_rot(rng):
    return anim.q_to_mat3(rand_unit(rng))


def qclose(p, q, tol):
    d1 = max(abs(a - b) for a, b in zip(p, q))
    d2 = max(abs(a + b) for a, b in zip(p, q))
    return min(d1, d2) <= tol


def mclose(a, b, tol):
    return all(abs(a[i][j] - b[i][j]) <= tol for i in range(len(a)) for j in range(len(a[0])))


def rot_angle(q):
    q = anim.q_normalize(q)
    return 2.0 * math.atan2(math.sqrt(q[1] ** 2 + q[2] ** 2 + q[3] ** 2), abs(q[0]))


# ---------------------------------------------------------------- anim.py


def test_vectors():
    a, b = (1.0, 2.0, 3.0), (4.0, -5.0, 6.0)
    assert anim.add(a, b) == (5.0, -3.0, 9.0)
    assert anim.sub(a, b) == (-3.0, 7.0, -3.0)
    assert anim.scale(a, 2.0) == (2.0, 4.0, 6.0)
    assert anim.dot(a, b) == 12.0
    c = anim.cross(a, b)
    assert abs(anim.dot(c, a)) < 1e-12 and abs(anim.dot(c, b)) < 1e-12
    assert c == (27.0, 6.0, -13.0)
    assert anim.cross2((1.0, 0.0), (0.0, 1.0)) == 1.0
    assert abs(anim.norm(anim.normalize(b)) - 1.0) < 1e-15
    assert anim.lerp(a, b, 0.5) == (2.5, -1.5, 4.5)


def test_matrices():
    rng = random.Random(1)
    for n in (2, 3, 4, 5):
        a = [[rng.uniform(-1, 1) for _ in range(n)] for _ in range(n)]
        ai = anim.inv(a)
        assert mclose(anim.mul(a, ai), anim.eye(n), 1e-10)
        x = [rng.uniform(-1, 1) for _ in range(n)]
        b = anim.matvec(a, x)
        y = anim.solve(a, b)
        assert max(abs(p - q) for p, q in zip(x, y)) < 1e-10
        # det by the Leibniz formula for small n, by the product rule otherwise
        bm = [[rng.uniform(-1, 1) for _ in range(n)] for _ in range(n)]
        assert abs(anim.det(anim.mul(a, bm)) - anim.det(a) * anim.det(bm)) < 1e-10
        assert abs(anim.det(anim.transpose(a)) - anim.det(a)) < 1e-12
    assert anim.det([[1.0, 2.0, 3.0, 4.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 2.0, 0.0], [0.0, 0.0, 0.0, 3.0]]) == 6.0
    try:
        anim.solve([[1.0, 2.0], [2.0, 4.0]], [1.0, 2.0])
        raise AssertionError("singular matrix was not detected")
    except ValueError:
        pass


def test_slerp_check_values():
    q0 = (1.0, 0.0, 0.0, 0.0)
    q1 = (math.sqrt(0.5), 0.0, 0.0, math.sqrt(0.5))
    h = anim.slerp(q0, q1, 0.5)
    assert max(abs(a - b) for a, b in zip(h, (0.92388, 0.0, 0.0, 0.38268))) < 1e-5
    nl = anim.q_normalize(anim.lerp(q0, q1, 0.5))
    assert qclose(h, nl, 1e-12)
    q = anim.slerp(q0, q1, 0.25)
    assert max(abs(a - b) for a, b in zip(q, (0.98079, 0.0, 0.0, 0.19509))) < 1e-5
    assert abs(rot_angle(q) - math.pi / 8) < 1e-12
    assert abs(rot_angle(q) - 0.392699) < 1e-6
    nl = anim.q_normalize(anim.lerp(q0, q1, 0.25))
    assert abs(rot_angle(nl) - 0.376959) < 1e-6
    # the sign flip: -q1 gives the same result
    assert qclose(anim.slerp(q0, tuple(-x for x in q1), 0.25), q, 1e-12)
    # the end points and the small angle branch
    rng = random.Random(2)
    for _ in range(50):
        a, b = rand_unit(rng), rand_unit(rng)
        assert qclose(anim.slerp(a, b, 0.0), a, 1e-12)
        assert qclose(anim.slerp(a, b, 1.0), b, 1e-12)
        assert abs(anim.norm(anim.slerp(a, b, rng.random())) - 1.0) < 1e-12
    a = rand_unit(rng)
    b = anim.q_normalize(anim.add(a, (1e-9, 0.0, 0.0, 0.0)))
    assert abs(anim.norm(anim.slerp(a, b, 0.3)) - 1.0) < 1e-12


def test_quaternions():
    rng = random.Random(3)
    for _ in range(100):
        q = rand_unit(rng)
        v = tuple(rng.uniform(-1, 1) for _ in range(3))
        r = anim.q_to_mat3(q)
        assert max(abs(a - b) for a, b in zip(anim.q_rotate(q, v), anim.matvec(r, v))) < 1e-12
        assert mclose(anim.mul(r, anim.transpose(r)), anim.eye(3), 1e-12)
        assert abs(anim.det(r) - 1.0) < 1e-12
        assert qclose(anim.q_from_mat3(r), q, 1e-12)
        assert qclose(anim.q_exp(anim.q_log(q)), q, 1e-12)
        p = rand_unit(rng)
        assert mclose(anim.q_to_mat3(anim.q_mul(p, q)), anim.mul(anim.q_to_mat3(p), r), 1e-12)
    # i j = k (Hamilton)
    assert anim.q_mul((0, 1, 0, 0), (0, 0, 1, 0)) == (0, 0, 0, 1)
    # rotation by pi about x: q = (0, 1, 0, 0), through the matrix and back
    q = anim.q_from_axis_angle((2.0, 0.0, 0.0), math.pi)
    r = anim.q_to_mat3(q)
    assert mclose(r, [[1, 0, 0], [0, -1, 0], [0, 0, -1]], 1e-15)
    qb = anim.q_from_mat3(r)
    assert qclose(qb, (0.0, 1.0, 0.0, 0.0), 1e-15)
    assert mclose(anim.q_to_mat3(qb), r, 1e-15)
    # the log of (cos phi, sin phi u) is (0, phi u)
    lg = anim.q_log(anim.q_from_axis_angle((0, 0, 1), 1.2))
    assert max(abs(a - b) for a, b in zip(lg, (0.0, 0.0, 0.0, 0.6))) < 1e-15


def test_polar():
    rng = random.Random(4)
    for _ in range(40):
        r = rand_rot(rng)
        m = [[rng.uniform(-1, 1) for _ in range(3)] for _ in range(3)]
        s = anim.mul(anim.transpose(m), m)
        for i in range(3):
            s[i][i] += 0.1
        f = anim.mul(r, s)
        r2, s2 = anim.polar(f)
        assert mclose(r2, r, 1e-9) and mclose(s2, s, 1e-9)
        assert abs(anim.det(r2) - 1.0) < 1e-12
        # det F < 0: R stays a rotation, R S = F, and S is symmetric
        g = [row[:] for row in f]
        g[0] = [-x for x in g[0]]
        r3, s3 = anim.polar(g)
        assert abs(anim.det(r3) - 1.0) < 1e-10
        assert mclose(anim.mul(r3, s3), g, 1e-10)
        assert mclose(s3, anim.transpose(s3), 1e-12)
    for _ in range(40):
        th = rng.uniform(-math.pi, math.pi)
        a = rng.uniform(0.2, 2.0)
        c = rng.uniform(0.2, 2.0)
        b = rng.uniform(-1, 1) * 0.9 * math.sqrt(a * c)
        s = [[a, b], [b, c]]
        r2, s2 = anim.polar(anim.mul(anim.rot2(th), s))
        assert mclose(r2, anim.rot2(th), 1e-12) and mclose(s2, s, 1e-12)


def test_transforms_and_num_grad():
    rng = random.Random(5)
    r = rand_rot(rng)
    rs = anim.mul(r, [[2.0, 0, 0], [0, 0.5, 0], [0, 0, 1.5]])
    m = anim.make_T(rs, (1.0, -2.0, 3.0))
    p = (0.3, 0.4, -0.5)
    assert max(abs(a - b) for a, b in zip(anim.T_apply(anim.T_inv(m), anim.T_apply(m, p)), p)) < 1e-12
    assert mclose(anim.T_mul(m, anim.T_inv(m)), anim.eye(4), 1e-12)

    def f(x):
        return x[0] ** 3 + 2.0 * x[0] * x[1] + math.sin(x[1])

    g = anim.num_grad(f, [0.7, -0.4], 1e-6)
    exact = [3 * 0.49 + 2 * -0.4, 2 * 0.7 + math.cos(-0.4)]
    assert max(abs(a - b) for a, b in zip(g, exact)) < 1e-8


# ---------------------------------------------------------------- squad


def random_keys(rng, n, step=1.0):
    keys = [rand_unit(rng)]
    for _ in range(n - 1):
        axis = rand_unit(rng, 3)
        keys.append(anim.q_mul(keys[-1], anim.q_from_axis_angle(axis, rng.uniform(0.2, step))))
    # random signs, which align_signs must undo
    return [q if rng.random() < 0.5 else tuple(-x for x in q) for q in keys]


def test_passes_through_keys_and_unit_norm():
    rng = random.Random(6)
    keys = random_keys(rng, 7, 1.5)
    c = Squad(keys)
    for i, q in enumerate(keys):
        assert qclose(c(float(i)), q, 1e-12)
    for k in range(0, 601):
        u = 6.0 * k / 600
        assert abs(anim.norm(c(u)) - 1.0) < 1e-12


def test_first_derivative_is_continuous():
    rng = random.Random(7)
    keys = random_keys(rng, 6, 1.5)
    c = Squad(keys)
    q = c.keys
    h = 1e-6
    for i in range(1, len(q) - 1):
        left = tuple((x - y) / h for x, y in zip(c.segment(i - 1, 1.0), c.segment(i - 1, 1.0 - h)))
        right = tuple((y - x) / h for x, y in zip(c.segment(i, 0.0), c.segment(i, h)))
        qc = anim.q_conj(q[i])
        a = anim.q_log(anim.q_mul(qc, q[i + 1]))
        b = anim.q_log(anim.q_mul(qc, q[i - 1]))
        tangent = anim.q_mul(q[i], tuple((x - y) / 2.0 for x, y in zip(a, b)))
        assert max(abs(x - y) for x, y in zip(left, tangent)) < 1e-4
        assert max(abs(x - y) for x, y in zip(right, tangent)) < 1e-4
    # slerp keyed piecewise has a jump in the derivative at the same keys
    i = 2
    l2 = tuple((x - y) / h for x, y in zip(arc(q[i - 1], q[i], 1.0), arc(q[i - 1], q[i], 1.0 - h)))
    r2 = tuple((y - x) / h for x, y in zip(arc(q[i], q[i + 1], 0.0), arc(q[i], q[i + 1], h)))
    assert max(abs(x - y) for x, y in zip(l2, r2)) > 1e-2


def test_two_keys_is_slerp():
    rng = random.Random(8)
    for _ in range(20):
        a, b = rand_unit(rng), rand_unit(rng)
        c = Squad([a, b])
        for k in range(11):
            t = k / 10
            assert qclose(c(t), anim.slerp(a, b, t), 1e-12)


def test_equal_steps_on_one_axis_is_constant_speed_slerp():
    keys = [anim.q_from_axis_angle((0.0, 0.0, 1.0), 0.7 * i) for i in range(5)]
    c = Squad(keys)
    for i in range(1, 4):
        assert qclose(c.ctrl[i], keys[i], 1e-15)
    for k in range(41):
        u = 4.0 * k / 40
        assert qclose(c(u), anim.q_from_axis_angle((0.0, 0.0, 1.0), 0.7 * u), 1e-12)


def test_arc_equals_slerp_on_short_arcs():
    rng = random.Random(9)
    for _ in range(50):
        a, b = rand_unit(rng), rand_unit(rng)
        if anim.q_dot(a, b) < 0:
            b = tuple(-x for x in b)
        t = rng.random()
        assert qclose(arc(a, b, t), anim.slerp(a, b, t), 1e-12)


def test_world_frame_invariance():
    rng = random.Random(10)
    keys = random_keys(rng, 5, 1.2)
    g = rand_unit(rng)
    c1 = Squad(keys)
    c2 = Squad([anim.q_mul(g, q) for q in keys])
    for k in range(41):
        u = 4.0 * k / 40
        assert qclose(c2(u), anim.q_mul(g, c1(u)), 1e-12)


def test_controls_of_aligned_keys():
    rng = random.Random(11)
    keys = align_signs(random_keys(rng, 5, 1.0))
    for p, q in zip(keys, keys[1:]):
        assert anim.q_dot(p, q) >= 0.0
    s = control_points(keys)
    assert s[0] == keys[0] and s[-1] == keys[-1]
