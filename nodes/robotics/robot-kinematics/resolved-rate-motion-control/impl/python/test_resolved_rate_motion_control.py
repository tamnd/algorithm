# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/resolved-rate-motion-control/. The authors are listed in prov/XNS6ZX.jsonl.
"""Tests of resolved-rate control with explicit Euler steps on planar 2R and
3R arms with unit links: the 2R check values, the minimum-norm joint rate
against a KKT solve, first-order drift of the open-loop scheme, a bounded
error with feedback, agreement with closed-form 2R inverse kinematics, the
linear error dynamics, and the error at a singularity."""

import math
import random

import pytest

import rbm
from resolved_rate_motion_control import joint_rate, resolved_rate


def maxdiff(a, b):
    if a and isinstance(a[0], list):
        return max(abs(x - y) for ra, rb in zip(a, b) for x, y in zip(ra, rb))
    return max(abs(x - y) for x, y in zip(a, b))


def fk_planar(q):
    a = x = y = 0.0
    for t in q:
        a += t
        x += math.cos(a)
        y += math.sin(a)
    return [x, y]


def jac_planar(q):
    n = len(q)
    out = [[0.0] * n, [0.0] * n]
    for j in range(n):
        a = sum(q[: j + 1])
        for i in range(j + 1):
            out[0][i] -= math.sin(a)
            out[1][i] += math.cos(a)
    return out


def ik_2r(x, elbow):
    """Closed-form inverse kinematics of the 2R arm with unit links."""
    c2 = (x[0] ** 2 + x[1] ** 2 - 2.0) / 2.0
    q2 = elbow * math.acos(c2)
    q1 = math.atan2(x[1], x[0]) - math.atan2(math.sin(q2), 1.0 + math.cos(q2))
    return [q1, q2]


CENTER = [1.0, 0.8]
RADIUS = 0.3
OMEGA = 1.0


def circle(t):
    return [CENTER[0] + RADIUS * math.cos(OMEGA * t), CENTER[1] + RADIUS * math.sin(OMEGA * t)]


def circle_dot(t):
    return [-RADIUS * OMEGA * math.sin(OMEGA * t), RADIUS * OMEGA * math.cos(OMEGA * t)]


def final_error(path, dt):
    t = (len(path) - 1) * dt
    return rbm.norm(rbm.sub(circle(t), fk_planar(path[-1])))


def test_2r_check_values():
    q = [0.0, math.pi / 2.0]
    assert maxdiff(fk_planar(q), [1.0, 1.0]) < 1e-15
    assert maxdiff(jac_planar(q), [[-1.0, -1.0], [1.0, 0.0]]) < 1e-15
    for q in ([0.4, 1.1], [0.2, -0.7, 1.3]):
        assert maxdiff(rbm.num_jacobian(fk_planar, q), jac_planar(q)) < 1e-6
    for elbow in (1.0, -1.0):
        assert maxdiff(fk_planar(ik_2r([1.0, 1.0], elbow)), [1.0, 1.0]) < 1e-12
    assert maxdiff(ik_2r([1.0, 1.0], -1.0), [math.pi / 2.0, -math.pi / 2.0]) < 1e-12


def test_joint_rate_is_minimum_norm():
    rng = random.Random(11)
    for _ in range(5):
        q = [rng.uniform(-1.0, 1.0) for _ in range(3)]
        j = jac_planar(q)
        v = [rng.uniform(-1.0, 1.0) for _ in range(2)]
        qd = joint_rate(j, v)
        kkt = rbm.zeros(5, 5)
        for i in range(3):
            kkt[i][i] = 1.0
        for r in range(2):
            for c in range(3):
                kkt[3 + r][c] = j[r][c]
                kkt[c][3 + r] = j[r][c]
        sol = rbm.solve(kkt, [0.0, 0.0, 0.0] + v)
        assert maxdiff(qd, sol[:3]) < 1e-12
        assert maxdiff(rbm.matvec(j, qd), v) < 1e-12
    # square case: the pseudoinverse is the inverse
    j = jac_planar([0.0, math.pi / 2.0])
    assert maxdiff(joint_rate(j, [0.0, 1.0]), rbm.solve(j, [0.0, 1.0])) < 1e-15


def test_open_loop_drift_is_first_order():
    q0 = ik_2r(circle(0.0), 1.0)
    errs = []
    for dt in (0.02, 0.01, 0.005):
        steps = int(round(2.0 / dt))
        path = resolved_rate(fk_planar, jac_planar, q0, circle, circle_dot, 0.0, dt, steps)
        errs.append(final_error(path, dt))
    assert errs[0] < 0.05
    for a, b in zip(errs, errs[1:]):
        assert 1.6 < a / b < 2.4


def test_feedback_bounds_the_error():
    q0 = ik_2r(circle(0.0), 1.0)
    q0 = [q0[0] + 0.1, q0[1] - 0.1]
    dt, k = 0.01, 20.0
    path = resolved_rate(fk_planar, jac_planar, q0, circle, circle_dot, k, dt, 300)
    errs = [rbm.norm(rbm.sub(circle(i * dt), fk_planar(q))) for i, q in enumerate(path)]
    assert errs[0] > 0.05
    assert max(errs[100:]) < 2e-3
    # the open-loop run from the same start keeps its initial error
    path0 = resolved_rate(fk_planar, jac_planar, q0, circle, circle_dot, 0.0, dt, 300)
    assert final_error(path0, dt) > 0.04
    # the tracked joints are close to the closed-form solution of the same branch
    t = 300 * dt
    assert maxdiff(path[-1], ik_2r(circle(t), 1.0)) < 5e-3


def test_error_halves_with_the_step():
    q0 = ik_2r(circle(0.0), -1.0)
    out = []
    for dt in (0.01, 0.005):
        steps = int(round(2.0 / dt))
        path = resolved_rate(fk_planar, jac_planar, q0, circle, circle_dot, 10.0, dt, steps)
        out.append(final_error(path, dt))
    assert out[1] < 1e-3
    assert 1.6 < out[0] / out[1] < 2.4


def test_linear_error_dynamics_for_a_fixed_target():
    x_d = [1.2, 0.6]
    dt, k = 0.01, 5.0
    path = resolved_rate(fk_planar, jac_planar, [0.1, 1.4], lambda t: x_d, lambda t: [0.0, 0.0], k, dt, 400)
    errs = [rbm.norm(rbm.sub(x_d, fk_planar(q))) for q in path]
    # near the solution, e_{j+1} = (1 - k dt) e_j + O(|e_j|^2)
    for a, b in zip(errs[200:260], errs[201:261]):
        assert abs(b / a - (1.0 - k * dt)) < 1e-3
    assert errs[-1] < 1e-4 * errs[0]


def test_3r_redundant_tracking():
    q0 = [0.3, -0.9, 1.4]
    dt, k = 0.005, 10.0
    path = resolved_rate(fk_planar, jac_planar, q0, circle, circle_dot, k, dt, 1000)
    errs = [rbm.norm(rbm.sub(circle(i * dt), fk_planar(q))) for i, q in enumerate(path)]
    assert max(errs[400:]) < 1e-3
    # a matrix gain gives the same run as the number k
    path_m = resolved_rate(fk_planar, jac_planar, q0, circle, circle_dot, [[k, 0.0], [0.0, k]], dt, 50)
    assert maxdiff(path_m[-1], path[50]) < 1e-14


def test_singular_configuration_raises():
    with pytest.raises(ValueError):
        joint_rate(jac_planar([0.3, 0.0]), [1.0, 0.0])
