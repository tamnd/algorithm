# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/vf2-algorithm/. The authors are listed in prov/M8JFJA.jsonl.

import itertools
import random

import pytest

from vf2_algorithm import vf2_count, vf2_isomorphic, vf2_matches

Edges = list[tuple[int, int]]


def brute(n1: int, e1: Edges, n2: int, e2: Edges, mode: str,
          l1: list[int] | None = None, l2: list[int] | None = None) -> set[tuple[int, ...]]:
    l1 = l1 or [0] * n1
    l2 = l2 or [0] * n2
    s2 = {frozenset(e) for e in e2}
    s1 = {frozenset(e) for e in e1}
    out = set()
    if mode == "iso" and n1 != n2:
        return out
    for m in itertools.permutations(range(n2), n1):
        if any(l1[u] != l2[m[u]] for u in range(n1)):
            continue
        ok = True
        for u, v in itertools.combinations(range(n1), 2):
            a = frozenset((u, v)) in s1
            b = frozenset((m[u], m[v])) in s2
            if (a and not b) or (mode != "mono" and b and not a):
                ok = False
                break
        if ok:
            out.add(m)
    return out


def rand_graph(rng: random.Random, n: int, p: float) -> Edges:
    return [(u, v) for u in range(n) for v in range(u + 1, n) if rng.random() < p]


def rook4() -> tuple[int, Edges]:
    c = [(i, j) for i in range(4) for j in range(4)]
    return 16, [(a, b) for a in range(16) for b in range(a + 1, 16) if c[a][0] == c[b][0] or c[a][1] == c[b][1]]


def shrikhande() -> tuple[int, Edges]:
    c = [(i, j) for i in range(4) for j in range(4)]
    d = {(0, 1), (0, 3), (1, 0), (3, 0), (1, 1), (3, 3)}
    return 16, [(a, b) for a in range(16) for b in range(a + 1, 16)
                if ((c[b][0] - c[a][0]) % 4, (c[b][1] - c[a][1]) % 4) in d]


def test_page_example() -> None:
    g1 = (4, [(0, 1), (1, 2), (2, 0), (2, 3)])
    g2 = (4, [(3, 1), (1, 0), (0, 3), (0, 2)])
    assert list(vf2_matches(g1, g2, "iso")) == [[1, 3, 0, 2], [3, 1, 0, 2]]
    p3 = (3, [(0, 1), (1, 2)])
    c5 = (5, [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0)])
    k4 = (4, [(i, j) for i in range(4) for j in range(i + 1, 4)])
    c4 = (4, [(0, 1), (1, 2), (2, 3), (3, 0)])
    assert vf2_count(p3, c5, "mono") == 10 and vf2_count(p3, c5, "induced") == 10
    assert vf2_count(c4, k4, "mono") == 24 and vf2_count(c4, k4, "induced") == 0


def test_edge_cases() -> None:
    assert list(vf2_matches((0, []), (0, []))) == [[]]
    assert list(vf2_matches((0, []), (3, [(0, 1)]), "induced")) == [[]]
    assert vf2_count((1, []), (1, [])) == 1
    assert vf2_count((2, []), (1, []), "mono") == 0
    assert not vf2_isomorphic((3, [(0, 1)]), (3, [(1, 2), (0, 2)]))
    assert vf2_isomorphic((2, []), (2, []), [0, 1], [1, 0])
    assert not vf2_isomorphic((2, []), (2, []), [0, 1], [1, 1])
    with pytest.raises(ValueError):
        list(vf2_matches((1, []), (1, []), "bad"))


def test_regular_and_strongly_regular_pairs() -> None:
    c6 = (6, [(i, (i + 1) % 6) for i in range(6)])
    two_k3 = (6, [(0, 1), (1, 2), (0, 2), (3, 4), (4, 5), (3, 5)])
    assert not vf2_isomorphic(c6, two_k3)
    assert vf2_count(c6, c6) == 12
    r, s = rook4(), shrikhande()
    assert not vf2_isomorphic(r, s)
    assert vf2_count(r, r) == 1152
    assert vf2_count(s, s) == 192
    perm = list(range(16))
    random.Random(3).shuffle(perm)
    s2 = (16, [(perm[u], perm[v]) for u, v in s[1]])
    m = next(vf2_matches(s, s2))
    assert m is not None


def test_random_against_brute_force() -> None:
    rng = random.Random(20261105)
    for trial in range(700):
        mode = ("iso", "induced", "mono")[trial % 3]
        if mode == "iso":
            n1 = n2 = rng.randint(1, 6)
        else:
            n2 = rng.randint(1, 7)
            n1 = rng.randint(1, min(n2, 5))
        p = rng.choice([0.25, 0.5, 0.75])
        e2 = rand_graph(rng, n2, p)
        if mode == "iso" and trial % 2 == 0:
            perm = list(range(n2))
            rng.shuffle(perm)
            e1 = [(perm[u], perm[v]) for u, v in e2]
        else:
            e1 = rand_graph(rng, n1, p)
        labelled = trial % 5 == 0
        l1 = [rng.randrange(2) for _ in range(n1)] if labelled else None
        l2 = [rng.randrange(2) for _ in range(n2)] if labelled else None
        got = [tuple(m) for m in vf2_matches((n1, e1), (n2, e2), mode, l1, l2)]
        assert len(got) == len(set(got))
        assert set(got) == brute(n1, e1, n2, e2, mode, l1, l2)
