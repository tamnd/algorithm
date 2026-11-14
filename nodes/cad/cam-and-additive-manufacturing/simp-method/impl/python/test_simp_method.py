# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/simp-method/. The authors are listed in prov/KDKEWF.jsonl.

import itertools
import random
from fractions import Fraction as F

from fem2d import dense_solve, element_dofs, element_energies, node, q4_stiffness, solve
from simp_method import compliance, filter_sensitivities, filter_weights, oc_update, simp

KE = [[float(v) for v in row] for row in q4_stiffness(F(3, 10))]


def cantilever(nelx, nely):
    """Left edge clamped, unit load down at the bottom right node."""
    force = {2 * node(nely, nelx, 0) + 1: -1.0}
    fixed = [k for j in range(nely + 1) for k in (2 * node(nely, 0, j), 2 * node(nely, 0, j) + 1)]
    return force, fixed


def checkerboards(x, nelx, nely):
    count = 0
    for ex in range(nelx - 1):
        for ey in range(nely - 1):
            a, b = x[ex * nely + ey] > 0.5, x[(ex + 1) * nely + ey] > 0.5
            c, d = x[ex * nely + ey + 1] > 0.5, x[(ex + 1) * nely + ey + 1] > 0.5
            count += a == d and b == c and a != b
    return count


def test_element_stiffness_matches_sigmund():
    nu = F(3, 10)
    k = [F(1, 2) - nu / 6, F(1, 8) + nu / 8, -F(1, 4) - nu / 12, -F(1, 8) + 3 * nu / 8,
         -F(1, 4) + nu / 12, -F(1, 8) - nu / 8, nu / 6, F(1, 8) - 3 * nu / 8]
    idx = [[0, 1, 2, 3, 4, 5, 6, 7], [1, 0, 7, 6, 5, 4, 3, 2], [2, 7, 0, 5, 6, 3, 4, 1], [3, 6, 5, 0, 7, 2, 1, 4],
           [4, 5, 6, 7, 0, 1, 2, 3], [5, 4, 3, 2, 1, 0, 7, 6], [6, 3, 4, 1, 2, 7, 0, 5], [7, 2, 1, 4, 3, 6, 5, 0]]
    assert q4_stiffness(nu) == [[k[idx[i][j]] / (1 - nu * nu) for j in range(8)] for i in range(8)]
    assert q4_stiffness(nu)[0][0] == F(45, 91)


def test_banded_solver_against_dense_elimination():
    rng = random.Random(1)
    ke = q4_stiffness(F(1, 4))
    for nelx, nely in [(2, 1), (3, 2), (2, 3)]:
        scale = [F(rng.randint(1, 9), rng.randint(1, 4)) for _ in range(nelx * nely)]
        force, fixed = cantilever(nelx, nely)
        force = {k: F(rng.randint(-5, 5)) for k in range(2 * (nelx + 1) * (nely + 1)) if k not in fixed}
        u = solve(nelx, nely, ke, scale, force, fixed)
        ndof = 2 * (nelx + 1) * (nely + 1)
        big = [[F(0)] * ndof for _ in range(ndof)]
        for e, dofs in enumerate(element_dofs(nelx, nely)):
            for p in range(8):
                for q in range(8):
                    big[dofs[p]][dofs[q]] += scale[e] * ke[p][q]
        free = [k for k in range(ndof) if k not in set(fixed)]
        ref = dense_solve([[big[i][j] for j in free] for i in free], [force.get(i, F(0)) for i in free])
        assert [u[k] for k in free] == ref  # exact equality in Fraction
        assert all(u[k] == 0 for k in fixed)


def test_patch_test_uniform_tension():
    # Plane stress bar under the stress sigma_x = 1: u_x = x, u_y = -nu y for E = 1.
    nu = F(1, 3)
    ke = q4_stiffness(nu)
    nelx, nely = 3, 2
    force = {}
    for j in range(nely + 1):  # consistent nodal forces of a unit traction on the right edge
        force[2 * node(nely, nelx, j)] = F(1, 2) if j in (0, nely) else F(1)
    fixed = [2 * node(nely, 0, j) for j in range(nely + 1)] + [1]  # u_x = 0 at x = 0, u_y = 0 at the origin
    u = solve(nelx, nely, ke, [F(1)] * (nelx * nely), force, fixed)
    for i in range(nelx + 1):
        for j in range(nely + 1):
            n = node(nely, i, j)
            assert (u[2 * n], u[2 * n + 1]) == (F(i), -nu * j)


def test_sensitivity_against_finite_differences():
    rng = random.Random(2)
    nelx, nely, p = 4, 3, 3
    force, fixed = cantilever(nelx, nely)
    x = [rng.uniform(0.3, 1.0) for _ in range(nelx * nely)]
    c, u = compliance(nelx, nely, KE, x, p, force, fixed)
    energy = element_energies(nelx, nely, KE, u)
    assert abs(c - sum(xi ** p * en for xi, en in zip(x, energy))) < 1e-9 * c  # c = f.u = u^T K u
    h = 1e-6
    for e in range(nelx * nely):
        xp, xm = list(x), list(x)
        xp[e] += h
        xm[e] -= h
        fd = (compliance(nelx, nely, KE, xp, p, force, fixed)[0] - compliance(nelx, nely, KE, xm, p, force, fixed)[0]) / (2 * h)
        assert abs(fd - (-p * x[e] ** (p - 1) * energy[e])) < 1e-5 * abs(fd)


def test_filter_keeps_uniform_fields_and_identity_for_small_radius():
    w = filter_weights(5, 4, 1.5)
    x = [0.4] * 20
    assert all(abs(v + 2.0) < 1e-12 for v in filter_sensitivities(w, x, [-2.0] * 20))
    rng = random.Random(3)
    dc = [-rng.random() for _ in range(20)]
    xs = [rng.uniform(0.1, 1) for _ in range(20)]
    assert all(abs(a - b) < 1e-12 for a, b in zip(filter_sensitivities(filter_weights(5, 4, 0.9), xs, dc), dc))


def test_oc_update_meets_the_volume_bound_and_stops():
    rng = random.Random(4)
    for scale in (1e-6, 1.0, 1e6):
        for _ in range(50):
            n = rng.randint(2, 30)
            x = [rng.uniform(1e-3, 1.0) for _ in range(n)]
            volfrac = rng.uniform(sum(x) / n, 1.0)  # the old design is feasible
            dc = [-scale * rng.random() for _ in range(n)]
            xnew = oc_update(x, dc, volfrac)
            assert sum(xnew) <= volfrac * n * (1 + 1e-12)
            assert all(max(1e-3, a - 0.2) - 1e-12 <= b <= min(1.0, a + 0.2) + 1e-12 for a, b in zip(x, xnew))
            # brute force on the multiplier: a slightly smaller lam breaks the bound,
            # unless every element is already at its upper move limit
            upper = sum(min(1.0, a + 0.2) for a in x)
            if upper > volfrac * n * (1 + 1e-6):
                assert sum(xnew) > volfrac * n * (1 - 1e-6)
    # zero sensitivities: every lam is feasible, the loop still stops
    x = [0.5] * 4
    assert oc_update(x, [0.0] * 4, 0.9) == [0.3] * 4


def test_oc_on_a_bar_gives_densities_proportional_to_force():
    # A bar of 6 elements in series, clamped at the left, with loads at the nodes.
    # With p = 1, c = sum N_e^2 / x_e and the optimum is x_e = V |N_e| / sum |N|.
    loads = [1.0, 2.0, 0.5, 1.0, 3.0, 1.5]
    normal = [sum(loads[e:]) for e in range(6)]
    volfrac = 0.4
    x = [volfrac] * 6
    for _ in range(80):
        dc = [-(n * n) / (xe * xe) for n, xe in zip(normal, x)]
        x = oc_update(x, dc, volfrac, move=0.2, xmin=1e-3)
    want = [volfrac * 6 * n / sum(normal) for n in normal]
    assert all(abs(a - b) < 1e-6 for a, b in zip(x, want))


def test_p1_is_a_lower_bound_and_brute_force_on_5x2():
    nelx, nely, xmin = 5, 2, 1e-3
    force, fixed = cantilever(nelx, nely)
    best = None
    for solid in itertools.combinations(range(10), 5):  # all 252 designs with 5 solid elements
        x = [1.0 if e in solid else xmin for e in range(10)]
        c = compliance(nelx, nely, KE, x, 3, force, fixed)[0]
        best = c if best is None else min(best, c)
    assert abs(best - 347.3777) < 1e-3  # the bottom row of 5 elements
    volfrac = (5 + 5 * xmin) / 10  # the same volume as a 0/1 design
    x1, h1 = simp(nelx, nely, volfrac, p=1, rmin=0.9, force=force, fixed=fixed, maxit=300, tol=1e-6)
    assert h1[-1] <= best  # p = 1 is convex, so its optimum is below every 0/1 design
    _, u = compliance(nelx, nely, KE, x1, 1, force, fixed)
    energy = element_energies(nelx, nely, KE, u)
    inner = [en for xe, en in zip(x1, energy) if 0.01 < xe < 0.99]
    assert max(inner) - min(inner) < 1e-4 * max(inner)  # KKT: equal energy where xmin < x < 1
    x3, h3 = simp(nelx, nely, volfrac, p=3, rmin=1.5, force=force, fixed=fixed, maxit=300, tol=1e-4)
    # x^3 <= x, so the p = 3 compliance of x3 is at least its p = 1 compliance, which is at least h1.
    assert h1[-1] <= h3[-1] * (1 + 1e-9)
    assert 1.0 < h3[-1] / best < 1.3  # measured: about 388 against 347, a local optimum with gray elements


def test_mbb_beam_filter_removes_checkerboards():
    nelx, nely, volfrac = 30, 10, 0.5
    x0, h0 = simp(nelx, nely, volfrac, rmin=0.9, maxit=100)
    x1, h1 = simp(nelx, nely, volfrac, rmin=1.5, maxit=100)
    for x, h in ((x0, h0), (x1, h1)):
        assert sum(x) <= volfrac * nelx * nely + 1e-6
        assert h[-1] < 0.3 * h[0]
    assert checkerboards(x0, nelx, nely) > 20  # measured 51 without the filter
    assert checkerboards(x1, nelx, nely) == 0
