# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/path-relinking/. The authors are listed in prov/EFCZD2.jsonl.

import itertools
import random

import pytest

from path_relinking import flip, flip_descent, path_relinking, unsatisfied_weight

CLAUSES = [(6, 2, 5), (1, -5), (4, -2), (-1, -3), (3, -6), (-6, 3, -4), (-6, -4, 2), (-2, -6, -3), (5, -3, 4), (2, 3), (6, -4, 5), (-2, -4)]
WEIGHTS = [3, 7, 5, 6, 4, 6, 9, 3, 4, 8, 4, 1]
F = unsatisfied_weight(CLAUSES, WEIGHTS)


def bits(s: str) -> tuple[int, ...]:
    return tuple(int(c) for c in s)


def is_local_min(x, f) -> bool:
    return all(f(flip(x, i)) >= f(x) for i in range(len(x)))


def test_example_of_the_page() -> None:
    every = list(itertools.product([0, 1], repeat=6))
    assert min(F(x) for x in every) == 1 and [x for x in every if F(x) == 1] == [bits("110110")]
    xs, xt = bits("010100"), bits("101110")
    assert (F(xs), F(xt)) == (5, 6) and is_local_min(xs, F) and is_local_min(xt, F)
    best, fb, path = path_relinking(xs, xt, F)
    assert [(s.flipped + 1, "".join(map(str, s.x)), s.fx) for s in path] == [
        (1, "110100", 5),
        (5, "110110", 1),
        (3, "111110", 7),
        (2, "101110", 6),
    ]
    assert (best, fb) == (bits("110110"), 1)
    back, fback, _ = path_relinking(xt, xs, F)
    assert (back, fback) == (bits("011100"), 5)
    assert flip_descent(back, F) == bits("011101") and F(bits("011101")) == 4


def check(xs, xt, f) -> None:
    best, fb, path = path_relinking(xs, xt, f)
    remaining = {i for i in range(len(xs)) if xs[i] != xt[i]}
    assert len(path) == len(remaining)
    x, seen = xs, [f(xs)]
    for s in path:
        # the flipped position is the cheapest remaining one, ties to the lowest position
        assert s.flipped in remaining
        assert (s.fx, s.flipped) == min((f(flip(x, i)), i) for i in remaining)
        remaining.discard(s.flipped)
        assert s.x == flip(x, s.flipped) and s.fx == f(s.x)
        assert sum(a != b for a, b in zip(s.x, xt)) == len(remaining)
        x = s.x
        seen.append(s.fx)
    assert x == xt and not remaining
    assert fb == f(best) == min(seen) <= min(f(xs), f(xt))
    assert best == xs or best in [s.x for s in path]


def test_invariants_on_random_instances() -> None:
    rng = random.Random(606)
    for _ in range(300):
        n = rng.randint(1, 9)
        clauses = [tuple(rng.choice([1, -1]) * v for v in rng.sample(range(1, n + 1), rng.randint(1, min(3, n)))) for _ in range(rng.randint(1, 20))]
        f = unsatisfied_weight(clauses, [rng.randint(1, 9) for _ in clauses])
        xs = tuple(rng.randint(0, 1) for _ in range(n))
        xt = tuple(rng.randint(0, 1) for _ in range(n))
        check(xs, xt, f)
        check(flip_descent(xs, f), flip_descent(xt, f), f)


def test_edges() -> None:
    with pytest.raises(ValueError):
        path_relinking((0, 1), (0,), F)
    assert path_relinking(bits("010100"), bits("010100"), F) == (bits("010100"), 5, [])
    assert path_relinking((), (), lambda x: 0) == ((), 0, [])


def test_fixed_seed_reaches_the_optimum() -> None:
    rng = random.Random(5)
    n = 10
    clauses = [tuple(rng.choice([1, -1]) * v for v in rng.sample(range(1, n + 1), 3)) for _ in range(45)]
    f = unsatisfied_weight(clauses, [rng.randint(1, 9) for _ in clauses])
    opt = min(f(x) for x in itertools.product([0, 1], repeat=n))
    starts = random.Random(1)
    pool = [flip_descent(tuple(starts.randint(0, 1) for _ in range(n)), f) for _ in range(5)]
    assert all(is_local_min(x, f) for x in pool)
    found = min(f(flip_descent(path_relinking(a, b, f)[0], f)) for a in pool for b in pool if a != b)
    assert found == opt == 1
