# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/maximum-csp/. The authors are listed in prov/75TMKH.jsonl.

import random

from maximum_csp import _cost, brute_force, max_csp_branch_and_bound


def random_csp(rng, n, d, density, tightness):
    doms = [list(range(d)) for _ in range(n)]
    cons, wts = {}, {}
    for i in range(n):
        for j in range(i + 1, n):
            if rng.random() < density:
                cons[(i, j)] = {(a, b) for a in range(d) for b in range(d) if rng.random() >= tightness}
                wts[(i, j)] = rng.randint(1, 4)
    return doms, cons, wts


def test_page_example():
    # A triangle that must get 3 different colors, with only 2 colors.
    doms = [[0, 1]] * 3
    ne = {(0, 1), (1, 0)}
    cons = {(0, 1): ne, (0, 2): ne, (1, 2): ne}
    cost, sol, _ = max_csp_branch_and_bound(doms, cons)
    assert cost == 1 and _cost(sol, cons, {}) == 1
    # With weights 3, 2, 1, the optimum gives up the lightest constraint.
    w = {(0, 1): 3, (0, 2): 2, (1, 2): 1}
    cost, sol, nodes = max_csp_branch_and_bound(doms, cons, w)
    assert (cost, sol, nodes) == (1, [0, 1, 1], 10)
    assert max_csp_branch_and_bound(doms, cons, w, use_ic=False) == (1, [0, 1, 1], 12)


def test_against_brute_force():
    rng = random.Random(1992)
    for _ in range(700):
        n = rng.randint(0, 6)
        d = rng.randint(1, 3)
        doms, cons, wts = random_csp(rng, n, d, rng.random(), rng.random())
        if rng.random() < 0.5:
            wts = {}
        want = brute_force(doms, cons, wts)
        cost, sol, nodes_ic = max_csp_branch_and_bound(doms, cons, wts)
        assert cost == want
        assert _cost(sol, cons, wts) == want
        cost0, sol0, nodes_plain = max_csp_branch_and_bound(doms, cons, wts, use_ic=False)
        assert cost0 == want and _cost(sol0, cons, wts) == want
        # The stronger bound prunes a superset of nodes, and both find the same optimum first.
        assert nodes_ic <= nodes_plain
        assert sol == sol0


def test_edges():
    assert max_csp_branch_and_bound([], {}) == (0, [], 0)
    assert max_csp_branch_and_bound([[0], []], {})[1] is None
    assert brute_force([[0], []], {}) is None
