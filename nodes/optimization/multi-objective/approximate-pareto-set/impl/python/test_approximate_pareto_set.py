# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/approximate-pareto-set/. The authors are listed in prov/ERC7WZ.jsonl.

import itertools
import random
from fractions import Fraction as Fr

from approximate_pareto_set import EpsilonArchive, dominates, eps_dominates, is_eps_pareto_set


def check_invariants(arc, seen, upper):
    pts = arc.points
    boxes = [arc.box(a) for a in pts]
    assert len(set(boxes)) == len(boxes)
    for a, b in itertools.permutations(range(len(pts)), 2):
        assert not dominates(boxes[a], boxes[b])
        assert not dominates(pts[a], pts[b])
    for y in seen:
        by = arc.box(y)
        # some archive box is weakly below the box of y, so a_i < y_i + eps
        assert any(all(u <= v for u, v in zip(ba, by)) for ba in boxes)
        assert any(all(ai < yi + arc.eps for ai, yi in zip(a, y)) for a in pts)
    assert is_eps_pareto_set(pts, seen, arc.eps)
    # only Pareto-optimal points of the seen points stay in the archive
    for a in pts:
        assert not any(dominates(z, a) for z in seen)
    p = len(arc.lower)
    k = max((u - lo) // arc.eps for u, lo in zip(upper, arc.lower)) + 1
    assert len(pts) <= k ** (p - 1)


def test_example() -> None:
    arc = EpsilonArchive(2, (0, 0))
    seen = [(t, 10 - t) for t in range(11)]
    for y in seen:
        arc.add(y)
    assert sorted(arc.points) == [(1, 9), (3, 7), (5, 5), (7, 3), (9, 1)]
    check_invariants(arc, seen, (10, 10))
    # a smaller eps-Pareto set of the same points
    assert is_eps_pareto_set([(2, 8), (7, 3), (10, 0)], seen, 2)
    assert not any(is_eps_pareto_set(list(s), seen, 2) for s in itertools.combinations(seen, 2))


def test_edges() -> None:
    arc = EpsilonArchive(1, (0, 0, 0))
    assert arc.add((0, 0, 0))
    assert not arc.add((0, 0, 0))
    assert not arc.add((3, 3, 3))
    assert arc.points == [(0, 0, 0)]
    assert eps_dominates((1, 1), (0, 0), 1) and not eps_dominates((2, 1), (0, 0), 1)


def test_same_box_rules() -> None:
    arc = EpsilonArchive(4, (0, 0))
    arc.add((3, 1))
    arc.add((1, 3))  # same box, not comparable; (1, 3) is not closer to the corner (0, 0)
    assert arc.points == [(3, 1)]
    arc.add((1, 2))  # same box, closer to the corner
    assert arc.points == [(1, 2)]
    arc.add((1, 1))  # same box, dominates
    assert arc.points == [(1, 1)]


def test_random_streams() -> None:
    rng = random.Random(42)
    for _ in range(150):
        p = rng.randint(2, 3)
        eps = rng.choice([1, 2, 3, Fr(3, 2)])
        upper = (12,) * p
        arc = EpsilonArchive(eps, (0,) * p)
        seen = []
        for _ in range(rng.randint(1, 60)):
            y = tuple(Fr(rng.randint(0, 24), 2) for _ in range(p))
            seen.append(y)
            arc.add(y)
            check_invariants(arc, seen, upper)


def test_size_bound_is_reached_for_two_objectives() -> None:
    # one point in each box of an anti-diagonal: K boxes, all kept
    eps, k = 1, 7
    arc = EpsilonArchive(eps, (0, 0))
    for t in range(k):
        arc.add((t, k - 1 - t))
    assert len(arc.points) == k == k ** (2 - 1)


def test_grid_bound_is_tight() -> None:
    # (c^k, c^(K-1-k)) with 1 + eps < c: no point covers another in the multiplicative sense
    eps, c, kk = Fr(1, 2), Fr(8, 5), 5
    pts = [(c**k, c ** (kk - 1 - k)) for k in range(kk)]
    for a, y in itertools.permutations(pts, 2):
        assert not all(ai <= (1 + eps) * yi for ai, yi in zip(a, y))
