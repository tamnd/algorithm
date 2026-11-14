# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/devgan-noise-metric/. The authors are listed in prov/6FQBVC.jsonl.

import math
import random
from fractions import Fraction as F

from devgan_noise_metric import devgan_noise, ramp_slopes
from rc_transient import backward_euler, matrices, ramp_peaks, solve

# The tree of the page: units kOhm, fF, ps and V, so a current is in mA.
PARENT = [-1, 0, 1, 1]
R = [F(1), F(1, 2), F(1, 2), F(1)]
CG = [F(5), F(10), F(10), F(15)]
COUPLING = [[], [(F(10), 0)], [(F(10), 0)], []]


def random_tree(rng, n, aggressors, exact):
    num = (lambda lo, hi: F(rng.randint(lo, hi), rng.randint(1, 4))) if exact else (lambda lo, hi: rng.uniform(lo, hi))
    parent = [-1] + [rng.randrange(k) for k in range(1, n)]
    r = [num(1, 8) for _ in range(n)]
    cg = [num(1, 20) for _ in range(n)]
    coupling = []
    for _ in range(n):
        coupling.append([(num(1, 20), rng.randrange(aggressors)) for _ in range(rng.randint(0, 2))])
    return parent, r, cg, coupling


def test_worked_example():
    v = devgan_noise(PARENT, R, COUPLING, ramp_slopes(F(1), [F(50)]))
    assert v == [F(2, 5), F(3, 5), F(7, 10), F(3, 5)]
    g, cap, b = matrices(PARENT, [float(x) for x in R], [float(x) for x in CG], [[(float(c), a) for c, a in cp] for cp in COUPLING], 1)
    peak = ramp_peaks(g, cap, b, [(0.0, 50.0, 1.0)])
    assert [round(p, 3) for p in peak] == [0.170, 0.260, 0.318, 0.217]


def test_equals_resistance_matrix_product():
    # V = G^-1 B s, solved exactly, is the matrix form of the two passes.
    rng = random.Random(1)
    for _ in range(300):
        n = rng.randint(1, 7)
        parent, r, cg, coupling = random_tree(rng, n, 2, True)
        slope = [F(rng.randint(1, 9), rng.randint(1, 9)) for _ in range(2)]
        g, cap, b = matrices(parent, r, cg, coupling, 2)
        want = solve(g, [sum(b[i][a] * slope[a] for a in range(2)) for i in range(n)])
        assert devgan_noise(parent, r, coupling, slope) == want


def test_common_path_resistance_form():
    # V_i = sum_k R_ik I_k with R_ik the resistance shared by the root paths of i and k.
    rng = random.Random(2)
    for _ in range(200):
        n = rng.randint(1, 8)
        parent, r, cg, coupling = random_tree(rng, n, 1, True)
        path = []
        for k in range(n):
            p = {k} | (path[parent[k]] if k else set())
            path.append(p)
        cur = [sum(c for c, _ in coupling[k]) for k in range(n)]
        want = [sum(sum(r[j] for j in path[i] & path[k]) * cur[k] for k in range(n)) for i in range(n)]
        assert devgan_noise(parent, r, coupling, [F(1)]) == want


def test_backward_euler_never_exceeds_bound_exactly():
    # In exact arithmetic, every backward Euler state satisfies |v_j| <= V.
    rng = random.Random(3)
    for _ in range(25):
        n = rng.randint(1, 3)
        parent, r, cg, coupling = random_tree(rng, n, 2, True)
        rise = [F(rng.randint(1, 30)), F(rng.randint(1, 30))]
        swing = [F(1), F(-1) if rng.random() < 0.5 else F(1)]
        start = [F(0), F(rng.randint(0, 10))]
        waves = [lambda t, a=a: swing[a] * min(max((t - start[a]) / rise[a], F(0)), F(1)) for a in range(2)]
        bound = devgan_noise(parent, r, coupling, [abs(swing[a]) / rise[a] for a in range(2)])
        g, cap, b = matrices(parent, r, cg, coupling, 2)
        h = F(rng.randint(1, 6), 2)
        for v in backward_euler(g, cap, b, waves, h, 24):
            assert all(abs(v[i]) <= bound[i] for i in range(n))


def test_backward_euler_single_rising_aggressor_is_nonnegative():
    rng = random.Random(4)
    for _ in range(20):
        n = rng.randint(1, 3)
        parent, r, cg, coupling = random_tree(rng, n, 1, True)
        rise = F(rng.randint(1, 20))
        bound = devgan_noise(parent, r, coupling, [1 / rise])
        g, cap, b = matrices(parent, r, cg, coupling, 1)
        for v in backward_euler(g, cap, b, [lambda t: min(t / rise, F(1))], F(1), 24):
            assert all(0 <= v[i] <= bound[i] for i in range(n))


def test_one_node_closed_form():
    # One node: peak = s R Cc (1 - exp(-tr / tau)), tau = R (Cg + Cc).
    for rr, cg, cc, tr in [(1.0, 10.0, 10.0, 5.0), (2.0, 3.0, 7.0, 40.0), (0.5, 20.0, 1.0, 300.0)]:
        g, cap, b = matrices([-1], [rr], [cg], [[(cc, 0)]], 1)
        peak = ramp_peaks(g, cap, b, [(0.0, tr, 1.0)])[0]
        metric = devgan_noise([-1], [rr], [[(cc, 0)]], [1.0 / tr])[0]
        tau = rr * (cg + cc)
        assert math.isclose(peak, metric * (1 - math.exp(-tr / tau)), rel_tol=1e-9)
        assert peak <= cc / (cg + cc)  # the charge sharing limit of a step


def test_exact_solution_bound_and_tightness():
    # Exact solution of the linear ODE on random trees: the bound holds,
    # it is loose for fast ramps and tight for slow ones.
    rng = random.Random(1997)
    ratios = {"fast": [], "slow": []}
    for _ in range(80):
        n = rng.randint(1, 5)
        parent, r, cg, coupling = random_tree(rng, n, 2, False)
        g, cap, b = matrices(parent, r, cg, coupling, 2)
        tau = sum(r) * sum(cap)  # at least the slowest time constant
        for kind, tr in (("fast", tau / 50), ("slow", 50 * tau)):
            ramps = [(0.0, tr, 1.0), (rng.uniform(0, tr), tr, -1.0)]
            bound = devgan_noise(parent, r, coupling, [1 / tr, 1 / tr])
            peak = ramp_peaks(g, cap, b, ramps, samples=60)
            for p, v in zip(peak, bound):
                assert p <= v * (1 + 1e-9) + 1e-15
                if v > 0:
                    ratios[kind].append(p / v)
    assert max(ratios["fast"]) < 0.2
    assert max(ratios["slow"]) > 0.95
