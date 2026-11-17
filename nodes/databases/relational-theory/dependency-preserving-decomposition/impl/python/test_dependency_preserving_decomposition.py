# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dependency-preserving-decomposition/. The authors are listed in prov/HRYHGM.jsonl.

import random

from dependency_preserving_decomposition import (
    closure_under_projections,
    preserves,
    preserves_brute_force,
    projected_fds,
)


def fds_of(text):
    out = []
    for part in text.split(","):
        lhs, rhs = part.strip().split("->")
        out.append((frozenset(lhs.strip()), frozenset(rhs.strip())))
    return out


def parts_of(text):
    return [frozenset(p) for p in text.split()]


def test_cycle_example() -> None:
    f = fds_of("A->B, B->C, C->A")
    parts = parts_of("AB BC")
    # C -> A lies in no part, but C -> B and B -> A are in the projections.
    assert closure_under_projections(frozenset("C"), f, parts) == frozenset("ABC")
    assert preserves(f, parts)
    assert preserves_brute_force(f, parts)


def test_street_city_zip() -> None:
    f = [(frozenset({"street", "city"}), frozenset({"zip"})), (frozenset({"zip"}), frozenset({"city"}))]
    parts = [frozenset({"zip", "city"}), frozenset({"street", "zip"})]
    assert not preserves(f, parts)
    assert not preserves_brute_force(f, parts)
    assert preserves(f, [frozenset({"street", "city", "zip"})])


def test_bcnf_example_of_the_page() -> None:
    f = fds_of("A->B, B->C, CD->E")
    assert not preserves(f, parts_of("AB BC ADE"))
    assert closure_under_projections(frozenset("CD"), f, parts_of("AB BC ADE")) == frozenset("CD")
    assert preserves(f, parts_of("CDE AD AB BC"))


def test_projection_sizes() -> None:
    f = fds_of("A->B, B->C")
    assert sorted(("".join(sorted(x)), "".join(sorted(y))) for x, y in projected_fds(f, frozenset("AC"))) == [("A", "C")]


def test_edges() -> None:
    assert preserves([], [frozenset("A")])
    f = fds_of("A->B")
    assert preserves(f, parts_of("AB"))
    assert not preserves(f, parts_of("A B"))


def test_random_against_brute_force() -> None:
    rng = random.Random(77)
    for _ in range(600):
        n = rng.randint(2, 6)
        attrs = list("ABCDEF"[:n])
        f = []
        for _ in range(rng.randint(1, 5)):
            lhs = frozenset(rng.sample(attrs, rng.randint(1, min(2, n))))
            rhs = frozenset(rng.sample(attrs, 1)) - lhs
            if rhs:
                f.append((lhs, rhs))
        parts = [frozenset(rng.sample(attrs, rng.randint(1, n))) for _ in range(rng.randint(1, 4))]
        assert preserves(f, parts) == preserves_brute_force(f, parts)
