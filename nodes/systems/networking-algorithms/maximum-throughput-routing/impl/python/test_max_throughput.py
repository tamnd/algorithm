# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/maximum-throughput-routing/. The authors are listed in prov/NC7YNV.jsonl.

import random
from fractions import Fraction

from max_throughput import exact_lp, garg_konemann, max_flow, simplex_max, sparsest_cut_ratio


def instance(rng, n=6, p=0.5, k=3):
    edges, cap = [], []
    for u in range(n):
        for v in range(u + 1, n):
            if rng.random() < p:
                c = rng.randint(1, 4)
                edges += [(u, v), (v, u)]
                cap += [c, c]
    com = []
    for _ in range(200):
        if len(com) == k:
            break
        s, t = rng.sample(range(n), 2)
        if max_flow(n, edges, cap, s, t) > 0:
            com.append((s, t, rng.randint(1, 3)))
    return edges, cap, com


def k23():
    """K_{2,3} with sides {0, 1} and {2, 3, 4}, capacity 1 in each direction."""
    edges, cap = [], []
    for u in (0, 1):
        for v in (2, 3, 4):
            edges += [(u, v), (v, u)]
            cap += [1, 1]
    return edges, cap, [(0, 1, 1), (2, 3, 1), (3, 4, 1), (2, 4, 1)]


def test_simplex_on_a_small_lp():
    # max 3x + 2y, x + y <= 4, x + 3y <= 6, x <= 3: optimum 11 at (3, 1).
    val, x = simplex_max([3, 2], [[1, 1], [1, 3], [1, 0]], [4, 6, 3])
    assert val == 11 and x == [3, 1]


def test_exact_lp_with_one_commodity_is_max_flow_over_demand():
    for seed in range(10):
        rng = random.Random(seed)
        edges, cap, com = instance(rng, k=1)
        (s, t, d), = com
        assert exact_lp(6, edges, cap, com) == Fraction(max_flow(6, edges, cap, s, t), d)


def test_flow_is_at_most_the_sparsest_cut_and_can_be_less():
    for seed in range(10):
        rng = random.Random(seed)
        edges, cap, com = instance(rng)
        assert exact_lp(6, edges, cap, com) <= sparsest_cut_ratio(6, edges, cap, com)
    edges, cap, com = k23()
    assert sparsest_cut_ratio(5, edges, cap, com) == 1
    assert exact_lp(5, edges, cap, com) == Fraction(8, 9)


def check_flow(n, edges, cap, com, flow, routed):
    for e, c in enumerate(cap):
        assert sum(f[e] for f in flow) <= c + 1e-9
    for (s, t, _), f, r in zip(com, flow, routed):
        for v in range(n):
            net = sum(f[e] for e, (a, _) in enumerate(edges) if a == v) - sum(f[e] for e, (_, b) in enumerate(edges) if b == v)
            want = r if v == s else -r if v == t else 0
            assert abs(net - want) < 1e-9


def test_garg_konemann_is_feasible_and_near_optimal():
    eps = 0.1
    cases = [(6, *instance(random.Random(seed))) for seed in range(20)] + [(5, *k23())]
    for n, edges, cap, com in cases:
        opt = exact_lp(n, edges, cap, com)
        lam, flow, routed = garg_konemann(n, edges, cap, com, eps)
        check_flow(n, edges, cap, com, flow, routed)
        assert all(r >= lam * d - 1e-9 for r, (_, _, d) in zip(routed, com))
        assert (1 - eps) ** 3 * opt <= lam <= opt + 1e-9


def test_smaller_eps_gets_closer():
    edges, cap, com = k23()
    opt = float(exact_lp(5, edges, cap, com))
    gaps = [opt - garg_konemann(5, edges, cap, com, eps)[0] for eps in (0.2, 0.1, 0.05)]
    assert gaps[0] > gaps[1] > gaps[2] > 0
