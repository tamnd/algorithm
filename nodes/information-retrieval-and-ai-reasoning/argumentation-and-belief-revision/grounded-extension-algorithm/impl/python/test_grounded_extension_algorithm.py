# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/grounded-extension-algorithm/. The authors are listed in prov/XNWEB6.jsonl.

import random

import pytest

import af
from grounded_extension_algorithm import grounded_extension_algorithm, grounded_labelling

# The framework of the page: a -> b -> c -> d -> e, e <-> f, g attacks g and d.
EXAMPLE_ARGS = set("abcdefg")
EXAMPLE_ATTACKS = {("a", "b"), ("b", "c"), ("c", "d"), ("d", "e"), ("e", "f"), ("f", "e"), ("g", "g"), ("g", "d")}


def least_fixed_point(args, attacks):
    """Iterate the characteristic function from the empty set (Dung 1995, Definition 20)."""
    s = frozenset()
    while True:
        t = af.characteristic(args, attacks, s)
        if t == s:
            return s
        s = t


def random_framework(rng, n, p):
    args = set(range(n))
    attacks = {(a, b) for a in range(n) for b in range(n) if rng.random() < p}
    return args, attacks


def test_example() -> None:
    stats = {}
    label = grounded_labelling(EXAMPLE_ARGS, EXAMPLE_ATTACKS, stats)
    assert label == {"a": "in", "b": "out", "c": "in", "d": "out", "e": "undec", "f": "undec", "g": "undec"}
    assert stats == {"pops": 2, "scans": 4}
    assert grounded_extension_algorithm(EXAMPLE_ARGS, EXAMPLE_ATTACKS) == frozenset("ac")
    assert af.grounded_extension(EXAMPLE_ARGS, EXAMPLE_ATTACKS) == frozenset("ac")


def test_small_cases() -> None:
    assert grounded_extension_algorithm(set(), set()) == frozenset()
    assert grounded_extension_algorithm({1}, set()) == frozenset({1})
    assert grounded_extension_algorithm({1}, {(1, 1)}) == frozenset()
    assert grounded_extension_algorithm({1, 2}, {(1, 2), (2, 1)}) == frozenset()
    assert grounded_extension_algorithm({1, 2, 3}, {(1, 2), (2, 3), (3, 1)}) == frozenset()
    # A chain 0 -> 1 -> ... -> 9: the even positions are in.
    chain = {(i, i + 1) for i in range(9)}
    assert grounded_extension_algorithm(set(range(10)), chain) == frozenset(range(0, 10, 2))
    # A self-attacker is never in, so an argument that only it attacks stays undec.
    assert grounded_labelling({1, 2}, {(2, 2), (2, 1)}) == {1: "undec", 2: "undec"}


def test_rejects_unknown_argument() -> None:
    with pytest.raises(ValueError):
        grounded_labelling({1, 2}, {(1, 3)})


def test_against_brute_force() -> None:
    rng = random.Random(20240601)
    for _ in range(400):
        n = rng.randint(0, 8)
        args, attacks = random_framework(rng, n, rng.choice([0.1, 0.2, 0.3, 0.5]))
        got = grounded_extension_algorithm(args, attacks)
        assert got == af.grounded_extension(args, attacks)
        assert got == least_fixed_point(args, attacks)
        assert af.is_complete(args, attacks, got)
        assert grounded_labelling(args, attacks) == af.labelling(args, attacks, got)


def test_against_fixed_point_on_larger_frameworks() -> None:
    rng = random.Random(77)
    for _ in range(60):
        n = rng.randint(10, 120)
        args, attacks = random_framework(rng, n, rng.choice([0.005, 0.01, 0.03, 0.08]))
        got = grounded_extension_algorithm(args, attacks)
        assert got == least_fixed_point(args, attacks)
        assert grounded_labelling(args, attacks) == af.labelling(args, attacks, got)


def test_linear_work() -> None:
    rng = random.Random(5)
    cases = [random_framework(rng, n, p) for n, p in [(50, 0.02), (200, 0.005), (300, 0.01), (100, 0.2)]]
    # A long chain needs n rounds of the characteristic function, but linear work here.
    cases.append((set(range(3000)), {(i, i + 1) for i in range(2999)}))
    for args, attacks in cases:
        stats = {}
        label = grounded_labelling(args, attacks, stats)
        n_in = sum(1 for x in label.values() if x == "in")
        assert stats["pops"] == n_in <= len(args)
        # Each attack (x, y) is scanned at most once: when x becomes in or when x becomes out.
        assert stats["scans"] <= len(attacks)


def test_order_does_not_matter() -> None:
    rng = random.Random(11)
    for _ in range(50):
        args, attacks = random_framework(rng, 30, 0.06)
        names = list(range(30))
        rng.shuffle(names)
        renamed_args = {names[a] for a in args}
        renamed_attacks = {(names[a], names[b]) for a, b in attacks}
        got = grounded_extension_algorithm(args, attacks)
        assert grounded_extension_algorithm(renamed_args, renamed_attacks) == frozenset(names[a] for a in got)
