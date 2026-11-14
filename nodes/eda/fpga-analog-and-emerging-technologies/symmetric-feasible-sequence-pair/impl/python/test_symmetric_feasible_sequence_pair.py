# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/symmetric-feasible-sequence-pair/. The authors are listed in prov/RFE075.jsonl.

import itertools
import math
import random
from fractions import Fraction

from symmetric_feasible_sequence_pair import _simplex_min, is_symmetric_feasible, positions, repair, sym_pack


def check_placement(gp, gm, w, h, sym, p) -> None:
    n = len(gp)
    x, y, ax = p["x"], p["y"], p["axis"]
    pp, pm = positions(gp), positions(gm)
    for u in range(n):
        assert x[u] >= 0 and y[u] >= 0
        assert x[u] + w[u] <= p["width"] and y[u] + h[u] <= p["height"]
    assert p["width"] == max(x[u] + w[u] for u in range(n))
    for u in range(n):
        for v in range(n):
            if u == v:
                continue
            if pp[u] < pp[v] and pm[u] < pm[v]:
                assert x[u] + w[u] <= x[v]
            if pp[u] > pp[v] and pm[u] < pm[v]:
                assert y[u] + h[u] <= y[v]
            # no overlap, checked directly on the rectangles
            assert x[u] + w[u] <= x[v] or x[v] + w[v] <= x[u] or y[u] + h[u] <= y[v] or y[v] + h[v] <= y[u]
    for u, v in sym.items():
        assert y[u] == y[v]
        assert (x[u] + Fraction(w[u], 2)) + (x[v] + Fraction(w[v], 2)) == 2 * ax


def test_small_example() -> None:
    # cells: 0 and 1 a pair (1 x 1), 2 self-symmetric (2 x 1), 3 free (1 x 2)
    w, h, sym = [1, 1, 2, 1], [1, 1, 1, 2], {0: 1, 1: 0, 2: 2}
    gp, gm = [3, 1, 0, 2], [3, 2, 1, 0]
    assert is_symmetric_feasible(gp, gm, sym)
    p = sym_pack(gp, gm, w, h, sym)
    check_placement(gp, gm, w, h, sym, p)
    assert (p["width"], p["height"], p["axis"]) == (3, 2, 2)
    assert sym_pack(gp, [3, 2, 0, 1], w, h, sym) is None


def test_count_of_feasible_pairs() -> None:
    for n, sym in ((3, {0: 1, 1: 0}), (3, {0: 0, 1: 1, 2: 2}), (4, {0: 1, 1: 0, 2: 3, 3: 2}), (4, {0: 1, 1: 0, 2: 2})):
        perms = list(itertools.permutations(range(n)))
        cnt = sum(1 for a in perms for b in perms if is_symmetric_feasible(list(a), list(b), sym))
        assert cnt == math.factorial(n) ** 2 // math.factorial(len(sym))


def test_repair() -> None:
    rng = random.Random(2000)
    sym = {0: 1, 1: 0, 2: 2, 3: 4, 4: 3}
    for _ in range(300):
        gp, gm = list(range(7)), list(range(7))
        rng.shuffle(gp)
        rng.shuffle(gm)
        gm2 = repair(gp, gm, sym)
        assert is_symmetric_feasible(gp, gm2, sym)
        assert [c for c in gm2 if c not in sym] == [c for c in gm if c not in sym]
        assert repair(gp, gm2, sym) == gm2


def test_mirror_lemma_on_all_pairs() -> None:
    sym = {0: 1, 1: 0, 2: 2, 3: 3}
    perms = list(itertools.permutations(range(4)))
    for a in perms:
        for b in perms:
            if not is_symmetric_feasible(list(a), list(b), sym):
                continue
            pp, pm = positions(a), positions(b)
            for u in sym:
                for v in sym:
                    if u == v:
                        continue
                    if pp[u] < pp[v] and pm[u] < pm[v]:  # u left of v
                        assert pp[sym[v]] < pp[sym[u]] and pm[sym[v]] < pm[sym[u]]
                    if pp[u] > pp[v] and pm[u] < pm[v]:  # u below v
                        assert pp[sym[u]] > pp[sym[v]] and pm[sym[u]] < pm[sym[v]]
            assert (pp[0] < pp[1]) == (pm[0] < pm[1])  # a pair is side by side
            assert (pp[2] < pp[3]) != (pm[2] < pm[3])  # self-symmetric cells are stacked


def brute_min_area(w, h, sym, free, xmax, ymax):
    """The least bounding-box area of a symmetric, overlap-free placement with x on a
    half-unit grid and y on the unit grid, found by trying every grid position."""
    halves = [Fraction(k, 2) for k in range(2 * xmax + 1)]
    ys = list(range(ymax + 1))
    pairs = [(u, v) for u, v in sym.items() if u < v]
    selfs = [u for u, v in sym.items() if u == v]
    best = None
    n = len(w)
    spots = list(itertools.product(halves, ys))
    for ax in halves:
        for choice in itertools.product(*([spots] * len(pairs) + [ys] * len(selfs) + [spots] * len(free))):
            x, y = [None] * n, [None] * n
            k = 0
            for u, v in pairs:
                x[u], y[u] = choice[k]
                x[v], y[v] = 2 * ax - w[u] - x[u], y[u]
                k += 1
            for s in selfs:
                x[s], y[s] = ax - Fraction(w[s], 2), choice[k]
                k += 1
            for f in free:
                x[f], y[f] = choice[k]
                k += 1
            if min(x) < 0:
                continue
            ok = all(x[a] + w[a] <= x[b] or x[b] + w[b] <= x[a] or y[a] + h[a] <= y[b] or y[b] + h[b] <= y[a] for a in range(n) for b in range(a + 1, n))
            if ok:
                area = max(x[a] + w[a] for a in range(n)) * max(y[a] + h[a] for a in range(n))
                best = area if best is None else min(best, area)
    return best


def best_over_pairs(w, h, sym):
    n = len(w)
    perms = list(itertools.permutations(range(n)))
    best = None
    for a in perms:
        for b in perms:
            p = sym_pack(list(a), list(b), w, h, sym)
            if p is None:
                continue
            check_placement(list(a), list(b), w, h, sym, p)
            area = p["width"] * p["height"]
            best = area if best is None else min(best, area)
    return best


def test_exhaustive_against_grid_search() -> None:
    # a pair 1 x 1, a self-symmetric cell 2 x 1 and a free cell 1 x 2
    w, h, sym = [1, 1, 2, 1], [1, 1, 1, 2], {0: 1, 1: 0, 2: 2}
    assert best_over_pairs(w, h, sym) == brute_min_area(w, h, sym, [3], 4, 3) == 6
    # two pairs: 2 x 1 and 1 x 2
    w, h, sym = [2, 2, 1, 1], [1, 1, 2, 2], {0: 1, 1: 0, 2: 3, 3: 2}
    assert best_over_pairs(w, h, sym) == brute_min_area(w, h, sym, [], 4, 3)


def test_random_instances_always_pack() -> None:
    rng = random.Random(7)
    for _ in range(60):
        n = rng.randint(4, 7)
        w = [rng.randint(1, 4) for _ in range(n)]
        h = [rng.randint(1, 4) for _ in range(n)]
        cells = list(range(n))
        rng.shuffle(cells)
        sym = {}
        for i in range(rng.randint(0, 2)):
            a, b = cells.pop(), cells.pop()
            w[b], h[b] = w[a], h[a]
            sym[a], sym[b] = b, a
        for i in range(rng.randint(0, min(2, len(cells)))):
            s = cells.pop()
            sym[s] = s
        gp, gm = list(range(n)), list(range(n))
        rng.shuffle(gp)
        rng.shuffle(gm)
        gm = repair(gp, gm, sym)
        p = sym_pack(gp, gm, w, h, sym)
        check_placement(gp, gm, w, h, sym, p)


def test_simplex_small() -> None:
    # min x + y with x + 2y >= 4, 3x + y >= 6: optimum at (8/5, 6/5)
    val, x = _simplex_min([1, 1], [([1, 2], ">=", 4), ([3, 1], ">=", 6)])
    assert val == Fraction(14, 5) and x == [Fraction(8, 5), Fraction(6, 5)]
    assert _simplex_min([1], [([1], "<=", -1)]) is None
