# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/variable-neighborhood-search/. The authors are listed in prov/WPXWMK.jsonl.

import itertools
import random

import pytest

from variable_neighborhood_search import (
    flip_neighbors,
    shake_flips,
    two_flip_neighbors,
    uncut_weight,
    variable_neighborhood_descent,
    variable_neighborhood_search,
)

E8 = [(0, 1, 1), (0, 2, 5), (0, 4, 5), (0, 5, 7), (0, 6, 2), (1, 3, 6), (1, 5, 6), (2, 7, 6), (3, 4, 3), (3, 6, 7), (4, 6, 1), (5, 6, 4)]


def f8(x: tuple[int, ...]) -> int:
    return uncut_weight(E8, x)


def bits(s: str) -> tuple[int, ...]:
    return tuple(int(c) for c in s)


def is_local_min(x, f, neighbors) -> bool:
    return all(f(y) >= f(x) for y in neighbors(x))


VND = variable_neighborhood_descent(f8, [flip_neighbors, two_flip_neighbors])


def test_example_of_the_page() -> None:
    assert sum(w for *_, w in E8) == 53
    assert VND((0,) * 8) == bits("10010101") and f8(bits("10010101")) == 8
    x, fx, log = variable_neighborhood_search((0,) * 8, f8, shake_flips, VND, 3, 4, random.Random(1))
    assert [(k, "".join(map(str, z)), c, m) for k, z, c, m in log] == [
        (1, "10010101", 8, False),
        (2, "10010101", 8, False),
        (3, "11000011", 6, True),
        (1, "11000011", 6, False),
    ]
    assert (x, fx) == (bits("11000011"), 6)
    space = list(itertools.product((0, 1), repeat=8))
    assert min(f8(s) for s in space) == 6
    one = sorted(f8(s) for s in space if is_local_min(s, f8, flip_neighbors))
    both = sorted(f8(s) for s in space if is_local_min(s, f8, flip_neighbors) and is_local_min(s, f8, two_flip_neighbors))
    assert one == [6, 6, 8, 8, 11, 11] and both == [6, 6, 8, 8]


def test_shake_distance() -> None:
    rng = random.Random(4)
    for _ in range(300):
        n = rng.randint(1, 9)
        x = tuple(rng.randint(0, 1) for _ in range(n))
        k = rng.randint(1, 10)
        y = shake_flips(x, k, rng)
        assert sum(a != b for a, b in zip(x, y)) == min(k, n)


def test_invariants_on_random_instances() -> None:
    rng = random.Random(626)
    for _ in range(200):
        n = rng.randint(2, 8)
        edges = [(u, v, rng.randint(1, 9)) for u in range(n) for v in range(u + 1, n) if rng.random() < 0.6]
        f = lambda x: uncut_weight(edges, x)  # noqa: E731
        ls = variable_neighborhood_descent(f, [flip_neighbors, two_flip_neighbors])
        k_max = rng.randint(1, n)
        x0 = tuple(rng.randint(0, 1) for _ in range(n))
        x, fx, log = variable_neighborhood_search(x0, f, shake_flips, ls, k_max, rng.randint(0, 12), random.Random(rng.random()))
        current, k = f(ls(x0)), 1
        assert current <= f(x0)
        for kk, z, c, moved in log:
            # the neighborhood index follows the rule of lines L6 and L7
            assert kk == k
            assert c == f(z)
            # VND ends at a local minimum of both neighborhoods
            assert is_local_min(z, f, flip_neighbors) and is_local_min(z, f, two_flip_neighbors)
            assert moved == (c < current)
            if moved:
                current, k = c, 1
            else:
                k = k + 1 if k < k_max else 1
        assert fx == f(x) == current
        assert is_local_min(x, f, flip_neighbors) and is_local_min(x, f, two_flip_neighbors)
        assert 2 * fx <= sum(w for *_, w in edges)


def test_edges() -> None:
    with pytest.raises(ValueError):
        variable_neighborhood_search((0,), f8, shake_flips, VND, 0, 3, random.Random(1))
    x, fx, log = variable_neighborhood_search((0,) * 8, f8, shake_flips, VND, 3, 0, random.Random(1))
    assert (fx, log) == (8, [])


def test_fixed_seed_reaches_the_optimum() -> None:
    rng = random.Random(2024)
    edges = [(u, v, rng.randint(1, 9)) for u in range(10) for v in range(u + 1, 10) if rng.random() < 0.5]
    f = lambda x: uncut_weight(edges, x)  # noqa: E731
    opt = min(f(x) for x in itertools.product((0, 1), repeat=10))
    assert opt == 25
    ls = variable_neighborhood_descent(f, [flip_neighbors, two_flip_neighbors])
    x, fx, _ = variable_neighborhood_search((0,) * 10, f, shake_flips, ls, 4, 20, random.Random(3))
    assert fx == opt and f(x) == opt
