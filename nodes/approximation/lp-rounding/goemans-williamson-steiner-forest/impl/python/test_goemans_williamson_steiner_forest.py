# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/goemans-williamson-steiner-forest/. The authors are listed in prov/AWBKWN.jsonl.

import random
from fractions import Fraction
from itertools import combinations

import pytest

from goemans_williamson_steiner_forest import _connects_all, goemans_williamson_steiner_forest


def lp_min(c, rows):
    """Exact two-phase simplex (Bland's rule) for min c.x, rows (a, '>=', b), x >= 0. Tiny LPs only."""
    n, m = len(c), len(rows)
    t = []
    for k, (a, _, b) in enumerate(rows):
        t.append([Fraction(v) for v in a] + [Fraction(-1 if q == k else 0) for q in range(m)]
                 + [Fraction(1 if q == k else 0) for q in range(m)] + [Fraction(b)])
    basis = [n + m + k for k in range(m)]

    def pivot(r, col):
        pv = t[r][col]
        t[r] = [v / pv for v in t[r]]
        for i in range(len(t)):
            f = t[i][col]
            if i != r and f:
                t[i] = [a - f * b for a, b in zip(t[i], t[r])]
        basis[r] = col

    def run(cost, ncols):
        while True:
            enter = next((j for j in range(ncols) if j not in basis and
                          cost[j] - sum(cost[basis[i]] * t[i][j] for i in range(len(t))) < 0), None)
            if enter is None:
                return
            cand = [(t[i][-1] / t[i][enter], basis[i], i) for i in range(len(t)) if t[i][enter] > 0]
            pivot(min(cand)[2], enter)

    run([0] * (n + m) + [1] * m, n + 2 * m)
    assert all(t[i][-1] == 0 for i in range(len(t)) if basis[i] >= n + m)
    for i in range(len(t)):
        if basis[i] >= n + m:
            j = next((j for j in range(n + m) if t[i][j] != 0), None)
            if j is not None:
                pivot(i, j)
    cost = [Fraction(v) for v in c] + [0] * (2 * m)
    run(cost, n + m)
    x = [Fraction(0)] * n
    for i, j in enumerate(basis):
        if j < n:
            x[j] = t[i][-1]
    return sum(cost[j] * x[j] for j in range(n))


def separating_sets(n, pairs):
    out = []
    for mask in range(1, 2 ** n - 1):
        if mask & 1:
            continue  # S and its complement give the same cut; keep the one without vertex 0
        if any(((mask >> s) & 1) != ((mask >> t) & 1) for s, t in pairs):
            out.append(mask)
    return out


def cut_lp(n, edges, pairs):
    rows = []
    for mask in separating_sets(n, pairs):
        rows.append(([1 if ((mask >> u) & 1) != ((mask >> v) & 1) else 0 for u, v, _ in edges], ">=", 1))
    return lp_min([w for _, _, w in edges], rows)


def brute_opt(n, edges, pairs):
    best = None
    for r in range(len(edges) + 1):
        for sub in combinations(range(len(edges)), r):
            cost = sum(edges[e][2] for e in sub)
            if (best is None or cost < best) and _connects_all(n, edges, sub, pairs):
                best = cost
    return best


def check(n, edges, pairs, with_lp=True):
    forest, y = goemans_williamson_steiner_forest(n, edges, pairs)
    assert _connects_all(n, edges, forest, pairs)
    req = [(s, t) for s, t in pairs if s != t]
    for s in y:
        assert y[s] >= 0 and any((a in s) != (b in s) for a, b in req)
    for u, v, w in edges:  # the dual is feasible
        assert sum(val for s, val in y.items() if (u in s) != (v in s)) <= w
    for e in forest:  # each edge of the forest is tight
        u, v, w = edges[e]
        assert sum(val for s, val in y.items() if (u in s) != (v in s)) == w
    k = len({x for p in req for x in p})
    alg = sum(edges[e][2] for e in forest)
    dual = sum(y.values(), Fraction(0))
    if k:
        assert alg <= (2 - Fraction(2, k)) * dual
    opt = brute_opt(n, edges, pairs)
    assert dual <= opt and alg <= 2 * opt
    if with_lp:
        lp = cut_lp(n, edges, req) if req else 0
        assert dual <= lp <= opt
    return forest, y, alg, dual, opt


def test_page_example():
    # vertices a .. f are 0 .. 5; the pairs are (a, d) and (c, f)
    edges = [(0, 1, 5), (0, 5, 4), (1, 3, 2), (2, 3, 5), (2, 4, 3), (2, 5, 3), (3, 4, 2), (3, 5, 5)]
    pairs = [(0, 3), (2, 5)]
    forest, y, alg, dual, opt = check(6, edges, pairs)
    assert forest == [5, 1, 3]
    assert (alg, dual, opt) == (12, 9, 10)
    assert cut_lp(6, edges, pairs) == Fraction(19, 2)
    h = Fraction(1, 2)
    assert {tuple(sorted(s)): v for s, v in y.items()} == {
        (0,): 5 * h, (2,): 3 * h, (3,): 2, (5,): 3 * h, (1, 3, 4): 1, (0, 2, 5): h}


def test_random_against_brute_force_and_lp():
    rng = random.Random(1995)
    done = 0
    while done < 120:
        n = rng.randint(2, 6)
        edges = [(u, v, rng.randint(0, 6)) for u, v in combinations(range(n), 2) if rng.random() < 0.55]
        if not edges or len(edges) > 9:
            continue
        pairs = [tuple(rng.sample(range(n), 2)) for _ in range(rng.randint(1, 3))]
        try:
            check(n, edges, pairs, with_lp=done < 60)
        except ValueError:
            assert brute_opt(n, edges, pairs) is None
        done += 1


def test_many_random_without_lp():
    rng = random.Random(4)
    for _ in range(500):
        n = rng.randint(2, 5)
        edges = [(u, v, rng.randint(1, 5)) for u, v in combinations(range(n), 2) if rng.random() < 0.7]
        pairs = [tuple(rng.sample(range(n), 2)) for _ in range(rng.randint(1, 2))]
        if brute_opt(n, edges, pairs) is None:
            with pytest.raises(ValueError):
                goemans_williamson_steiner_forest(n, edges, pairs)
            continue
        check(n, edges, pairs, with_lp=False)


def test_forward_delete_keeps_the_bound():
    # the proof needs only a minimal forest inside the grown edges, so a forward deletion order also works
    rng = random.Random(11)
    for _ in range(300):
        n = rng.randint(2, 6)
        edges = [(u, v, rng.randint(1, 5)) for u, v in combinations(range(n), 2) if rng.random() < 0.7]
        pairs = [tuple(rng.sample(range(n), 2)) for _ in range(rng.randint(1, 3))]
        grown = []
        try:
            forest, y = goemans_williamson_steiner_forest(n, edges, pairs, grown)
        except ValueError:
            continue
        kept = list(grown)
        for e in grown:  # forward order
            rest = [q for q in kept if q != e]
            if _connects_all(n, edges, rest, pairs):
                kept = rest
        k = len({x for p in pairs for x in p})
        assert sum(edges[e][2] for e in kept) <= (2 - Fraction(2, k)) * sum(y.values(), Fraction(0))


def test_tight_family_cycle_and_hub():
    # k terminals on a cycle with edges of cost 2 - eps, and a hub joined to each terminal at cost 1
    eps = Fraction(1, 100)
    for k in (3, 4, 5):
        hub = k
        edges = [(i, (i + 1) % k, 2 - eps) for i in range(k)] + [(i, hub, 1) for i in range(k)]
        pairs = [(0, i) for i in range(1, k)]
        forest, y, alg, dual, opt = check(k + 1, edges, pairs, with_lp=(k < 5))
        assert opt == k and alg == (k - 1) * (2 - eps)
        assert alg == (2 - Fraction(2, k)) * dual


def test_no_pairs_and_unreachable():
    assert goemans_williamson_steiner_forest(3, [(0, 1, 1)], []) == ([], {})
    with pytest.raises(ValueError):
        goemans_williamson_steiner_forest(3, [(0, 1, 1)], [(0, 2)])
