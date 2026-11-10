# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/shmoys-tardos-aardal-facility-location/. The authors are listed in prov/C5BW1S.jsonl.

import random
from fractions import Fraction
from itertools import combinations

from shmoys_tardos_aardal_facility_location import alpha_point, cluster, lp_min, shmoys_tardos_aardal, ufl_lp

RATIO = Fraction(31572, 10000)  # 3 / (1 - e^-3) = 3.15718...


def cost(f, c, opened, assign):
    return sum(f[i] for i in set(opened)) + sum(c[assign[j]][j] for j in range(len(c[0])))


def brute_opt(f, c):
    m, n = len(f), len(c[0])
    return min(sum(f[i] for i in s) + sum(min(c[i][j] for i in s) for j in range(n))
               for k in range(1, m + 1) for s in combinations(range(m), k))


def check(f, c):
    m, n = len(f), len(c[0])
    lp, x, y = ufl_lp(f, c)
    for j in range(n):
        assert sum(x[i][j] for i in range(m)) == 1
        assert all(0 <= x[i][j] <= y[i] for i in range(m))
    fl = sum(f[i] * y[i] for i in range(m))
    cj = [sum(c[i][j] * x[i][j] for i in range(m)) for j in range(n)]
    assert lp == fl + sum(cj)
    breaks = {s for j in range(n) for s in (sum(x[i][j] for i in range(m) if c[i][j] <= c[k][j]) for k in range(m)) if s > 0}
    for alpha in sorted(breaks | {Fraction(1, 4), Fraction(1, 2)}):
        opened, assign, g = cluster(f, c, x, alpha)
        assert len(set(opened)) == len(opened) and all(a in opened for a in assign)
        for j in range(n):
            assert c[assign[j]][j] <= 3 * g[j]  # the cluster center is at most 3 g_j away
            if alpha < 1:
                assert g[j] <= cj[j] / (1 - alpha)  # Markov bound for the alpha-point
        assert cost(f, c, opened, assign) <= fl / alpha + 3 * sum(g)
        if alpha == Fraction(1, 4):
            assert cost(f, c, opened, assign) <= 4 * lp
    opened, assign, lp2, alpha = shmoys_tardos_aardal(f, c)
    assert lp2 == lp
    alg = cost(f, c, opened, assign)
    opt = brute_opt(f, c)
    assert lp <= opt <= alg <= RATIO * lp
    return opened, assign, lp, alpha, alg, opt


def metric_instance(rng, m, n, side):
    pts = [(rng.randint(0, side), rng.randint(0, side)) for _ in range(m + n)]
    c = [[abs(pts[i][0] - pts[m + j][0]) + abs(pts[i][1] - pts[m + j][1]) for j in range(n)] for i in range(m)]
    f = [rng.randint(0, 3 * side) for _ in range(m)]
    return f, c


def test_page_example():
    # three facilities and three clients; client j is at distance 1 from facilities j and j + 1
    f = [2, 2, 2]
    c = [[1, 3, 1], [1, 1, 3], [3, 1, 1]]
    opened, assign, lp, alpha, alg, opt = check(f, c)
    assert (lp, alg, opt) == (6, 7, 7)
    _, x, y = ufl_lp(f, c)
    h = Fraction(1, 2)
    assert y == [h, h, h]
    assert alpha_point(x, c, 0, h) == 1 and alpha_point(x, c, 0, 1) == 1


def test_lp_min_small():
    assert lp_min([1, 1], [([1, 2], ">=", 2), ([3, 1], ">=", 3)]) == (Fraction(7, 5), [Fraction(4, 5), Fraction(3, 5)])
    assert lp_min([1], [([1], "<=", -1)]) is None


def test_random_metric_against_brute_force():
    rng = random.Random(1997)
    fractional = 0
    for it in range(500):
        m, n = rng.randint(1, 4), rng.randint(1, 5)
        if it % 3 == 0:
            f, c = metric_instance(rng, m, n, rng.randint(1, 6))
        elif it % 3 == 1 and m >= 2:
            # each client is near two random facilities; such instances often have a fractional LP
            near = [rng.sample(range(m), 2) for _ in range(n)]
            c = [[1 if i in near[j] else 3 for j in range(n)] for i in range(m)]
            f = [rng.randint(1, 3) for _ in range(m)]
        else:
            # all costs in [1, 3]: c_ij <= c_ij' + c_i'j' + c_i'j holds, so this is metric too
            c = [[rng.randint(1, 3) for _ in range(n)] for _ in range(m)]
            f = [rng.randint(0, 4) for _ in range(m)]
        _, _, lp, _, _, opt = check(f, c)
        fractional += lp < opt
    assert fractional >= 5


def test_gap_instances():
    # k clients each near two of k facilities on a cycle: the LP opens every facility to 1/2
    for k in (3, 4, 5):
        c = [[1 if j in (i, (i + 1) % k) else 3 for j in range(k)] for i in range(k)]
        check([2] * k, c)
