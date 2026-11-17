# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dependency-implication-problem/. The authors are listed in prov/THAFBS.jsonl.

import random
from itertools import combinations

from dependency_implication_problem import (
    all_keys,
    closure,
    equivalent,
    fd,
    implies,
    keys_brute_force,
    prime_attributes,
    vertex_cover_schema,
)

CTHRSG = [fd("C", "T"), fd("HR", "C"), fd("HT", "R"), fd("CS", "G"), fd("HS", "R")]


def random_fds(rng: random.Random, attrs: str, k: int) -> list:
    return [fd(rng.sample(attrs, rng.randint(0, 3)), rng.sample(attrs, rng.randint(1, 2))) for _ in range(k)]


def implied_by_two_tuple_relations(attrs: str, fds: list, dep: tuple) -> bool:
    """F |= X -> Y over all relations, decided by the two-tuple relations."""
    lhs, rhs = dep
    for mask in range(1 << len(attrs)):
        s = frozenset(attrs[i] for i in range(len(attrs)) if mask >> i & 1)
        if all(not v <= s or w <= s for v, w in fds) and lhs <= s and not rhs <= s:
            return False
    return True


def test_example() -> None:
    assert implies(CTHRSG, fd("HS", "CTHRSG"))
    assert implies(CTHRSG, fd("HR", "T"))
    assert not implies(CTHRSG, fd("CS", "R"))
    assert sorted("".join(sorted(k)) for k in all_keys("CTHRSG", CTHRSG)) == ["HS"]
    assert prime_attributes("CTHRSG", CTHRSG) == frozenset("HS")
    # City, Street, Zip: CS -> Z, Z -> C has the two keys CS and SZ.
    csz = [fd("CS", "Z"), fd("Z", "C")]
    assert sorted("".join(sorted(k)) for k in all_keys("CSZ", csz)) == ["CS", "SZ"]


def test_equivalence() -> None:
    f = [fd("A", "BC"), fd("B", "A"), fd("C", "A")]
    g = [fd("A", "B"), fd("B", "C"), fd("C", "A")]
    assert equivalent(f, g)
    assert not equivalent(f, [fd("A", "B"), fd("B", "C")])
    assert equivalent([], [fd("AB", "A")])


def test_implication_against_semantics() -> None:
    rng = random.Random(3)
    attrs = "ABCDE"
    for _ in range(200):
        fds = random_fds(rng, attrs, rng.randint(0, 6))
        for _ in range(5):
            dep = fd(rng.sample(attrs, rng.randint(0, 3)), rng.sample(attrs, rng.randint(1, 3)))
            assert implies(fds, dep) == implied_by_two_tuple_relations(attrs, fds, dep)


def test_lucchesi_osborn_against_brute_force() -> None:
    rng = random.Random(5)
    attrs = "ABCDEFG"
    for _ in range(300):
        fds = random_fds(rng, attrs, rng.randint(0, 8))
        got = all_keys(attrs, fds)
        assert len(got) == len(set(got))
        assert set(got) == set(keys_brute_force(attrs, fds))


def test_many_keys() -> None:
    # A_i <-> B_i for i < n: every choice of one attribute of each pair is a key.
    n = 5
    fds = []
    for i in range(n):
        fds += [fd([("a", i)], [("b", i)]), fd([("b", i)], [("a", i)])]
    universe = [(c, i) for i in range(n) for c in "ab"]
    keys = all_keys(universe, fds)
    assert len(keys) == 2**n
    assert all(len(k) == n for k in keys)


def test_vertex_cover_reduction() -> None:
    rng = random.Random(9)
    for _ in range(60):
        n = rng.randint(1, 6)
        pairs = [(a, b) for a in range(n) for b in range(a + 1, n)]
        edges = rng.sample(pairs, rng.randint(0, len(pairs)))
        cover = min(
            size
            for size in range(n + 1)
            for c in combinations(range(n), size)
            if all(a in c or b in c for a, b in edges)
        )
        u, fds = vertex_cover_schema(n, edges)
        attrs = sorted(u)
        smallest = next(
            size
            for size in range(len(attrs) + 1)
            if any(closure(fds, c) >= u for c in combinations(attrs, size))
        )
        assert smallest == cover
        assert min(len(k) for k in all_keys(u, fds)) == cover
