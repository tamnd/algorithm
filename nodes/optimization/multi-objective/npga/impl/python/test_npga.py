# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/npga/. The authors are listed in prov/H04GPP.jsonl.

import itertools
import random
from fractions import Fraction as Fr

from npga import dominated_by_set, dominates, niche_count, npga, prob_found_dominated, tournament

POINTS = [(1, 8), (2, 5), (3, 6), (4, 2), (5, 4), (6, 7), (7, 1), (8, 3)]


def sch(x):
    return (x[0] ** 2, (x[0] - 2) ** 2)


def candidates(rng, n):
    """Replay the first two draws of tournament() on a copy of the generator."""
    r = random.Random()
    r.setstate(rng.getstate())
    return r.randrange(n), r.randrange(n)


def test_example() -> None:
    a, b, c, d, e, f, g, h = POINTS
    assert dominated_by_set(c, [b, f]) and not dominated_by_set(h, [b, f])
    assert not dominated_by_set(a, [d, e]) and not dominated_by_set(g, [d, e])
    assert prob_found_dominated(8, 1, 2) == Fr(1, 4)
    assert prob_found_dominated(8, 4, 2) == Fr(11, 14)
    assert prob_found_dominated(8, 2, 2) == Fr(13, 28)
    assert prob_found_dominated(8, 0, 5) == 0


def test_probability_by_enumeration() -> None:
    rng = random.Random(4)
    for _ in range(60):
        n = rng.randint(2, 8)
        pts = [tuple(rng.randint(0, 4) for _ in range(2)) for _ in range(n)]
        for t in range(0, n + 1):
            subsets = list(itertools.combinations(range(n), t))
            for i in range(n):
                k = sum(1 for z in pts if dominates(z, pts[i]))
                hits = sum(1 for s in subsets if dominated_by_set(pts[i], [pts[j] for j in s]))
                assert Fr(hits, len(subsets)) == prob_found_dominated(n, k, t)


def test_niche_count() -> None:
    lo, span = [0, 0], [10, 10]
    pool = [(1, 8)] * 3
    assert niche_count((1, 8), pool, 0.3, lo, span) == 3
    assert niche_count((7, 1), pool, 0.3, lo, span) == 0
    assert niche_count((1, 8), [], 0.3, lo, span) == 0


def test_tournament_rules() -> None:
    lo, span = [0, 0], [10, 10]
    rng = random.Random(2)
    # both non-dominated: the candidate with the smaller niche count in the pool wins
    images = [(1, 8), (7, 1)]
    pool = [(1, 8)] * 3
    for _ in range(100):
        a, b = candidates(rng, 2)
        w = tournament(images, pool, 2, 0.3, rng, lo, span)
        if a != b:
            assert images[w] == (7, 1)
    # t = n: the comparison set is the whole population, so a dominated candidate loses to a non-dominated one
    for _ in range(300):
        n = rng.randint(2, 7)
        pts = [tuple(rng.randint(0, 5) for _ in range(2)) for _ in range(n)]
        a, b = candidates(rng, n)
        w = tournament(pts, [], n, 0.5, rng, lo, span)
        assert w in (a, b)
        da = any(dominates(z, pts[a]) for z in pts)
        db = any(dominates(z, pts[b]) for z in pts)
        if da != db:
            assert w == (b if da else a)


def test_run_invariants() -> None:
    for seed, n in [(1, 10), (2, 7), (3, 1)]:
        rng = random.Random(seed)

        def hook(pop):
            assert len(pop) == n
            assert all(-4 <= x[0] <= 4 and y == sch(x) for x, y in pop)

        out = npga(sch, n, [-4], [4], 3, 0.3, 25, rng, on_generation=hook)
        assert out
        for (_, a), (_, b) in itertools.permutations(out, 2):
            assert not dominates(a, b)
