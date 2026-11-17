# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/attribute-closure-algorithm/. The authors are listed in prov/VZN265.jsonl.

import random

from attribute_closure_algorithm import fd, linear_closure, naive_closure, semantic_closure

# Ullman's course schema: Course, Teacher, Hour, Room, Student, Grade.
CTHRSG = [fd("C", "T"), fd("HR", "C"), fd("HT", "R"), fd("CS", "G"), fd("HS", "R")]


def random_fds(rng: random.Random, attrs: str, k: int) -> list:
    out = []
    for _ in range(k):
        lhs = rng.sample(attrs, rng.randint(0, 3))
        rhs = rng.sample(attrs, rng.randint(1, 2))
        out.append(fd(lhs, rhs))
    return out


def test_example() -> None:
    assert linear_closure(CTHRSG, "HS") == frozenset("CTHRSG")
    assert linear_closure(CTHRSG, "CS") == frozenset("CTSG")
    assert linear_closure(CTHRSG, "HR") == frozenset("HRCT")
    assert linear_closure(CTHRSG, "T") == frozenset("T")


def test_edges() -> None:
    assert linear_closure([], "AB") == frozenset("AB")
    assert linear_closure([], "") == frozenset()
    assert linear_closure([fd("", "A")], "") == frozenset("A")
    assert linear_closure([fd("", "A"), fd("A", "B")], "C") == frozenset("ABC")
    assert linear_closure([fd("AA", "B")], "A") == frozenset("AB")
    assert linear_closure([fd("AB", "C")], "A") == frozenset("A")
    assert linear_closure([fd("A", "B"), fd("B", "A")], "A") == frozenset("AB")


def test_against_naive_and_semantic() -> None:
    rng = random.Random(7)
    attrs = "ABCDEF"
    for _ in range(300):
        fds = random_fds(rng, attrs, rng.randint(0, 7))
        for _ in range(4):
            x = rng.sample(attrs, rng.randint(0, 3))
            want = semantic_closure(attrs, fds, x)
            assert linear_closure(fds, x) == want
            assert naive_closure(fds, x) == want


def test_linear_work_bound() -> None:
    rng = random.Random(11)
    attrs = "ABCDEFGHIJ"
    for _ in range(200):
        fds = random_fds(rng, attrs, rng.randint(0, 12))
        x = rng.sample(attrs, rng.randint(0, 4))
        stats: dict = {}
        c = linear_closure(fds, x, stats)
        assert stats["pushes"] == len(c)
        assert stats["decrements"] <= sum(len(lhs) for lhs, _ in fds)


def test_chain_needs_many_naive_passes() -> None:
    # A1 -> A2, ..., A(n-1) -> An listed in reverse order: the naive loop adds
    # one attribute per pass, while the linear algorithm does n - 1 decrements.
    n = 40
    fds = [fd([i], [i + 1]) for i in range(n - 1, 0, -1)]
    stats: dict = {}
    assert naive_closure(fds, [1], stats) == frozenset(range(1, n + 1))
    assert stats["passes"] == n
    stats = {}
    assert linear_closure(fds, [1], stats) == frozenset(range(1, n + 1))
    assert stats["decrements"] == n - 1
