# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/heap-fpga-placement/. The authors are listed in prov/5EREMJ.jsonl.

import math
import random
from fractions import Fraction

from heap_fpga_placement import (
    build_system,
    conjugate_gradient,
    exhaustive_min_hpwl,
    heap_place,
    hpwl,
    solve_quadratic,
    spread,
)

PAGE_COLS = ["L", "M", "L"]
PAGE_TYPES = ["L", "L", "L", "M"]
PAGE_PADS = [(-1, 0.5), (3, 0.5)]
PAGE_NETS = [
    [("p", 0), ("b", 0)],
    [("b", 0), ("b", 3)],
    [("b", 3), ("b", 1)],
    [("b", 1), ("p", 1)],
    [("b", 2), ("b", 3)],
]


def random_instance(rng, nx, ny, col_type, counts, n_pads, n_nets):
    types = [t for t, c in counts.items() for _ in range(c)]
    n = len(types)
    pads = [(rng.choice([-1, nx]), rng.uniform(0, ny - 1)) for _ in range(n_pads)]
    nets = []
    for _ in range(n_nets):
        terms = [("b", i) for i in rng.sample(range(n), min(rng.randint(2, 4), n))]
        if n_pads and rng.random() < 0.4:
            terms.append(("p", rng.randrange(n_pads)))
        nets.append(terms)
    return types, pads, nets


def gauss_solve(a, b):
    """Exact dense Gaussian elimination over the rationals, the reference for conjugate gradients."""
    n = len(b)
    m = [[Fraction(a[i].get(j, 0.0)) for j in range(n)] + [Fraction(b[i])] for i in range(n)]
    for c in range(n):
        p = next(r for r in range(c, n) if m[r][c] != 0)
        m[c], m[p] = m[p], m[c]
        for r in range(n):
            if r != c and m[r][c] != 0:
                f = m[r][c] / m[c][c]
                m[r] = [x - f * y for x, y in zip(m[r], m[c])]
    return [float(m[i][n] / m[i][i]) for i in range(n)]


def test_hpwl_by_hand():
    loc = [(0.0, 0.0), (2.0, 0.0), (0.0, 1.0), (1.0, 0.0)]
    assert hpwl(PAGE_NETS, loc, PAGE_PADS) == 1.5 + 1 + 1 + 1.5 + 2


def test_page_example():
    c = (1.0, 0.5)
    pos = solve_quadratic(4, PAGE_NETS, PAGE_PADS, None, 0.0, c, [c] * 4, eps=0.0)
    want = [(0.0, 0.5), (2.0, 0.5), (1.0, 0.5), (1.0, 0.5)]
    assert all(math.isclose(p[0], w[0], abs_tol=1e-9) and math.isclose(p[1], w[1], abs_tol=1e-9) for p, w in zip(pos, want))
    out = {}
    spread([0, 1, 2], [(0, 0), (0, 1), (2, 0), (2, 1)], pos, out)
    assert out == {0: (0, 0), 2: (0, 1), 1: (2, 0)}
    best, cost, history = heap_place(3, 2, PAGE_COLS, PAGE_TYPES, PAGE_PADS, PAGE_NETS, iters=5)
    assert cost == 7.0 == exhaustive_min_hpwl(3, 2, PAGE_COLS, PAGE_TYPES, PAGE_PADS, PAGE_NETS)
    assert best[3] == (1.0, 0.0)


def test_conjugate_gradient_matches_gaussian_elimination():
    rng = random.Random(3)
    for _ in range(30):
        n = rng.randint(2, 7)
        types, pads, nets = random_instance(rng, 4, 3, ["L"] * 4, {"L": n}, 2, rng.randint(1, 6))
        anchors = [(rng.uniform(0, 3), rng.uniform(0, 2)) for _ in range(n)] if rng.random() < 0.5 else None
        a, bx, by = build_system(n, nets, pads, anchors, 0.3, 1e-3)
        for b in (bx, by):
            got = conjugate_gradient(a, b, [0.0] * n)
            want = gauss_solve(a, b)
            assert all(math.isclose(g, w, rel_tol=1e-7, abs_tol=1e-7) for g, w in zip(got, want))


def test_quadratic_solution_is_a_minimum():
    """No small step of one block lowers the clique-model objective."""
    rng = random.Random(4)
    for _ in range(20):
        n = rng.randint(2, 6)
        types, pads, nets = random_instance(rng, 4, 3, ["L"] * 4, {"L": n}, 2, rng.randint(2, 6))
        anchors = [(rng.uniform(0, 3), rng.uniform(0, 2)) for _ in range(n)]
        c = (1.5, 1.0)
        pos = solve_quadratic(n, nets, pads, anchors, 0.5, c, [c] * n)

        def objective(p):
            total = 0.0
            for net in nets:
                pts = [p[i] if k == "b" else pads[i] for k, i in net]
                w = 1.0 / (len(net) - 1)
                for s in range(len(pts)):
                    for t in range(s + 1, len(pts)):
                        total += w * ((pts[s][0] - pts[t][0]) ** 2 + (pts[s][1] - pts[t][1]) ** 2)
            for i in range(n):
                total += 0.5 * ((p[i][0] - anchors[i][0]) ** 2 + (p[i][1] - anchors[i][1]) ** 2)
                total += 1e-3 * ((p[i][0] - c[0]) ** 2 + (p[i][1] - c[1]) ** 2)
            return total

        base = objective(pos)
        for i in range(n):
            for dx, dy in ((0.01, 0), (-0.01, 0), (0, 0.01), (0, -0.01)):
                moved = list(pos)
                moved[i] = (pos[i][0] + dx, pos[i][1] + dy)
                assert objective(moved) >= base - 1e-9


def test_spread_is_legal_and_ordered():
    rng = random.Random(5)
    for _ in range(300):
        nx, ny = rng.randint(1, 5), rng.randint(1, 5)
        sites = [(x, y) for x in range(nx) for y in range(ny) if rng.random() < 0.8] or [(0, 0)]
        m = rng.randint(1, len(sites))
        pos = [(rng.uniform(-1, nx), rng.uniform(-1, ny)) for _ in range(m)]
        out = {}
        spread(list(range(m)), sites, pos, out)
        assert sorted(out) == list(range(m))
        assert len(set(out.values())) == m and set(out.values()) <= set(sites)


def test_heap_is_legal_and_reports_its_cost():
    rng = random.Random(6)
    cols = ["L", "L", "M", "L", "D", "L"]
    for _ in range(10):
        counts = {"L": rng.randint(5, 16), "M": rng.randint(1, 4), "D": rng.randint(0, 4)}
        types, pads, nets = random_instance(rng, 6, 4, cols, counts, 3, rng.randint(5, 25))
        best, cost, history = heap_place(6, 4, cols, types, pads, nets, iters=8)
        assert len(set(best)) == len(types)
        for i, (x, y) in enumerate(best):
            assert x == int(x) and y == int(y) and 0 <= y < 4 and cols[int(x)] == types[i]
        assert cost == hpwl(nets, best, pads) == min(history)


def test_never_below_exhaustive_optimum():
    rng = random.Random(1)
    equal = 0
    ratios = []
    for _ in range(60):
        cols = ["L", "M", "L"]
        counts = {"L": rng.randint(2, 4), "M": rng.randint(1, 2)}
        types, pads, nets = random_instance(rng, 3, 2, cols, counts, 2, rng.randint(3, 6))
        _, cost, _ = heap_place(3, 2, cols, types, pads, nets, iters=15)
        opt = exhaustive_min_hpwl(3, 2, cols, types, pads, nets)
        assert cost >= opt - 1e-9
        equal += math.isclose(cost, opt)
        ratios.append(cost / opt)
    # measured on these toy instances, not a bound: 20 of 60 optimal, mean ratio about 1.10
    assert equal >= 15 and sum(ratios) / len(ratios) < 1.2


def test_too_many_blocks_of_one_type():
    try:
        heap_place(3, 2, ["L", "M", "L"], ["M", "M", "M"], [], [[("b", 0), ("b", 1)]])
    except ValueError:
        return
    raise AssertionError("expected ValueError")
