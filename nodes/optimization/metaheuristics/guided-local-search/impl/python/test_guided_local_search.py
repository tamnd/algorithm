# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/guided-local-search/. The authors are listed in prov/0JTKYZ.jsonl.

import itertools
import random
from fractions import Fraction

import pytest

from guided_local_search import distance_matrix, guided_local_search, tour_edges, tour_length, two_opt_descent, two_opt_neighbors

P9 = [(17, 2), (11, 19), (19, 9), (2, 16), (11, 12), (13, 0), (1, 3), (14, 20), (7, 11)]
D9 = distance_matrix(P9)


def g9(t: tuple[int, ...]) -> int:
    return tour_length(D9, t)


def brute_force(d) -> int:
    return min(tour_length(d, (0,) + p) for p in itertools.permutations(range(1, len(d))))


def tour(s: str) -> tuple[int, ...]:
    return tuple(int(c) for c in s)


def test_example_of_the_page() -> None:
    best, gb, p, log = guided_local_search(tuple(range(9)), g9, tour_edges, lambda e: D9[e[0]][e[1]], two_opt_descent, Fraction(1, 5), 3)
    assert [(s.penalized, "".join(map(str, s.x)), s.g, s.h) for s in log] == [
        ([(3, 6)], "024871365", 72, Fraction(368, 5)),
        ([(5, 6)], "024871365", 72, Fraction(376, 5)),
        ([(7, 8)], "027148365", 69, Fraction(361, 5)),
    ]
    assert p == {(3, 6): 1, (5, 6): 1, (7, 8): 1}
    assert (best, gb) == (tour("027148365"), 69) and brute_force(D9) == 69


def check_run(d, x0, a, iterations) -> None:
    n = len(d)
    g = lambda t: tour_length(d, t)  # noqa: E731
    cost = lambda e: d[e[0]][e[1]]  # noqa: E731
    best, gb, p, log = guided_local_search(x0, g, tour_edges, cost, two_opt_descent, a, iterations)
    x = two_opt_descent(x0, lambda y: Fraction(g(y)))
    lam = Fraction(a) * g(x) / n
    pen: dict = {}
    seen = [g(x)]
    for s in log:
        # utilities with the penalties before this iteration; exactly the maximal ones are penalized
        util = {e: Fraction(cost(e)) / (1 + pen.get(e, 0)) for e in tour_edges(x)}
        top = max(util.values())
        assert sorted(s.penalized) == sorted(e for e, u in util.items() if u == top)
        old = dict(pen)
        for e in s.penalized:
            pen[e] = pen.get(e, 0) + 1
        # penalties never decrease, and only the penalized features change, by one
        assert all(pen.get(e, 0) - old.get(e, 0) == (1 if e in s.penalized else 0) for e in set(pen) | set(old))

        def h(y):
            return g(y) + lam * sum(pen.get(e, 0) for e in tour_edges(y))

        # the new solution is a 2-opt local minimum of the augmented objective
        assert s.h == h(s.x) and s.g == g(s.x)
        assert all(h(y) >= h(s.x) for y in two_opt_neighbors(s.x))
        assert sorted(s.x) == list(range(n)) and s.x[0] == x0[0]
        x = s.x
        seen.append(g(x))
    assert p == pen
    assert gb == g(best) == min(seen)


def test_invariants_on_random_instances() -> None:
    rng = random.Random(1999)
    for _ in range(60):
        n = rng.randint(5, 8)
        d = distance_matrix([(rng.randint(0, 30), rng.randint(0, 30)) for _ in range(n)])
        x0 = (0,) + tuple(rng.sample(range(1, n), n - 1))
        check_run(d, x0, Fraction(rng.randint(1, 10), 10), rng.randint(0, 12))


def test_edges() -> None:
    with pytest.raises(ValueError):
        guided_local_search(tuple(range(9)), g9, tour_edges, lambda e: 1, two_opt_descent, Fraction(1, 5), -1)
    best, gb, p, log = guided_local_search(tuple(range(9)), g9, tour_edges, lambda e: 1, two_opt_descent, Fraction(1, 5), 0)
    assert (gb, p, log) == (72, {}, [])


def test_fixed_instance_reaches_the_optimum() -> None:
    rng = random.Random(2024)
    d = distance_matrix([(rng.randint(0, 100), rng.randint(0, 100)) for _ in range(10)])
    g = lambda t: tour_length(d, t)  # noqa: E731
    assert brute_force(d) == 231
    best, gb, _, _ = guided_local_search(tuple(range(10)), g, tour_edges, lambda e: d[e[0]][e[1]], two_opt_descent, Fraction(1, 5), 20)
    assert gb == 231 and g(best) == 231
