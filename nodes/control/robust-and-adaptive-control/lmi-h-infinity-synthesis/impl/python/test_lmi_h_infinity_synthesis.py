# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lmi-h-infinity-synthesis/. The authors are listed in prov/HWW5GT.jsonl.

import math
import random

import ctlmat as cm
from lmi_h_infinity_synthesis import (
    _value,
    chol,
    closed_loop,
    controller_lmi,
    gamma_lmis,
    is_hurwitz,
    lmi_synthesis,
    null_space,
    optimal_gamma,
    reconstruct_x,
    sdp_center,
    sdp_feasible,
)


def scalar_plant(a):
    # x' = a x + w1 + u, z = (x, u), y = x + w2
    return {"A": [[a]], "B1": [[1, 0]], "B2": [[1]], "C1": [[1], [0]], "C2": [[1]],
            "D11": [[0, 0], [0, 0]], "D12": [[0], [1]], "D21": [[0, 1]]}


SCALAR = {a: scalar_plant(a) for a in (-1, 0, 1, 2)}

PLANT2 = {"A": [[0, 1], [2, -1]], "B1": [[1, 0, 0], [0, 1, 0]], "B2": [[0], [1]],
          "C1": [[1, 0], [0, 1], [0, 0]], "C2": [[1, 0]], "D11": [[0, 0, 0]] * 3,
          "D12": [[0], [0], [1]], "D21": [[0, 0, 1]]}

# Reference: the two-Riccati synthesis page computes gamma_opt for PLANT2 by
# bisection on its three conditions (relative tolerance 1e-9).
PLANT2_GAMMA = 7.2145628072

# A singular problem: z = x has no control weight, so D12 = 0 and the
# two-Riccati method does not apply.
SINGULAR = {"A": [[1]], "B1": [[1, 0]], "B2": [[1]], "C1": [[1]], "C2": [[1]],
            "D11": [[0, 0]], "D12": [[0]], "D21": [[0, 1]]}

FREQS = [10 ** (e / 40) for e in range(-160, 161)] + [0.0]

_CACHE = {}


def opt(p):
    # The SDPs take a moment in pure Python, so each one runs once.
    key = ("opt", id(p))
    if key not in _CACHE:
        _CACHE[key] = optimal_gamma(p)
    return _CACHE[key]


def synth(p):
    key = ("synth", id(p))
    if key not in _CACHE:
        _CACHE[key] = lmi_synthesis(p, gopt=opt(p)[0])
    return _CACHE[key]


def peak(sys):
    a, b, c, d = sys
    n = len(a)
    best = 0.0
    for w in FREQS:
        m = [[(1j * w if i == j else 0.0) - a[i][j] for j in range(n)] for i in range(n)]
        g = cm.add(cm.mul(c, cm.solve(m, [[complex(v) for v in row] for row in b])), d)
        best = max(best, cm.norm2(g))
    return best


def min_pivot(m):
    low = chol(m)
    return 0.0 if low is None else min(low[i][i] for i in range(len(low))) ** 2


def test_ctlmat_self_test():
    assert cm._self_test()


def test_null_space_is_an_orthonormal_kernel_basis():
    rng = random.Random(3)
    for rows, cols in ((1, 3), (2, 5), (3, 4)):
        m = [[rng.uniform(-1, 1) for _ in range(cols)] for _ in range(rows)]
        n = null_space(m)
        k = len(n[0])
        assert k == cols - rows
        assert max(abs(v) for row in cm.mul(m, n) for v in row) < 1e-12
        g = cm.mul(cm.transpose(n), n)
        assert max(abs(g[i][j] - (i == j)) for i in range(k) for j in range(k)) < 1e-12


def test_scalar_optimum_matches_the_closed_form():
    for a, p in SCALAR.items():
        g, r, s = opt(p)
        assert abs(g - (a + math.sqrt(a * a + 2))) < 1e-7 * g
        # At the optimum the coupling constraint is active: R = S = 1.
        assert abs(r[0][0] - 1) < 1e-6 and abs(s[0][0] - 1) < 1e-6


def test_two_state_optimum_matches_the_riccati_method():
    g, _, _ = opt(PLANT2)
    assert abs(g - PLANT2_GAMMA) < 1e-7 * PLANT2_GAMMA


def test_feasible_above_and_infeasible_below_the_optimum():
    for p in (SCALAR[1], PLANT2):
        g = opt(p)[0]
        lmis, x0, _ = gamma_lmis(p, 0.99 * g)
        assert sdp_feasible(lmis, x0) is None
        lmis, x0, _ = gamma_lmis(p, 1.01 * g)
        x = sdp_center(lmis, sdp_feasible(lmis, x0))
        # A certificate: every LMI is positive definite with a clear margin.
        assert all(min_pivot(_value(lmi, x)) > 1e-6 for lmi in lmis)


def test_reconstruction_of_the_closed_loop_lyapunov_matrix():
    p = PLANT2
    lmis, x0, split = gamma_lmis(p, 1.05 * opt(p)[0])
    r, s, _ = split(sdp_center(lmis, sdp_feasible(lmis, x0)))
    xcl = reconstruct_x(r, s)
    n = len(r)
    assert cm.is_pos_def(xcl)
    xi = cm.inv(xcl)
    big = 1 + max(abs(v) for row in r for v in row)
    assert max(abs(xcl[i][j] - s[i][j]) for i in range(n) for j in range(n)) < 1e-12
    assert max(abs(xi[i][j] - r[i][j]) for i in range(n) for j in range(n)) < 1e-8 * big


def test_controllers_meet_the_bound():
    for p in (SCALAR[0], SCALAR[1], PLANT2):
        gopt, g, k, xcl = synth(p)
        cl = closed_loop(p, k)
        assert is_hurwitz(cl[0])
        pk = peak(cl)
        assert gopt * (1 - 1e-4) <= pk < g


def test_controller_lmi_is_infeasible_below_the_level():
    # With X_cl fixed, the bounded real LMI in Omega has no solution at a
    # level below gamma_opt, since a solution would give a better controller.
    p = SCALAR[1]
    gopt, g, k, xcl = synth(p)
    assert controller_lmi(p, xcl, 0.98 * gopt) is None


def test_singular_problem():
    # For any stabilizing K, the map from w2 to z equals -1 at s = 1, the
    # unstable pole, so gamma_opt >= 1 by the maximum modulus principle.
    g, r, s = opt(SINGULAR)
    assert 1.0 <= g < 1.01
    gopt, gk, k, _ = synth(SINGULAR)
    cl = closed_loop(SINGULAR, k)
    assert is_hurwitz(cl[0])
    assert 1.0 - 1e-6 <= peak(cl) < gk
