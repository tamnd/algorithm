# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/feasibility-pump/. The authors are listed in prov/N3GN92.jsonl.

import itertools
import random
from fractions import Fraction

from feasibility_pump import feasibility_pump, solve_lp


def is_feasible(a, b, binaries, x) -> bool:
    if any(v < 0 for v in x):
        return False
    if any(x[j] not in (0, 1) for j in binaries):
        return False
    return all(sum(Fraction(r[j]) * x[j] for j in range(len(x))) <= bi for r, bi in zip(a, b))


def has_binary_point(a, b, n) -> bool:
    return any(is_feasible(a, b, range(n), list(p)) for p in itertools.product((0, 1), repeat=n))


def test_lp_solver_small_cases() -> None:
    assert solve_lp([1, 1], [[1, 2], [3, 1]], [4, 6]) == ("optimal", [Fraction(8, 5), Fraction(6, 5)], Fraction(14, 5))
    assert solve_lp([1], [[-1], [1]], [-2, 5]) == ("optimal", [5], 5)
    assert solve_lp([-1], [[-1], [1]], [-2, 5]) == ("optimal", [2], -2)
    assert solve_lp([1], [[1], [-1]], [1, -2])[0] == "infeasible"
    assert solve_lp([1, 0], [[0, 1]], [3])[0] == "unbounded"


def test_example_of_the_page() -> None:
    a = [[-1, 0, 3], [3, 2, -1]]
    b = [1, 3]
    trace: list = []
    st, x, it = feasibility_pump([0, -3, -2], a, b, [0, 1, 2], flips=1, trace=trace)
    assert (st, x, it) == ("feasible", [0, 1, 0], 3)
    h = Fraction(1, 2)
    assert trace == [
        ("lp", (h, 1, h)),
        ("round", (1, 1, 1)),
        ("lp", (h, 1, h)),
        ("flip", (0, 1, 1)),
        ("lp", (0, 1, Fraction(1, 3))),
        ("round", (0, 1, 0)),
        ("lp", (0, 1, 0)),
    ]


def test_no_integer_point() -> None:
    # 2 x1 + 2 x2 = 1 has LP solutions but no 0-1 solution
    a = [[2, 2], [-2, -2]]
    b = [1, -1]
    st, x, it = feasibility_pump([0, 0], a, b, [0, 1], max_iter=30)
    assert (st, x, it) == ("fail", None, 30)
    # an empty LP relaxation
    assert feasibility_pump([0], [[1], [-1]], [1, -2], [0])[0] == "infeasible"


def test_unbounded_cost_still_works() -> None:
    # the cost pushes the continuous x2 to infinity; the pump ignores it after L1
    st, x, _ = feasibility_pump([0, -1], [[2, -1]], [1], [0])
    assert st == "feasible" and is_feasible([[2, -1]], [1], [0], x)


def test_random_pure_binary() -> None:
    rng = random.Random(11)
    seen = {"feasible": 0, "infeasible": 0, "fail": 0}
    moves = set()
    for _ in range(250):
        n = rng.randint(2, 5)
        m = rng.randint(1, 4)
        a = [[rng.randint(-3, 4) for _ in range(n)] for _ in range(m)]
        b = [rng.randint(-2, 5) for _ in range(m)]
        c = [rng.randint(-4, 2) for _ in range(n)]
        trace: list = []
        st, x, it = feasibility_pump(c, a, b, list(range(n)), max_iter=40, flips=2, restart_every=10, seed=rng.randint(0, 99), trace=trace)
        moves.update(t[0] for t in trace)
        seen[st] += 1
        exists = has_binary_point(a, b, n)
        if st == "feasible":
            assert is_feasible(a, b, range(n), x)
        if st == "infeasible":
            assert not exists
        if not exists:
            assert st != "feasible"
    assert min(seen.values()) > 0
    assert {"flip", "round", "restart"} <= moves


def test_random_mixed() -> None:
    rng = random.Random(5)
    found = 0
    for _ in range(150):
        n = rng.randint(2, 5)
        binaries = sorted(rng.sample(range(n), rng.randint(1, n)))
        m = rng.randint(1, 3)
        a = [[rng.randint(-3, 4) for _ in range(n)] for _ in range(m)]
        b = [rng.randint(-1, 6) for _ in range(m)]
        c = [rng.randint(-3, 3) for _ in range(n)]
        st, x, _ = feasibility_pump(c, a, b, binaries, max_iter=30, flips=2, seed=3)
        if st == "feasible":
            found += 1
            assert is_feasible(a, b, binaries, x)
    assert found > 50


def test_same_seed_same_run() -> None:
    a = [[3, 3, 3, -1], [-1, 2, -2, 3]]
    b = [4, 2]
    r1 = feasibility_pump([1, -2, 1, -1], a, b, [0, 1, 2], seed=9)
    r2 = feasibility_pump([1, -2, 1, -1], a, b, [0, 1, 2], seed=9)
    assert r1 == r2
