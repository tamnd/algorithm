# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dpll/. The authors are listed in prov/V4WR4Y.jsonl.

import itertools
import random

from dpll import assign, dpll


def brute_force_sat(n: int, clauses: list[list[int]]) -> bool:
    """True when one of the 2^n assignments satisfies every clause."""
    for bits in itertools.product([False, True], repeat=n):
        if all(any(bits[abs(q) - 1] == (q > 0) for q in c) for c in clauses):
            return True
    return False


def satisfies(model: list[int], clauses: list[list[int]]) -> bool:
    s = set(model)
    return all(any(q in s for q in c) for c in clauses)


def pigeonhole(p: int, h: int) -> tuple[int, list[list[int]]]:
    x = lambda i, j: i * h + j + 1  # noqa: E731
    cl = [[x(i, j) for j in range(h)] for i in range(p)]
    for j in range(h):
        for a in range(p):
            for b in range(a + 1, p):
                cl.append([-x(a, j), -x(b, j)])
    return p * h, cl


EXAMPLE = [[1, 2], [-1, 3], [-1, -3], [-2, 4, 5], [-4, 6], [-5, 6], [-4, -5]]


def test_page_example() -> None:
    log: list[tuple[str, int]] = []
    model = dpll(6, EXAMPLE, log)
    assert model == [-1, 2, -3, 4, -5, 6]
    assert satisfies(model, EXAMPLE)
    assert log == [
        ("pure", 6),
        ("split", 1),
        ("unit", 3),
        ("conflict", 0),
        ("unit", 2),
        ("split", 4),
        ("unit", -5),
        ("sat", 0),
    ]


def test_assign() -> None:
    f = [frozenset(c) for c in EXAMPLE]
    g = assign(f, 1)
    assert sorted(sorted(c) for c in g) == [[-5, -4], [-5, 6], [-4, 6], [-3], [-2, 4, 5], [3]]


def test_unit_propagation_ends_trivial_cases() -> None:
    for n in range(1, 30):
        log: list[tuple[str, int]] = []
        assert dpll(n, [[n], [-n]], log) is None
        assert log == [("unit", n), ("conflict", 0)]


def test_hand_cases() -> None:
    assert dpll(0, []) == []
    assert dpll(0, [[]]) is None
    assert dpll(3, []) == [-1, -2, -3]
    assert dpll(2, [[1, -1]]) == [-1, -2]
    assert dpll(2, [[1, 1, 2], [-2]]) == [1, -2]
    assert dpll(2, [[1, 2], [-1, 2], [1, -2], [-1, -2]]) is None


def test_pigeonhole() -> None:
    for h in range(1, 5):
        n, f = pigeonhole(h + 1, h)
        assert dpll(n, f) is None
        n, f = pigeonhole(h, h)
        model = dpll(n, f)
        assert model is not None and satisfies(model, f)


def test_random_against_brute_force() -> None:
    rng = random.Random(1960)
    for t in range(700):
        n = rng.randint(1, 12)
        if t % 2 == 0:
            m, k = round(4.26 * n), min(3, n)
            f = [[v if rng.random() < 0.5 else -v for v in rng.sample(range(1, n + 1), k)] for _ in range(m)]
        else:
            f = []
            for _ in range(rng.randint(0, 4 * n)):
                vs = rng.sample(range(1, n + 1), rng.randint(1, min(4, n)))
                f.append([v if rng.random() < 0.5 else -v for v in vs])
        got = dpll(n, f)
        if got is None:
            assert not brute_force_sat(n, f)
        else:
            assert len(got) == n and satisfies(got, f)
