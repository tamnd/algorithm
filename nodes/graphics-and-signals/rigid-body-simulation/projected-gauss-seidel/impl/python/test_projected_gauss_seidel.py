# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/projected-gauss-seidel/. The authors are listed in prov/MA63NH.jsonl.

import itertools
import random
from fractions import Fraction as F

from projected_gauss_seidel import (INF, Body, Row, assemble, clamp, ground, objective, pgs, residual,
                                    row_velocity, sequential_impulses, violation)


def box_scene(v, w, xs):
    """A 2D box (mass 1, sides 2 and 1, I = 5/12) on the ground, with contacts at the bottom offsets xs."""
    bodies = [Body(F(1), F(5, 12), v, w), ground()]
    rows = [Row(0, 1, (F(x), F(-1, 2)), (0, 0), (0, 1)) for x in xs]
    return bodies, rows


def solve(M, rhs):
    n = len(rhs)
    aug = [list(M[i]) + [rhs[i]] for i in range(n)]
    for c in range(n):
        p = next((r for r in range(c, n) if aug[r][c] != 0), None)
        if p is None:
            return None
        aug[c], aug[p] = aug[p], aug[c]
        for r in range(n):
            if r != c and aug[r][c] != 0:
                fac = aug[r][c] / aug[c][c]
                aug[r] = [x - fac * y for x, y in zip(aug[r], aug[c])]
    return [aug[i][n] / aug[i][i] for i in range(n)]


def brute_force(A, b, bounds):
    """All solutions of the box problem with fixed bounds, over the 3^n choices lo / hi / free."""
    n = len(b)
    out = []
    for pattern in itertools.product(("lo", "hi", "free"), repeat=n):
        if any((p == "lo" and bounds[i][0] == -INF) or (p == "hi" and bounds[i][1] == INF)
               for i, p in enumerate(pattern)):
            continue
        lam = [F(0)] * n
        for i, p in enumerate(pattern):
            if p != "free":
                lam[i] = F(bounds[i][0] if p == "lo" else bounds[i][1])
        free = [i for i, p in enumerate(pattern) if p == "free"]
        if free:
            x = solve([[A[i][j] for j in free] for i in free],
                      [-b[i] - sum(A[i][j] * lam[j] for j in range(n) if j not in free) for i in free])
            if x is None:
                continue
            for i, xi in zip(free, x):
                lam[i] = xi
        if violation(A, b, bounds, lam) == 0:
            out.append(lam)
    return out


def test_page_example_two_corners_error_factor():
    bodies, rows = box_scene((0, -1), 0, [-1, 1])
    A, b = assemble(bodies, rows, [0, 0])
    assert A == [[F(17, 5), F(-7, 5)], [F(-7, 5), F(17, 5)]] and b == [-1, -1]
    trace = []
    pgs(A, b, [(0, INF)] * 2, 6, trace=trace)
    assert trace[0] == [F(5, 17), F(120, 289)]
    assert trace[1] == [F(2285, 4913), F(40560, 83521)]
    err = [[x - F(1, 2) for x in lam] for lam in trace]
    assert err[0] == [F(-7, 34), F(-49, 578)]
    for k in range(1, 6):
        assert err[k] == [F(49, 289) * x for x in err[k - 1]]
    # the box after one sweep: v_y and the angular velocity of the collision-impulse page
    lam = trace[0]
    assert sum(lam) - 1 == F(-84, 289)
    assert (lam[1] - lam[0]) * F(12, 5) == F(84, 289)


def test_warm_start_at_the_solution_is_a_fixed_point():
    bodies, rows = box_scene((0, -1), 0, [-1, 1])
    A, b = assemble(bodies, rows, [0, 0])
    assert pgs(A, b, [(0, INF)] * 2, 1, lam0=[F(1, 2), F(1, 2)]) == [F(1, 2), F(1, 2)]


def test_tipping_box_clamp_the_total_not_the_increment():
    bodies, rows = box_scene((0, -10), -36, [-1, 0, 1])
    A, b = assemble(bodies, rows, [0, 0, 0])
    assert b == [26, -10, -46]
    trace = []
    lam = pgs(A, b, [(0, INF)] * 3, 3, trace=trace)
    assert trace == [[0, 10, F(180, 17)], [0, 0, F(230, 17)], [0, 0, F(230, 17)]]
    assert residual(A, b, lam) == [F(120, 17), F(60, 17), 0]
    # the wrong variant: clamp each increment at zero, so an impulse can never decrease
    bad = [F(0)] * 3
    for _ in range(50):
        for i in range(3):
            r = residual(A, b, bad)[i]
            bad[i] += max(-r / A[i][i], 0)
    assert bad == [0, 10, F(180, 17)]
    w = residual(A, b, bad)
    assert w == [F(360, 17), F(180, 17), 0]
    assert bad[1] * w[1] > 0  # the middle contact pushes while it separates


def test_spd_fixed_bounds_matches_brute_force():
    rng = random.Random(11)
    for _ in range(60):
        n = rng.randint(1, 4)
        G = [[F(rng.randint(-4, 4), rng.randint(1, 2)) for _ in range(n + 1)] for _ in range(n)]
        A = [[sum(x * y for x, y in zip(G[i], G[j])) + (1 if i == j else 0) for j in range(n)] for i in range(n)]
        b = [F(rng.randint(-8, 8), rng.randint(1, 3)) for _ in range(n)]
        bounds = []
        for _ in range(n):
            kind = rng.randint(0, 2)
            if kind == 0:
                bounds.append((0, INF))
            elif kind == 1:
                bounds.append((-INF, INF))
            else:
                lo = F(rng.randint(-3, 1))
                bounds.append((lo, lo + rng.randint(1, 3)))
        sols = sorted({tuple(s) for s in brute_force(A, b, bounds)})
        assert len(sols) == 1  # one solution, found by several patterns when it is degenerate
        Af = [[float(x) for x in row] for row in A]
        lam = pgs(Af, [float(x) for x in b], bounds, 400)
        assert max(abs(x - float(y)) for x, y in zip(lam, sols[0])) < 1e-9


def test_each_sweep_lowers_the_objective_by_the_proved_amount():
    rng = random.Random(13)
    for _ in range(40):
        n = rng.randint(1, 5)
        G = [[F(rng.randint(-4, 4), rng.randint(1, 2)) for _ in range(n)] for _ in range(n)]
        A = [[sum(x * y for x, y in zip(G[i], G[j])) + F(1, 4) * (i == j) for j in range(n)] for i in range(n)]
        b = [F(rng.randint(-8, 8), rng.randint(1, 3)) for _ in range(n)]
        bounds = [(F(rng.randint(-2, 0)), F(rng.randint(1, 3))) for _ in range(n)]
        lam = [clamp(F(rng.randint(-3, 3)), lo, hi) for lo, hi in bounds]
        for _ in range(4):
            new = pgs(A, b, bounds, 1, lam0=lam)
            drop = objective(A, b, lam) - objective(A, b, new)
            assert drop >= sum(A[i][i] * (new[i] - lam[i]) ** 2 for i in range(n)) / 2
            lam = new


def test_redundant_contacts_give_unique_velocities():
    rng = random.Random(17)
    xs = [-1, F(-1, 3), F(1, 3), 1]
    for _ in range(10):
        v, w = (0, F(rng.randint(-20, -1), 4)), F(rng.randint(-8, 8), 4)
        bodies, rows = box_scene(v, w, xs)
        A, b = assemble(bodies, rows, [0] * 4)
        Af, bf = [[float(x) for x in r] for r in A], [float(x) for x in b]
        bounds = [(0, INF)] * 4
        lam = pgs(Af, bf, bounds, 3000)
        assert violation(Af, bf, bounds, lam) < 1e-9
        perm = [3, 1, 0, 2]
        lam_p = pgs([[Af[i][j] for j in perm] for i in perm], [bf[i] for i in perm], bounds, 3000)
        w1 = residual(Af, bf, lam)
        w2 = residual([[Af[i][j] for j in perm] for i in perm], [bf[i] for i in perm], lam_p)
        assert max(abs(w1[perm[k]] - w2[k]) for k in range(4)) < 1e-8


def random_scene(rng):
    dirs = [(F(3, 5), F(4, 5)), (F(0), F(1)), (F(1), F(0)), (F(-4, 5), F(3, 5)), (F(5, 13), F(12, 13))]
    nb = rng.randint(1, 3)
    params = [(F(rng.randint(1, 4)), F(rng.randint(1, 6), 3),
               (F(rng.randint(-4, 4), 2), F(rng.randint(-4, 4), 2)), F(rng.randint(-4, 4), 3)) for _ in range(nb)]
    contacts = []
    for _ in range(rng.randint(1, 3)):
        a = rng.randrange(nb)
        b = rng.choice([x for x in range(nb + 1) if x != a])
        n = rng.choice(dirs)
        t = (n[1], -n[0])
        ra = (F(rng.randint(-3, 3), 2), F(rng.randint(-3, 3), 2))
        rb = (F(rng.randint(-3, 3), 2), F(rng.randint(-3, 3), 2))
        contacts.append((a, b, ra, rb, n, t, F(rng.randint(1, 8), 8)))
    return params, contacts


def build(params, contacts):
    bodies = [Body(m, I, v, w) for m, I, v, w in params] + [ground()]
    rows, bounds = [], []
    for a, b, ra, rb, n, t, mu in contacts:
        k = len(rows)
        rows.append(Row(a, b, ra, rb, n))
        bounds.append((0, INF))
        rows.append(Row(a, b, ra, rb, t))
        bounds.append(("friction", k, mu))
    return bodies, rows, bounds


def test_sequential_impulses_equal_matrix_pgs_exactly():
    rng = random.Random(19)
    for trial in range(40):
        params, contacts = random_scene(rng)
        bodies, rows, bounds = build(params, contacts)
        bias = [F(rng.randint(-2, 2), 4) if k % 2 == 0 else 0 for k in range(len(rows))]
        A, b = assemble(bodies, rows, bias)
        lam0 = None if trial % 2 == 0 else [F(rng.randint(0, 3), 4) if k % 2 == 0 else 0 for k in range(len(rows))]
        lam_matrix = pgs(A, b, bounds, 3, lam0=lam0)
        lam_free = sequential_impulses(bodies, rows, bias, bounds, 3, lam0=lam0)
        assert lam_free == lam_matrix
        # the body velocities of the matrix-free route give w = A lam + b
        assert [row_velocity(rows[i], bodies) + bias[i] for i in range(len(rows))] == residual(A, b, lam_matrix)


def test_sequential_impulses_float_route_agrees():
    rng = random.Random(23)
    for _ in range(20):
        params, contacts = random_scene(rng)
        fparams = [(float(m), float(I), (float(v[0]), float(v[1])), float(w)) for m, I, v, w in params]
        fcontacts = [(a, b, tuple(map(float, ra)), tuple(map(float, rb)), tuple(map(float, n)), tuple(map(float, t)),
                      float(mu)) for a, b, ra, rb, n, t, mu in contacts]
        bodies, rows, bounds = build(fparams, fcontacts)
        bias = [0.0] * len(rows)
        A, b = assemble(bodies, rows, bias)
        lam_matrix = pgs(A, b, bounds, 40)
        lam_free = sequential_impulses(bodies, rows, bias, bounds, 40)
        assert max(abs(x - y) for x, y in zip(lam_matrix, lam_free)) < 1e-12


def test_sliding_and_sticking_box():
    for mu, sticks in ((F(2), True), (F(1, 10), False)):
        bodies = [Body(F(1), F(5, 12), (1.0, -1.0), 0.0), ground()]
        rows, bounds = [], []
        for x in (-1.0, 1.0):
            k = len(rows)
            rows.append(Row(0, 1, (x, -0.5), (0, 0), (0, 1)))
            bounds.append((0, INF))
            rows.append(Row(0, 1, (x, -0.5), (0, 0), (1, 0)))
            bounds.append(("friction", k, float(mu)))
        A, b = assemble(bodies, rows, [0.0] * 4)
        lam = pgs(A, b, bounds, 500)
        assert violation(A, b, bounds, lam) < 1e-10
        w = residual(A, b, lam)
        if sticks:
            assert abs(w[1]) < 1e-10 and abs(w[3]) < 1e-10
        else:
            assert abs(lam[1] + float(mu) * lam[0]) < 1e-10 and abs(lam[3] + float(mu) * lam[2]) < 1e-10
            assert w[1] > 0 and w[3] > 0
