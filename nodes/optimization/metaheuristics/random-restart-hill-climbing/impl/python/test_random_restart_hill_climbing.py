# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/random-restart-hill-climbing/. The authors are listed in prov/JWD170.jsonl.

import itertools
import random
from fractions import Fraction

import pytest

from random_restart_hill_climbing import (
    flip_neighbors,
    hill_climbing,
    random_bits,
    random_restart_hill_climbing,
    uncut_weight,
)

E6 = [(0, 1, 3), (0, 2, 1), (0, 3, 2), (1, 2, 2), (1, 4, 4), (2, 3, 3), (2, 5, 1), (3, 4, 1), (3, 5, 2), (4, 5, 3)]


def f6(x: tuple[int, ...]) -> int:
    return uncut_weight(E6, x)


def bits(s: str) -> tuple[int, ...]:
    return tuple(int(c) for c in s)


def is_local_min(x, f) -> bool:
    return all(f(y) >= f(x) for y in flip_neighbors(x))


def test_example_of_the_page() -> None:
    best, fb, log = random_restart_hill_climbing(random_bits(6), f6, flip_neighbors, 4, random.Random(11))
    assert [(a, b, c) for a, b, c in log] == [
        (bits("111001"), bits("011001"), 6),
        (bits("001100"), bits("001110"), 7),
        (bits("011000"), bits("011001"), 6),
        (bits("000001"), bits("010101"), 3),
    ]
    assert (best, fb) == (bits("010101"), 3)


def test_success_probability_of_one_run() -> None:
    starts = list(itertools.product((0, 1), repeat=6))
    ends = {x: hill_climbing(x, f6, flip_neighbors)[1] for x in starts}
    good = sum(1 for x in starts if ends[x] == 3)
    assert Fraction(good, 64) == Fraction(11, 16)
    # all pairs of starts: the best of two runs is optimal unless both fail
    ok = sum(1 for a in starts for b in starts if min(ends[a], ends[b]) == 3)
    assert Fraction(ok, 64 * 64) == 1 - Fraction(5, 16) ** 2


def test_edges() -> None:
    with pytest.raises(ValueError):
        random_restart_hill_climbing(random_bits(3), f6, flip_neighbors, 0, random.Random(1))
    best, fb, log = random_restart_hill_climbing(lambda r: (), lambda x: 0, flip_neighbors, 3, random.Random(1))
    assert (best, fb, len(log)) == ((), 0, 3)
    # a target stops the runs early
    best, fb, log = random_restart_hill_climbing(random_bits(6), f6, flip_neighbors, 50, random.Random(11), target=3)
    assert fb == 3 and len(log) == 4


def test_invariants_on_random_instances() -> None:
    rng = random.Random(3301)
    for _ in range(500):
        n = rng.randint(1, 7)
        edges = [(u, v, rng.randint(1, 9)) for u in range(n) for v in range(u + 1, n) if rng.random() < 0.6]
        f = lambda x: uncut_weight(edges, x)  # noqa: E731
        runs = rng.randint(1, 5)
        best, fb, log = random_restart_hill_climbing(random_bits(n), f, flip_neighbors, runs, random.Random(rng.random()))
        assert len(log) == runs
        assert fb == f(best) == min(c for _, _, c in log)
        for start, end, c in log:
            assert c == f(end) <= f(start)
            assert is_local_min(end, f)
        assert 2 * fb <= sum(w for *_, w in edges)


def test_fixed_seed_reaches_the_optimum() -> None:
    rng = random.Random(2024)
    edges = [(u, v, rng.randint(1, 9)) for u in range(10) for v in range(u + 1, 10) if rng.random() < 0.5]
    f = lambda x: uncut_weight(edges, x)  # noqa: E731
    opt = min(f(x) for x in itertools.product((0, 1), repeat=10))
    assert opt == 25
    best, fb, _ = random_restart_hill_climbing(random_bits(10), f, flip_neighbors, 20, random.Random(7))
    assert fb == opt and f(best) == opt
