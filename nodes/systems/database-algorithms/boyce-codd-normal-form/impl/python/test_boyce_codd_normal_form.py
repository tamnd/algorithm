# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/boyce-codd-normal-form/. The authors are listed in prov/W6NDNV.jsonl.

import random
from itertools import combinations

from boyce_codd_normal_form import (
    bcnf_violation,
    closure,
    is_bcnf,
    is_bcnf_projection,
    parse_fds,
)


def subsets(attrs):
    s = sorted(attrs)
    for k in range(len(s) + 1):
        for c in combinations(s, k):
            yield frozenset(c)


def implied(x, a, schema, fds):
    """X -> A holds in every two-tuple relation that satisfies fds.

    Two tuples that agree exactly on W satisfy fds when W is closed under each FD.
    """
    for w in subsets(schema):
        if all(not lhs <= w or rhs <= w for lhs, rhs in fds) and x <= w and a not in w:
            return False
    return True


def bcnf_by_definition(sub, schema, fds):
    """Every nontrivial implied X -> A inside sub has X a superkey of sub."""
    for x in subsets(sub):
        for a in sub - x:
            if implied(x, a, schema, fds):
                if not all(implied(x, b, schema, fds) for b in sub):
                    return False
    return True


def random_fds(rng, attrs, m):
    out = []
    for _ in range(m):
        lhs = frozenset(rng.sample(attrs, rng.randint(1, min(2, len(attrs)))))
        rhs = frozenset(rng.sample(attrs, 1)) - lhs
        if rhs:
            out.append((lhs, rhs))
    return out


def test_street_city_zip() -> None:
    r = frozenset({"street", "city", "zip"})
    f = [(frozenset({"street", "city"}), frozenset({"zip"})), (frozenset({"zip"}), frozenset({"city"}))]
    assert bcnf_violation(r, f) == (frozenset({"zip"}), frozenset({"city"}))
    assert is_bcnf_projection(frozenset({"zip", "city"}), f)
    assert is_bcnf_projection(frozenset({"street", "zip"}), f)


def test_small_examples() -> None:
    f = parse_fds("A->B, B->C")
    assert closure(frozenset("A"), f) == frozenset("ABC")
    assert not is_bcnf(frozenset("ABC"), f)
    assert is_bcnf(frozenset("AB"), parse_fds("A->B"))
    assert is_bcnf(frozenset("ABC"), parse_fds("A->BC, BC->A"))
    assert is_bcnf(frozenset("ABC"), [])
    assert is_bcnf(frozenset("A"), [])


def test_projection_pitfall() -> None:
    # No FD of F lies inside ACD, but A -> C holds there and A is not a key of ACD.
    f = parse_fds("A->B, B->C")
    sub = frozenset("ACD")
    assert all(not (lhs | rhs) <= sub for lhs, rhs in f)
    assert not is_bcnf_projection(sub, f)


def test_two_attribute_schemas_are_bcnf() -> None:
    rng = random.Random(7)
    attrs = list("ABCDE")
    for _ in range(200):
        f = random_fds(rng, attrs, rng.randint(0, 5))
        for pair in combinations(attrs, 2):
            assert is_bcnf_projection(frozenset(pair), f)


def test_checking_f_alone_is_enough_for_the_full_schema() -> None:
    rng = random.Random(11)
    for _ in range(500):
        n = rng.randint(1, 5)
        attrs = list("ABCDE"[:n])
        f = random_fds(rng, attrs, rng.randint(0, 4))
        r = frozenset(attrs)
        want = bcnf_by_definition(r, r, f)
        assert is_bcnf(r, f) == want
        assert is_bcnf_projection(r, f) == want


def test_projection_against_definition() -> None:
    rng = random.Random(12)
    for _ in range(500):
        attrs = list("ABCDE")
        f = random_fds(rng, attrs, rng.randint(1, 5))
        sub = frozenset(rng.sample(attrs, rng.randint(1, 4)))
        assert is_bcnf_projection(sub, f) == bcnf_by_definition(sub, frozenset(attrs), f)
