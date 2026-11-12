# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/agm-bound/. The authors are listed in prov/79KBSS.jsonl.

import random
from fractions import Fraction as F

from agm_bound import (attributes, count_le_bound, cover_vertices, join_size, optimal_cover,
                       packing_vertices, product_instance, rho_star)

TRIANGLE = [("A", "B"), ("B", "C"), ("A", "C")]
CYCLE4 = [("A", "B"), ("B", "C"), ("C", "D"), ("A", "D")]
LW4 = [("A", "B", "C"), ("A", "B", "D"), ("A", "C", "D"), ("B", "C", "D")]
PATH = [("A", "B"), ("B", "C")]
STAR = [("A", "B"), ("A", "C"), ("A", "D")]


def test_rho_star() -> None:
    assert rho_star(TRIANGLE) == F(3, 2)
    assert rho_star(CYCLE4) == 2
    assert rho_star(LW4) == F(4, 3)
    assert rho_star(PATH) == 2
    assert rho_star(STAR) == 3
    assert rho_star([("A", "B", "C")]) == 1


def test_triangle_vertices() -> None:
    assert set(cover_vertices(TRIANGLE)) == {(F(1, 2),) * 3, (1, 1, 0), (1, 0, 1), (0, 1, 1)}


def test_duality() -> None:
    for q in (TRIANGLE, CYCLE4, LW4, PATH, STAR):
        assert max(sum(y) for y in packing_vertices(q)) == rho_star(q)


def test_optimal_cover_nonuniform() -> None:
    # Sizes 100, 100, 1: the cover (0, 1, 1) gives 100 and so does (1/2, 1/2, 1/2).
    x = optimal_cover(TRIANGLE, [100, 100, 1])
    assert count_le_bound(100, [100, 100, 1], x) and not count_le_bound(101, [100, 100, 1], x)
    x = optimal_cover(TRIANGLE, [4, 9, 16])
    assert x == (F(1, 2),) * 3
    assert count_le_bound(24, [4, 9, 16], x) and not count_le_bound(25, [4, 9, 16], x)


def test_tight_on_product_instance() -> None:
    for q, n in ((TRIANGLE, 16), (CYCLE4, 16), (LW4, 27), (PATH, 5), (STAR, 3)):
        y = max(packing_vertices(q), key=sum)
        rels = product_instance(q, y, n)
        assert all(len(r) <= n for r in rels)
        size = join_size(q, rels)
        rho = rho_star(q)
        assert F(size) ** rho.denominator == F(n) ** rho.numerator   # size = n^rho*


def random_query(rng):
    vs = "ABCD"[: rng.randrange(2, 5)]
    edges = []
    while not edges or set(attributes(edges)) != set(vs):
        k = rng.randrange(1, 4)
        edges.append(tuple(sorted(rng.sample(vs, min(k, len(vs))))))
        if len(edges) > 4:
            edges = []
    return edges


def test_random_instances_never_exceed() -> None:
    rng = random.Random(2024)
    for _ in range(150):
        q = random_query(rng)
        dom = rng.randrange(2, 4)
        rels = []
        for e in q:
            allt = [tuple(rng.randrange(dom) for _ in e) for _ in range(30)]
            rels.append(set(allt[: rng.randrange(1, 12)]))
        sizes = [len(r) for r in rels]
        size = join_size(q, rels)
        for x in cover_vertices(q):
            assert count_le_bound(size, sizes, x)
        assert count_le_bound(size, sizes, optimal_cover(q, sizes))


def test_skewed_triangle() -> None:
    m = 6
    star = {(0, b) for b in range(1, m + 1)} | {(a, 0) for a in range(1, m + 1)}
    rels = [star, star, star]
    n = len(star)
    size = join_size(TRIANGLE, rels)
    assert count_le_bound(size, [n] * 3, (F(1, 2),) * 3)
