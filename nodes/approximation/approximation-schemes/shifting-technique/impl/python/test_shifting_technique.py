# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/shifting-technique/. The authors are listed in prov/MCW6TZ.jsonl.

import random
from fractions import Fraction
from itertools import combinations

from shifting_technique import cover_exact, covers, shift_and_solve, shifting_cover, strips


def brute_opt(points):
    """Try all sets of squares whose corners are (x of a point, y of a point), by increasing size."""
    pts = list(set(points))
    if not pts:
        return 0
    cand = sorted({(p[0], q[1]) for p in pts for q in pts})
    for k in range(1, len(pts) + 1):
        for c in combinations(cand, k):
            if all(any(covers(q, p) for q in c) for p in pts):
                return k
    raise AssertionError


def is_cover(points, squares):
    return all(any(covers(q, p) for q in squares) for p in points)


def random_points(rng, n, size, step):
    return [(Fraction(rng.randint(0, size * step), step), Fraction(rng.randint(0, size * step), step)) for _ in range(n)]


EXAMPLE = [(Fraction(a), Fraction(b)) for a, b in
           [(0.5, 0.5), (1.25, 0.75), (1.75, 2.5), (2.25, 2.25), (3.5, 0.25), (3.75, 1.0), (4.5, 3.5), (5.0, 3.75)]]


def test_example() -> None:
    assert len(cover_exact(EXAMPLE)) == 4 and brute_opt(EXAMPLE) == 4
    cover, costs = shift_and_solve(EXAMPLE, 2, 0, cover_exact)
    assert costs == [5, 6] and len(cover) == 5
    assert [len(g) for g in strips(EXAMPLE, 2, 0, 0)] == [3, 3, 2]
    assert [len(g) for g in strips(EXAMPLE, 2, 1, 0)] == [1, 3, 3, 1]
    assert len(shifting_cover(EXAMPLE, 2)) == 5


def test_exact_cover_matches_brute_force() -> None:
    rng = random.Random(1985)
    for _ in range(120):
        pts = random_points(rng, rng.randint(1, 6), 3, 2)
        sol = cover_exact(pts)
        assert is_cover(pts, sol)
        assert len(sol) == brute_opt(pts)


def test_each_square_is_cut_by_exactly_one_shift() -> None:
    rng = random.Random(130)
    for _ in range(300):
        x = Fraction(rng.randint(0, 80), 8)
        for ell in (1, 2, 3, 4):
            cut = [s for s in range(ell) if any(x < c <= x + 1 for c in range(-1, 13) if c % ell == s)]
            assert len(cut) == 1


def test_shifting_lemma_and_ratio() -> None:
    rng = random.Random(136)
    for ell in (1, 2, 3):
        for _ in range(40):
            pts = random_points(rng, rng.randint(1, 11), 7, 4)
            opt = len(cover_exact(pts))
            cover, costs = shift_and_solve(pts, ell, 0, cover_exact)
            assert is_cover(pts, cover)
            # each optimal square is split by one shift, so the costs sum to at most (ell + 1) OPT
            assert sum(costs) <= (ell + 1) * opt
            assert len(cover) * ell <= (ell + 1) * opt
            # each strip is solved exactly, so no shift is below OPT
            assert min(costs) >= opt
            two = shifting_cover(pts, ell)
            assert is_cover(pts, two)
            assert len(two) * ell * ell <= (ell + 1) ** 2 * opt


def test_cell_search_size() -> None:
    # a cell of side ell has an optimum of at most ell^2 squares, so the search depth is at most ell^2
    rng = random.Random(7)
    for ell in (1, 2):
        for _ in range(30):
            pts = [(Fraction(rng.randint(0, 4 * ell - 1), 4), Fraction(rng.randint(0, 4 * ell - 1), 4)) for _ in range(9)]
            st = {}
            sol = cover_exact(pts, st)
            assert len(sol) <= ell * ell
            n = len(set(pts))
            assert st["nodes"] <= sum(n ** d for d in range(ell * ell + 1))
