# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lossless-join-decomposition/. The authors are listed in prov/M09NZ8.jsonl.

import random
from itertools import combinations, product

from lossless_join_decomposition import (
    binary_lossless,
    chase_lossless,
    join_of_projections,
    satisfies,
    spurious_tuples,
)


def fs(s):
    return frozenset(s)


def brute_lossless(schema, parts, fds):
    """Search relations with at most k tuples over k values per column.

    If the decomposition is lossy, the final chase tableau, read as a relation, is a
    counterexample of this size, so the search is complete for these small cases.
    """
    k = len(parts)
    tuples = list(product(range(k), repeat=len(schema)))
    ordered = [tuple(sorted(p)) for p in parts]
    for size in range(1, k + 1):
        for rel in combinations(tuples, size):
            rel = set(rel)
            if satisfies(schema, rel, fds) and join_of_projections(schema, rel, ordered) != rel:
                return False
    return True


def random_case(rng, n, k):
    schema = tuple("ABCDE"[:n])
    fds = []
    for _ in range(rng.randint(0, 3)):
        lhs = fs(rng.sample(schema, rng.randint(1, min(2, n))))
        rhs = fs(rng.sample(schema, 1)) - lhs
        if rhs:
            fds.append((lhs, rhs))
    parts = [fs(rng.sample(schema, rng.randint(1, n))) for _ in range(k)]
    missing = set(schema) - set().union(*parts)
    parts[0] = parts[0] | missing
    return schema, parts, fds


def test_supplier_example() -> None:
    schema = ("supplier", "part", "city")
    fds = [(fs({"supplier"}), fs({"city"}))]
    r = {("s1", "p1", "Paris"), ("s2", "p2", "Paris")}
    assert satisfies(schema, r, fds)
    bad = [("city", "supplier"), ("city", "part")]
    assert spurious_tuples(schema, r, bad) == {("s1", "p2", "Paris"), ("s2", "p1", "Paris")}
    assert not chase_lossless(schema, [fs(p) for p in bad], fds)
    good = [("supplier", "city"), ("supplier", "part")]
    assert spurious_tuples(schema, r, good) == set()
    assert chase_lossless(schema, [fs(p) for p in good], fds)


def test_three_way_example() -> None:
    # The three-part example of the page: AB and CD alone share nothing, but AC joins them.
    abcd = tuple("ABCD")
    f2 = [(fs("A"), fs("B")), (fs("C"), fs("D"))]
    assert chase_lossless(abcd, [fs("AB"), fs("CD"), fs("AC")], f2)
    assert not chase_lossless(abcd, [fs("AB"), fs("CD")], f2)
    assert not chase_lossless(abcd, [fs("AB"), fs("CD"), fs("BD")], f2)
    # A five-part decomposition that the chase shows lossless.
    schema = tuple("ABCDE")
    fds = [(fs("A"), fs("C")), (fs("B"), fs("C")), (fs("C"), fs("D")), (fs("DE"), fs("C")), (fs("CE"), fs("A"))]
    parts = [fs("AD"), fs("AB"), fs("BE"), fs("CDE"), fs("AE")]
    assert chase_lossless(schema, parts, fds)
    assert not chase_lossless(schema, [fs("AB"), fs("BC"), fs("CDE")], [])


def test_edges() -> None:
    schema = tuple("ABC")
    assert chase_lossless(schema, [fs("ABC")], [])
    assert chase_lossless(schema, [fs("ABC"), fs("A")], [])
    assert not chase_lossless(schema, [fs("AB"), fs("C")], [])
    assert chase_lossless(schema, [fs("AB"), fs("BC")], [(fs("B"), fs("C"))])


def test_binary_test_equals_chase() -> None:
    rng = random.Random(5)
    for _ in range(600):
        schema, parts, fds = random_case(rng, rng.randint(2, 5), 2)
        assert binary_lossless(parts[0], parts[1], fds) == chase_lossless(schema, parts, fds)


def test_chase_against_brute_force() -> None:
    rng = random.Random(6)
    for _ in range(400):
        schema, parts, fds = random_case(rng, rng.randint(2, 4), 2)
        assert chase_lossless(schema, parts, fds) == brute_lossless(schema, parts, fds)
    for _ in range(40):
        schema, parts, fds = random_case(rng, rng.randint(2, 3), 3)
        assert chase_lossless(schema, parts, fds) == brute_lossless(schema, parts, fds)
