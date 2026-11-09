# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/iterated-local-search/. The authors are listed in prov/AVNAXF.jsonl.

import itertools
import random

import pytest

from iterated_local_search import (
    distance_matrix,
    double_bridge,
    double_bridge_at,
    iterated_local_search,
    tour_length,
    two_opt_descent,
    two_opt_neighbors,
)

P9 = [(17, 2), (11, 19), (19, 9), (2, 16), (11, 12), (13, 0), (1, 3), (14, 20), (7, 11)]
D9 = distance_matrix(P9)


def f9(t: tuple[int, ...]) -> int:
    return tour_length(D9, t)


def tour(s: str) -> tuple[int, ...]:
    return tuple(int(c) for c in s)


def edges(t: tuple[int, ...]) -> set[frozenset[int]]:
    return {frozenset((t[k], t[(k + 1) % len(t)])) for k in range(len(t))}


def brute_force(d) -> int:
    return min(tour_length(d, (0,) + p) for p in itertools.permutations(range(1, len(d))))


def is_two_opt_local_min(t, f) -> bool:
    return all(f(y) >= f(t) for y in two_opt_neighbors(t))


def test_example_of_the_page() -> None:
    ls = two_opt_descent(f9)
    start = tuple(range(9))
    assert f9(start) == 128
    assert ls(start) == tour("024871365") and f9(ls(start)) == 72
    best, fb, log = iterated_local_search(start, f9, ls, double_bridge, 6, random.Random(3))
    assert [("".join(map(str, z)), c, ok) for z, c, ok in log] == [
        ("027134865", 71, True),
        ("027134865", 71, False),
        ("027134865", 71, False),
        ("056831742", 70, True),
        ("056384172", 69, True),
        ("056384172", 69, False),
    ]
    assert (best, fb) == (tour("056384172"), 69)
    assert brute_force(D9) == 69
    # the instance has exactly four 2-opt local optima as cycles, of lengths 69, 70, 71 and 72
    local = {min(t, (0,) + t[1:][::-1]) for t in ((0,) + p for p in itertools.permutations(range(1, 9))) if is_two_opt_local_min(t, f9)}
    assert sorted(f9(t) for t in local) == [69, 70, 71, 72]


def test_double_bridge_changes_four_edges() -> None:
    for n in range(5, 12):
        t = tuple(range(n))
        for p1, p2, p3 in itertools.combinations(range(1, n), 3):
            y = double_bridge_at(t, p1, p2, p3)
            assert sorted(y) == list(t) and y[0] == 0
            lengths = (p1, p2 - p1, p3 - p2, n - p3)
            single_pair = any(lengths[i] == 1 and lengths[(i + 1) % 4] == 1 for i in range(4))
            changed = len(edges(t) - edges(y))
            assert changed <= 4 and (changed == 4) == (not single_pair)
    rng = random.Random(8)
    for _ in range(200):
        t = (0,) + tuple(rng.sample(range(1, 9), 8))
        assert sorted(double_bridge(t, rng)) == list(range(9))


def test_invariants_on_random_instances() -> None:
    rng = random.Random(515)
    for _ in range(120):
        n = rng.randint(5, 8)
        d = distance_matrix([(rng.randint(0, 30), rng.randint(0, 30)) for _ in range(n)])
        f = lambda t: tour_length(d, t)  # noqa: E731
        ls = two_opt_descent(f)
        rule = rng.choice(["better", "always"])
        x0 = (0,) + tuple(rng.sample(range(1, n), n - 1))
        best, fb, log = iterated_local_search(x0, f, ls, double_bridge, rng.randint(0, 10), random.Random(rng.random()), rule)
        current = f(ls(x0))
        seen = [current]
        for z, c, ok in log:
            assert c == f(z) and sorted(z) == list(range(n))
            assert is_two_opt_local_min(z, f)
            assert ok == (rule == "always" or c < current)
            if ok:
                current = c
            seen.append(current)
        if rule == "better":
            assert all(a >= b for a, b in zip(seen, seen[1:]))
        assert fb == f(best) == min(seen)
        assert is_two_opt_local_min(best, f)


def test_edges() -> None:
    with pytest.raises(ValueError):
        iterated_local_search(tuple(range(9)), f9, two_opt_descent(f9), double_bridge, 3, random.Random(1), "sometimes")
    best, fb, log = iterated_local_search(tuple(range(9)), f9, two_opt_descent(f9), double_bridge, 0, random.Random(1))
    assert (fb, log) == (72, [])


def test_fixed_seed_reaches_the_optimum() -> None:
    rng = random.Random(2024)
    d = distance_matrix([(rng.randint(0, 100), rng.randint(0, 100)) for _ in range(10)])
    f = lambda t: tour_length(d, t)  # noqa: E731
    opt = brute_force(d)
    assert opt == 231
    best, fb, _ = iterated_local_search(tuple(range(10)), f, two_opt_descent(f), double_bridge, 30, random.Random(1))
    assert fb == opt and f(best) == opt
