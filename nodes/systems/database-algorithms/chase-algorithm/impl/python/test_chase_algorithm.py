# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chase-algorithm/. The authors are listed in prov/JMAKT7.jsonl.

import random
from itertools import combinations, product

from chase_algorithm import (
    chase,
    implies_fd,
    implies_jd,
    jd_tableau,
    lossless,
    mvd_as_jd,
    satisfies_all,
    satisfies_fd,
    satisfies_jd,
)


def fs(s):
    return frozenset(s)


def closure(x, fds):
    res = set(x)
    changed = True
    while changed:
        changed = False
        for lhs, rhs in fds:
            if lhs <= res and not rhs <= res:
                res |= rhs
                changed = True
    return res


def small_relations(schema, max_size):
    tuples = list(product(range(2), repeat=len(schema)))
    for size in range(1, max_size + 1):
        for rel in combinations(tuples, size):
            yield set(rel)


def test_lossless_example() -> None:
    schema = tuple("ABCDE")
    fds = [(fs("A"), fs("C")), (fs("B"), fs("C")), (fs("C"), fs("D")), (fs("DE"), fs("C")), (fs("CE"), fs("A"))]
    parts = [fs("AD"), fs("AB"), fs("BE"), fs("CDE"), fs("AE")]
    assert lossless(schema, parts, fds)
    assert not lossless(schema, [fs("AB"), fs("BC"), fs("CDE")], [])


def test_page_example_tableau() -> None:
    # The example of the page: R = ABCD, F = {A -> B, C -> D}, parts AB, CD, AC.
    schema = tuple("ABCD")
    fds = [(fs("A"), fs("B")), (fs("C"), fs("D"))]
    t = chase(schema, jd_tableau(schema, [fs("AB"), fs("CD"), fs("AC")]), fds, [])
    assert t == {(0, 0, 1, 1), (2, 2, 0, 0), (0, 0, 0, 0)}


def test_mvd_rules() -> None:
    schema = tuple("ABCD")
    a_b = mvd_as_jd(schema, fs("A"), fs("B"))
    b_c = mvd_as_jd(schema, fs("B"), fs("C"))
    # Transitivity: A ->> B and B ->> C give A ->> C - B.
    assert implies_jd(schema, [], [a_b, b_c], mvd_as_jd(schema, fs("A"), fs("C")))
    # Complementation: A ->> B gives A ->> CD.
    assert implies_jd(schema, [], [a_b], mvd_as_jd(schema, fs("A"), fs("CD")))
    # An FD gives an MVD, not the other way.
    assert implies_jd(schema, [(fs("A"), fs("B"))], [], a_b)
    assert not implies_fd(schema, [], [a_b], fs("A"), fs("B"))
    # Coalescence: A ->> B and C -> B give A -> B.
    assert implies_fd(schema, [(fs("C"), fs("B"))], [a_b], fs("A"), fs("B"))
    assert not implies_jd(schema, [], [a_b], b_c)


def test_fd_only_matches_closure() -> None:
    rng = random.Random(11)
    for _ in range(600):
        n = rng.randint(1, 5)
        schema = tuple("ABCDE"[:n])
        fds = []
        for _ in range(rng.randint(0, 4)):
            lhs = fs(rng.sample(schema, rng.randint(1, min(2, n))))
            fds.append((lhs, fs(rng.sample(schema, 1))))
        x = fs(rng.sample(schema, rng.randint(0, n)))
        y = fs(rng.sample(schema, 1))
        assert implies_fd(schema, fds, [], x, y) == (y <= closure(x, fds))


def random_deps(rng, schema):
    fds = []
    for _ in range(rng.randint(0, 2)):
        lhs = fs(rng.sample(schema, 1))
        fds.append((lhs, fs(rng.sample(schema, 1))))
    jds = []
    for _ in range(rng.randint(0, 2)):
        x = fs(rng.sample(schema, rng.randint(0, 1)))
        y = fs(rng.sample(schema, rng.randint(1, 2)))
        jds.append(mvd_as_jd(schema, x, y))
    return fds, jds


def test_jd_implication_certified() -> None:
    # "Not implied" is certified by the final tableau, which satisfies the dependencies
    # and violates the target. "Implied" is checked on all relations of at most 3 tuples
    # over {0, 1}.
    rng = random.Random(12)
    smalls = {n: list(small_relations(tuple("ABCD"[:n]), 3)) for n in (3, 4)}
    counts = [0, 0]
    for case in range(600):
        n = rng.choice((3, 4))
        schema = tuple("ABCD"[:n])
        fds, jds = random_deps(rng, schema)
        target = mvd_as_jd(schema, fs(rng.sample(schema, rng.randint(0, 1))), fs(rng.sample(schema, rng.randint(1, 2))))
        final = chase(schema, jd_tableau(schema, target), fds, jds)
        if tuple(0 for _ in schema) in final:
            counts[0] += 1
            assert implies_jd(schema, fds, jds, target)
            if case % 3 == 0:
                for rel in smalls[n]:
                    if satisfies_all(schema, rel, fds, jds):
                        assert satisfies_jd(schema, rel, target)
        else:
            counts[1] += 1
            assert not implies_jd(schema, fds, jds, target)
            assert satisfies_all(schema, final, fds, jds)
            assert not satisfies_jd(schema, final, target)
    assert min(counts) > 50


def test_fd_implication_with_mvds_certified() -> None:
    rng = random.Random(13)
    schema = tuple("ABCD")
    smalls = list(small_relations(schema, 3))
    counts = [0, 0]
    for case in range(500):
        fds, jds = random_deps(rng, schema)
        x = fs(rng.sample(schema, 1))
        y = fs(rng.sample(schema, 1))
        u = (0, 0, 0, 0)
        v = tuple(0 if a in x else 1 for a in schema)
        final = chase(schema, [u, v], fds, jds)
        if implies_fd(schema, fds, jds, x, y):
            counts[0] += 1
            if case % 4 == 0:
                for rel in smalls:
                    if satisfies_all(schema, rel, fds, jds):
                        assert satisfies_fd(schema, rel, x, y)
        else:
            counts[1] += 1
            assert satisfies_all(schema, final, fds, jds)
            assert not satisfies_fd(schema, final, x, y)
    assert min(counts) > 50


def test_edges() -> None:
    schema = tuple("AB")
    assert chase(schema, [], [(fs("A"), fs("B"))], []) == set()
    assert implies_fd(schema, [], [], fs("AB"), fs("A"))
    assert lossless(schema, [fs("AB")], [])
    assert not lossless(schema, [fs("A"), fs("B")], [])
