# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/functional-dependency/. The authors are listed in prov/61TNHC.jsonl.

import random

from functional_dependency import holding_fds, holds, holds_pairwise, violation

ROWS = [
    ("CS101", "Smith", "Mon9", "R1"),
    ("CS101", "Smith", "Wed9", "R1"),
    ("MA201", "Jones", "Mon9", "R2"),
    ("MA201", "Jones", "Tue11", "R1"),
    ("PH110", "Smith", "Tue11", "R2"),
]
SCHED = [dict(zip(("Course", "Teacher", "Hour", "Room"), r)) for r in ROWS]


def test_example() -> None:
    assert holds(SCHED, ["Course"], ["Teacher"])
    assert violation(SCHED, ["Teacher"], ["Course"]) == (0, 4)
    assert holds(SCHED, ["Hour", "Room"], ["Course"])
    assert violation(SCHED, ["Course"], ["Room"]) == (2, 3)
    assert not holds(SCHED, ["Hour"], ["Room"])


def test_edges() -> None:
    assert holds([], ["A"], ["B"])
    assert holds([{"A": 1, "B": 2}], ["A"], ["B"])
    # X -> Y with X empty says that Y is constant.
    assert holds([{"A": 1, "B": 2}, {"A": 3, "B": 2}], [], ["B"])
    assert not holds([{"A": 1, "B": 2}, {"A": 3, "B": 4}], [], ["B"])
    # Trivial FDs always hold.
    assert holds(SCHED, ["Course", "Room"], ["Room"])
    assert holds(SCHED, ["Course"], [])


def test_against_pairwise() -> None:
    rng = random.Random(6)
    attrs = ["A", "B", "C", "D"]
    for _ in range(500):
        rel = [{a: rng.randrange(3) for a in attrs} for _ in range(rng.randint(0, 7))]
        x = rng.sample(attrs, rng.randint(0, 3))
        y = rng.sample(attrs, rng.randint(0, 2))
        assert holds(rel, x, y) == holds_pairwise(rel, x, y)
        w = violation(rel, x, y)
        if w is not None:
            i, j = w
            assert i < j
            assert all(rel[i][a] == rel[j][a] for a in x) and any(rel[i][a] != rel[j][a] for a in y)


def test_holding_fds_are_closed_under_augmenting_the_left_side() -> None:
    rng = random.Random(10)
    attrs = ["A", "B", "C"]
    for _ in range(100):
        rel = [{a: rng.randrange(2) for a in attrs} for _ in range(rng.randint(1, 5))]
        fds = set(holding_fds(rel, attrs))
        for x, a in fds:
            for b in attrs:
                if b != a:
                    assert (x | {b}, a) in fds
