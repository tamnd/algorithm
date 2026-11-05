# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/forward-star/. The authors are listed in prov/83VY7T.jsonl.

import random
from collections import Counter

import pytest

from forward_star import ForwardStar


def test_example() -> None:
    g = ForwardStar(5, [(3, 4, 2), (0, 2, 5), (2, 3, 1), (3, 1, 4), (0, 1, 3), (1, 2, 1)])
    g.check_invariant()
    assert g.arcs() == [(0, 2, 5), (0, 1, 3), (1, 2, 1), (2, 3, 1), (3, 4, 2), (3, 1, 4)]
    assert g.point == [0, 2, 3, 4, 6, 6]
    assert g.rpoint == [0, 0, 2, 4, 5, 6]
    assert g.trace == [1, 5, 0, 2, 3, 4]
    assert g.out_arcs(3) == [4, 5]
    assert g.in_arcs(1) == [1, 5]
    g.flow[5] = 7
    assert [g.flow[e] for e in g.out_arcs(3)] == [0, 7]
    assert [g.flow[e] for e in g.in_arcs(1)] == [0, 7]
    assert [g.out_degree(i) for i in range(5)] == [2, 1, 1, 2, 0]
    assert [g.in_degree(i) for i in range(5)] == [0, 2, 2, 1, 1]


def test_edge_cases() -> None:
    g = ForwardStar(0, [])
    assert g.point == [0] and g.trace == []
    h = ForwardStar(2, [(0, 1, 1), (0, 1, 2), (1, 1, 0)])
    h.check_invariant()
    assert h.out_arcs(0) == [0, 1] and h.in_arcs(1) == [0, 1, 2]
    assert h.out_arcs(1) == [2] and h.in_arcs(0) == []
    with pytest.raises(IndexError):
        ForwardStar(2, [(0, 2, 1)])
    with pytest.raises(ValueError):
        ForwardStar(-1, [])
    with pytest.raises(IndexError):
        h.out_arcs(2)


def test_random_against_multiset_model() -> None:
    rng = random.Random(8377)
    for _ in range(600):
        n = rng.randint(1, 7)
        arcs = [(rng.randrange(n), rng.randrange(n), rng.randint(0, 9)) for _ in range(rng.randint(0, 20))]
        g = ForwardStar(n, arcs)
        g.check_invariant()
        assert Counter(g.arcs()) == Counter(arcs)
        # stability: arcs with the same tail keep the input order
        for i in range(n):
            assert [g.arcs()[e] for e in g.out_arcs(i)] == [a for a in arcs if a[0] == i]
            assert Counter(g.arcs()[e] for e in g.in_arcs(i)) == Counter(a for a in arcs if a[1] == i)
            assert g.out_degree(i) == sum(a[0] == i for a in arcs)
            assert g.in_degree(i) == sum(a[1] == i for a in arcs)
