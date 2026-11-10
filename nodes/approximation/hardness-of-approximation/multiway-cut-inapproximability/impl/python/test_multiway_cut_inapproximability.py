# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/multiway-cut-inapproximability/. The authors are listed in prov/4GNDEM.jsonl.

import random
from itertools import combinations

from multiway_cut_inapproximability import (
    is_vertex_cover,
    min_node_multiway_cut,
    separates,
    vc_to_node_multiway_cut,
    vertex_cover_number,
)


def test_example() -> None:
    # The 5-cycle has vertex cover number 3.
    c5 = [(i, (i + 1) % 5) for i in range(5)]
    nv, edges, terms = vc_to_node_multiway_cut(5, c5)
    assert nv == 10 and len(edges) == 10 and len(terms) == 5
    assert min_node_multiway_cut(nv, edges, terms) == 3


def test_cuts_are_exactly_vertex_covers() -> None:
    rng = random.Random(12)
    for _ in range(80):
        n = rng.randint(1, 7)
        g = [e for e in combinations(range(n), 2) if rng.random() < 0.4]
        nv, edges, terms = vc_to_node_multiway_cut(n, g)
        for size in range(n + 1):
            for s in combinations(range(n), size):
                assert separates(nv, edges, terms, set(s)) == is_vertex_cover(g, set(s))
        assert min_node_multiway_cut(nv, edges, terms) == vertex_cover_number(n, g)
