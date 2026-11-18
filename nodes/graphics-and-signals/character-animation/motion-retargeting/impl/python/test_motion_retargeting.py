# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/motion-retargeting/. The authors are listed in prov/0KV7A9.jsonl.
"""Tests of motion retargeting with a minimal B-spline displacement.

The foot constraints of the new character hold. The same character needs no
displacement. The solution meets the first order optimality condition (W c
in the row space of the constraint Jacobian), and feasible neighbors have a
larger objective. Frames far from all constraints do not change. The check
value of the page, one constraint on a straight leg, holds.
"""

import math
import random

import anim
from motion_retargeting import basis, control_count, displacement, foot, foot_jacobian, retarget

FRAMES = 24
SRC_LEN = (1.0, 1.0)
NEW_LEN = (0.8, 0.9)
PLANT = (0.6, 0.0)
CONS = [(f, PLANT) for f in range(6, 16)]


def source():
    out = []
    for f in range(FRAMES):
        a1 = 0.5 * math.sin(2 * math.pi * f / FRAMES)
        a2 = 0.3 + 0.3 * math.cos(2 * math.pi * f / FRAMES)
        if 6 <= f <= 15:
            p = PLANT
        elif f < 6:
            p = (0.6 - 0.1 * (6 - f), 0.05 * (6 - f))
        else:
            p = (0.6 + 0.1 * (f - 15), 0.05 * (f - 15))
        o = foot((0.0, 0.0, a1, a2), SRC_LEN)
        out.append((p[0] - o[0], p[1] - o[1], a1, a2))
    return out


def jac_and_res(src, c, lengths, cons, spacing):
    count = control_count(len(src), spacing)
    jac, res = [], []
    for f, p in cons:
        q = [a + b for a, b in zip(src[f], displacement(c, f, spacing, count))]
        g = foot(q, lengths)
        jq = foot_jacobian(q, lengths)
        for row in range(2):
            r = [0.0] * len(c)
            for k in range(4):
                for j, w in basis(f, spacing, count):
                    r[k * count + j] = jq[row][k] * w
            jac.append(r)
            res.append(g[row] - p[row])
    return jac, res


def test_source_plants_the_foot():
    src = source()
    for f, p in CONS:
        assert max(abs(a - b) for a, b in zip(foot(src[f], SRC_LEN), p)) < 1e-12


def test_constraints_hold_for_the_new_character():
    src = source()
    motion, _, it = retarget(src, NEW_LEN, CONS)
    assert it < 50
    for f, p in CONS:
        assert max(abs(a - b) for a, b in zip(foot(motion[f], NEW_LEN), p)) < 1e-9
    # The source does not meet them: the leg is shorter.
    assert max(abs(foot(src[f], NEW_LEN)[1]) for f, _ in CONS) > 0.1


def test_same_character_needs_no_displacement():
    src = source()
    motion, c, _ = retarget(src, SRC_LEN, CONS)
    assert max(abs(v) for v in c) < 1e-12
    assert all(abs(a - b) < 1e-12 for p, q in zip(motion, src) for a, b in zip(p, q))


def test_first_order_optimality():
    src = source()
    _, c, _ = retarget(src, NEW_LEN, CONS)
    jac, _ = jac_and_res(src, c, NEW_LEN, CONS, 2)
    m = len(jac)
    gram = [[sum(x * y for x, y in zip(jac[a], jac[b])) for b in range(m)] for a in range(m)]
    mu = anim.solve(gram, [sum(x * y for x, y in zip(r, c)) for r in jac])
    proj = [ci - sum(jac[a][i] * mu[a] for a in range(m)) for i, ci in enumerate(c)]
    assert max(abs(v) for v in proj) < 1e-8


def test_feasible_neighbors_are_not_better():
    src = source()
    _, c, _ = retarget(src, NEW_LEN, CONS)
    best = sum(v * v for v in c)
    rng = random.Random(5)
    for _ in range(10):
        x = [v + rng.gauss(0, 0.01) for v in c]
        for _ in range(30):
            jac, res = jac_and_res(src, x, NEW_LEN, CONS, 2)
            m = len(jac)
            gram = [[sum(p * q for p, q in zip(jac[a], jac[b])) for b in range(m)] for a in range(m)]
            mu = anim.solve(gram, res)
            x = [xi - sum(jac[a][i] * mu[a] for a in range(m)) for i, xi in enumerate(x)]
        _, res = jac_and_res(src, x, NEW_LEN, CONS, 2)
        assert max(abs(v) for v in res) < 1e-9
        assert sum(v * v for v in x) >= best - 1e-12


def test_far_frames_do_not_change():
    src = source()
    motion, _, _ = retarget(src, NEW_LEN, CONS)
    for f in (0, 22, 23):
        assert motion[f] == tuple(src[f])
    assert any(abs(a - b) > 1e-3 for a, b in zip(motion[3], src[3]))


def test_check_value_one_constraint_on_a_straight_leg():
    src = [(0.0, 2.0, 0.0, 0.0)] * 17
    cons = [(8, (0.0, 0.0))]
    big = 1e12
    motion, c, _ = retarget(src, (0.9, 0.9), cons, spacing=2, weights=(1.0, 1.0, big, big))
    count = control_count(17, 2)
    cy = c[count : 2 * count]
    j = 8 // 2 + 1
    for jj, want in ((j - 1, -0.2 / 3), (j, -0.8 / 3), (j + 1, -0.2 / 3)):
        assert abs(cy[jj] - want) < 1e-9
    assert all(abs(v) < 1e-9 for i, v in enumerate(cy) if abs(i - j) > 1)
    for f, want in ((8, -0.2), (10, -0.2 * 8 / 18), (12, -0.2 / 18), (14, 0.0)):
        assert abs((motion[f][1] - 2.0) - want) < 1e-9
        assert abs((motion[16 - f][1] - 2.0) - want) < 1e-9
