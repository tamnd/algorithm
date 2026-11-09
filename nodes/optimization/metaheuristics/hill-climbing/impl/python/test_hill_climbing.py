# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hill-climbing/. The authors are listed in prov/NDHC1V.jsonl.

import itertools
import random

import pytest

from hill_climbing import flip_neighbors, hill_climbing, tour_length, two_opt_neighbors, uncut_weight

E6 = [(0, 1, 3), (0, 2, 1), (0, 3, 2), (1, 2, 2), (1, 4, 4), (2, 3, 3), (2, 5, 1), (3, 4, 1), (3, 5, 2), (4, 5, 3)]


def f6(x: tuple[int, ...]) -> int:
    return uncut_weight(E6, x)


def is_local_min(x, f, neighbors) -> bool:
    fx = f(x)
    return all(f(y) >= fx for y in neighbors(x))


def test_example_of_the_page() -> None:
    x, fx, path = hill_climbing((0,) * 6, f6, flip_neighbors)
    assert path == [(0, 0, 0, 0, 0, 0), (0, 1, 0, 0, 0, 0), (0, 1, 0, 1, 0, 0), (0, 1, 0, 1, 0, 1)]
    assert [f6(p) for p in path] == [22, 13, 5, 3]
    assert (x, fx) == ((0, 1, 0, 1, 0, 1), 3)
    best = min(f6(y) for y in itertools.product((0, 1), repeat=6))
    assert fx == best


def test_stuck_at_a_local_minimum() -> None:
    x, fx, path = hill_climbing((0, 0, 1, 1, 0, 0), f6, flip_neighbors)
    assert (x, fx, len(path)) == ((0, 0, 1, 1, 1, 0), 7, 2)
    assert is_local_min(x, f6, flip_neighbors)
    assert fx > 3


def test_basin_count_of_the_page() -> None:
    ends = [hill_climbing(x, f6, flip_neighbors)[1] for x in itertools.product((0, 1), repeat=6)]
    assert (ends.count(3), ends.count(6), ends.count(7)) == (44, 12, 8)


def test_edges() -> None:
    assert hill_climbing((), lambda x: 0, flip_neighbors) == ((), 0, [()])
    assert hill_climbing(5, lambda x: 0, lambda x: []) == (5, 0, [5])
    # a constant objective: every point is a local minimum, no move is made
    assert hill_climbing((1, 0), lambda x: 7, flip_neighbors) == ((1, 0), 7, [(1, 0)])
    with pytest.raises(ValueError):
        hill_climbing((0,), lambda x: 0, flip_neighbors, rule="random")


def test_random_max_cut_against_brute_force() -> None:
    rng = random.Random(4417)
    for _ in range(500):
        n = rng.randint(1, 7)
        edges = [(u, v, rng.randint(1, 9)) for u in range(n) for v in range(u + 1, n) if rng.random() < 0.6]
        x0 = tuple(rng.randint(0, 1) for _ in range(n))
        rule = rng.choice(["best", "first"])
        f = lambda x: uncut_weight(edges, x)  # noqa: E731
        x, fx, path = hill_climbing(x0, f, flip_neighbors, rule)
        assert path[0] == x0 and path[-1] == x and fx == f(x)
        # each step moves to a neighbor and lowers f
        for a, b in zip(path, path[1:]):
            assert sum(p != q for p, q in zip(a, b)) == 1
            assert f(b) < f(a)
        # the end is a local minimum: every neighbor checked
        assert is_local_min(x, f, flip_neighbors)
        # integer weights: f drops by at least 1 per step
        assert len(path) - 1 <= f(x0) - min(f(y) for y in itertools.product((0, 1), repeat=n))
        if rule == "best":
            for a, b in zip(path, path[1:]):
                assert f(b) == min(f(y) for y in flip_neighbors(a))
        # a local optimum of Max-Cut cuts at least half of the total weight
        assert 2 * fx <= sum(w for *_, w in edges)


def test_two_opt_on_small_tsp() -> None:
    rng = random.Random(81)
    for _ in range(40):
        n = rng.randint(4, 9)
        pts = [(rng.randint(0, 50), rng.randint(0, 50)) for _ in range(n)]
        d = [[round(((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5) for b in pts] for a in pts]
        start = list(range(n))
        rng.shuffle(start)
        f = lambda t: tour_length(d, t)  # noqa: E731
        x, fx, _ = hill_climbing(tuple(start), f, two_opt_neighbors)
        assert sorted(x) == list(range(n))
        assert is_local_min(x, f, two_opt_neighbors)
        assert len(list(two_opt_neighbors(x))) == n * (n - 3) // 2


def snake(j: int) -> list[tuple[int, ...]]:
    """An induced path with 2^(j+1) - 1 vertices in the cube of dimension 2j."""
    p: list[tuple[int, ...]] = [()]
    for _ in range(j):
        b = p[-1]
        p = [x + (0, 0) for x in p] + [b + (0, 1)] + [x + (1, 1) for x in reversed(p)]
    return p


def test_exponential_improving_path() -> None:
    for j in range(1, 6):
        p = snake(j)
        index = {x: i for i, x in enumerate(p)}
        assert len(index) == len(p) == 2 ** (j + 1) - 1
        for a in p:  # induced: path vertices are adjacent only to their path neighbors
            for b in p:
                if sum(s != t for s, t in zip(a, b)) == 1:
                    assert abs(index[a] - index[b]) == 1
        f = lambda x: -index[x] if x in index else 1  # noqa: E731
        for rule in ("best", "first"):
            x, fx, path = hill_climbing(p[0], f, flip_neighbors, rule)
            assert path == p and len(path) - 1 == 2 ** (j + 1) - 2
