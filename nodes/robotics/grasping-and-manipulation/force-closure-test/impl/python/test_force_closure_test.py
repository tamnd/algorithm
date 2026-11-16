# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/force-closure-test/. The authors are listed in prov/ZZXTNV.jsonl.

import itertools
import math
import random
from fractions import Fraction as Q

from force_closure_test import (FRICTIONLESS, HARD, SOFT, cone_edges,
                                force_closure, force_closure_of_wrenches,
                                phase_one, primitive_wrenches, rank)


# Reference method, independent of the linear program. If the wrenches span
# R^d, they are not force closure exactly when some u != 0 has u . w >= 0 for
# every wrench w. That cone of u is then pointed, so it has an extreme ray,
# and an extreme ray is orthogonal to d - 1 linearly independent wrenches.
# The reference tries every such set of d - 1 wrenches.

def _null_vector(rows, d):
    M = [list(r) for r in rows]
    pivots = []
    r = 0
    for c in range(d):
        p = next((i for i in range(r, len(M)) if M[i][c] != 0), None)
        if p is None:
            continue
        M[r], M[p] = M[p], M[r]
        M[r] = [v / M[r][c] for v in M[r]]
        for i in range(len(M)):
            if i != r and M[i][c] != 0:
                f = M[i][c]
                M[i] = [a - f * b for a, b in zip(M[i], M[r])]
        pivots.append(c)
        r += 1
    if r != d - 1:
        return None
    free = next(c for c in range(d) if c not in pivots)
    u = [Q(0)] * d
    u[free] = Q(1)
    for i, c in enumerate(pivots):
        u[c] = -M[i][free]
    return u


def brute_force_closure(W):
    d = len(W[0])
    if rank(W) < d:
        return False
    for S in itertools.combinations(W, d - 1):
        u = _null_vector(S, d)
        if u is None:
            continue
        dots = [sum(a * b for a, b in zip(u, w)) for w in W]
        if all(x >= 0 for x in dots) or all(x <= 0 for x in dots):
            return False
    return True


def check_certificate(W, k):
    assert len(k) == len(W)
    assert all(v >= 1 for v in k)
    d = len(W[0])
    for i in range(d):
        assert sum(k[j] * W[j][i] for j in range(len(W))) == 0


def run(W):
    closed, k = force_closure_of_wrenches(W)
    if closed:
        check_certificate(W, k)
    else:
        assert k is None
    return closed


def rational_unit(rng):
    # A rational point on the unit circle.
    t = Q(rng.randint(-9, 9), rng.randint(1, 9))
    return ((1 - t * t) / (1 + t * t), 2 * t / (1 + t * t))


# Hand cases with known answers.

SQUARE = [((-1, Q(1, 2)), (1, 0)), ((1, Q(-1, 5)), (-1, 0)),
          ((Q(3, 10), -1), (0, 1)), ((Q(-2, 5), 1), (0, -1))]

CUBE7 = [((1, 0, Q(-1, 2)), (-1, 0, 0)), ((-1, Q(-1, 2), 0), (1, 0, 0)),
         ((Q(1, 2), 1, 0), (0, -1, 0)), ((0, -1, 0), (0, 1, 0)),
         ((Q(-1, 2), 0, 1), (0, 0, -1)), ((0, Q(-1, 2), -1), (0, 0, 1)),
         ((0, Q(1, 2), -1), (0, 0, 1))]


def test_square_form_closure():
    W = primitive_wrenches(SQUARE, model=FRICTIONLESS)
    assert W == [[Q(-1, 2), 1, 0], [Q(-1, 5), -1, 0],
                 [Q(3, 10), 0, 1], [Q(2, 5), 0, -1]]
    closed, k = force_closure(SQUARE, model=FRICTIONLESS)
    assert closed and k == [1, 1, 1, 1]
    assert brute_force_closure(W)


def test_pinwheel_is_not_closed():
    # Every contact gives the moment -1/2, so no combination cancels it.
    pin = [((-1, Q(1, 2)), (1, 0)), ((1, Q(-1, 2)), (-1, 0)),
           ((Q(1, 2), 1), (0, -1)), ((Q(-1, 2), -1), (0, 1))]
    W = primitive_wrenches(pin, model=FRICTIONLESS)
    assert all(w[0] == Q(-1, 2) for w in W)
    assert rank(W) == 3
    assert force_closure(pin, model=FRICTIONLESS) == (False, None)
    assert not brute_force_closure(W)


def test_lynch_park_example():
    # The columns of F = [[0,0,-1,2],[-1,0,1,0],[0,-1,0,1]].
    W = [[0, -1, 0], [0, 0, -1], [-1, 1, 0], [2, 0, 1]]
    W = [[Q(v) for v in w] for w in W]
    assert run(W)
    assert force_closure_of_wrenches(W)[1] == [2, 1, 2, 1]


def test_planar_antipodal():
    anti = [((-1, 0), (1, 0)), ((1, 0), (-1, 0))]
    for mu in (Q(1, 2), Q(1, 100), Q(3)):
        closed, k = force_closure(anti, mu)
        assert closed
        check_certificate(primitive_wrenches(anti, mu), k)
    assert force_closure(anti, 0) == (False, None)
    # Contacts off the common normal line: closed only if mu is large enough.
    off = [((-1, Q(1, 2)), (1, 0)), ((1, Q(-1, 2)), (-1, 0))]
    assert not force_closure(off, Q(1, 3))[0]
    assert not force_closure(off, Q(1, 2))[0]   # the line is on the cone edge
    assert force_closure(off, Q(3, 5))[0]


def test_disc_is_never_in_form_closure():
    rng = random.Random(11)
    for _ in range(30):
        c = rng.randint(1, 8)
        contacts = []
        for _ in range(c):
            x, y = rational_unit(rng)
            contacts.append(((x, y), (-x, -y)))
        W = primitive_wrenches(contacts, model=FRICTIONLESS)
        assert all(w[0] == 0 for w in W)
        assert not run(W)


def test_seven_contacts_on_a_cube():
    W = primitive_wrenches(CUBE7, model=FRICTIONLESS)
    closed, k = force_closure_of_wrenches(W)
    assert closed
    check_certificate(W, k)
    assert brute_force_closure(W)
    # Six of them are never enough.
    for i in range(7):
        assert not run(W[:i] + W[i + 1:])


def test_six_frictionless_contacts_are_never_enough():
    rng = random.Random(3)
    for _ in range(40):
        W = [[Q(rng.randint(-3, 3)) for _ in range(6)] for _ in range(6)]
        assert not run(W)


def test_spatial_two_and_three_fingers():
    a3 = [((-1, 0, 0), (1, 0, 0)), ((1, 0, 0), (-1, 0, 0))]
    W = primitive_wrenches(a3, Q(1, 2), 4)
    assert rank(W) == 5          # no moment about the line of the contacts
    assert not run(W)
    W = primitive_wrenches(a3, Q(1, 2), 4, SOFT, Q(1, 10))
    assert len(W) == 16 and run(W)
    three = [((-1, 0, 0), (1, 0, 0)), ((1, Q(1, 2), 0), (-1, 0, 0)),
             ((1, Q(-1, 2), 0), (-1, 0, 0))]
    W = primitive_wrenches(three, Q(1, 2), 4, HARD)
    assert run(W) and brute_force_closure(W)


def test_cone_edges_lie_on_the_cone():
    rng = random.Random(5)
    for _ in range(20):
        n = rational_unit(rng)
        mu = Q(rng.randint(1, 9), 4)
        for e in cone_edges(n, mu):
            normal = e[0] * n[0] + e[1] * n[1]
            tangent = -e[0] * n[1] + e[1] * n[0]
            assert normal == 1 and abs(tangent) == mu
    for k in (3, 4, 5, 8):
        for n in ((0, 0, 1), (0.6, 0.0, 0.8), (1 / math.sqrt(3),) * 3):
            for e in cone_edges(n, 0.5, k):
                fn = sum(e[i] * n[i] for i in range(3))
                ft = math.sqrt(sum((e[i] - fn * n[i]) ** 2 for i in range(3)))
                assert abs(fn - 1) < 1e-12 and abs(ft - 0.5) < 1e-12


def test_random_planar_wrenches_against_brute_force():
    rng = random.Random(7)
    seen = set()
    for _ in range(150):
        N = rng.randint(2, 7)
        W = [[Q(rng.randint(-2, 2)) for _ in range(3)] for _ in range(N)]
        got = run(W)
        assert got == brute_force_closure(W)
        seen.add(got)
    assert seen == {True, False}


def test_random_planar_grasps_against_brute_force():
    rng = random.Random(8)
    seen = set()
    for _ in range(80):
        c = rng.randint(2, 4)
        contacts = []
        for _ in range(c):
            x, y = rational_unit(rng)
            r = Q(rng.randint(1, 4), 2)
            dx, dy = rational_unit(rng)
            # A point on a ray from the center and a normal that points in.
            p = (r * x, r * y)
            n = (dx, dy) if dx * x + dy * y < 0 else (-dx, -dy)
            contacts.append((p, n))
        mu = Q(rng.randint(0, 4), 4)
        W = primitive_wrenches(contacts, mu)
        got = run(W)
        assert got == brute_force_closure(W)
        assert force_closure(contacts, mu)[0] == got
        seen.add(got)
    assert seen == {True, False}


def test_random_spatial_wrenches_against_brute_force():
    rng = random.Random(9)
    seen = set()
    for _ in range(40):
        N = rng.randint(6, 9)
        W = [[Q(rng.randint(-2, 2)) for _ in range(6)] for _ in range(N)]
        got = run(W)
        assert got == brute_force_closure(W)
        seen.add(got)
    assert seen == {True, False}


def test_finer_cone_keeps_closure():
    # The 2k-edge pyramid contains the k-edge pyramid, so closure persists.
    rng = random.Random(10)
    for _ in range(12):
        contacts = []
        for _ in range(3):
            ax = rng.randrange(3)
            s = rng.choice((1, -1))
            p = [Q(rng.randint(-2, 2), 2) for _ in range(3)]
            p[ax] = Q(s)
            n = [0, 0, 0]
            n[ax] = -s
            contacts.append((tuple(p), tuple(n)))
        mu = Q(rng.randint(1, 4), 4)
        if force_closure(contacts, mu, 4)[0]:
            assert force_closure(contacts, mu, 8)[0]


def test_phase_one_feasible_and_infeasible():
    rng = random.Random(12)
    for _ in range(60):
        m = rng.randint(1, 4)
        nv = rng.randint(1, 6)
        A = [[Q(rng.randint(-3, 3)) for _ in range(nv)] for _ in range(m)]
        y0 = [Q(rng.randint(0, 3)) for _ in range(nv)]
        b = [sum(A[i][j] * y0[j] for j in range(nv)) for i in range(m)]
        y = phase_one(A, b)
        assert y is not None and all(v >= 0 for v in y)
        assert [sum(A[i][j] * y[j] for j in range(nv)) for i in range(m)] == b
    # All entries positive and a negative right side: no y >= 0 exists.
    assert phase_one([[1, 2], [3, 1]], [-1, 2]) is None
    assert phase_one([[1, -1], [-1, 1]], [1, 1]) is None


def test_rank():
    assert rank([[1, 2], [2, 4]]) == 1
    assert rank([[0, 0], [0, 0]]) == 0
    assert rank([[1, 0, 0], [0, 1, 0], [1, 1, 0]]) == 2
    assert rank([]) == 0
