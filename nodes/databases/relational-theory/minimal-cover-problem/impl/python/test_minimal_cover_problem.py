# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/minimal-cover-problem/. The authors are listed in prov/M2Z1TE.jsonl.

import random
from itertools import combinations

from minimal_cover_problem import closure, equivalent, fd, is_minimal, minimal_cover


def show(g: list) -> list[str]:
    return sorted("".join(sorted(l)) + "->" + "".join(sorted(r)) for l, r in g)


def test_example() -> None:
    f = [fd("A", "BC"), fd("B", "C"), fd("A", "B"), fd("AB", "C")]
    assert show(minimal_cover(f)) == ["A->B", "B->C"]
    # Ullman's course schema is already a minimal cover.
    cthrsg = [fd("C", "T"), fd("HR", "C"), fd("HT", "R"), fd("CS", "G"), fd("HS", "R")]
    assert show(minimal_cover(cthrsg)) == show(cthrsg)


def test_order_of_the_steps() -> None:
    # Left reduction turns AC -> B into C -> B, and only then is C -> A redundant.
    f = [fd("B", "A"), fd("C", "A"), fd("AC", "B")]
    g = minimal_cover(f)
    assert show(g) == ["B->A", "C->B"]
    assert not is_minimal([fd("B", "A"), fd("C", "A"), fd("C", "B")])


def test_not_unique_and_not_minimum() -> None:
    f = [fd("A", "BC"), fd("B", "AC"), fd("C", "AB")]
    one = [fd("A", "B"), fd("B", "C"), fd("C", "A")]
    two = [fd("A", "C"), fd("C", "B"), fd("B", "A")]
    four = [fd("A", "B"), fd("A", "C"), fd("B", "A"), fd("C", "A")]
    for g in (one, two, four):
        assert equivalent(f, g) and is_minimal(g)
    assert is_minimal(minimal_cover(f))


def test_edges() -> None:
    assert minimal_cover([]) == []
    assert minimal_cover([fd("AB", "A")]) == []
    assert show(minimal_cover([fd("", "A"), fd("B", "A")])) == ["->A"]


def test_random_against_brute_force() -> None:
    rng = random.Random(2)
    attrs = "ABCDE"
    for _ in range(300):
        f = [fd(rng.sample(attrs, rng.randint(0, 3)), rng.sample(attrs, rng.randint(1, 3))) for _ in range(rng.randint(0, 6))]
        g = minimal_cover(f)
        assert equivalent(f, g)
        assert is_minimal(g)


def test_is_minimal_matches_its_definition_on_tiny_sets() -> None:
    # Exhaustive check of is_minimal on all sets of at most 3 single-right FDs over A, B, C.
    attrs = "ABC"
    cands = [fd(l, a) for n in range(3) for l in combinations(attrs, n) for a in attrs if a not in l]
    for k in range(4):
        for g in combinations(cands, k):
            g = list(g)
            drop_fd = any(equivalent(g[:i] + g[i + 1 :], g) for i in range(len(g)))
            drop_attr = any(
                (closure(g, l - {b}) >= r) for l, r in g for b in l
            )
            assert is_minimal(g) == (not drop_fd and not drop_attr)
