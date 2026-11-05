# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/incidence-list/. The authors are listed in prov/QV04NF.jsonl.

import random
from collections import Counter

from incidence_list import IncidenceList


def build_example() -> IncidenceList:
    g = IncidenceList(4)
    for u, v in [(0, 1), (1, 2), (0, 2), (1, 2), (2, 3), (3, 3)]:
        g.add_edge(u, v)
    return g


def test_example() -> None:
    g = build_example()
    assert [g.degree(v) for v in range(4)] == [2, 3, 4, 3]
    assert sorted(g.incident(2)) == [(1, 1), (2, 0), (3, 1), (4, 3)]
    assert sorted(g.incident(3)) == [(4, 2), (5, 3), (5, 3)]
    g.remove_edge(1)
    assert sorted(g.incident(1)) == [(0, 0), (3, 2)]
    assert sorted(g.incident(2)) == [(2, 0), (3, 1), (4, 3)]
    assert g.find_edge(2, 1) == 3
    assert g.m == 5
    assert sum(g.degree(v) for v in range(4)) == 2 * g.m


def test_directed() -> None:
    g = IncidenceList(3, directed=True)
    a = g.add_edge(0, 1)
    g.add_edge(1, 2)
    g.add_edge(2, 0)
    assert list(g.incident(0)) == [(a, 1)]
    assert list(g.in_incident(0)) == [(2, 2)]
    assert g.find_edge(1, 0) is None
    assert g.find_edge(0, 1) == a


def test_random_against_multiset() -> None:
    rng = random.Random(7)
    for directed in (False, True):
        g = IncidenceList(6, directed=directed)
        live: dict[int, tuple[int, int]] = {}
        for _ in range(400):
            if live and rng.random() < 0.4:
                e = rng.choice(list(live))
                g.remove_edge(e)
                del live[e]
            else:
                u, v = rng.randrange(6), rng.randrange(6)
                live[g.add_edge(u, v)] = (u, v)
            for x in range(6):
                want: Counter[tuple[int, int]] = Counter()
                for e, (u, v) in live.items():
                    if u == x:
                        want[(e, v)] += 1
                    if not directed and v == x:
                        want[(e, u)] += 1
                assert Counter(g.incident(x)) == want
            assert g.m == len(live)
            u, v = rng.randrange(6), rng.randrange(6)
            hit = g.find_edge(u, v)
            ok = {e for e, (a, b) in live.items() if (a, b) == (u, v) or (not directed and (b, a) == (u, v))}
            assert (hit is None and not ok) or hit in ok
            assert sorted(e for e, *_ in g.edges()) == sorted(live)
