# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/vectorless-power-grid-verification/. The authors are listed in prov/H1QXN8.jsonl.

import itertools
import random
from fractions import Fraction

from pgrid import Grid, matvec, random_mesh, solve
from vectorless_power_grid_verification import greedy_one_bound, inverse_row, simplex_max, verify, worst_drop


def vertex_max(c, a, b):
    """Brute force: the best vertex of {y >= 0, a y <= b}, by trying every set of tight constraints."""
    n = len(c)
    rows = [[Fraction(int(i == j)) for j in range(n)] for i in range(n)] + [list(r) for r in a]
    rhs = [Fraction(0)] * n + [Fraction(v) for v in b]
    sign = [-1] * n + [1] * len(a)  # -y <= 0 written as y >= 0
    best = None
    for tight in itertools.combinations(range(len(rows)), n):
        try:
            y = solve([rows[t] for t in tight], [rhs[t] for t in tight])
        except ZeroDivisionError:
            continue
        ok = all(v >= 0 for v in y) and all(sum(r[j] * y[j] for j in range(n)) <= bb for r, bb in zip(a, b))
        if ok:
            val = sum(c[j] * y[j] for j in range(n))
            if best is None or val > best:
                best = val
    return best


def small_case(rng, nx=3, ny=3, ns=4, n_groups=2):
    g = random_mesh(nx, ny, rng, n_pads=2)
    a = g.matrix()
    sources = rng.sample(range(g.n), ns)
    u = [Fraction(rng.randint(1, 6)) for _ in range(ns)]
    groups = [rng.sample(range(ns), rng.randint(2, ns)) for _ in range(n_groups)]
    w = [Fraction(rng.randint(2, 10)) for _ in range(n_groups)]
    return g, a, sources, u, groups, w


def test_simplex_matches_vertex_enumeration():
    rng = random.Random(21)
    for _ in range(40):
        n = rng.randint(1, 4)
        m = rng.randint(1, 5)
        c = [Fraction(rng.randint(-3, 6)) for _ in range(n)]
        a = [[Fraction(rng.randint(0, 4)) for _ in range(n)] for _ in range(m)]
        for j in range(n):  # keep the region bounded: a row with every coefficient positive
            a[0][j] = Fraction(rng.randint(1, 4))
        b = [Fraction(rng.randint(0, 12)) for _ in range(m)]
        val, y = simplex_max(c, a, b)
        assert val == vertex_max(c, a, b)
        assert all(v >= 0 for v in y)
        assert all(sum(r[j] * y[j] for j in range(n)) <= bb for r, bb in zip(a, b))
        assert sum(c[j] * y[j] for j in range(n)) == val


def test_inverse_rows_are_nonnegative_and_symmetric():
    rng = random.Random(22)
    g = random_mesh(3, 3, rng)
    a = g.matrix()
    rows = [inverse_row(a, k) for k in range(g.n)]
    for k in range(g.n):
        assert all(v >= 0 for v in rows[k])
        for j in range(g.n):
            assert rows[k][j] == rows[j][k]


def test_worst_drop_is_attained_and_bounds_every_feasible_current():
    rng = random.Random(23)
    for _ in range(6):
        g, a, sources, u, groups, w = small_case(rng)
        for k in range(g.n):
            z, iw = worst_drop(a, sources, k, u, groups, w)
            full = [Fraction(0)] * g.n
            for s, v in zip(sources, iw):
                full[s] = v
            assert solve(a, full)[k] == z  # the worst currents give the drop z_k
            for _ in range(15):  # random feasible currents never do worse
                i = [Fraction(rng.randint(0, int(us) * 4), 4) for us in u]
                if all(sum(i[t] for t in grp) <= wq for grp, wq in zip(groups, w)):
                    full = [Fraction(0)] * g.n
                    for s, v in zip(sources, i):
                        full[s] = v
                    assert solve(a, full)[k] <= z


def test_lp_against_vertex_enumeration_on_grids():
    rng = random.Random(24)
    for _ in range(5):
        g, a, sources, u, groups, w = small_case(rng)
        k = rng.randrange(g.n)
        r_full = inverse_row(a, k)
        r = [r_full[s] for s in sources]
        rows = [[Fraction(int(s == t)) for t in range(len(sources))] for s in range(len(sources))]
        rows += [[Fraction(int(t in grp)) for t in range(len(sources))] for grp in groups]
        z, _ = worst_drop(a, sources, k, u, groups, w)
        assert z == vertex_max(r, rows, list(u) + list(w))


def test_greedy_equals_lp_with_one_global_bound():
    rng = random.Random(25)
    for _ in range(25):
        g = random_mesh(3, 3, rng)
        a = g.matrix()
        ns = rng.randint(1, 5)
        sources = rng.sample(range(g.n), ns)
        u = [Fraction(rng.randint(1, 6)) for _ in range(ns)]
        total = Fraction(rng.randint(1, 20))
        k = rng.randrange(g.n)
        r_full = inverse_row(a, k)
        r = [r_full[s] for s in sources]
        gz, gi = greedy_one_bound(r, u, total)
        lz, _ = worst_drop(a, sources, k, u, [list(range(ns))], [total])
        assert gz == lz
        assert sum(gi) <= total and all(0 <= v <= us for v, us in zip(gi, u))


def test_no_global_bound_means_all_currents_at_their_maximum():
    rng = random.Random(26)
    g = random_mesh(3, 3, rng)
    a = g.matrix()
    sources = [0, 4, 8]
    u = [Fraction(2), Fraction(3), Fraction(1)]
    full = [Fraction(0)] * g.n
    for s, v in zip(sources, u):
        full[s] = v
    x = solve(a, full)
    for k in range(g.n):
        assert worst_drop(a, sources, k, u, [], [])[0] == x[k]


def test_page_example():
    # Pads of 20 S at nodes 0 and 3, wires of 10 S: 0 - 1 - 2 - 3. Sources at nodes 1 and 2.
    g = Grid(4)
    for x, y in [(0, 1), (1, 2), (2, 3)]:
        g.add_wire(x, y, Fraction(10))
    g.gpad[0] = g.gpad[3] = Fraction(20)
    g.cur = [Fraction(0)] * 4
    a = g.matrix()
    assert inverse_row(a, 1) == [Fraction(1, 32), Fraction(3, 32), Fraction(9, 160), Fraction(3, 160)]
    u = [Fraction(4, 10), Fraction(4, 10)]
    bad, z = verify(a, [1, 2], u, [[0, 1]], [Fraction(5, 10)], [0, 1, 2, 3], Fraction(4, 100))
    assert z == {0: Fraction(23, 1600), 1: Fraction(69, 1600), 2: Fraction(69, 1600), 3: Fraction(23, 1600)}
    assert bad == [1, 2]
    assert worst_drop(a, [1, 2], 1, u, [[0, 1]], [Fraction(5, 10)])[1] == [Fraction(2, 5), Fraction(1, 10)]
    assert worst_drop(a, [1, 2], 2, u, [[0, 1]], [Fraction(5, 10)])[1] == [Fraction(1, 10), Fraction(2, 5)]
    assert worst_drop(a, [1, 2], 1, u, [], [])[0] == Fraction(3, 50)
